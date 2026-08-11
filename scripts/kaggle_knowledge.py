#!/usr/bin/env python3
"""Kaggle 横断知見をリポジトリ相対パスだけで管理する。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CARD_REQUIRED = {
    "schema_version",
    "id",
    "status",
    "title",
    "kind",
    "source_competition",
    "competition_types",
    "problem_signature",
    "intervention",
    "outcome",
    "evidence_level",
    "confidence",
    "transferability",
    "source_refs",
    "tags",
    "taxonomy",
    "search_document",
    "embedding",
    "concept_key",
    "lifecycle_status",
    "provenance",
}
EVIDENCE_LEVELS = {"L0", "L1", "L2", "L3"}
EVIDENCE_RANK = {"L0": 0, "L1": 1, "L2": 2, "L3": 3}
LIFECYCLE_STATUSES = {
    "active", "conditional", "disputed", "deprecated", "superseded"
}
ABSOLUTE_PATH_RE = re.compile(r"^(?:[A-Za-z]:[\\/]|\\\\|/(?!/))")
SECRET_PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "openai-key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "aws-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "google-api-key": re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+\b"),
    "credential-assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[\"']?[^\s\"']{8,}"
    ),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_error(message: str) -> None:
    print(f"[kaggle-knowledge] ERROR: {message}", file=sys.stderr)


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"JSON not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        log_error(f"JSON read failed ({path}): {exc}")
        raise


def write_json(path: Path, data: Any) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(path)
    except OSError as exc:
        log_error(f"JSON write failed ({path}): {exc}")
        raise


def write_text(path: Path, text: str) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    except OSError as exc:
        log_error(f"text write failed ({path}): {exc}")
        raise


def resolve_repo_root(value: str) -> Path:
    candidate = Path(value).resolve() if value else Path(__file__).resolve().parent.parent
    if not (candidate / "scripts").is_dir():
        raise ValueError(f"repository root must contain scripts/: {candidate}")
    return candidate


def resolve_comp_root(repo_root: Path, value: str) -> Path:
    if not value:
        raise ValueError("--comp-root is required")
    raw = Path(value)
    candidate = (repo_root / raw).resolve() if not raw.is_absolute() else raw.resolve()
    try:
        candidate.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError("competition root must stay under repository root") from exc
    if not (candidate / "exp").is_dir():
        raise ValueError(f"competition root must contain exp/: {candidate}")
    return candidate


def knowledge_root(repo_root: Path) -> Path:
    return repo_root / "knowledge"


def relative_ref(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError as exc:
        raise ValueError(f"source must stay under repository root: {path}") from exc


def schema_document() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Kaggle knowledge card",
        "type": "object",
        "required": sorted(CARD_REQUIRED),
        "properties": {
            "schema_version": {"const": 1},
            "id": {"type": "string", "pattern": "^KGL-[a-z0-9-]+$"},
            "status": {"enum": ["candidate", "promoted", "validated"]},
            "title": {"type": "string", "minLength": 1},
            "kind": {"enum": ["anti-pattern", "lesson", "winning-pattern"]},
            "source_competition": {"type": "string", "minLength": 1},
            "competition_types": {"type": "array", "items": {"type": "string"}},
            "problem_signature": {"type": "array", "items": {"type": "string"}},
            "intervention": {"type": "array", "items": {"type": "string"}},
            "outcome": {"type": "string"},
            "evidence_level": {"enum": sorted(EVIDENCE_LEVELS)},
            "confidence": {"enum": ["low", "medium", "high"]},
            "transferability": {"enum": ["conditional", "general"]},
            "source_refs": {"type": "array", "items": {"type": "string"}},
            "tags": {"type": "array", "items": {"type": "string"}},
            "taxonomy": {"type": "object"},
            "search_document": {"type": "string"},
            "embedding": {
                "type": "object",
                "required": ["status", "model", "dimensions", "vector_ref"],
            },
            "concept_key": {"type": "string", "pattern": "^CONCEPT-[a-f0-9]{16}$"},
            "lifecycle_status": {"enum": sorted(LIFECYCLE_STATUSES)},
            "provenance": {
                "type": "object",
                "required": [
                    "origin_type", "source_url", "license",
                    "redistribution", "review_status",
                ],
            },
        },
        "additionalProperties": True,
    }


def taxonomy_document() -> dict[str, Any]:
    return {
        "version": 1,
        "dimensions": {
            "modality": [
                "tabular", "image", "text", "audio", "multimodal",
                "graph", "simulation", "other", "unknown",
            ],
            "task_type": [
                "classification", "regression", "ranking", "generation",
                "forecasting", "optimization", "agent", "other", "unknown",
            ],
            "metric_structure": [
                "row-additive", "group-additive", "task-additive",
                "global", "simulation", "other", "unknown",
            ],
            "validation_risk": [
                "group-leakage", "time-shift", "domain-shift",
                "hidden-interaction", "public-private-shift", "other", "unknown",
            ],
            "submission_format": [
                "csv", "notebook-output", "model-artifact",
                "agent", "other", "unknown",
            ],
            "resource_constraint": [
                "cpu", "gpu", "time-limit", "memory-limit",
                "model-size", "internet-off", "other", "unknown",
            ],
            "domain_shift": [
                "none-observed", "possible", "confirmed", "unknown",
            ],
            "external_data_policy": [
                "allowed", "restricted", "forbidden", "unknown",
            ],
        },
        "aliases": {
            "image-heavy": {"modality": ["image"]},
            "tabular": {"modality": ["tabular"]},
            "simulation": {
                "modality": ["simulation"],
                "task_type": ["agent"],
                "metric_structure": ["simulation"],
                "submission_format": ["agent"],
            },
            "notebook-output": {"submission_format": ["notebook-output"]},
            "csv": {"submission_format": ["csv"]},
        },
    }


def infer_taxonomy(competition_types: list[str], tags: list[str]) -> dict[str, list[str]]:
    taxonomy = taxonomy_document()
    result: dict[str, set[str]] = {}
    for signal in [*competition_types, *tags]:
        alias = taxonomy["aliases"].get(str(signal).lower(), {})
        for dimension, values in alias.items():
            result.setdefault(dimension, set()).update(values)
    if "onnx-per-task" in tags:
        result.setdefault("submission_format", set()).add("model-artifact")
        result.setdefault("metric_structure", set()).add("task-additive")
        result.setdefault("resource_constraint", set()).add("model-size")
    return {
        dimension: sorted(values)
        for dimension, values in sorted(result.items())
    }


def make_search_document(card: dict[str, Any]) -> str:
    parts = [
        str(card.get("title", "")),
        str(card.get("mechanism", "")),
        str(card.get("outcome", "")),
        *[str(item) for item in card.get("problem_signature", [])],
        *[str(item) for item in card.get("intervention", [])],
        *[str(item) for item in card.get("conditions", [])],
        *[str(item) for item in card.get("contraindications", [])],
        *[str(item) for item in card.get("tags", [])],
    ]
    return " ".join(part.strip() for part in parts if part.strip())



def normalize_concept_text(value: str) -> str:
    text = value.lower()
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\b(?:chk|sub|exp|inf|f)[-_]?\d+\b", " ", text)
    text = re.sub(r"\b\d+(?:\.\d+)?\b", " ", text)
    text = re.sub(r"[^0-9a-zぁ-んァ-ヶ一-龠]+", " ", text)
    return " ".join(text.split())


def make_concept_key(card: dict[str, Any]) -> str:
    concept_source = " ".join(
        [
            str(card.get("title", "")),
            str(card.get("mechanism", "")),
            *[str(item) for item in card.get("intervention", [])],
            *[str(item) for item in card.get("problem_signature", [])],
        ]
    )
    normalized = normalize_concept_text(concept_source)
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]
    return f"CONCEPT-{digest}"


def default_provenance(card: dict[str, Any]) -> dict[str, str]:
    if card.get("kind") == "winning-pattern":
        return {
            "origin_type": "public-solution",
            "source_url": "",
            "license": "unknown",
            "redistribution": "summary-only",
            "review_status": "pending",
        }
    return {
        "origin_type": "own-experiment",
        "source_url": "",
        "license": "own",
        "redistribution": "summary-only",
        "review_status": "reviewed",
    }


def enrich_card(card: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(card)
    if "taxonomy" not in enriched:
        enriched["taxonomy"] = infer_taxonomy(
            [str(item) for item in enriched.get("competition_types", [])],
            [str(item) for item in enriched.get("tags", [])],
        )
    enriched["search_document"] = make_search_document(enriched)
    enriched.setdefault(
        "embedding",
        {
            "status": "not-generated",
            "model": "",
            "dimensions": 0,
            "vector_ref": "",
        },
    )
    enriched.setdefault("concept_key", make_concept_key(enriched))
    enriched.setdefault("lifecycle_status", "conditional")
    enriched.setdefault("provenance", default_provenance(enriched))
    enriched.setdefault("related_cards", [])
    enriched.setdefault("lifecycle_history", [])
    return enriched


def ensure_store(repo_root: Path) -> Path:
    root = knowledge_root(repo_root)
    for relative in ("cards", "candidates", "evidence", "schemas", "vectors"):
        folder = root / relative
        folder.mkdir(parents=True, exist_ok=True)
        keep = folder / ".gitkeep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")
    store_path = root / "store.json"
    if not store_path.exists():
        write_json(
            store_path,
            {
                "schema_version": 2,
                "store_id": str(uuid.uuid4()),
                "created_at": utc_now(),
                "description": "Kaggle cross-competition knowledge store",
            },
        )
    taxonomy_path = root / "taxonomy.json"
    if not taxonomy_path.exists():
        write_json(taxonomy_path, taxonomy_document())
    schema_path = root / "schemas" / "knowledge-card.schema.json"
    write_json(schema_path, schema_document())
    index_path = root / "index.json"
    if not index_path.exists():
        write_json(
            index_path,
            {
                "schema_version": 2,
                "updated_at": utc_now(),
                "cards": [],
                "candidates": [],
            },
        )
    # 戦略前カタログ: テンプレから空ストアへ確実に配置
    catalog_path = root / "mechanical-improvements.md"
    if not catalog_path.exists():
        for candidate in (
            repo_root / "scripts" / "templates" / "mechanical-improvements.md.template",
            Path(__file__).resolve().parent / "templates" / "mechanical-improvements.md.template",
        ):
            if candidate.is_file():
                catalog_path.write_text(
                    candidate.read_text(encoding="utf-8-sig"),
                    encoding="utf-8",
                )
                break
    readme_path = root / "README.md"
    if not readme_path.exists():
        write_text(
            readme_path,
            "# Kaggle Knowledge\n\n"
            "Kaggleコンペ横断のPrivate知見ストアです。\n\n"
            "- `candidates/`: 未検証候補\n"
            "- `cards/`: 承認・昇格済みカード\n"
            "- `evidence/`: 別コンペでの再現証拠\n"
            "- `index.json`: 自動生成索引\n"
            "- `store.json`: 共有ストア識別子\n"
            "- `taxonomy.json`: 検索用の共通語彙\n"
            "- `mechanical-improvements.md`: 戦略前の機械的改善カタログ（読み専用）\n"
            "- `vectors/`: 将来のPrivateベクトル索引（現在は未生成）\n"
            "- カードはconcept_key・provenance・寿命状態を持つ\n"
            "- 共有前に秘密情報・license auditを通す\n"
            "- 外側のリポジトリでは `knowledge/` 全体をGit除外する\n"
            "- 必要なら本フォルダ自体を別のPrivate Gitリポジトリとして管理する\n",
        )
    return root


def normalize_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:48] or "knowledge"


def card_id(source_competition: str, kind: str, key: str) -> str:
    fingerprint = hashlib.sha256(
        f"{source_competition}|{kind}|{key}".encode("utf-8")
    ).hexdigest()[:10]
    return f"KGL-{normalize_slug(source_competition)}-{normalize_slug(kind)}-{fingerprint}"


def parse_comp_profile(comp_root: Path) -> tuple[list[str], list[str]]:
    profile = comp_root / "docs-ja" / "comp-profile.md"
    if not profile.is_file():
        return ["unknown"], []
    try:
        text = profile.read_text(encoding="utf-8-sig")
    except OSError as exc:
        log_error(f"profile read failed ({profile}): {exc}")
        raise
    type_match = re.search(
        r"\|\s*\*{0,2}comp-type\*{0,2}\s*\|\s*`?([^|`\r\n]+)",
        text,
        re.IGNORECASE,
    )
    comp_type = type_match.group(1).strip() if type_match else "unknown"
    tag_match = re.search(r"\|\s*\*{0,2}副タグ\*{0,2}\s*\|\s*([^|\r\n]+)", text)
    tags = []
    if tag_match:
        tags = [
            item.strip().strip("`").lower()
            for item in tag_match.group(1).split(",")
            if item.strip()
        ]
    return [comp_type.lower()], tags


def iter_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from iter_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_strings(child)


def validate_taxonomy_values(card: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    allowed = taxonomy_document()["dimensions"]
    for dimension, values in card.get("taxonomy", {}).items():
        if dimension not in allowed:
            errors.append(f"unknown taxonomy dimension: {dimension}")
            continue
        for value in values:
            if value not in allowed[dimension]:
                errors.append(f"unknown taxonomy value: {dimension}={value}")
    return errors


def validate_card(card: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(CARD_REQUIRED - set(card))
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")
    if card.get("evidence_level") not in EVIDENCE_LEVELS:
        errors.append("evidence_level must be L0/L1/L2/L3")
    if not re.fullmatch(r"KGL-[a-z0-9-]+", str(card.get("id", ""))):
        errors.append("id must match KGL-[a-z0-9-]+")
    if not re.fullmatch(r"CONCEPT-[a-f0-9]{16}", str(card.get("concept_key", ""))):
        errors.append("concept_key must match CONCEPT-<16 hex>")
    if card.get("lifecycle_status") not in LIFECYCLE_STATUSES:
        errors.append("invalid lifecycle_status")
    provenance = card.get("provenance", {})
    provenance_required = {
        "origin_type", "source_url", "license", "redistribution", "review_status"
    }
    missing_provenance = sorted(provenance_required - set(provenance))
    if missing_provenance:
        errors.append(
            f"provenance missing fields: {', '.join(missing_provenance)}"
        )
    for text in iter_strings(card):
        if ABSOLUTE_PATH_RE.match(text) and not text.startswith(("http://", "https://")):
            errors.append(f"absolute path is forbidden: {text}")
    errors.extend(validate_taxonomy_values(card))
    return errors


def migrate_cards(root: Path) -> int:
    migrated = 0
    for folder in ("cards", "candidates"):
        for path in sorted((root / folder).glob("KGL-*.json")):
            original = read_json(path)
            enriched = enrich_card(original)
            if enriched != original:
                write_json(path, enriched)
                migrated += 1
    return migrated


def audit_store(root: Path) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []
    audit_paths = [
        *sorted((root / "cards").glob("*.json")),
        *sorted((root / "candidates").glob("*.json")),
        *sorted((root / "evidence").glob("**/*.json")),
    ]
    for path in audit_paths:
        document = read_json(path)
        for text in iter_strings(document):
            if ABSOLUTE_PATH_RE.match(text) and not text.startswith(("http://", "https://")):
                failures.append(f"{path.name}: absolute path: {text}")
            for secret_name, pattern in SECRET_PATTERNS.items():
                if pattern.search(text):
                    failures.append(f"{path.name}: possible secret ({secret_name})")
        if path.parent.name not in {"cards", "candidates"}:
            continue
        provenance = document.get("provenance", {})
        origin_type = provenance.get("origin_type", "unknown")
        source_url = str(provenance.get("source_url", ""))
        license_name = str(provenance.get("license", "unknown"))
        review_status = provenance.get("review_status", "pending")
        if origin_type != "own-experiment":
            if not source_url.startswith("https://"):
                failures.append(f"{path.name}: external provenance requires HTTPS source_url")
            if origin_type == "external-code" and license_name == "unknown":
                failures.append(f"{path.name}: external code license is unknown")
            elif license_name == "unknown":
                warnings.append(f"{path.name}: external knowledge license is unknown")
            if review_status != "reviewed":
                warnings.append(f"{path.name}: provenance review is pending")
            if len(str(document.get("search_document", ""))) > 4000:
                warnings.append(f"{path.name}: external summary may contain excessive copied text")
    return sorted(set(failures)), sorted(set(warnings))


def command_audit(repo_root: Path) -> int:
    root = ensure_store(repo_root)
    failures, warnings = audit_store(root)
    for warning in warnings:
        print(f"[kaggle-knowledge] WARN: {warning}")
    for failure in failures:
        log_error(failure)
    print(
        f"[kaggle-knowledge] audit failures={len(failures)} "
        f"warnings={len(warnings)}"
    )
    return 1 if failures else 0


def save_candidate(root: Path, card: dict[str, Any]) -> bool:
    card = enrich_card(card)
    errors = validate_card(card)
    if errors:
        raise ValueError(f"{card.get('id', '?')}: {'; '.join(errors)}")
    candidate_path = root / "candidates" / f"{card['id']}.json"
    promoted_path = root / "cards" / f"{card['id']}.json"
    if candidate_path.exists() or promoted_path.exists():
        return False
    write_json(candidate_path, card)
    return True


def harvest_failures(repo_root: Path, comp_root: Path, root: Path) -> int:
    failures_path = comp_root / "exp" / "improvement-loop-failures.json"
    if not failures_path.is_file():
        return 0
    document = read_json(failures_path)
    competition = comp_root.name
    competition_types, profile_tags = parse_comp_profile(comp_root)
    source = relative_ref(repo_root, failures_path)
    created = 0
    for failure in document.get("failures", []):
        failure_id = str(failure.get("id", "")).strip()
        reason = str(failure.get("reason", "")).strip()
        if not failure_id or not reason:
            continue
        keywords = [str(item) for item in failure.get("keywords", []) if str(item).strip()]
        actions = [
            str(item) for item in failure.get("action_types_blocked", []) if str(item).strip()
        ]
        key = f"{failure_id}|{reason}"
        card = {
            "schema_version": 1,
            "id": card_id(competition, "anti-pattern", key),
            "status": "candidate",
            "title": f"{failure_id}: {reason[:100]}",
            "kind": "anti-pattern",
            "source_competition": competition,
            "competition_types": competition_types,
            "problem_signature": keywords,
            "intervention": actions,
            "mechanism": reason,
            "outcome": "NO-GO",
            "conditions": (
                [f"base_pattern={failure['base_pattern']}"]
                if failure.get("base_pattern")
                else []
            ),
            "contraindications": [],
            "evidence_level": "L0",
            "confidence": "low",
            "transferability": "conditional",
            "default_policy_eligible": False,
            "source_refs": [f"{source}#{failure_id}"],
            "tags": sorted(set(["failure-ledger", *profile_tags, *[a.lower() for a in actions]])),
            "created_at": utc_now(),
        }
        if save_candidate(root, card):
            created += 1
    return created


def lesson_axis_tag(heading: str) -> str:
    """Map retro-lessons ### heading text to a knowledge-axis tag."""
    h = heading.lower()
    # A: CV / selection yardstick (Japanese + English cues)
    if any(
        key in heading
        for key in (
            "CV",
            "cv",
            "物差し",
            "提出判断",
            "validation",
            "yardstick",
            "選択",
        )
    ) or re.search(r"(?i)\bA\b", heading) or heading.strip().startswith(("A.", "A．", "A ")):
        return "knowledge-axis-cv-validation"
    # B: solution / modeling
    if any(
        key in heading
        for key in (
            "解法",
            "モデリング",
            "モデル",
            "method",
            "solution",
            "本体",
        )
    ) or re.search(r"(?i)\bB\b", heading) or heading.strip().startswith(("B.", "B．", "B ")):
        return "knowledge-axis-method-solution"
    # C: ops / CLI / post-comp hygiene
    if any(
        key in heading
        for key in (
            "運用",
            "post-comp",
            "postcomp",
            "CLI",
            "cli",
            "CodeComp",
            "提出",
            "保管",
        )
    ) or re.search(r"(?i)\bC\b", heading) or heading.strip().startswith(("C.", "C．", "C ")):
        return "knowledge-axis-ops"
    return "knowledge-axis-unclassified"



