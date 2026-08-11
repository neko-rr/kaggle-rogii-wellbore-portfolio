#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""492b tip-cv COMPLETE/ERROR 後に output を harvest（提出なし）."""
from __future__ import annotations

import datetime as dt
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COMP = ROOT / "20260722-rogii-wellbore"
PS = ROOT / "scripts/kaggle-cli.ps1"
SLUG = "kazeneko77/tip-cv-chk492b-ess1p0-h20"
OUT = COMP / "exp/work/wave31-neural-proposal/out-492b-tipcv-v3"
LOG = COMP / "exp/latest/wait-harvest-chk492b.log"
POLL = 180
WINDOW = 14000


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
    for key in ("RUNNING", "COMPLETE", "ERROR", "CANCELLED", "QUEUED"):
        if key in out:
            return key
    return "UNKNOWN"


def main() -> int:
    log("492b harvest waiter start")
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
                    "download",
                    "-k",
                    SLUG,
                    "-p",
                    str(OUT),
                    "-f",
                ],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
            log(f"download rc={r.returncode}\n{(r.stdout or '')[-500:]}\n{(r.stderr or '')[-500:]}")
            note = OUT / "chk492b-v3-harvest.md"
            note.write_text(
                f"# CHK-492b Ver3 harvest\n\nstatus: **{st}**\n\nout: `{OUT}`\n",
                encoding="utf-8",
            )
            return 0 if r.returncode == 0 else 1
        time.sleep(POLL)
    log("timeout")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
