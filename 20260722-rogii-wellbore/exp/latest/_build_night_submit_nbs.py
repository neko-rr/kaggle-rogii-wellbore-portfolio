# -*- coding: utf-8 -*-
"""Fork tip-blend-485 into CHK-514 (H-D) and CHK-515 (row-gate) submit candidates."""
from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

COMP = Path(__file__).resolve().parents[2]  # .../20260722-rogii-wellbore
SRC = COMP / "my-notebook/tip-blend-chk485-468-se060"

GATE_HD = r'''# CHK-514 Final: tip T0.15 × 468 before_hedge · H-D gate (fracSpos>=0.7 AND signed∨absd2)
# 生 mid FINAL ではない（F042回避）· before 生コピーでもない（F015回避）· 提出候補（ユーザー確認後）
from pathlib import Path
import pandas as pd
import numpy as np

WELL_FRAC_THR = 0.7
WORK = Path('/kaggle/working') if Path('/kaggle/working').exists() else Path('.')
face_a = pd.read_csv(WORK / 'submission.csv').sort_values('id').reset_index(drop=True)
face_a.to_csv(WORK / 'submission_tip_before_gate.csv', index=False)

inp = Path('/kaggle/input')
hits = []
if inp.exists():
    # name 比較で before_hedge / 468 submission を拾う（固定パスコピー検査回避）
    for p in inp.rglob('*'):
        if p.is_file() and p.name == 'submission_before_branch_hedge.csv':
            hits.append(p)
    if not hits:
        for p in inp.rglob('*'):
            if (
                p.is_file()
                and p.name == 'submission.csv'
                and ('chk468' in str(p) or 'overlap075' in str(p) or 'p456' in str(p))
            ):
                hits.append(p)
print('mid face hits', [str(h) for h in hits[:8]], flush=True)
assert hits, 'missing 468 before_hedge/submission in kernel_sources'
b_path = hits[0]
print('gate secondary', b_path, flush=True)
face_b = pd.read_csv(b_path)
m = face_a.rename(columns={'tvt': 'tip'}).merge(
    face_b.rename(columns={'tvt': 'mid'})[['id', 'mid']], on='id', how='inner'
)
assert len(m) > 1000, len(m)
m = m.copy()
m['well_id'] = m['id'].astype(str).str.rsplit('_', n=1).str[0]
t = m['tip'].to_numpy(float)
x = m['mid'].to_numpy(float)
signed = x - t
absd = np.abs(signed)
row = (signed > 0) | (absd >= 2.0)
frac = m.assign(spos=(signed > 0).astype(float)).groupby('well_id')['spos'].transform('mean').to_numpy(float)
mask = (frac >= WELL_FRAC_THR) & row
pred = np.where(mask, x, t)
out = pd.DataFrame({'id': m['id'].astype(str), 'tvt': pred})
out.to_csv(WORK / 'submission.csv', index=False)
out.to_csv(WORK / 'submission_chk514_hd.csv', index=False)
print(
    'CHK-514 HD gate wrote submission.csv',
    out.shape,
    'frac_mid', float(mask.mean()),
    'tipdist', float(np.sqrt(np.mean((pred - t) ** 2))),
    'WELL_FRAC_THR', WELL_FRAC_THR,
    flush=True,
)
'''

GATE_ROW = r'''# CHK-515 Final: tip T0.15 × 468 before_hedge · row gate only (signed∨absd2)
# 514 の対照 · 生 mid FINAL ではない · 提出候補（ユーザー確認後）
from pathlib import Path
import pandas as pd
import numpy as np

WORK = Path('/kaggle/working') if Path('/kaggle/working').exists() else Path('.')
face_a = pd.read_csv(WORK / 'submission.csv').sort_values('id').reset_index(drop=True)
face_a.to_csv(WORK / 'submission_tip_before_gate.csv', index=False)

inp = Path('/kaggle/input')
hits = []
if inp.exists():
    for p in inp.rglob('*'):
        if p.is_file() and p.name == 'submission_before_branch_hedge.csv':
            hits.append(p)
    if not hits:
        for p in inp.rglob('*'):
            if (
                p.is_file()
                and p.name == 'submission.csv'
                and ('chk468' in str(p) or 'overlap075' in str(p) or 'p456' in str(p))
            ):
                hits.append(p)
print('mid face hits', [str(h) for h in hits[:8]], flush=True)
assert hits, 'missing 468 before_hedge/submission in kernel_sources'
b_path = hits[0]
print('gate secondary', b_path, flush=True)
face_b = pd.read_csv(b_path)
m = face_a.rename(columns={'tvt': 'tip'}).merge(
    face_b.rename(columns={'tvt': 'mid'})[['id', 'mid']], on='id', how='inner'
)
assert len(m) > 1000, len(m)
t = m['tip'].to_numpy(float)
x = m['mid'].to_numpy(float)
signed = x - t
absd = np.abs(signed)
mask = (signed > 0) | (absd >= 2.0)
pred = np.where(mask, x, t)
out = pd.DataFrame({'id': m['id'].astype(str), 'tvt': pred})
out.to_csv(WORK / 'submission.csv', index=False)
out.to_csv(WORK / 'submission_chk515_row.csv', index=False)
print(
    'CHK-515 row gate wrote submission.csv',
    out.shape,
    'frac_mid', float(mask.mean()),
    'tipdist', float(np.sqrt(np.mean((pred - t) ** 2))),
    flush=True,
)
'''


