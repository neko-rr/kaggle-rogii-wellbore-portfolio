#!/usr/bin/env python3
"""Kaggle知見ストアの安全同期・証拠上限テスト。"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kaggle_knowledge as kk


class KaggleKnowledgeTest(unittest.TestCase):
    def make_repo(self, root: Path, name: str) -> Path:
        repo = root / name
        (repo / "scripts").mkdir(parents=True)
        kk.ensure_store(repo)
        return repo

    def make_comp(self, repo: Path, name: str) -> Path:
        comp = repo / name
        (comp / "exp").mkdir(parents=True)
        (comp / "docs-ja").mkdir(parents=True)
        (comp / "docs-ja" / "comp-profile.md").write_text(
            "## コンペ型\n\n| 項目 | 値 |\n|---|---|\n"
            "| **comp-type** | image-heavy |\n"
            "| **副タグ** | onnx-per-task, cost-minimization |\n",
            encoding="utf-8",
        )
        return comp

    def make_candidate(self, repo: Path, card_id: str) -> None:
        root = kk.ensure_store(repo)
        card = kk.enrich_card(
            {
                "schema_version": 1,
                "id": card_id,
                "status": "candidate",
                "title": "同じ作用型の再現テスト",
                "kind": "lesson",
                "source_competition": "source-comp",
                "competition_types": ["image-heavy"],
                "problem_signature": ["repeated-no-go"],
                "intervention": ["change-action-type"],
                "outcome": "reported lesson",
                "evidence_level": "L0",
                "confidence": "low",
                "transferability": "conditional",
                "source_refs": ["source-comp/retro/retro-lessons.md#L1"],
                "tags": ["onnx-per-task"],
            }
        )
        kk.write_json(root / "candidates" / f"{card_id}.json", card)

    def test_sync_is_dry_run_and_never_overwrites(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            local_repo = self.make_repo(base, "local")
            peer_repo = self.make_repo(base, "peer")
            local_root = kk.knowledge_root(local_repo)
            peer_root = kk.knowledge_root(peer_repo)
            peer_store = kk.read_json(peer_root / "store.json")
            local_store = kk.read_json(local_root / "store.json")
            peer_store["store_id"] = local_store["store_id"]
            kk.write_json(peer_root / "store.json", peer_store)
            self.make_candidate(peer_repo, "KGL-sync-marker")
            marker = peer_root / "candidates" / "KGL-sync-marker.json"

            result = kk.command_sync(
                local_repo, str(peer_root), "pull", apply=False, adopt_store=False
            )
            self.assertEqual(result, 0)
            self.assertFalse((local_root / "candidates" / marker.name).exists())

            result = kk.command_sync(
                local_repo, str(peer_root), "pull", apply=True, adopt_store=False
            )
            self.assertEqual(result, 0)
            copied = local_root / "candidates" / marker.name
            self.assertTrue(copied.is_file())

            conflicting = kk.read_json(marker)
            conflicting["title"] = "競合させる変更"
            kk.write_json(marker, kk.enrich_card(conflicting))
            self.assertEqual(
                kk.command_sync(
                    local_repo, str(peer_root), "pull", apply=True, adopt_store=False
                ),
                1,
            )
            self.assertNotEqual(
                kk.read_json(copied)["title"],
                kk.read_json(marker)["title"],
            )

    def test_feedback_controls_promotion_ceiling(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = self.make_repo(Path(temporary), "repo")
            comp_a = self.make_comp(repo, "comp-a")
            comp_b = self.make_comp(repo, "comp-b")
            card_id = "KGL-feedback-test"
            self.make_candidate(repo, card_id)

            kk.command_feedback(
                repo, comp_a, card_id, "CHK-001", "GO",
                ["comp-a/exp/result.md#CHK-001"], "own-experiment",
            )
            self.assertEqual(kk.evidence_ceiling(kk.knowledge_root(repo), card_id), "L0")

            kk.command_feedback(
                repo, comp_a, card_id, "CHK-002", "GO",
                ["comp-a/exp/result.md#CHK-002"], "own-experiment",
            )
            self.assertEqual(kk.evidence_ceiling(kk.knowledge_root(repo), card_id), "L1")

            kk.command_feedback(
                repo, comp_b, card_id, "CHK-003", "GO",
                ["comp-b/exp/result.md#CHK-003"], "own-experiment",
            )
            self.assertEqual(kk.evidence_ceiling(kk.knowledge_root(repo), card_id), "L2")

            with self.assertRaises(ValueError):
                kk.command_promote(repo, card_id, "L3", approved=True)

    def test_absolute_source_ref_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            kk.validate_source_ref("C:/private/result.md")

    def test_duplicate_alias_requires_approval_and_preserves_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = self.make_repo(Path(temporary), "repo")
            comp = self.make_comp(repo, "comp-a")
            source_id = "KGL-duplicate-source"
            target_id = "KGL-duplicate-target"
            self.make_candidate(repo, source_id)
            self.make_candidate(repo, target_id)
            root = kk.knowledge_root(repo)

            kk.command_feedback(
                repo, comp, source_id, "CHK-010", "GO",
                ["comp-a/exp/result.md#CHK-010"], "own-experiment",
            )
            kk.command_duplicates(repo, threshold=0.9)
            pairs = kk.read_json(root / "duplicate-candidates.json")["pairs"]
            self.assertEqual(len(pairs), 1)
            self.assertEqual(
                kk.read_json(root / "candidates" / f"{source_id}.json")[
                    "lifecycle_status"
                ],
                "conditional",
            )

            with self.assertRaises(ValueError):
                kk.command_alias(
                    repo, source_id, target_id, "same concept", approved=False
                )
            kk.command_alias(
                repo, source_id, target_id, "same concept", approved=True
            )
            source = kk.read_json(root / "candidates" / f"{source_id}.json")
            target = kk.read_json(root / "candidates" / f"{target_id}.json")
            self.assertEqual(source["lifecycle_status"], "superseded")
            self.assertEqual(source["superseded_by"], target_id)
            self.assertIn(source_id, target["related_cards"])
            self.assertEqual(len(kk.evidence_files(root, source_id)), 1)
            self.assertEqual(len(kk.evidence_files(root, target_id)), 1)

    def test_no_go_disputes_active_card_and_adds_condition(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = self.make_repo(Path(temporary), "repo")
            comp = self.make_comp(repo, "comp-a")
            card_id = "KGL-disputed-test"
            self.make_candidate(repo, card_id)
            root = kk.knowledge_root(repo)
            card_path = root / "candidates" / f"{card_id}.json"
            card = kk.read_json(card_path)
            card["lifecycle_status"] = "active"
            kk.write_json(card_path, card)

            kk.command_feedback(
                repo, comp, card_id, "CHK-020", "NO-GO",
                ["comp-a/exp/result.md#CHK-020"], "own-experiment",
            )
            disputed = kk.read_json(card_path)
            self.assertEqual(disputed["lifecycle_status"], "disputed")
            self.assertEqual(len(disputed["contraindications"]), 1)

    def test_audit_rejects_secret_and_unknown_external_code_license(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = self.make_repo(Path(temporary), "repo")
            card_id = "KGL-audit-test"
            self.make_candidate(repo, card_id)
            path = kk.knowledge_root(repo) / "candidates" / f"{card_id}.json"
            card = kk.read_json(path)
            # 検出テスト用ダミー（実行時のみ連結。実キーではない）
            _dummy = "sk-" + "TESTONLY_not_a_real" + "_secret_xxxxxx"
            card["mechanism"] = "api" + "_key=" + _dummy
            card["provenance"] = {
                "origin_type": "external-code",
                "source_url": "https://example.com/code",
                "license": "unknown",
                "redistribution": "unknown",
                "review_status": "pending",
            }
            kk.write_json(path, kk.enrich_card(card))
            failures, warnings = kk.audit_store(kk.knowledge_root(repo))
            self.assertTrue(any("possible secret" in item for item in failures))
            self.assertTrue(any("license is unknown" in item for item in failures))
            self.assertTrue(warnings)

    def test_extract_generic_lessons_splits_abc_axes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "retro-lessons.md"
            path.write_text(
                "\n".join(
                    [
                        "# lessons",
                        "## 汎用",
                        "### A. CV・物差し・提出判断",
                        "1. **lane split**",
                        "   - body: keep trust and public apart",
                        "   - apply: partial public slice",
                        "   - avoid: public is full test",
                        "   - origin: own",
                        "   - domain: kaggle",
                        "### B. 解法・モデリング本体",
                        "1. **path over rows**",
                        "   - body: use path volume",
                        "   - apply: sequential alignment problems",
                        "   - avoid: i.i.d. tabular rows",
                        "   - origin: topsolution",
                        "   - domain: kaggle",
                        "### C. 運用・post-comp",
                        "1. **leaderboard -s**",
                        "   - body: use show for private lb",
                        "   - apply: post-comp cli",
                        "   - avoid: mid-comp",
                        "   - origin: ops",
                        "   - domain: kaggle",
                        "## コンペ固有",
                        "1. **tip alpha**",
                    ]
                ),
                encoding="utf-8",
            )
            items = kk.extract_generic_lessons(path)
            self.assertEqual(len(items), 3)
            tags = [item["axis_tag"] for item in items]
            titles = [item["title"] for item in items]
            self.assertEqual(
                tags,
                [
                    "knowledge-axis-cv-validation",
                    "knowledge-axis-method-solution",
                    "knowledge-axis-ops",
                ],
            )
            self.assertTrue(titles[0].startswith("lane"))
            self.assertIn("partial public", items[0]["apply"])
            self.assertIn("full test", items[0]["avoid"])
            self.assertNotIn("tip alpha", " ".join(titles))


if __name__ == "__main__":
    unittest.main()
