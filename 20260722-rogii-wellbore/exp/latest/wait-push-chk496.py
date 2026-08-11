#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GPU枠が空いたら CHK-496 を1回だけ push（492/492b をキャンセルしない）."""
from __future__ import annotations

import datetime as dt
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # repo root
COMP = ROOT / "20260722-rogii-wellbore"
NB = COMP / "my-notebook/chk496-297-dual-e2e-gpu"
LOG = COMP / "exp/latest/wait-push-chk496.log"
PS = ROOT / "scripts/kaggle-cli.ps1"
HOLD = [
    "kazeneko77/tip-cv-chk492-490b-h20",
    "kazeneko77/tip-cv-chk492b-ess1p0-h20",
]
TARGET = "kazeneko77/chk496-297-dual-e2e-gpu"
POLL = 120
WINDOW_S = 7200


def log(msg: str) -> None:
    line = f"{dt.datetime.now(dt.timezone.utc).isoformat()} {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def status(slug: str) -> str:
    r = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-File",
            str(PS),
            "kernels",
            "status",
            slug,
        ],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    out = (r.stdout or "") + (r.stderr or "")
    for key in ("RUNNING", "COMPLETE", "ERROR", "CANCELLED", "QUEUED"):
        if key in out:
            return key
    if "denied" in out.lower() or "Cannot access" in out:
        return "MISSING"
    return "UNKNOWN"


def n_running(slugs: list[str]) -> int:
    return sum(1 for s in slugs if status(s) == "RUNNING")


def push_496() -> int:
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
    log(f"push rc={r.returncode}\n{(r.stdout or '')[-800:]}\n{(r.stderr or '')[-400:]}")
    return int(r.returncode)


def main() -> int:
    log(f"monitor start poll={POLL}s window={WINDOW_S}s target={TARGET}")
    t0 = time.time()
    pushed = False
    while time.time() - t0 < WINDOW_S:
        st_t = status(TARGET)
        if st_t == "RUNNING":
            log("496 already RUNNING — exit")
            return 0
        if st_t == "COMPLETE":
            log("496 already COMPLETE — exit")
            return 0
        # count known GPU jobs + target
        run_hold = {s: status(s) for s in HOLD}
        n = sum(1 for v in run_hold.values() if v == "RUNNING")
        log(f"hold={run_hold} n_running={n} target={st_t}")
        if (not pushed) and n < 2:
            rc = push_496()
            if rc == 0:
                pushed = True
                log("496 push OK — exit")
                return 0
            log("496 push failed (maybe still full) — retry")
        time.sleep(POLL)
    log("window elapsed — stop")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
