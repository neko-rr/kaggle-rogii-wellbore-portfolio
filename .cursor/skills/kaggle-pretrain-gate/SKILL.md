---
name: kaggle-pretrain-gate
description: >-
  長時間学習・重い GPU 実行の前に、短いコストで即死エラーと
  「完走しても提出無意味・ensemble 不可」を弾く。Tier 0/1/2 スモーク検証。
  学習前チェック、スモークテスト、pretrain gate、無駄 GPU 防止と言ったときに使う。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| pretrain 系スモーク · check-kaggle-cli.ps1 | —（長時間 GPU は Colab 方針） | — | docs-ja/pretrain-acceptance.md | exp/exp-train.md · run-log.md |

**要ユーザー明示 OK:** 長時間学習開始（ユーザー OK）

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle Pretrain Gate

**全コンペ共通。** Colab 長時間学習・重い Kaggle 実行の **前** に必ず通すゲート。

防ぐもの:

| 類型 | 例 |
|---|---|
| **A. 即死系** | import エラー、パス違い、OOM、timeout |
| **B. 無意味系** | CV が baseline 以下、ensemble 不可、仮説と不一致 |

**Kaggle 完走・LB 提出は前提にしない。** Tier 0〜2 はローカル / 短時間 Kaggle / Colab 短時間で実施。

---

## 3段ゲート内の位置

```
CHK 項目 → ⓪ static-check → ① pretrain-gate → ② kernels-runbook → ③ submission-validator → 提出
```

| ゲート | Skill |
|---|---|
| ⓪ コード直後 | **`kaggle-static-check`**（`run-static-checks.ps1` · 拡張 Ruff 不可換） |
| ① 学習前 | **本 Skill** |
| ② 実行 | `kaggle-kernels-runbook` |
| ③ 提出前 | `kaggle-submission-validator` |

**static FAIL または pretrain PASS 以外で長時間学習を開始しない。**

### 形 smoke との関係（CV-DESIGN · checklist CHK-00S）

| 層 | 役割 |
|---|---|
| **CHK-00S / 形 smoke** | id · 列 · 行数 · 短時間 run など **形**（性能は見ない） |
| **本 Skill Tier 0** | 学習直後死 · 提出形 profile 依存 |
| **shippable OOF** | primary 採択根拠（`docs-ja/cv-design.md`）— oracle と混同しない |

**性能 primary CHK の前**に形 smoke（または同等の validator 短 run）を通す。詳細: `_shared/DECISION-FLOW.md` · `_shared/CV-DESIGN.md`

---

## サブエージェント連携（SA-4）

- 20 seed 等 **反復 eval** は Task `shell` に委譲（`_shared/SUBAGENT-BRIEF.md` § SA-4）
- **本 Skill PASS 前** にサブ shell を走らせない
- サブは summary ファイルのみ返す · 親が `exp/` · `run-log.md` に確定記録

---

## 出力ファイル

```
docs-ja/
├─ pretrain-acceptance.md       # コンペ合格基準 SSOT（概要作成時に初版）
└─ pretrain-gates/              # 1実験1ログ（追記のみ）
   └─ YYYY-MM-DD-exp012-gate.md

my-ran-notebook/{nb}/run-log.md # Tier 1 失敗時のデバッグログ（runbook 連携）
```

テンプレ: `kaggle-template/comp/docs-ja/pretrain-acceptance.md.template`

---

## Profile（AGENTS.md に1行）

`pretrain-profile: tabular | lora | simulation | ensemble`

| profile | Tier 0 | Tier 1 | Tier 2 |
|---|---|---|---|
| **tabular** | 列名・row_id・件数・リーク候補 | 10行 infer・提出形式一致 | CV ≥ baseline；**`metric-repro.md`** の holdout / LB 差を確認 |
| **lora** | template・rank・jsonl 形式 | 1 step loss、1 sample generate | holdout + **`metric-repro.md`**（LB 本番 params。非 public なら proxy 方針を記録） |
| **simulation** | main.py import、obs/action 型 | 1 episode / validation episode | 対 random win/tie、timeout なし |
| **ensemble** | oof 列名・index 一致 | 新予測 shape・join | 相関 < 0.99、blend CV 改善見込み |

---

## Tier 定義

