#!/usr/bin/env python3
"""Static preflight for Agent-written Kaggle code (generic).

Catches syntax / notebook JSON / private metadata / ruff issues BEFORE
train, eval kernels, or long GPU runs.

Usage:
  python scripts/check-static.py --repo-root .
  python scripts/check-static.py --repo-root . --comp-root ./20260101-slug
  python scripts/check-static.py --repo-root . --path my-notebook/foo.py --path bar.ipynb
  python scripts/check-static.py --repo-root . --no-ruff

Exit 0 = PASS (warnings allowed). Exit 1 = FAIL.
Writes JSON summary to --out or <exp>/work/static-check-last.json when possible.
"""
from __future__ import annotations

import argparse
import ast
import json
import py_compile
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


SKIP_DIR_NAMES = {
    ".venv",
    "venv",
    ".git",
    "node_modules",
    "__pycache__",
    ".ipynb_checkpoints",
    "dataset",
    "knowledge",
    "input",
    "output",
    ".cursor",
    "others-notebook",
    "retro",
}

DEFAULT_DIR_NAMES = (
    "my-notebook",
    "my-local-eval-notebook",
    # my-ran / my-submitted are historical — scan only via --path when re-editing
    "scripts",
    "sim-track",
)

RUFF_SELECT = "F821,F822,F823,E902"  # undefined names / IO; syntax is py_compile


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def should_skip_dir(name: str) -> bool:
    return name in SKIP_DIR_NAMES or name.startswith(".")


def iter_targets(roots: list[Path], explicit: list[Path], exclusive_paths: bool) -> list[Path]:
    out: list[Path] = []
    seen: set[Path] = set()

    def add(p: Path) -> None:
        try:
            r = p.resolve()
        except OSError:
            return
        if r in seen or not r.exists():
            return
        seen.add(r)
        out.append(r)

    for p in explicit:
        add(p)

    if exclusive_paths and explicit:
        return out

    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if any(should_skip_dir(part) for part in path.parts):
                continue
            if path.suffix.lower() in {".py", ".ipynb"}:
                add(path)
            elif path.name in {"kernel-metadata.json", "dataset-metadata.json", "model-metadata.json"}:
                add(path)
    return out


def check_py_file(path: Path) -> list[dict]:
    issues: list[dict] = []
    try:
        py_compile.compile(str(path), doraise=True)
    except py_compile.PyCompileError as e:
        issues.append(
            {
                "severity": "error",
                "code": "syntax",
                "path": str(path),
                "message": str(e).strip()[:500],
            }
        )
        return issues
    try:
        src = path.read_text(encoding="utf-8")
    except OSError as e:
        issues.append(
            {
                "severity": "error",
                "code": "io",
                "path": str(path),
                "message": f"cannot read: {e}",
            }
        )
        return issues
    try:
        ast.parse(src, filename=str(path))
    except SyntaxError as e:
        issues.append(
            {
                "severity": "error",
                "code": "syntax",
                "path": str(path),
                "message": f"{e.msg} (line {e.lineno})",
            }
        )
    return issues


def notebook_cell_source(cell: dict) -> str:
    src = cell.get("source", "")
    if isinstance(src, list):
        return "".join(src)
    return str(src)


