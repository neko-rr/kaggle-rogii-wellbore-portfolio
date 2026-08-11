#!/usr/bin/env python3
"""Simulation submission strength gate (L2.5).

Compares candidate vs baseline KPIs using docs-ja/strength-gate-profile.json.
Exit 0 = PASS (warnings allowed). Non-zero = FAIL (do not submit).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except OSError as exc:
        raise SystemExit(f"ERROR: cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: invalid JSON {path}: {exc}") from exc


def resolve_profile(comp_root: Path, profile_arg: str | None) -> Path:
    if profile_arg:
        path = Path(profile_arg)
        if not path.is_absolute():
            path = (Path.cwd() / path).resolve()
        return path
    candidate = comp_root / "docs-ja" / "strength-gate-profile.json"
    if candidate.is_file():
        return candidate
    raise SystemExit(
        "ERROR: strength-gate-profile.json not found. "
        "Copy scripts/templates/strength-gate-profile.simulation.template.json "
        "to <comp>/docs-ja/strength-gate-profile.json and edit dimensions."
    )


def parse_stratified_md(path: Path, section_markers: dict[str, str]) -> dict[str, dict[str, float]]:
    """Extract baseline/candidate pct from markdown tables or key lines.

    Looks for lines like:
      | overall | 62.0 | 58.0 |
    or markers mapping dimension_id -> regex with named groups baseline/candidate.
    """
    text = path.read_text(encoding="utf-8-sig")
    out: dict[str, dict[str, float]] = {}

    for dim_id, pattern in (section_markers or {}).items():
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if not match:
            continue
        groups = match.groupdict()
        try:
            out[dim_id] = {
                "baseline_pct": float(groups["baseline"]),
                "candidate_pct": float(groups["candidate"]),
            }
        except (KeyError, ValueError):
            continue

    # Fallback: table rows "| id | baseline | candidate |"
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        key = cells[0].strip("`").lower()
        if key in {"id", "dimension", "---", ""} or set(key) <= {"-"}:
            continue
        try:
            baseline = float(cells[1].replace("%", ""))
            candidate = float(cells[2].replace("%", ""))
        except ValueError:
            continue
        out.setdefault(key, {"baseline_pct": baseline, "candidate_pct": candidate})
    return out


def load_metrics_json(path: Path) -> dict[str, dict[str, float]]:
    data = load_json(path)
    metrics = data.get("metrics") or {}
    out: dict[str, dict[str, float]] = {}
    for key, value in metrics.items():
        if not isinstance(value, dict):
            continue
        if "baseline_pct" in value and "candidate_pct" in value:
            out[key] = {
                "baseline_pct": float(value["baseline_pct"]),
                "candidate_pct": float(value["candidate_pct"]),
            }
    return out


def protocol_overall_pass(path: Path) -> bool | None:
    data = load_json(path)
    if "overall_pass" in data:
        return bool(data["overall_pass"])
    if "pass" in data:
        return bool(data["pass"])
    summary = data.get("summary") or {}
    if "overall_pass" in summary:
        return bool(summary["overall_pass"])
    status = str(data.get("status", "")).lower()
    if status in {"pass", "passed", "ok"}:
        return True
    if status in {"fail", "failed"}:
        return False
    return None


def evaluate(
    profile: dict[str, Any],
    purpose: str,
    stratified: dict[str, dict[str, float]],
    metrics: dict[str, dict[str, float]],
    protocol_path: Path | None,
    is_last_effective_slot: bool,
) -> tuple[bool, list[str], list[str], dict[str, float]]:
    failures: list[str] = []
    warnings: list[str] = []
    deltas: dict[str, float] = {}

    slots = profile.get("slots") or {}
    if (
        purpose == "diagnostic"
        and is_last_effective_slot
        and slots.get("block_diagnostic_as_effective", True)
    ):
        failures.append(
            "diagnostic purpose blocked on last effective slot "
            "(slots.block_diagnostic_as_effective)"
        )

    protocol_cfg = profile.get("protocol") or {}
    if purpose == "mu" and protocol_cfg.get("mu_require_overall_pass") and protocol_path:
        passed = protocol_overall_pass(protocol_path)
        if passed is False:
            failures.append("protocol overall_pass is False (required for mu)")
        elif passed is None:
            warnings.append("protocol overall_pass could not be determined")

    for dim in profile.get("dimensions") or []:
        dim_id = str(dim.get("id", ""))
        label = str(dim.get("label") or dim_id)
        tier = str(dim.get("tier", "optional")).lower()
        source = str(dim.get("source", "")).lower()
        thresholds = dim.get("thresholds") or {}
        required_for = [str(x).lower() for x in (dim.get("required_for") or [])]

        if source == "protocol_json":
            if dim.get("check") == "overall_pass":
                if not protocol_path:
                    if purpose in required_for or (
                        purpose == "mu" and tier in {"primary", "guard"}
                    ):
                        failures.append(f"{dim_id}: protocol_json required but missing")
                    continue
                passed = protocol_overall_pass(protocol_path)
                if passed is False and (purpose in required_for or purpose == "mu"):
                    failures.append(f"{label}: protocol overall_pass failed")
                elif passed is None:
                    warnings.append(f"{label}: protocol overall_pass unknown")
            continue

        values: dict[str, float] | None = None
        if source == "stratified_md":
            key = str(dim.get("metrics_key") or dim_id).lower()
            values = stratified.get(key) or stratified.get(dim_id.lower())
        elif source == "metrics_json":
            key = str(dim.get("metrics_key") or dim_id)
            values = metrics.get(key) or metrics.get(key.lower())

        if values is None:
            if tier in {"primary", "guard"} and purpose in {"mu", "hedge"}:
                failures.append(f"{label}: missing evidence for source={source}")
            elif tier == "secondary":
                warnings.append(f"{label}: missing evidence (secondary)")
            continue

        delta = float(values["candidate_pct"]) - float(values["baseline_pct"])
        deltas[dim_id] = delta

        mu_fail = thresholds.get("mu_fail_pt")
        hedge_fail = thresholds.get("hedge_fail_pt", mu_fail)
        warn_pt = thresholds.get("warn_pt")

        fail_limit = mu_fail if purpose == "mu" else hedge_fail
        if fail_limit is not None and delta < float(fail_limit):
            msg = f"{label}: regression {delta:+.2f}pt (limit {float(fail_limit):+.2f})"
            if tier in {"primary", "guard"}:
                failures.append(msg)
            else:
                warnings.append(msg)
        elif warn_pt is not None and delta < float(warn_pt):
            warnings.append(f"{label}: soft regression {delta:+.2f}pt")

    return (len(failures) == 0), failures, warnings, deltas


def main() -> int:
    parser = argparse.ArgumentParser(description="Kaggle simulation strength gate")
    parser.add_argument("--comp-root", required=True)
    parser.add_argument("--purpose", required=True, choices=["mu", "hedge", "diagnostic"])
    parser.add_argument("--profile", default=None)
    parser.add_argument("--stratified-md", default=None)
    parser.add_argument("--metrics-json", default=None)
    parser.add_argument("--protocol-json", default=None)
    parser.add_argument("--baseline-label", default=None)
    parser.add_argument("--candidate-label", default=None)
    parser.add_argument("--is-last-effective-slot", action="store_true")
    parser.add_argument("--report-json", default=None)
    args = parser.parse_args()

    comp_root = Path(args.comp_root)
    if not comp_root.is_absolute():
        comp_root = (Path.cwd() / comp_root).resolve()
    if not comp_root.is_dir():
        print(f"ERROR: comp-root not found: {comp_root}", file=sys.stderr)
        return 2

    profile_path = resolve_profile(comp_root, args.profile)
    profile = load_json(profile_path)
    if str(profile.get("submission_profile", "simulation")).lower() != "simulation":
        print(
            "WARN: profile submission_profile is not simulation — "
            "this gate is intended for simulation comps",
            file=sys.stderr,
        )

    stratified: dict[str, dict[str, float]] = {}
    if args.stratified_md:
        md_path = Path(args.stratified_md)
        if not md_path.is_absolute():
            md_path = (Path.cwd() / md_path).resolve()
        markers = (profile.get("stratified") or {}).get("section_markers") or {}
        stratified = parse_stratified_md(md_path, markers)

    metrics: dict[str, dict[str, float]] = {}
    metrics_path: Path | None = None
    if args.metrics_json:
        metrics_path = Path(args.metrics_json)
    else:
        rel = (profile.get("metrics") or {}).get("file")
        if rel:
            metrics_path = comp_root / rel
    if metrics_path and metrics_path.is_file():
        if not metrics_path.is_absolute():
            metrics_path = metrics_path.resolve()
        metrics = load_metrics_json(metrics_path)

    protocol_path: Path | None = None
    if args.protocol_json:
        protocol_path = Path(args.protocol_json)
        if not protocol_path.is_absolute():
            protocol_path = (Path.cwd() / protocol_path).resolve()
        if not protocol_path.is_file():
            print(f"ERROR: protocol-json not found: {protocol_path}", file=sys.stderr)
            return 2

    # Evidence presence for mu/hedge
    metrics_req = (profile.get("metrics") or {}).get("required_for_purpose") or []
    stratified_req = (profile.get("stratified") or {}).get("required_for_purpose") or []
    if args.purpose in metrics_req and not metrics and not stratified:
        print(
            "ERROR: purpose requires metrics/stratified evidence but none loaded",
            file=sys.stderr,
        )
        return 1
    if args.purpose in stratified_req and not stratified and not metrics:
        print(
            "ERROR: purpose requires stratified/metrics evidence but none loaded",
            file=sys.stderr,
        )
        return 1

    ok, failures, warnings, deltas = evaluate(
        profile=profile,
        purpose=args.purpose,
        stratified=stratified,
        metrics=metrics,
        protocol_path=protocol_path,
        is_last_effective_slot=args.is_last_effective_slot,
    )

    report = {
        "result": "PASS" if ok else "FAIL",
        "purpose": args.purpose,
        "profile": str(profile_path),
        "baseline_label": args.baseline_label or profile.get("baseline_label"),
        "candidate_label": args.candidate_label or profile.get("candidate_label"),
        "deltas": deltas,
        "failures": failures,
        "warnings": warnings,
    }
    if args.report_json:
        out = Path(args.report_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"[strength-gate] result={report['result']} purpose={args.purpose}")
    print(f"[strength-gate] profile={profile_path}")
    if deltas:
        print("[strength-gate] deltas:")
        for key, value in deltas.items():
            print(f"  - {key}: {value:+.2f}pt")
    for item in warnings:
        print(f"[strength-gate] WARN: {item}")
    for item in failures:
        print(f"[strength-gate] FAIL: {item}")

    if not ok:
        print("[strength-gate] BLOCKED - do not submit / do not freeze my-submitted-notebook/")
        return 1
    print("[strength-gate] PASS - proceed to kaggle-submission-validator")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