def extract_generic_lessons(path: Path) -> list[dict[str, Any]]:
    """Parse structured lessons under ``## 汎用``.

    Each item starts with ``N. **Title**`` and optional field lines:

    - body: ...
    - apply: ...   → conditions
    - avoid: ...   → contraindications
    - origin: own|topsolution|ops|mixed
    - domain: kaggle|ahc|shared
    - evidence: ...
    """
    if not path.is_file():
        return []
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except OSError as exc:
        log_error(f"retro lessons read failed ({path}): {exc}")
        raise

    active = False
    axis_tag = "knowledge-axis-unclassified"
    lessons: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    def flush() -> None:
        nonlocal current
        if not current:
            return
        title = str(current.get("title", "")).strip()
        if not title or "要記入" in title:
            current = None
            return
        current.setdefault("body", "")
        current.setdefault("apply", "")
        current.setdefault("avoid", "")
        current.setdefault("origin", "mixed")
        current.setdefault("domain", "kaggle")
        current.setdefault("evidence", "")
        current["axis_tag"] = current.get("axis_tag") or axis_tag
        lessons.append(current)
        current = None

    field_re = re.compile(
        r"^\s*-\s*(body|apply|avoid|origin|domain|evidence)\s*:\s*(.+?)\s*$",
        re.IGNORECASE,
    )
    item_re = re.compile(r"^\s*\d+\.\s+(.+?)\s*$")

    for line_number, line in enumerate(lines, start=1):
        if re.match(r"^##\s+汎用", line):
            flush()
            active = True
            axis_tag = "knowledge-axis-unclassified"
            continue
        if active and line.startswith("## "):
            if re.match(r"^##\s+汎用", line):
                flush()
                axis_tag = "knowledge-axis-unclassified"
                continue
            flush()
            break
        if not active:
            continue
        h3 = re.match(r"^###\s+(.+?)\s*$", line)
        if h3:
            flush()
            axis_tag = lesson_axis_tag(h3.group(1))
            continue
        item = item_re.match(line)
        if item:
            raw = item.group(1).strip()
            if raw.startswith("|") or raw in {"—", "-"} or "要記入" in raw:
                continue
            flush()
            title = re.sub(r"^\*\*(.+?)\*\*$", r"\1", raw).strip()
            current = {
                "line": line_number,
                "title": title[:200],
                "axis_tag": axis_tag,
            }
            continue
        if current is None:
            continue
        field = field_re.match(line)
        if field:
            key = field.group(1).lower()
            val = field.group(2).strip()
            current[key] = val
            continue

    flush()
    return lessons