def check_ipynb(path: Path) -> list[dict]:
    issues: list[dict] = []
    try:
        raw = path.read_text(encoding="utf-8-sig")
        nb = json.loads(raw)
    except json.JSONDecodeError as e:
        issues.append(
            {
                "severity": "error",
                "code": "notebook-json",
                "path": str(path),
                "message": f"invalid JSON: {e}",
            }
        )
        return issues
    except OSError as e:
        issues.append(
            {
                "severity": "error",
                "code": "io",
                "path": str(path),
                "message": f"cannot read: {e}",
            }
        )
        return issues

    cells = nb.get("cells")
    if not isinstance(cells, list):
        issues.append(
            {
                "severity": "error",
                "code": "notebook-shape",
                "path": str(path),
                "message": "missing cells[]",
            }
        )
        return issues
    if len(cells) == 0:
        issues.append(
            {
                "severity": "warning",
                "code": "notebook-empty",
                "path": str(path),
                "message": "notebook has 0 cells",
            }
        )

    code_n = 0
    for i, cell in enumerate(cells):
        if cell.get("cell_type") != "code":
            continue
        code_n += 1
        src = notebook_cell_source(cell)
        # Jupyter magics / shell (line-start). Keep conversion codes like {x!r} intact.
        cleaned_lines = []
        for line in src.splitlines():
            s = line.lstrip()
            if s.startswith("%%") or s.startswith("%") or s.startswith("!"):
                cleaned_lines.append("pass  # stripped magic")
            else:
                cleaned_lines.append(line)
        cleaned = "\n".join(cleaned_lines)
        if not cleaned.strip() or cleaned.strip() == "pass  # stripped magic":
            continue
        try:
            compile(cleaned, f"{path.name}:cell{i}", "exec")
        except SyntaxError as e:
            issues.append(
                {
                    "severity": "error",
                    "code": "notebook-syntax",
                    "path": str(path),
                    "message": f"code cell {i}: {e.msg} (line {e.lineno})",
                }
            )
    if code_n == 0 and len(cells) > 0:
        issues.append(
            {
                "severity": "warning",
                "code": "notebook-no-code",
                "path": str(path),
                "message": "no code cells",
            }
        )
    return issues


def check_metadata(path: Path) -> list[dict]:
    issues: list[dict] = []
    try:
        meta = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as e:
        issues.append(
            {
                "severity": "error",
                "code": "metadata-json",
                "path": str(path),
                "message": str(e)[:300],
            }
        )
        return issues

    name = path.name
    # Own artifacts must stay private (generic Kaggle rule)
    if name == "kernel-metadata.json":
        priv = meta.get("is_private")
        if priv is False:
            issues.append(
                {
                    "severity": "error",
                    "code": "not-private",
                    "path": str(path),
                    "message": "is_private is false — set true before push",
                }
            )
        elif priv is None:
            issues.append(
                {
                    "severity": "warning",
                    "code": "missing-private",
                    "path": str(path),
                    "message": "is_private not set",
                }
            )
        code_file = meta.get("code_file")
        if code_file:
            cf = path.parent / str(code_file)
            if not cf.is_file():
                issues.append(
                    {
                        "severity": "error",
                        "code": "missing-code-file",
                        "path": str(path),
                        "message": f"code_file missing: {code_file}",
                    }
                )
    elif name in {"dataset-metadata.json", "model-metadata.json"}:
        # dataset-metadata uses isPrivate (camelCase) in Kaggle API
        priv = meta.get("isPrivate", meta.get("is_private"))
        if priv is False:
            issues.append(
                {
                    "severity": "error",
                    "code": "not-private",
                    "path": str(path),
                    "message": "isPrivate/is_private is false",
                }
            )
    return issues


