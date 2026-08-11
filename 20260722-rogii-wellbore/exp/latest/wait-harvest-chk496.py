#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""496 COMPLETE を待ち kernels output → S0′ harvest."""
from __future__ import annotations

import datetime as dt
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COMP = ROOT / "20260722-rogii-wellbore"
PS = ROOT / "scripts/kaggle-cli.ps1"
OUT = COMP / "exp/work/wave31-neural-proposal/out-496-e2e"
HARVEST_SRC = COMP / "exp/work/wave31-neural-proposal/out-491-e2e/harvest_s0prime.py"
LOG = COMP / "exp/latest/wait-harvest-chk496.log"
SLUG = "kazeneko77/chk496-297-dual-e2e-gpu"
POLL = 180
WINDOW = 21600  # 6h · 長時間 E2E 向け


def log(msg: str) -> None:
    line = f"{dt.datetime.now(dt.timezone.utc).isoformat()} {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def status() -> str:
    r = subprocess.run(
        ["powershell", "-NoProfile", "-File", str(PS), "kernels", "status", SLUG],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    out = (r.stdout or "") + (r.stderr or "")
    for key in ("RUNNING", "COMPLETE", "ERROR", "CANCELLED"):
        if key in out:
            return key
    return "UNKNOWN"


def main() -> int:
    log(f"wait harvest start {SLUG}")
    t0 = time.time()
    while time.time() - t0 < WINDOW:
        st = status()
        log(f"status={st}")
        if st in ("COMPLETE", "ERROR"):
            OUT.mkdir(parents=True, exist_ok=True)
            r = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-File",
                    str(PS),
                    "kernels",
                    "output",
                    SLUG,
                    "-p",
                    str(OUT),
                ],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
            log(f"output rc={r.returncode}")
            # copy harvest script and retarget chk id
            dst = OUT / "harvest_s0prime.py"
            text = HARVEST_SRC.read_text(encoding="utf-8")
            text = text.replace("CHK-491", "CHK-496").replace(
                '"chk": "CHK-491"', '"chk": "CHK-496"'
            )
            dst.write_text(text, encoding="utf-8")
            r2 = subprocess.run(
                [str(ROOT / ".venv/Scripts/python.exe"), str(dst)],
                capture_output=True,
                text=True,
                cwd=str(OUT),
            )
            log(f"harvest rc={r2.returncode}\n{(r2.stdout or '')[-1500:]}\n{(r2.stderr or '')[-500:]}")
            # rename report if present
            for name in ("chk491-s0prime-harvest.md", "chk491-s0prime-compare.json"):
                p = OUT / name
                dst = OUT / name.replace("491", "496")
                if p.exists():
                    if dst.exists():
                        dst.unlink()
                    p.rename(dst)
            # append gate selector counts if report csv exists
            sel = OUT / "bimodal_selector_report.csv"
            note = OUT / "chk496-s0prime-harvest.md"
            if note.exists() and sel.exists():
                import pandas as pd

                try:
                    df = pd.read_csv(sel)
                    cols = [c for c in df.columns if "chk451" in c.lower() or "selector" in c.lower() or "chk297" in c.lower()]
                    extra = "\n\n## selector tags\n\n"
                    if "chk451_selector" in df.columns:
                        extra += df["chk451_selector"].value_counts(dropna=False).to_string()
                    elif cols:
                        extra += f"cols={cols}\n"
                    else:
                        extra += f"columns={list(df.columns)[:20]}\n"
                    note.write_text(note.read_text(encoding="utf-8") + extra + "\n", encoding="utf-8")
                except Exception as exc:
                    log(f"selector summarize skip: {exc}")
            return 0 if st == "COMPLETE" else 1
        time.sleep(POLL)
    log("timeout")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