def _split_field_list(text: str) -> list[str]:
    if not text:
        return []
    parts = re.split(r"\s*[;；|/]\s*|\s+·\s+", text)
    return [p.strip() for p in parts if p.strip() and p.strip() not in {"—", "-"}]


def harvest_lessons(repo_root: Path, comp_root: Path, root: Path) -> int:
    lessons_path = comp_root / "retro" / "retro-lessons.md"
    competition = comp_root.name
    competition_types, profile_tags = parse_comp_profile(comp_root)
    source = relative_ref(repo_root, lessons_path)
    created = 0
    for item in extract_generic_lessons(lessons_path):
        title = str(item["title"])
        axis_tag = str(item.get("axis_tag") or "knowledge-axis-unclassified")
        body = str(item.get("body") or "")
        apply = str(item.get("apply") or "")
        avoid = str(item.get("avoid") or "")
        origin = str(item.get("origin") or "mixed").lower()
        domain = str(item.get("domain") or "kaggle").lower()
        evidence = str(item.get("evidence") or "")
        line_number = int(item.get("line") or 0)

        conditions = _split_field_list(apply) or ([apply] if apply else [])
        contraindications = _split_field_list(avoid) or ([avoid] if avoid else [])
        if apply and len(conditions) > 3:
            conditions = [apply]
        if avoid and len(contraindications) > 3:
            contraindications = [avoid]

        tags = sorted(
            set(
                [
                    "retro-lesson",
                    axis_tag,
                    f"origin-{origin}",
                    f"domain-{domain}",
                    "transfer-conditional",
                    *profile_tags,
                ]
            )
        )
        mechanism_parts = [axis_tag]
        if body:
            mechanism_parts.append(body)
        if evidence:
            mechanism_parts.append(f"evidence: {evidence}")
        mechanism = " | ".join(mechanism_parts)

        intervention = [title]
        if body:
            intervention.append(body)
        intervention.append(
            f"[conditional] apply: {apply or '（未記入→採用前に人手で条件を書け）'}"
        )
        intervention.append(f"[avoid] {avoid or '（未記入）'}")

        card = {
            "schema_version": 1,
            "id": card_id(competition, "lesson", title + "|" + body[:80]),
            "status": "candidate",
            "title": title[:120],
            "kind": "lesson",
            "source_competition": competition,
            "competition_types": competition_types,
            "problem_signature": [],
            "intervention": intervention,
            "mechanism": mechanism[:2000],
            "outcome": "reported lesson (conditional transfer)",
            "conditions": conditions,
            "contraindications": contraindications,
            "evidence_level": "L0",
            "confidence": "low",
            "transferability": "conditional",
            "default_policy_eligible": False,
            "source_refs": [f"{source}#L{line_number}"],
            "tags": tags,
            "created_at": utc_now(),
        }
        if save_candidate(root, card):
            created += 1
    return created


