#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""496 をキャンセルせず、GPU枠が空いたら allowlist 修正済 492 を1回 push."""
from __future__ import annotations

import datetime as dt
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COMP = ROOT / "20260722-rogii-wellbore"
PS = ROOT / "scripts/kaggle-cli.ps1"
NB = COMP / "my-notebook/tip-cv-chk492-490b-h20"
LOG = COMP / "exp/latest/wait-push-chk492-after-492b.log"
HOLD = [
    "kazeneko77/chk496-297-dual-e2e-gpu",
    "kazeneko77/tip-cv-chk492b-ess1p0-h20",
]
TARGET = "kazeneko77/tip-cv-chk492-490b-h20"
POLL = 180
WINDOW = 12000


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
    for key in ("RUNNING", "COMPLETE", "ERROR", "CANCELLED", "QUEUED"):
        if key in out:
            return key
    return "UNKNOWN"


def main() -> int:
    log("492 after-492b monitor start (allowlist fix)")
    t0 = time.time()
    while time.time() - t0 < WINDOW:
        hold = {s: status(s) for s in HOLD}
        n = sum(1 for v in hold.values() if v == "RUNNING")
        st = status(TARGET)
        log(f"hold={hold} n={n} target={st}")
        if st == "RUNNING":
            log("492 already RUNNING — exit")
            return 0
        if n < 2 and st in ("ERROR", "COMPLETE", "MISSING", "UNKNOWN", "CANCELLED"):
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
            log(f"push rc={r.returncode}\n{(r.stdout or '')[-800:]}")
            if r.returncode == 0:
                return 0
        time.sleep(POLL)
    log("timeout")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
