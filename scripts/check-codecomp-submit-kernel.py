#!/usr/bin/env python3
"""Code Competition 提出 kernel が「固定提出物コピーだけ」でないか検査する（汎用）。

用法:
  python scripts/check-codecomp-submit-kernel.py -p <kernel-dir>
  python scripts/check-codecomp-submit-kernel.py -p <kernel-dir> --artifact-names submission.csv,submission.zip

FAIL なら competitions submit 禁止。
コンペ固有の失敗台帳 ID・提出列名は本スクリプトに書かない（docs-ja / exp 側）。
成果物ファイル名は Overview / submission-rules に合わせ、--artifact-names で渡す。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


# コンペデータを触っていることの一般ヒント（slug 固有名は書かない）
COMP_PATH_HINTS = (
    "/kaggle/input/competitions/",
    "competition_sources",
    "sample_submission",
    "COMPETITION_DATA",
    "dataset_path",
    "competition_data",
    "kaggle_competitions",
)

DEFAULT_ARTIFACT_NAMES = ("submission.csv", "submission.zip")


def _notebook_text(nb_path: Path) -> str:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    parts: list[str] = []
    for c in nb.get("cells", []):
        src = c.get("source", "")
        if isinstance(src, list):
            parts.append("".join(src))
        else:
            parts.append(str(src))
    return "\n".join(parts)


def _parse_artifact_names(raw: str | None) -> tuple[str, ...]:
    if not raw or not raw.strip():
        return DEFAULT_ARTIFACT_NAMES
    names = tuple(x.strip() for x in raw.split(",") if x.strip())
    return names or DEFAULT_ARTIFACT_NAMES


def check_kernel_dir(
    kernel_dir: Path,
    artifact_names: tuple[str, ...] = DEFAULT_ARTIFACT_NAMES,
) -> list[str]:
    fails: list[str] = []
    meta_path = kernel_dir / "kernel-metadata.json"
    if not meta_path.exists():
        return [f"missing kernel-metadata.json in {kernel_dir}"]
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    code_file = meta.get("code_file") or ""
    nb_path = kernel_dir / code_file
    if not nb_path.exists():
        fails.append(f"code_file missing: {nb_path}")
        return fails

    comps = meta.get("competition_sources") or []
    if not comps:
        fails.append("competition_sources is empty — Code Competition 提出不可（hidden 再実行前提）")

    text = _notebook_text(nb_path)
    text_l = text.lower()
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    n_code_cells = sum(1 for c in nb.get("cells", []) if c.get("cell_type") == "code")

    has_comp_hint = any(h.lower() in text_l for h in COMP_PATH_HINTS) or any(
        str(c).lower().replace("-", "") in text_l.replace("-", "")
        for c in comps
        if c
    )

    art_l = [a.lower() for a in artifact_names]
    writes_sub = any(a in text_l for a in art_l) and (
        "to_csv" in text_l or "write" in text_l or "dump" in text_l or "to_pickle" in text_l
    )
    # rglob('submission.csv') 等の固定ファイル拾い
    art_alt = "|".join(re.escape(a) for a in artifact_names)
    looks_like_rglob_copy = bool(
        re.search(rf"rglob\(['\"](?:{art_alt})['\"]\)", text, flags=re.IGNORECASE)
    )
    only_copy = looks_like_rglob_copy or (
        n_code_cells <= 3
        and writes_sub
        and not has_comp_hint
    )
    if only_copy:
        fails.append(
            "copy-only notebook detected: Dataset/固定ファイルを読んで提出物にするだけの "
            "Script は Code Competition で Scoring Error になりうる。"
            "コンペデータから E2E 生成する Version のみ提出可。"
        )

    if writes_sub and not has_comp_hint and n_code_cells <= 5:
        fails.append(
            "no competition-data path hints in short notebook — likely not E2E on hidden test"
        )

    if meta.get("is_private") is False:
        fails.append("is_private must be true")

    return fails


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True, help="kernel folder with metadata + ipynb")
    ap.add_argument(
        "--artifact-names",
        default=",".join(DEFAULT_ARTIFACT_NAMES),
        help="comma-separated output filenames from Overview/submission-rules "
        f"(default: {','.join(DEFAULT_ARTIFACT_NAMES)})",
    )
    args = ap.parse_args()
    kernel_dir = Path(args.path)
    artifact_names = _parse_artifact_names(args.artifact_names)
    fails = check_kernel_dir(kernel_dir, artifact_names=artifact_names)
    if fails:
        print("FAIL: check-codecomp-submit-kernel")
        for f in fails:
            print(f"  - {f}")
        return 1
    print(f"PASS: check-codecomp-submit-kernel ({kernel_dir})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