def load_cards(root: Path, include_candidates: bool) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for path in sorted((root / "cards").glob("KGL-*.json")):
        cards.append(read_json(path))
    if include_candidates:
        for path in sorted((root / "candidates").glob("KGL-*.json")):
            card = read_json(path)
            if card.get("status") == "candidate":
                cards.append(card)
    return cards


def rebuild_index(root: Path) -> None:
    cards = load_cards(root, include_candidates=False)
    summaries = [
        {
            "id": card["id"],
            "concept_key": card["concept_key"],
            "title": card["title"],
            "kind": card["kind"],
            "lifecycle_status": card["lifecycle_status"],
            "competition_types": card["competition_types"],
            "evidence_level": card["evidence_level"],
            "tags": card["tags"],
            "taxonomy": card.get("taxonomy", {}),
            "embedding_status": card.get("embedding", {}).get("status", "not-generated"),
            "provenance_review": card.get("provenance", {}).get("review_status", "pending"),
        }
        for card in cards
    ]
    write_json(
        root / "index.json",
        {"version": 1, "updated_at": utc_now(), "cards": summaries},
    )


def find_card(root: Path, card_id_value: str) -> tuple[Path, dict[str, Any]]:
    for folder in ("cards", "candidates"):
        path = root / folder / f"{card_id_value}.json"
        if path.is_file():
            return path, read_json(path)
    raise FileNotFoundError(f"knowledge card not found: {card_id_value}")


