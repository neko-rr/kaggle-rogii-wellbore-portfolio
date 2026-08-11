---
name: kaggle-submission-strength-gate
description: >-
  simulation コンペ提出前に「現行強み（KPI）を壊していないか」をコンペ固有プロファイルで判定する。
  strength-gate-profile.json の dimensions（overall・任意スライス）と replay 層別 /
  metrics JSON / local protocol を併用。強み維持、非劣化、層別、slot 差し替え、
  diagnostic 提出、protocol PASS だけでは足りない、と言ったときに使う。
  kaggle-submission-validator の直前（L2.5）。2p/4p 固定ではない。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| check-submission-strength-gate.py · 関連 replay 脚本 | —（replay DL は kaggle-cli-fetch 経由） | — | exp/ · strength-gate-profile.json | exp/ レポート · ゲートログ |

**要ユーザー明示 OK:** LB 提出は validator + ユーザー OK 後

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle Submission Strength Gate（simulation 汎用）

**「強みを壊さずに改善したか」** を提出ブロッーカーにする。  
`kaggle-submission-validator`（L0–L2）は形式・締切のみ — **KPI 退行は検知しない**。

**コンペ固有の軸は SSOT ファイルで定義** — Skill 本文に 2p/4p を硬書きしない。

---

## 適用範囲

| submission-profile | 本 Skill |
|---|---|
| **simulation** | 使用する |
| lora / csv / notebook-output | **対象外**（別ゲートを comp-profile で定義） |

対戦人数が可変でない simulation（常に 1v1 等）でも可。  
`dimensions` を **overall + 弱点スライス**（相手 tier・map・戦法タグ等）に差し替える。

---

## SSOT（コンペごとに1セット）

| ファイル | 役割 |
|---|---|
| **`docs-ja/strength-gate-profile.json`** | 機械判定（スクリプト入力） |
| **`docs-ja/strength-gate-profile.md`** | 人間向け KPI 設計メモ |
| テンプレ | `scripts/templates/strength-gate-profile.simulation.template.json` |

新コンペ bootstrap 時: テンプレをコピーし `dimensions` を編集。

### dimension の tier

| tier | 意味 | μ 提出 |
|---|---|---|
| **primary** | LB の主 KPI（多くは overall win%） | 閾値超過で **FAIL** |
| **guard** | 既知の強みスライス | 閾値超過で **FAIL** |
| **secondary** | hedge・改善検証用 | 主に WARN |
| optional | データ無しでスキップ可 | — |

### source（データの取り方）

| source | 入力 | 用途 |
|---|---|---|
| `stratified_md` | `exp/*-stratified-compare.md` | replay 層別表 |
| `metrics_json` | `exp/strength-gate-metrics.json` | MD 形式が無いコンペ |
| `protocol_json` | `exp/local-eval/runs/*.json` | overall PASS 等 |

**protocol 単独 PASS は μ 提出の根拠にしない** — primary/guard の evidence が必須。

### metrics JSON 例（1v1 のみコンペ）

```json
{
  "baseline_label": "best_v3",
  "candidate_label": "candidate_v4",
  "metrics": {
    "overall": { "baseline_pct": 62.0, "candidate_pct": 58.0 },
    "guard_main": { "baseline_pct": 71.0, "candidate_pct": 55.0 }
  }
}
```

---

## 3段ゲート内の位置

```
CHK → pretrain-gate → kernels-runbook → 【strength-gate L2.5】→ submission-validator → 提出
```

---

## 提出目的（必ず宣言）

| purpose | 意味 | 有効枠（effective）に載せてよいか |
|---|---|---|
| **mu** | LB / Private 確定 | ○（PASS 時） |
| **hedge** | 限定改善・実験 | △（PASS-WITH-WARNINGS + 明示 OK） |
| **diagnostic** | replay / 検証のみ | × **単独では不可**（後で μ bot を再提出） |

未宣言 → **提出禁止**。

---

## ワークフロー

### Step 0: 読む

1. `docs-ja/strength-gate-profile.json` + `.md`
2. `docs-ja/comp-timeline.md`（有効提出数 `slots.effective_count`）
3. 現行 Best の replay / metrics SSOT

### Step 1: evidence を揃える

- replay 層別 MD を生成 **または** `strength-gate-metrics.json` を更新
- （任意）local protocol JSON
- baseline = **現行 slot の Best**（Peak・有効枠 bot）

### Step 2: スクリプト実行

```powershell
python scripts/check-submission-strength-gate.py `
  --comp-root "20260623-orbit-wars" `
  --purpose mu `
  --stratified-md "20260623-orbit-wars/exp/replay-today-two-stratified-compare.md" `
  --protocol-json "20260623-orbit-wars/exp/local-eval/runs/protocol_v2_....json" `
  --baseline-label "Adaptor" `
  --candidate-label "Adaptor-final" `
  --is-last-effective-slot
```

`--profile` で JSON パスを明示可能。exit **0 以外 → 提出禁止**。

### Step 3: 検証ログ（L2.5 節）

`docs-ja/submission-validations/YYYY-MM-DD-submit-NNN.md`:

```markdown
## L2.5 Strength Gate
- profile: docs-ja/strength-gate-profile.json
- purpose: mu
- result: FAIL
- deltas: { "guard_2p_active": -24.1, ... }
- **BLOCKER（ユーザーへ必ず引用）:** guard_2p_active regression -24.1pt
```

### Step 4: ユーザー報告（FAIL 時必須）

- 🔴 **{dimension.label} 退行:** {delta}pt — **μ 用提出ブロック**
- 「条件付き」「ユーザー判断のみ」だけで FAIL を伏せない

---

## Agent 規則

1. 「強みを壊さず」→ **CHK / protocol A+B PASS だけで「維持」と言わない**
2. `strength-gate-profile.json` の **guard / primary** を根拠にする
3. strength-gate **FAIL** 時は `kaggle-submission-validator` PASS と報告しない
4. `diagnostic` + 有効枠最終スロット → **FAIL**（プロファイル `slots`）
5. プロファイル未作成の simulation コンペ → bootstrap でテンプレコピー **または** 提出保留

---

## 他 Skill

| Skill | 関係 |
|---|---|
| `kaggle-submission-validator` | L2.5 の後 |
| `kaggle-comp-bootstrap` | 新コンペで profile 初期化 |
| `kaggle-pretrain-gate` | 学習前 |
| `kaggle-experiment-checklist` | CHK 完了 ≠ 提出 OK |

---

## 事例（Orbit Wars — mode-split あり）

| 教訓 | 内容 |
|---|---|
| protocol「2p 0pp」 | Peak replay 比 **−24pt** を見逃した |
| 対策 | profile の `guard_2p_active` mu_fail_pt: **-10** |

詳細: `docs-ja/strength-gate-profile.md`
