# -*- coding: utf-8 -*-
"""Local preview of CHK-514/515 gates (not for submit — E2E kernels are submit path)."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

COMP = Path(__file__).resolve().parents[2]
WORK = COMP / "exp/work/wave31-neural-proposal"
OUT = WORK / "out-514-515-local-preview"
OUT.mkdir(parents=True, exist_ok=True)

TIP = (
    COMP
    / "exp/work/wave31-nonssoft-blend/out-485-se060-harvest/submission_tip_before_blend.csv"
)
if not TIP.exists():
    TIP = COMP / "exp/work/wave31-nonssoft-blend/out-485-se060-harvest/submission.csv"
MID = COMP / "exp/work/wave31-selector-replace/out-468-e2e/submission_before_branch_hedge.csv"


def gate_hd(tip: pd.DataFrame, mid: pd.DataFrame, thr: float = 0.7) -> tuple[pd.DataFrame, dict]:
    m = tip.rename(columns={"tvt": "tip"}).merge(
        mid.rename(columns={"tvt": "mid"})[["id", "mid"]], on="id", how="inner"
    )
    m = m.copy()
    m["well_id"] = m["id"].astype(str).str.rsplit("_", n=1).str[0]
    t = m["tip"].to_numpy(float)
    x = m["mid"].to_numpy(float)
    signed = x - t
    absd = np.abs(signed)
    row = (signed > 0) | (absd >= 2.0)
    frac = (
        m.assign(spos=(signed > 0).astype(float))
        .groupby("well_id")["spos"]
        .transform("mean")
        .to_numpy(float)
    )
    mask = (frac >= thr) & row
    pred = np.where(mask, x, t)
    out = pd.DataFrame({"id": m["id"].astype(str), "tvt": pred})
    meta = {
        "frac_mid": float(mask.mean()),
        "tipdist": float(np.sqrt(np.mean((pred - t) ** 2))),
        "n": int(len(out)),
        "thr": thr,
    }
    return out, meta


def gate_row(tip: pd.DataFrame, mid: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    m = tip.rename(columns={"tvt": "tip"}).merge(
        mid.rename(columns={"tvt": "mid"})[["id", "mid"]], on="id", how="inner"
    )
    t = m["tip"].to_numpy(float)
    x = m["mid"].to_numpy(float)
    signed = x - t
    absd = np.abs(signed)
    mask = (signed > 0) | (absd >= 2.0)
    pred = np.where(mask, x, t)
    out = pd.DataFrame({"id": m["id"].astype(str), "tvt": pred})
    meta = {
        "frac_mid": float(mask.mean()),
        "tipdist": float(np.sqrt(np.mean((pred - t) ** 2))),
        "n": int(len(out)),
    }
    return out, meta


def main() -> None:
    assert TIP.exists(), TIP
    assert MID.exists(), MID
    tip = pd.read_csv(TIP)
    mid = pd.read_csv(MID)
    # if tip path was final blend, prefer tip_before if present next to it
    tip_before = TIP.parent / "submission_tip_before_blend.csv"
    if tip_before.exists():
        tip = pd.read_csv(tip_before)
    hd, mhd = gate_hd(tip, mid)
    row, mrow = gate_row(tip, mid)
    hd.to_csv(OUT / "preview_chk514_hd.csv", index=False)
    row.to_csv(OUT / "preview_chk515_row.csv", index=False)
    report = {
        "tip": str(TIP if not tip_before.exists() else tip_before),
        "mid": str(MID),
        "chk514": mhd,
        "chk515": mrow,
        "note": "local preview only · submit via tip-submit-chk514/515 E2E kernels",
    }
    (OUT / "preview-report.json").write_text(
        __import__("json").dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(report)


if __name__ == "__main__":
    main()