def evidence_files(root: Path, card_id_value: str) -> list[Path]:
    folder = root / "evidence" / card_id_value
    return sorted(folder.glob("*.json")) if folder.is_dir() else []


def evidence_ceiling(root: Path, card_id_value: str) -> str:
    own_go: dict[str, int] = {}
    top_solution_competitions: set[str] = set()
    for path in evidence_files(root, card_id_value):
        evidence = read_json(path)
        if evidence.get("verdict") != "GO":
            continue
        competition = str(evidence.get("competition", ""))
        if evidence.get("evidence_type") == "top-solution":
            top_solution_competitions.add(competition)
        else:
            own_go[competition] = own_go.get(competition, 0) + 1
    distinct_own = len(own_go)
    if distinct_own >= 2 and top_solution_competitions:
        return "L3"
    if distinct_own >= 2:
        return "L2"
    if any(count >= 2 for count in own_go.values()):
        return "L1"
    return "L0"


def validate_source_ref(value: str) -> None:
    if not value.strip():
        raise ValueError("--source-ref must not be empty")
    if ABSOLUTE_PATH_RE.match(value) and not value.startswith(("http://", "https://")):
        raise ValueError(f"absolute source_ref is forbidden: {value}")


def command_feedback(
    repo_root: Path,
    comp_root: Path,
    card_id_value: str,
    experiment_id: str,
    verdict: str,
    source_refs: list[str],
    evidence_type: str,
) -> int:
    if not card_id_value or not experiment_id:
        raise ValueError("feedback requires --card-id and --experiment-id")
    if verdict not in {"GO", "NO-GO", "MIXED"}:
        raise ValueError("feedback verdict must be GO/NO-GO/MIXED")
    if evidence_type not in {"own-experiment", "top-solution"}:
        raise ValueError("invalid evidence type")
    if not source_refs:
        raise ValueError("feedback requires at least one --source-ref")
    for source_ref in source_refs:
        validate_source_ref(source_ref)
    root = ensure_store(repo_root)
    card_path, card = find_card(root, card_id_value)
    if card.get("lifecycle_status") == "superseded":
        raise ValueError(
            f"card is superseded; use {card.get('superseded_by', 'canonical card')}"
        )
    competition_types, profile_tags = parse_comp_profile(comp_root)
    key = f"{card_id_value}|{comp_root.name}|{experiment_id}|{evidence_type}"
    evidence_id = f"EVD-{hashlib.sha256(key.encode('utf-8')).hexdigest()[:12]}"
    evidence = {
        "schema_version": 1,
        "id": evidence_id,
        "card_id": card_id_value,
        "competition": comp_root.name,
        "competition_types": competition_types,
        "taxonomy": infer_taxonomy(competition_types, profile_tags),
        "experiment_id": experiment_id,
        "verdict": verdict,
        "evidence_type": evidence_type,
        "source_refs": source_refs,
        "created_at": utc_now(),
    }
    for text in iter_strings(evidence):
        if ABSOLUTE_PATH_RE.match(text) and not text.startswith(("http://", "https://")):
            raise ValueError(f"absolute path is forbidden: {text}")
    output = root / "evidence" / card_id_value / f"{evidence_id}.json"
    if output.exists():
        existing = read_json(output)
        comparable_existing = {k: v for k, v in existing.items() if k != "created_at"}
        comparable_new = {k: v for k, v in evidence.items() if k != "created_at"}
        if comparable_existing != comparable_new:
            raise ValueError(f"evidence conflict: {evidence_id}")
        print(f"[kaggle-knowledge] feedback already exists: {evidence_id}")
    else:
        write_json(output, evidence)
        print(f"[kaggle-knowledge] feedback recorded: {evidence_id}")
        if verdict in {"NO-GO", "MIXED"}:
            contradiction = (
                f"{comp_root.name}:{experiment_id}:{verdict} "
                f"({', '.join(source_refs)})"
            )
            contraindications = list(card.get("contraindications", []))
            if contradiction not in contraindications:
                contraindications.append(contradiction)
            card["contraindications"] = contraindications
            if card.get("lifecycle_status") == "active":
                card["lifecycle_status"] = "disputed"
            history = list(card.get("lifecycle_history", []))
            history.append(
                {
                    "timestamp": utc_now(),
                    "status": card.get("lifecycle_status", "conditional"),
                    "reason": contradiction,
                    "source_ref": source_refs[0],
                }
            )
            card["lifecycle_history"] = history
            write_json(card_path, enrich_card(card))
    print(
        f"[kaggle-knowledge] promotion ceiling "
        f"{card_id_value}={evidence_ceiling(root, card_id_value)}"
    )
    return 0


def character_ngrams(value: str, size: int = 3) -> set[str]:
    normalized = normalize_concept_text(value).replace(" ", "")
    if len(normalized) <= size:
        return {normalized} if normalized else set()
    return {
        normalized[index:index + size]
        for index in range(len(normalized) - size + 1)
    }


def concept_similarity(left: dict[str, Any], right: dict[str, Any]) -> tuple[float, list[str]]:
    if left.get("concept_key") == right.get("concept_key"):
        return 1.0, ["exact-concept-key"]
    left_grams = character_ngrams(str(left.get("search_document", "")))
    right_grams = character_ngrams(str(right.get("search_document", "")))
    union = left_grams | right_grams
    lexical = len(left_grams & right_grams) / len(union) if union else 0.0
    reasons = [f"char-3gram={lexical:.3f}"]
    left_taxonomy = left.get("taxonomy", {})
    right_taxonomy = right.get("taxonomy", {})
    shared_dimensions = sum(
        1
        for dimension, values in left_taxonomy.items()
        if set(values).intersection(right_taxonomy.get(dimension, []))
    )
    taxonomy_bonus = min(shared_dimensions * 0.03, 0.12)
    if shared_dimensions:
        reasons.append(f"taxonomy-shared={shared_dimensions}")
    return min(lexical + taxonomy_bonus, 0.99), reasons


