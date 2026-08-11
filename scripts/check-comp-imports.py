#!/usr/bin/env python3
"""Import smoke for competition requirements-local.txt (generic).

Usage:
  .\\.venv\\Scripts\\python.exe scripts\\check-comp-imports.py --requirements path\\to\\requirements-local.txt
Exit 0 = all mapped packages import; 1 = failure.
"""
from __future__ import annotations

import argparse
import importlib
import re
import sys
from pathlib import Path

# PyPI name -> import name (common)
IMPORT_MAP = {
    "scikit-learn": "sklearn",
    "sklearn": "sklearn",
    "opencv-python": "cv2",
    "opencv-python-headless": "cv2",
    "opencv-contrib-python": "cv2",
    "pillow": "PIL",
    "pyyaml": "yaml",
    "pyarrow": "pyarrow",
    "python-dateutil": "dateutil",
    "beautifulsoup4": "bs4",
    "pytorch": "torch",
    "torchvision": "torchvision",
    "torchaudio": "torchaudio",
    "tensorflow-cpu": "tensorflow",
    "tensorflow-gpu": "tensorflow",
    "jupyter": "jupyter",
    "ipython": "IPython",
    "nbformat": "nbformat",
    "lightgbm": "lightgbm",
    "xgboost": "xgboost",
    "catboost": "catboost",
    "sentencepiece": "sentencepiece",
    "tokenizers": "tokenizers",
    "transformers": "transformers",
    "accelerate": "accelerate",
    "datasets": "datasets",
    "polars": "polars",
    "kaggle-environments": "kaggle_environments",
}


def parse_req_line(line: str) -> str | None:
    s = line.strip()
    if not s or s.startswith("#"):
        return None
    if s.startswith("-"):
        return None  # -e / -r extras skipped for smoke
    # strip env markers
    s = s.split(";", 1)[0].strip()
    # name only
    m = re.match(r"^([A-Za-z0-9_.\-]+)", s)
    if not m:
        return None
    return m.group(1).lower().replace("_", "-")


def to_import(pkg: str) -> str:
    if pkg in IMPORT_MAP:
        return IMPORT_MAP[pkg]
    # default: hyphens to underscores
    return pkg.replace("-", "_")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--requirements", required=True)
    args = ap.parse_args()
    path = Path(args.requirements)
    if not path.is_file():
        print(f"error: missing {path}", file=sys.stderr)
        return 2

    pkgs: list[str] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        name = parse_req_line(line)
        if name:
            pkgs.append(name)

    if not pkgs:
        print("[comp-imports] no packages listed — PASS (empty list)")
        return 0

    fails: list[str] = []
    for pkg in pkgs:
        mod = to_import(pkg)
        try:
            importlib.import_module(mod)
            print(f"  OK import {mod}  (from {pkg})")
        except Exception as e:  # noqa: BLE001 — report any import fail
            fails.append(f"{pkg} -> {mod}: {e}")
            print(f"  FAIL import {mod}  (from {pkg}): {e}")

    if fails:
        print(f"[comp-imports] FAIL {len(fails)}/{len(pkgs)}", file=sys.stderr)
        return 1
    print(f"[comp-imports] PASS {len(pkgs)} packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