def find_ruff(python_exe: Path) -> list[str] | None:
    """Return command prefix for ruff, or None."""
    # 1) same venv as python
    for name in ("ruff.exe", "ruff"):
        cand = python_exe.parent / name
        if cand.is_file():
            return [str(cand)]
    # 2) python -m ruff
    try:
        r = subprocess.run(
            [str(python_exe), "-m", "ruff", "--version"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if r.returncode == 0:
            return [str(python_exe), "-m", "ruff"]
    except (OSError, subprocess.TimeoutExpired):
        pass
    # 3) PATH
    try:
        r = subprocess.run(
            ["ruff", "--version"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if r.returncode == 0:
            return ["ruff"]
    except (OSError, subprocess.TimeoutExpired):
        pass
    return None


def run_ruff(ruff_cmd: list[str], paths: list[Path], repo_root: Path) -> list[dict]:
    issues: list[dict] = []
    py_paths = [p for p in paths if p.suffix.lower() == ".py" and p.is_file()]
    # Materialize notebook cells is heavy; ruff on .py is enough for L0
    if not py_paths:
        return issues
    args = ruff_cmd + [
        "check",
        "--select",
        RUFF_SELECT,
        "--output-format",
        "json",
        "--force-exclude",
    ] + [str(p) for p in py_paths]
    try:
        r = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(repo_root),
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        issues.append(
            {
                "severity": "warning",
                "code": "ruff-run",
                "path": str(repo_root),
                "message": f"ruff failed to run: {e}",
            }
        )
        return issues
    body = (r.stdout or "").strip()
    if not body:
        if r.returncode not in (0, 1):
            issues.append(
                {
                    "severity": "warning",
                    "code": "ruff-run",
                    "path": str(repo_root),
                    "message": (r.stderr or "ruff non-zero")[:300],
                }
            )
        return issues
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        # older ruff text
        if r.returncode != 0:
            issues.append(
                {
                    "severity": "error",
                    "code": "ruff",
                    "path": str(repo_root),
                    "message": body[:800],
                }
            )
        return issues
    for item in data if isinstance(data, list) else []:
        loc = item.get("filename") or item.get("location") or ""
        code = item.get("code") or "ruff"
        msg = item.get("message") or str(item)[:200]
        row = item.get("location", {}) if isinstance(item.get("location"), dict) else {}
        line = row.get("row")
        line_s = f" line {line}" if line else ""
        # Treat all selected codes as errors (they are crash-prone)
        issues.append(
            {
                "severity": "error",
                "code": f"ruff-{code}",
                "path": str(loc),
                "message": f"{code}{line_s}: {msg}",
            }
        )
    return issues


def resolve_scan_roots(repo_root: Path, comp_root: Path | None) -> list[Path]:
    roots: list[Path] = []
    bases = [comp_root] if comp_root else []
    bases.append(repo_root)
    # nested date-slug under repo
    if comp_root is None:
        for child in sorted(repo_root.iterdir()) if repo_root.is_dir() else []:
            if child.is_dir() and re.match(r"^\d{8}-", child.name):
                bases.append(child)
    for base in bases:
        if base is None or not base.is_dir():
            continue
        for name in DEFAULT_DIR_NAMES:
            p = base / name
            if p.is_dir():
                roots.append(p)
        # scripts only at repo root once
        scr = base / "scripts"
        if scr.is_dir() and scr not in roots:
            roots.append(scr)
    # dedupe
    uniq: list[Path] = []
    seen: set[Path] = set()
    for r in roots:
        rr = r.resolve()
        if rr not in seen:
            seen.add(rr)
            uniq.append(rr)
    return uniq


def find_exp_work(repo_root: Path, comp_root: Path | None) -> Path | None:
    candidates = []
    if comp_root:
        candidates.append(comp_root / "exp" / "work")
    candidates.append(repo_root / "exp" / "work")
    for child in sorted(repo_root.iterdir()) if repo_root.is_dir() else []:
        if child.is_dir() and re.match(r"^\d{8}-", child.name):
            candidates.append(child / "exp" / "work")
    for c in candidates:
        if c.parent.is_dir():  # exp exists
            c.mkdir(parents=True, exist_ok=True)
            return c
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Static preflight for Agent-written Kaggle code")
    ap.add_argument("--repo-root", default=".", help="Repository root (has .venv, scripts)")
    ap.add_argument("--comp-root", default="", help="Optional competition inner folder")
    ap.add_argument("--path", action="append", default=[], help="Extra file or dir (repeatable)")
    ap.add_argument("--no-ruff", action="store_true", help="Skip ruff even if installed")
    ap.add_argument("--out", default="", help="JSON report path")
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    comp_root = Path(args.comp_root).resolve() if args.comp_root else None
    if comp_root and not comp_root.is_dir():
        print(f"error: --comp-root not a directory: {comp_root}", file=sys.stderr)
        return 2

    explicit: list[Path] = []
    for raw in args.path:
        p = Path(raw)
        if not p.is_absolute():
            p = (repo_root / p).resolve()
        else:
            p = p.resolve()
        if p.is_dir():
            explicit.extend(
                x
                for x in p.rglob("*")
                if x.is_file()
                and x.suffix.lower() in {".py", ".ipynb"}
                and not any(should_skip_dir(part) for part in x.parts)
            )
        else:
            explicit.append(p)

    roots = resolve_scan_roots(repo_root, comp_root)
    exclusive = bool(explicit)
    targets = iter_targets(roots, explicit, exclusive_paths=exclusive)

    if not targets:
        report = {
            "verdict": "PASS",
            "timestamp": utc_now(),
            "repo_root": str(repo_root),
            "comp_root": str(comp_root) if comp_root else None,
            "scanned": 0,
            "errors": 0,
            "warnings": 0,
            "issues": [],
            "note": "no .py/.ipynb in default scopes — nothing to check",
            "ruff": "skipped",
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    issues: list[dict] = []
    for path in targets:
        suffix = path.suffix.lower()
        name = path.name
        if suffix == ".py":
            issues.extend(check_py_file(path))
        elif suffix == ".ipynb":
            issues.extend(check_ipynb(path))
        elif name in {
            "kernel-metadata.json",
            "dataset-metadata.json",
            "model-metadata.json",
        }:
            issues.extend(check_metadata(path))

    ruff_status = "skipped"
    if not args.no_ruff:
        # prefer venv python at repo
        py = repo_root / ".venv" / "Scripts" / "python.exe"
        if not py.is_file():
            py = Path(sys.executable)
        ruff_cmd = find_ruff(py)
        if ruff_cmd is None:
            ruff_status = "not-installed"
            issues.append(
                {
                    "severity": "warning",
                    "code": "ruff-missing",
                    "path": str(repo_root),
                    "message": "ruff not in .venv — run setup-kaggle-venv.ps1 "
                    "(editor Ruff extension does NOT run for Agents). "
                    "syntax checks still applied.",
                }
            )
        else:
            ruff_status = " ".join(ruff_cmd)
            issues.extend(run_ruff(ruff_cmd, targets, repo_root))

    errors = [i for i in issues if i.get("severity") == "error"]
    warnings = [i for i in issues if i.get("severity") == "warning"]
    verdict = "FAIL" if errors else "PASS"

    report = {
        "verdict": verdict,
        "timestamp": utc_now(),
        "repo_root": str(repo_root),
        "comp_root": str(comp_root) if comp_root else None,
        "scanned": len(targets),
        "errors": len(errors),
        "warnings": len(warnings),
        "issues": issues,
        "ruff": ruff_status,
        "agent_note": (
            "Editor Ruff extension is for humans only. "
            "Agents MUST pass this script before train/eval/kernels."
        ),
    }

    out_path = Path(args.out) if args.out else None
    if out_path is None:
        work = find_exp_work(repo_root, comp_root)
        if work is not None:
            out_path = work / "static-check-last.json"
    if out_path is not None:
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            report["report_path"] = str(out_path)
        except OSError:
            pass

    print(json.dumps(report, ensure_ascii=False, indent=2))
    # console human summary
    print(f"\n[static-check] {verdict} scanned={len(targets)} errors={len(errors)} warnings={len(warnings)}", file=sys.stderr)
    for i in errors[:12]:
        print(f"  FAIL [{i.get('code')}] {i.get('path')}: {i.get('message')}", file=sys.stderr)
    for i in warnings[:6]:
        print(f"  WARN [{i.get('code')}] {i.get('path')}: {i.get('message')}", file=sys.stderr)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