def command_duplicates(repo_root: Path, threshold: float) -> int:
    if threshold < 0.0 or threshold > 1.0:
        raise ValueError("duplicate threshold must be between 0 and 1")
    root = ensure_store(repo_root)
    cards = [
        card
        for card in load_cards(root, include_candidates=True)
        if card.get("lifecycle_status") not in {"superseded", "deprecated"}
    ]
    pairs: list[dict[str, Any]] = []
    for left_index, left in enumerate(cards):
        for right in cards[left_index + 1:]:
            score, reasons = concept_similarity(left, right)
            if score < threshold:
                continue
            pairs.append(
                {
                    "left_card_id": left["id"],
                    "right_card_id": right["id"],
                    "score": round(score, 4),
                    "reasons": reasons,
                    "left_concept_key": left["concept_key"],
                    "right_concept_key": right["concept_key"],
                    "action": "review-only; alias requires user approval",
                }
            )
    pairs.sort(key=lambda item: (-item["score"], item["left_card_id"], item["right_card_id"]))
    output = root / "duplicate-candidates.json"
    write_json(
        output,
        {
            "version": 1,
            "updated_at": utc_now(),
            "threshold": threshold,
            "pairs": pairs,
        },
    )
    print(
        f"[kaggle-knowledge] duplicate candidates={len(pairs)} "
        f"output=knowledge/duplicate-candidates.json"
    )
    return 0


def append_lifecycle_history(
    card: dict[str, Any], status: str, reason: str, source_ref: str = ""
) -> None:
    history = list(card.get("lifecycle_history", []))
    history.append(
        {
            "timestamp": utc_now(),
            "status": status,
            "reason": reason,
            "source_ref": source_ref,
        }
    )
    card["lifecycle_history"] = history


def command_alias(
    repo_root: Path,
    source_card_id: str,
    target_card_id: str,
    reason: str,
    approved: bool,
) -> int:
    if not approved:
        raise ValueError("alias requires --approve after user confirmation")
    if not source_card_id or not target_card_id or source_card_id == target_card_id:
        raise ValueError("alias requires different source and target card IDs")
    if not reason.strip():
        raise ValueError("alias requires --reason")
    root = ensure_store(repo_root)
    source_path, source = find_card(root, source_card_id)
    target_path, target = find_card(root, target_card_id)
    if source.get("lifecycle_status") == "superseded":
        raise ValueError("source card is already superseded")
    if target.get("lifecycle_status") in {"superseded", "deprecated"}:
        raise ValueError("target card must be active/conditional/disputed")

    target["source_refs"] = sorted(
        set(target.get("source_refs", [])) | set(source.get("source_refs", []))
    )
    target["related_cards"] = sorted(
        set(target.get("related_cards", [])) | {source_card_id}
    )
    source["related_cards"] = sorted(
        set(source.get("related_cards", [])) | {target_card_id}
    )
    source["original_concept_key"] = source.get("concept_key")
    source["concept_key"] = target["concept_key"]
    source["lifecycle_status"] = "superseded"
    source["superseded_by"] = target_card_id
    append_lifecycle_history(source, "superseded", reason)
    append_lifecycle_history(target, target.get("lifecycle_status", "conditional"), reason)

    copied_evidence = 0
    for evidence_path in evidence_files(root, source_card_id):
        evidence = read_json(evidence_path)
        evidence["card_id"] = target_card_id
        evidence["aliased_from"] = source_card_id
        target_evidence = root / "evidence" / target_card_id / evidence_path.name
        if target_evidence.exists():
            if read_json(target_evidence) != evidence:
                raise ValueError(f"alias evidence conflict: {evidence_path.name}")
            continue
        write_json(target_evidence, evidence)
        copied_evidence += 1

    write_json(target_path, enrich_card(target))
    write_json(source_path, enrich_card(source))
    rebuild_index(root)
    print(
        f"[kaggle-knowledge] alias source={source_card_id} "
        f"target={target_card_id} evidence_copied={copied_evidence}"
    )
    return 0


def command_lifecycle(
    repo_root: Path,
    card_id_value: str,
    lifecycle_status: str,
    reason: str,
    source_ref: str,
    approved: bool,
) -> int:
    if not approved:
        raise ValueError("lifecycle change requires --approve")
    if lifecycle_status not in LIFECYCLE_STATUSES - {"superseded"}:
        raise ValueError("use alias action to set superseded")
    if not reason.strip():
        raise ValueError("lifecycle change requires --reason")
    if source_ref:
        validate_source_ref(source_ref)
    root = ensure_store(repo_root)
    path, card = find_card(root, card_id_value)
    if lifecycle_status == "active":
        ceiling = evidence_ceiling(root, card_id_value)
        if EVIDENCE_RANK[ceiling] < EVIDENCE_RANK["L2"]:
            raise ValueError("active lifecycle requires L2 or higher evidence ceiling")
    card["lifecycle_status"] = lifecycle_status
    append_lifecycle_history(card, lifecycle_status, reason, source_ref)
    write_json(path, enrich_card(card))
    rebuild_index(root)
    print(f"[kaggle-knowledge] lifecycle {card_id_value}={lifecycle_status}")
    return 0


def store_is_empty(root: Path) -> bool:
    data_files = [
        *list((root / "cards").glob("*.json")),
        *list((root / "candidates").glob("*.json")),
        *list((root / "evidence").glob("**/*.json")),
    ]
    return len(data_files) == 0


def resolve_peer_knowledge(repo_root: Path, value: str) -> Path:
    if not value:
        raise ValueError("sync requires --peer-root")
    raw = Path(value)
    candidate = (repo_root / raw).resolve() if not raw.is_absolute() else raw.resolve()
    if not candidate.is_dir() or not (candidate / "store.json").is_file():
        raise ValueError("peer root must be an initialized knowledge/ directory")
    return candidate


