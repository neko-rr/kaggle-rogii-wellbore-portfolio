#!/usr/bin/env python3
"""Generic hypothesis-ban gate for Kaggle comps.

Blocks repeating an abstract failed hypothesis (keyword match) and
escalates after consecutive NO-GO of the same action_type.

Comp-specific extras (ONNX hash, hardcoded CHK allowlists) live in
per-comp scripts — not here.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def text_matches_failure(hypothesis: str, mechanism: str, entry: dict) -> bool:
    blob = f"{hypothesis} {mechanism}".lower()
    for kw in entry.get("keywords", []):
        if str(kw).lower() in blob:
            return True
    return False


def check_failure_registry(
    action_type: str,
    hypothesis: str,
    mechanism: str,
    failures: list,
    bypass_ids: set,
) -> list[str]:
    blocked: list[str] = []
    for entry in failures:
        if action_type not in entry.get("action_types_blocked", []):
            continue
        fid = str(entry.get("id", ""))
        if fid and fid in bypass_ids:
            continue
        if text_matches_failure(hypothesis, mechanism, entry):
            blocked.append(f"{fid}: {entry.get('reason', '')}")
    return blocked


def check_escalation(action_type: str, state: dict, escalation: dict, bypass_escalation: bool) -> list[str]:
    if bypass_escalation:
        return []
    rules = escalation.get(action_type)
    if not rules:
        return []
    streak = int(state.get("streaks", {}).get(action_type, {}).get("consecutive_nogo", 0))
    limit = int(rules.get("max_consecutive_nogo", 2))
    if streak >= limit:
        target = rules.get("escalate_to", "T3")
        return [
            f"action_type {action_type} has {streak} consecutive NO-GO — escalate to {target}"
        ]
    return []


def record_outcome(state_path: Path, action_type: str, chk_id: str, verdict: str) -> None:
    state = load_json(state_path) if state_path.is_file() else {"version": 1, "streaks": {}}
    streaks = state.setdefault("streaks", {})
    row = streaks.setdefault(action_type, {"consecutive_nogo": 0, "last_chk": ""})
    if verdict == "GO":
        row["consecutive_nogo"] = 0
        state["last_go"] = {
            "chk": chk_id,
            "action_type": action_type,
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        }
    else:
        row["consecutive_nogo"] = int(row.get("consecutive_nogo", 0)) + 1
    row["last_chk"] = chk_id
    state["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    save_json(state_path, state)


def soft_decision_warnings(exp_dir: Path, chk_id: str) -> list[str]:
    """Lane / cv_unit hygiene — WARN only (never adds hard fail reasons)."""
    warnings: list[str] = []
    chk_u = chk_id.upper()
    checklist = exp_dir / "experiment-checklist.md"
    if checklist.is_file():
        found = False
        try:
            lines = checklist.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        except OSError:
            lines = []
        for line in lines:
            if chk_u not in line.upper():
                continue
            if not line.lstrip().startswith("-"):
                continue
            found = True
            low = line.lower()
            if "lane:" not in low and "lane：" not in line:
                warnings.append(
                    f"soft: {chk_id} checklist line missing lane:primary|public|diagnostic "
                    "(see DECISION-FLOW / kaggle-lanes-final-strategy)"
                )
            break
        if not found:
            warnings.append(
                f"soft: {chk_id} not found in experiment-checklist.md "
                "(Active row should exist before heavy work)"
            )
    else:
        warnings.append("soft: experiment-checklist.md missing under exp/")

    # docs-ja next to exp/ (comp-inner layout) or parent
    candidates = [
        exp_dir.parent / "docs-ja" / "cv-design.md",
        exp_dir.parent.parent / "docs-ja" / "cv-design.md",
    ]
    cv_path = next((p for p in candidates if p.is_file()), None)
    if cv_path is None:
        warnings.append(
            "soft: docs-ja/cv-design.md missing — declare cv_unit before primary CV bets "
            "(Skill kaggle-cv-design)"
        )
    else:
        try:
            body = cv_path.read_text(encoding="utf-8-sig", errors="replace").lower()
        except OSError:
            body = ""
        has_unit = (
            "cv_unit" in body
            or "cv-unit" in body
            or "cv unit" in body
            or "groupkfold" in body
            or "group kfold" in body
            or "分割単位" in body
            or "unit: row" in body
            or "unit: group" in body
            or "unit: time" in body
            or "unit: custom" in body
        )
        if not has_unit:
            warnings.append(
                "soft: cv-design.md has no clear cv_unit (row|group|time|custom)"
            )
    return warnings


def resolve_exp_dir(explicit: str) -> Path:
    if explicit:
        p = Path(explicit).resolve()
        if not (p / "improvement-loop-failures.json").is_file() and not p.name == "exp":
            cand = p / "exp"
            if (cand / "improvement-loop-failures.json").is_file() or cand.is_dir():
                return cand
        return p
    here = Path(__file__).resolve().parent
    # ROOT/scripts -> look for */exp/improvement-loop-failures.json
    root = here.parent
    direct = root / "exp"
    if (direct / "improvement-loop-failures.json").is_file() or direct.is_dir():
        return direct
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        exp = child / "exp"
        if (exp / "improvement-loop-failures.json").is_file() or exp.is_dir():
            return exp
    raise FileNotFoundError("exp/ with improvement-loop-failures.json not found; pass --exp-dir")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generic hypothesis-ban gate")
    parser.add_argument("--exp-dir", default="", help="Path to exp/ (contains failures JSON)")
    parser.add_argument("--chk-id", required=True)
    parser.add_argument(
        "--action-type",
        required=True,
        choices=["T0", "T1", "T2", "T3", "T4"],
        help="T0 baseline / T1 external graft / T2 blend / T3 own rewrite / T4 screen-only",
    )
    parser.add_argument("--hypothesis", required=True)
    parser.add_argument("--mechanism", default="", help="Required for T3 (what you change)")
    parser.add_argument("--phase", choices=["pre", "post"], default="pre")
    parser.add_argument("--verdict", choices=["GO", "NO-GO"], default="")
    parser.add_argument("--out", default="")
    parser.add_argument("--force", action="store_true", help="User override; still logged")
    args = parser.parse_args()

    exp_dir = resolve_exp_dir(args.exp_dir)
    failures_path = exp_dir / "improvement-loop-failures.json"
    state_path = exp_dir / "improvement-loop-state.json"
    allow_path = exp_dir / "improvement-loop-allowlist.json"
    work_dir = exp_dir / "work"

    if args.phase == "post":
        if not args.verdict:
            print("error: --phase post requires --verdict GO|NO-GO", file=sys.stderr)
            return 2
        if not state_path.is_file():
            save_json(
                state_path,
                {
                    "version": 1,
                    "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "streaks": {},
                    "last_go": None,
                },
            )
        record_outcome(state_path, args.action_type, args.chk_id, args.verdict)
        out = {
            "phase": "post",
            "chk_id": args.chk_id,
            "action_type": args.action_type,
            "verdict": args.verdict,
            "state_path": str(state_path),
        }
        out_path = Path(args.out) if args.out else work_dir / f"gate-{args.chk_id.lower()}-post.json"
        save_json(out_path, out)
        print(json.dumps(out, ensure_ascii=True, indent=2))
        return 0

    if not failures_path.is_file():
        print(f"error: missing {failures_path}", file=sys.stderr)
        return 2

    failures_doc = load_json(failures_path)
    state_doc = load_json(state_path) if state_path.is_file() else {"streaks": {}}
    allow_doc = load_json(allow_path) if allow_path.is_file() else {"allowlist": {}}
    allow_entry = allow_doc.get("allowlist", {}).get(args.chk_id.upper(), {})
    if not allow_entry:
        allow_entry = allow_doc.get("allowlist", {}).get(args.chk_id, {})
    bypass = set(allow_entry.get("bypass", []))
    bypass_escalation = "escalation" in bypass

    reasons: list[str] = []
    warnings: list[str] = []

    if args.action_type == "T3" and not str(args.mechanism).strip():
        reasons.append("T3 requires --mechanism (concrete change description)")

    reasons.extend(
        check_escalation(
            args.action_type,
            state_doc,
            failures_doc.get("escalation", {}),
            bypass_escalation,
        )
    )

    if not args.force:
        reasons.extend(
            check_failure_registry(
                args.action_type,
                args.hypothesis,
                args.mechanism,
                failures_doc.get("failures", []),
                bypass_ids=bypass,
            )
        )
    else:
        warnings.append("forced=true — failure registry skipped by user override")

    if allow_entry.get("reason"):
        warnings.append(f"allowlist: {allow_entry.get('reason')}")

    if args.action_type == "T4":
        warnings.append("T4 is screen/intel only — do not treat as a full training/eval loop")

    # Soft decision hygiene (does not FAIL the gate): lane + cv_unit
    if args.phase == "pre" and args.action_type in ("T0", "T1", "T2", "T3"):
        warnings.extend(soft_decision_warnings(exp_dir, args.chk_id))

    verdict = "PASS" if not reasons else "FAIL"
    result = {
        "phase": "pre",
        "verdict": verdict,
        "chk_id": args.chk_id,
        "action_type": args.action_type,
        "hypothesis": args.hypothesis,
        "mechanism": args.mechanism,
        "reasons": reasons,
        "warnings": warnings,
        "next_if_fail": "change action_type / hypothesis; see improvement-loop-failures.json",
        "forced": bool(args.force),
        "exp_dir": str(exp_dir),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    out_path = Path(args.out) if args.out else work_dir / f"gate-{args.chk_id.lower()}-pre.json"
    save_json(out_path, result)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