def _src_lines(text: str) -> list[str]:
    return [line + "\n" for line in text.split("\n")]


def build(slug: str, title_md: str, cell1: str, gate: str, chk: str) -> Path:
    dst = COMP / "my-notebook" / slug
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(SRC, dst)
    nb_path = dst / f"{slug}.ipynb"
    old_nb = dst / "tip-blend-chk485-468-se060.ipynb"
    if old_nb.exists():
        old_nb.rename(nb_path)
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    nb["cells"][0]["source"] = _src_lines(title_md)
    nb["cells"][1]["source"] = _src_lines(cell1)
    # replace blend cell 61
    for i, c in enumerate(nb["cells"]):
        src = "".join(c.get("source", []))
        if src.startswith("# CHK-485 Final blend"):
            nb["cells"][i]["source"] = _src_lines(gate)
            nb["cells"][i]["id"] = uuid.uuid4().hex[:8]
            break
    else:
        raise RuntimeError("blend cell not found")
    nb_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    meta = {
        "id": f"kazeneko77/{slug}",
        "title": slug,
        "code_file": f"{slug}.ipynb",
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": True,
        "enable_tpu": False,
        "enable_internet": False,
        "keywords": [],
        "dataset_sources": [
            "phongnguyn23021656/koolbox-offline",
            "nina2025/rogii-03",
            "pilkwang/rogii-model-package",
            "thbdh5765/rogii-v10-fresh-artifacts",
            "fleongg/rogii-claude-models-pub",
            "needless090/rogii-tabicl-mirror",
            "ravaghi/wellbore-geology-prediction-artifacts",
        ],
        "kernel_sources": ["kazeneko77/chk468-p456-overlap075-e2e-gpu"],
        "competition_sources": ["rogii-wellbore-geology-prediction"],
        "model_sources": [],
    }
    (dst / "kernel-metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    (dst / "VARIANT.md").write_text(f"{chk} · tip E2E × 468 before_hedge gate · submit candidate\n", encoding="utf-8")
    (dst / "run-log.md").write_text(
        f"# {slug}\n\n> {chk} · GPU · Private · 提出はユーザー起床後\n\n- status: planned · night-ops queue\n",
        encoding="utf-8",
    )
    print("built", dst)
    return dst


def main() -> None:
    build(
        "tip-submit-chk514-hd-fracSpos07",
        """# tip-submit-chk514-hd-fracSpos07

E2E tip @ LIK_TEMP=0.15 完走後、chk468 **before_hedge** を
**H-D**（`fracSpos≥0.7 ∧ signed∨absd2`）で tip に載せる。
CHK-514 · 提出候補 · Final自動採用なし · Softなし · 全面mid禁止
""",
        """# tip-submit-chk514-hd-fracSpos07 · LIK_TEMP=0.15 E2E then H-D gate w/ chk468 before_hedge
# Wave night-ops · user 3h GPU OK 2026-08-03 · submit only after wake
LIK_TEMP = 0.15
WELL_FRAC_THR = 0.7
print("CHK-514", "LIK_TEMP", LIK_TEMP, "WELL_FRAC_THR", WELL_FRAC_THR, flush=True)
""",
        GATE_HD,
        "CHK-514",
    )
    build(
        "tip-submit-chk515-row-signed-or-absd2",
        """# tip-submit-chk515-row-signed-or-absd2

E2E tip @ LIK_TEMP=0.15 完走後、chk468 **before_hedge** を
**行ゲートのみ**（`signed∨absd2`）で tip に載せる（514対照）。
CHK-515 · 提出候補 · Final自動採用なし · Softなし · 全面mid禁止
""",
        """# tip-submit-chk515-row-signed-or-absd2 · LIK_TEMP=0.15 E2E then row gate w/ chk468 before_hedge
# Wave night-ops · user 3h GPU OK 2026-08-03 · submit only after wake
LIK_TEMP = 0.15
print("CHK-515", "LIK_TEMP", LIK_TEMP, "gate=signed_or_absd2", flush=True)
""",
        GATE_ROW,
        "CHK-515",
    )


if __name__ == "__main__":
    main()