def file_digest(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        log_error(f"hash read failed ({path}): {exc}")
        raise


def sync_relative_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for folder in ("cards", "candidates", "evidence", "schemas"):
        base = root / folder
        if base.is_dir():
            files.extend(path for path in base.glob("**/*") if path.is_file())
    for name in ("taxonomy.json", "vector-index.json", "mechanical-improvements.md"):
        path = root / name
        if path.is_file():
            files.append(path)
    return sorted(files)


def command_sync(
    repo_root: Path,
    peer_root_value: str,
    direction: str,
    apply: bool,
    adopt_store: bool,
) -> int:
    if direction not in {"pull", "push"}:
        raise ValueError("sync direction must be pull/push")
    local = ensure_store(repo_root)
    peer = resolve_peer_knowledge(repo_root, peer_root_value)
    source, destination = (peer, local) if direction == "pull" else (local, peer)
    for label, audit_root in (("source", source), ("destination", destination)):
        failures, warnings = audit_store(audit_root)
        for warning in warnings:
            print(f"[kaggle-knowledge] WARN {label}: {warning}")
        if failures:
            for failure in failures:
                log_error(f"sync audit {label}: {failure}")
            return 1
    source_store = read_json(source / "store.json")
    destination_store = read_json(destination / "store.json")
    adopt_required = False
    if source_store.get("store_id") != destination_store.get("store_id"):
        if not adopt_store:
            raise ValueError(
                "store_id mismatch; use --adopt-store only for an empty destination"
            )
        if not store_is_empty(destination):
            raise ValueError("cannot adopt store_id into a non-empty destination")
        adopt_required = True
    additions: list[tuple[Path, Path]] = []
    conflicts: list[str] = []
    for source_path in sync_relative_files(source):
        relative = source_path.relative_to(source)
        destination_path = destination / relative
        if not destination_path.exists():
            additions.append((source_path, destination_path))
        elif file_digest(source_path) != file_digest(destination_path):
            conflicts.append(relative.as_posix())
    print(
        f"[kaggle-knowledge] sync direction={direction} apply={str(apply).lower()} "
        f"additions={len(additions)} conflicts={len(conflicts)}"
    )
    if conflicts:
        for conflict in conflicts[:20]:
            log_error(f"sync conflict (no overwrite): {conflict}")
        return 1
    if not apply:
        print("[kaggle-knowledge] dry-run only; add --apply after review")
        return 0
    if adopt_required:
        adopted = dict(destination_store)
        adopted["store_id"] = source_store["store_id"]
        adopted["adopted_at"] = utc_now()
        write_json(destination / "store.json", adopted)
    for source_path, destination_path in additions:
        try:
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination_path)
        except OSError as exc:
            log_error(f"sync copy failed ({source_path}): {exc}")
            raise
    print(f"[kaggle-knowledge] synced additions={len(additions)} (no deletion)")
    return 0


def command_init(repo_root: Path) -> int:
    root = ensure_store(repo_root)
    migrated = migrate_cards(root)
    rebuild_index(root)
    print(f"[kaggle-knowledge] initialized: knowledge/ migrated={migrated}")
    return 0


def command_harvest(repo_root: Path, comp_root: Path) -> int:
    root = ensure_store(repo_root)
    failures = harvest_failures(repo_root, comp_root, root)
    lessons = harvest_lessons(repo_root, comp_root, root)
    rebuild_index(root)
    print(
        f"[kaggle-knowledge] harvested candidates={failures + lessons} "
        f"(failures={failures}, lessons={lessons})"
    )
    return 0


def command_promote(
    repo_root: Path, card_id_value: str, evidence_level: str, approved: bool
) -> int:
    if not approved:
        raise ValueError("promotion requires --approve after user confirmation")
    if evidence_level not in EVIDENCE_LEVELS:
        raise ValueError("evidence level must be L0/L1/L2/L3")
    root = ensure_store(repo_root)
    candidate_path = root / "candidates" / f"{card_id_value}.json"
    candidate = read_json(candidate_path)
    if candidate.get("status") != "candidate":
        raise ValueError(f"candidate is not promotable: {card_id_value}")
    ceiling = evidence_ceiling(root, card_id_value)
    if EVIDENCE_RANK[evidence_level] > EVIDENCE_RANK[ceiling]:
        raise ValueError(
            f"requested {evidence_level} exceeds evidence ceiling {ceiling}"
        )
    promoted = enrich_card(candidate)
    promoted["status"] = "validated"
    promoted["evidence_level"] = evidence_level
    promoted["confidence"] = "high" if evidence_level in {"L2", "L3"} else "medium"
    promoted["transferability"] = (
        "general" if evidence_level in {"L2", "L3"} else "conditional"
    )
    promoted["default_policy_eligible"] = evidence_level in {"L2", "L3"}
    promoted["lifecycle_status"] = (
        "active" if evidence_level in {"L2", "L3"} else "conditional"
    )
    append_lifecycle_history(
        promoted,
        promoted["lifecycle_status"],
        f"promoted with evidence {evidence_level}",
    )
    promoted["promoted_at"] = utc_now()
    errors = validate_card(promoted)
    if errors:
        raise ValueError("; ".join(errors))
    write_json(root / "cards" / f"{card_id_value}.json", promoted)
    candidate["status"] = "promoted"
    candidate["promoted_to"] = f"cards/{card_id_value}.json"
    write_json(candidate_path, candidate)
    rebuild_index(root)
    print(
        f"[kaggle-knowledge] promoted {card_id_value} "
        f"evidence={evidence_level} ceiling={ceiling} "
        f"default={promoted['default_policy_eligible']}"
    )
    return 0


def score_card(
    card: dict[str, Any], competition_types: list[str], profile_tags: list[str]
) -> int:
    score = 2 if card.get("status") == "validated" else 0
    if card.get("lifecycle_status") == "disputed":
        score -= 3
    card_types = {str(item).lower() for item in card.get("competition_types", [])}
    if "all" in card_types:
        score += 3
    if card_types.intersection(competition_types):
        score += 5
    card_tags = {str(item).lower() for item in card.get("tags", [])}
    score += len(card_tags.intersection(profile_tags))
    profile_taxonomy = infer_taxonomy(competition_types, profile_tags)
    for dimension, values in card.get("taxonomy", {}).items():
        if set(values).intersection(profile_taxonomy.get(dimension, [])):
            score += 2
    return score