| Tier | コスト | 内容 |
|---|---|---|
| **0** | GPU 不要・数分 | 静的: 設定・パス・import・データ件数・提出形式整合。**新規 external 依存あり → Skill `kaggle-license-compliance` Tier R PASS 必須** |
| **1** | 数分 | スモーク: 1 batch / 1 step / 1 episode / 10行推論 |
| **2** | 〜30分（任意） | ミニ検証: 部分 holdout、相関、CV 下限、acceptance 照合 |

### 長時間学習の解禁

| 条件 | 必須 Tier |
|---|---|
| 通常の新手法 | **0 + 1** |
| ensemble 候補・高コスト学習 | **0 + 1 + 2** |
| CHK 行に `pretrain-tier: 0+1+2` とあればそれに従う |

---

## ワークフロー

### トリガー

- `kaggle-experiment-checklist` Phase 2: CHK を `in-progress` にする **直前**
- ユーザー「長時間学習していい？」
- Colab 夜間 run の前

### Step 1: 読む

1. `docs-ja/pretrain-acceptance.md`
2. `docs-ja/metric-repro.md`（Tier 2・visibility・LB 本番パラメータ）
3. `docs-ja/license-ledger.md`（新規 external 採用時 — Tier R 済みか）
4. 当該 CHK 行（`hypothesis`, `acceptance`, `pretrain-tier`）
5. `exp/hyperparameter-table.md`（baseline 参照）
6. `docs-ja/comp-timeline.md`（締切・1日上限）

### Step 2: Tier 0 → 1 → 2 を順に実行

FAIL した時点で **打ち切り**。以降の Tier と長時間学習は行わない。

### Step 3: ゲートログを書く

`docs-ja/pretrain-gates/YYYY-MM-DD-{exp-id}-gate.md`

| 結果 | 意味 |
|---|---|
| **PASS** | 長時間学習 / runbook 本番実行へ |
| **FAIL** | 長時間禁止。原因と次アクションを記録 |
| **DEFER** | Tier 2 未実施だが 0+1 PASS。ユーザー判断待ち |

### Step 4: exp 記録

- PASS → `exp-train.md` に gate PASS を1行
- FAIL → `exp-train.md` に **無駄 GPU 回避** として記録（rejected 候補）

### Step 5: 連携

- PASS → Skill `kaggle-kernels-runbook` で本番実行
- FAIL のデバッグログ → `my-ran-notebook/.../run-log.md`

---

## ゲートログ必須フィールド

```markdown
> profile: lora
> tier: 0+1+2
> result: PASS | FAIL | DEFER
> chk: CHK-003
> execution: local-smoke | kaggle-short | colab-short
```

各 Tier: チェック項目と `[x]` / `[ ]`。FAIL 時はブロッカーを明記。

---

## experiment-checklist 連携

各 pending 行に追加:

```markdown
pretrain-tier: 0+1        # または 0+1+2
pretrain-gate: pending | pass | fail
```

Phase 2 手順（更新）:

```
1. CHK を in-progress にする前に pretrain-gate 実行
2. PASS のみ in-progress → 長時間学習 / 本番実行
3. 実験完了 → acceptance 判定 → done / rejected
```

---

## Agent 規則

1. **FAIL / DEFER で Colab 長時間・9h Kaggle を開始しない**
2. Tier 1 失敗ログは `run-log.md` に残す（共有用）
3. **完走しても acceptance 未達** は Tier 2 または事後 rejected — 提出 validator まで進めない
4. ensemble: 相関 0.99 超・index 不一致は Tier 2 で FAIL
5. partial progress 禁止 — gate ログまで完了

---

## ユーザー依頼別

| 依頼 | 動作 |
|---|---|
| 「学習していい？」 | Tier 判定 → gate 実行 |
| 「CHK-003 を実行」 | 先に gate → PASS 後に runbook |
| 「pretrain 初期化」 | `pretrain-acceptance.md` テンプレ作成 |

---

## 他 Skill

| Skill | 役割 |
|---|---|
| `kaggle-experiment-checklist` | CHK と gate の紐付け |
| `kaggle-kernels-runbook` | PASS 後の実行 |
| `kaggle-submission-validator` | 成果物提出前 |
| `kaggle-license-compliance` | 外部依存 Tier R / メダル前 Tier A+ |
| `metric-repro.md` | Tier 2 評価・visibility 別 Metric 手順（Skill なし） |
| `local-eval-*` | tabular 下流（eval CSV・ログ分析） |
| `competition-conditions` | pretrain-acceptance 初版の入力 |

---

## テンプレート

`%USERPROFILE%\.cursor\kaggle-template\comp\docs-ja/`
