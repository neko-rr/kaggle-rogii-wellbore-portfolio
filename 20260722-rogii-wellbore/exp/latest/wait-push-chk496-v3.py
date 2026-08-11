#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CHK-496 Ver3（490b再コピー）を GPU 空きで push。"""
from __future__ import annotations

import datetime as dt
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COMP = ROOT / "20260722-rogii-wellbore"
PS = ROOT / "scripts/kaggle-cli.ps1"
NB = COMP / "my-notebook/chk496-297-dual-e2e-gpu"
LOG = COMP / "exp/latest/wait-push-chk496-v3.log"
WATCH = [
    "kazeneko77/tip-cv-chk492-490b-h20",
    "kazeneko77/tip-cv-chk492b-ess1p0-h20",
    "kazeneko77/chk496-297-dual-e2e-gpu",
]
TARGET = "kazeneko77/chk496-297-dual-e2e-gpu"
POLL = 120
WINDOW = 9000


def log(msg: str) -> None:
    line = f"{dt.datetime.now(dt.timezone.utc).isoformat()} {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def status(slug: str) -> str:
    r = subprocess.run(
        ["powershell", "-NoProfile", "-File", str(PS), "kernels", "status", slug],
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
    log("496 v3 push monitor")
    t0 = time.time()
    while time.time() - t0 < WINDOW:
        st = {s: status(s) for s in WATCH}
        n = sum(1 for s, v in st.items() if v == "RUNNING" and s != TARGET)
        # if target already running with new version we can't know; if RUNNING leave it
        log(f"st={st} others_running={n}")
        if st[TARGET] == "RUNNING":
            # may be stale ERROR session already ended — if RUNNING after our rebuild, OK
            log("target RUNNING — assume ok / wait harvest elsewhere")
            return 0
        if n < 2:
            r = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-File",
                    str(PS),
                    "kernels",
                    "push",
                    "-p",
                    str(NB),
                ],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
            log(f"push rc={r.returncode}\n{(r.stdout or '')[-700:]}")
            if r.returncode == 0:
                return 0
        time.sleep(POLL)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