def command_retrieve(
    repo_root: Path, comp_root: Path, include_candidates: bool, limit: int
) -> int:
    if limit <= 0:
        raise ValueError("--limit must be positive")
    root = ensure_store(repo_root)
    competition_types, profile_tags = parse_comp_profile(comp_root)
    retrievable_cards = [
        card
        for card in load_cards(root, include_candidates)
        if card.get("lifecycle_status") not in {"deprecated", "superseded"}
    ]
    ranked = sorted(
        retrievable_cards,
        key=lambda card: (
            score_card(card, competition_types, profile_tags),
            card.get("evidence_level", ""),
            card.get("id", ""),
        ),
        reverse=True,
    )
    selected = [
        card
        for card in ranked
        if score_card(card, competition_types, profile_tags) > 0
    ][:limit]
    output = comp_root / "exp" / "prior-knowledge.md"
    lines = [
        f"# prior-knowledge — {comp_root.name}",
        "",
        "> 自動生成。SSOTはリポジトリ相対の `knowledge/`。",
        "> 候補を自動でCHK化しない。条件と根拠を確認し、ユーザー承認後に実験へ昇格する。",
        "",
        f"- comp-type: `{', '.join(competition_types)}`",
        f"- include-candidates: `{str(include_candidates).lower()}`",
        f"- selected: `{len(selected)}`",
        "",
    ]
    if not selected:
        lines.extend(["## 該当知見", "", "該当する承認済み知見はありません。", ""])
    for card in selected:
        evidence_count = len(evidence_files(root, card["id"]))
        ceiling = evidence_ceiling(root, card["id"])
        lines.extend(
            [
                f"## {card['id']} — {card['title']}",
                "",
                f"- 状態: `{card['status']}` / 証拠: `{card['evidence_level']}`",
                f"- 種別: `{card['kind']}` / 転用: `{card['transferability']}` / 寿命: `{card['lifecycle_status']}`",
                f"- 再検証: `{evidence_count}`件 / 昇格上限: `{ceiling}`",
                f"- 結果: {card.get('outcome', '')}",
                f"- 条件・兆候: {', '.join(card.get('problem_signature', [])) or '未整理'}",
                f"- 施策: {', '.join(card.get('intervention', [])) or '未整理'}",
                f"- 根拠: {', '.join(card.get('source_refs', []))}",
                "",
            ]
        )
    write_text(output, "\n".join(lines))
    print(
        f"[kaggle-knowledge] retrieved={len(selected)} "
        f"output={relative_ref(repo_root, output)}"
    )
    return 0


def command_validate(repo_root: Path) -> int:
    root = ensure_store(repo_root)
    errors: list[str] = []
    ids: set[str] = set()
    store = read_json(root / "store.json")
    try:
        uuid.UUID(str(store.get("store_id", "")))
    except ValueError:
        errors.append("store.json: invalid store_id UUID")
    for folder in ("cards", "candidates"):
        for path in sorted((root / folder).glob("*.json")):
            document = read_json(path)
            card_errors = validate_card(document)
            if document.get("id") in ids and folder == "cards":
                # promoted候補との重複は許可し、cards同士だけを一意にする。
                card_errors.append(f"duplicate card id: {document.get('id')}")
            if folder == "cards":
                ids.add(str(document.get("id", "")))
            errors.extend(f"{path.name}: {message}" for message in card_errors)
    evidence_required = {
        "schema_version", "id", "card_id", "competition",
        "competition_types", "taxonomy", "experiment_id", "verdict",
        "evidence_type", "source_refs", "created_at",
    }
    for path in sorted((root / "evidence").glob("**/*.json")):
        evidence = read_json(path)
        missing = sorted(evidence_required - set(evidence))
        if missing:
            errors.append(f"{path.name}: missing fields: {', '.join(missing)}")
        if evidence.get("verdict") not in {"GO", "NO-GO", "MIXED"}:
            errors.append(f"{path.name}: invalid verdict")
        if not any(
            (root / folder / f"{evidence.get('card_id', '')}.json").is_file()
            for folder in ("cards", "candidates")
        ):
            errors.append(f"{path.name}: card_id not found")
        for text in iter_strings(evidence):
            if ABSOLUTE_PATH_RE.match(text) and not text.startswith(("http://", "https://")):
                errors.append(f"{path.name}: absolute path is forbidden: {text}")
    if errors:
        for error in errors:
            log_error(error)
        return 1
    rebuild_index(root)
    print("[kaggle-knowledge] validation PASS (relative paths only)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Kaggle cross-competition knowledge")
    parser.add_argument(
        "action",
        choices=[
            "init", "harvest", "audit", "duplicates", "alias",
            "feedback", "lifecycle", "promote", "retrieve", "sync", "validate",
        ],
    )
    parser.add_argument("--repo-root", default="")
    parser.add_argument("--comp-root", default="")
    parser.add_argument("--card-id", default="")
    parser.add_argument("--source-card-id", default="")
    parser.add_argument("--target-card-id", default="")
    parser.add_argument("--evidence-level", default="")
    parser.add_argument("--lifecycle-status", default="")
    parser.add_argument("--reason", default="")
    parser.add_argument("--experiment-id", default="")
    parser.add_argument("--verdict", default="")
    parser.add_argument(
        "--evidence-type",
        choices=["own-experiment", "top-solution"],
        default="own-experiment",
    )
    parser.add_argument("--source-ref", action="append", default=[])
    parser.add_argument("--peer-root", default="")
    parser.add_argument("--direction", choices=["pull", "push"], default="pull")
    parser.add_argument("--include-candidates", action="store_true")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--threshold", type=float, default=0.72)
    parser.add_argument("--approve", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--adopt-store", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        repo_root = resolve_repo_root(args.repo_root)
        if args.action == "init":
            return command_init(repo_root)
        if args.action == "validate":
            return command_validate(repo_root)
        if args.action == "audit":
            return command_audit(repo_root)
        if args.action == "duplicates":
            return command_duplicates(repo_root, args.threshold)
        if args.action == "alias":
            return command_alias(
                repo_root,
                args.source_card_id,
                args.target_card_id,
                args.reason,
                args.approve,
            )
        if args.action == "lifecycle":
            return command_lifecycle(
                repo_root,
                args.card_id,
                args.lifecycle_status,
                args.reason,
                args.source_ref[0] if args.source_ref else "",
                args.approve,
            )
        if args.action == "sync":
            return command_sync(
                repo_root,
                args.peer_root,
                args.direction,
                args.apply,
                args.adopt_store,
            )
        if args.action == "promote":
            if not args.card_id:
                raise ValueError("promote requires --card-id")
            return command_promote(
                repo_root, args.card_id, args.evidence_level, args.approve
            )
        comp_root = resolve_comp_root(repo_root, args.comp_root)
        if args.action == "harvest":
            return command_harvest(repo_root, comp_root)
        if args.action == "feedback":
            return command_feedback(
                repo_root,
                comp_root,
                args.card_id,
                args.experiment_id,
                args.verdict,
                args.source_ref,
                args.evidence_type,
            )
        return command_retrieve(
            repo_root, comp_root, args.include_candidates, args.limit
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        log_error(str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
