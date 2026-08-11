---
name: kaggle-submission-validator
description: >-
  提出直前に validate-submission.ps1（L0-L1）と Code Competition 時は
  check-codecomp-submit-kernel.py（固定成果物コピー専用 NB の禁止）を実行し、
  submission-rules.md（L2・提出形式は Overview どおり）を確認して提出可否を判定する。
  Scoring Error・固定 CSV コピー・提出形式の勝手な変更を防ぐ。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| validate-submission.ps1 · check-codecomp-submit-kernel.py · check-staged-secrets.ps1 | — | — | my-submitted-notebook/ · lifecycle-manifest.md · docs-ja/submission-rules.md · my-notebook/ | submission-validations/ · my-submitted-notebook/（PASS 凍結） · lifecycle-manifest.md |

**要ユーザー明示 OK:** competitions submit（本 Skill では実行禁止）。OK 時も **Notebook 紐づけ提出**（`.cursor/skills/_shared/NOTEBOOK-LINKED-SUBMIT.md`）。**`-k` は自 kernel のみ · 403 時 zip-only 禁止 · 自 fork 更新を先に。**

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle Submission Validator

`my-submitted-notebook/` 凍結と `kaggle competitions submit` の **直前** に必ず実行する。
Kaggle Notebook 完走は必須条件にしない。

**提出方式（すべての提出プロファイル共通の既定）:** validator PASS 後は **Notebook 紐づけ**（Kaggle UI「Submit to Competition」または CLI **`-k` / `-v`**）。ローカル成果物の zip/csv 直 `-f` のみは非推奨（採点は通っても Notebook 非表示になり、Kaggle 上でコードを辿れない）。SSOT: **`NOTEBOOK-LINKED-SUBMIT.md`**。ユーザーが「NB 不要・緊急」と明示したときだけ例外。

### 提出形式はコンペ指定のまま（変更禁止）

- 列名・ファイル名・ID 規則は **Overview / `docs-ja/submission-rules.md` の「提出形式」のみ**。Agent が独自に変えない。
- L0 で形式を確認する。形式を「楽にするため」に変えて提出しない。

### Code Competition — 固定成果物コピー提出の禁止

Code Competition は採点時に Notebook を **hidden test 上で再実行**する。次は **L0 で成果物が綺麗でも Submission Scoring Error** になりうる:

| 禁止 | 内容 |
|---|---|
| 固定成果物コピー専用 NB | Dataset / ローカルに置いた完成 `submission.csv`（や zip）を読むだけで出力する Script |
| 他 kernel 出力の丸コピー | `kernel_sources` 等で他者・別 Version の提出物だけを載せる |
| 提出パイプライン欠落 | コンペデータを読まず、hidden 再実行で同じ成果物を生成できない Version |

**必須:** 提出に使う Version は、**自 kernel がコンペデータから予測（またはコンペ指定の成果物）を E2E 生成**すること。中間面・別レイヤを出したい場合も **同一 E2E 実行の末尾で昇格**する（別の短 NB で固定ファイルを載せ替えない）。

提出直前（Code Competition · csv / notebook-output 等）:

```powershell
.\.venv\Scripts\python.exe .\scripts\check-codecomp-submit-kernel.py -p ".\<comp-root>\my-notebook\<slug>"
# 成果物名が Overview と違うときのみ（形式自体は変えない）:
#   --artifact-names "<Overviewの提出ファイル名>"
# FAIL なら competitions submit 禁止
.\scripts\validate-submission.ps1 ...
```

コンペ固有の失敗事例・台帳 ID は **`docs-ja/submission-rules.md` / `exp/improvement-loop-failures.json`** に書く（本 Skill には書かない）。

---

## 出力ファイル

```
docs-ja/
├─ submission-rules.md          # コンペ固有提出ルール SSOT
└─ submission-validations/      # 1提出1ログ
   └─ YYYY-MM-DD-submit-001.md
```

テンプレ: `scripts/templates/submission-rules.md.template`（`kaggle-template/comp/docs-ja/` に同期可）

---

## Profile（AGENTS.md に1行）

`submission-profile: lora | csv | simulation | notebook-output`

---

## チェック層

| 層 | 内容 |
|---|---|
| **L0-L1（自動）** | `scripts/validate-submission.ps1` |
| **L2（手動）** | `docs-ja/submission-rules.md` のコンペ固有条件 |
| **L3（ライセンス）** | `docs-ja/license-ledger.md` + Skill `kaggle-license-compliance` **Tier A+**（Final 2 / メダル・賞金狙い時 **必須**） |

---

## サブエージェント連携（SA-5）

- diff レビューは **ユーザー明示依頼時** Task `bugbot`（`_shared/SUBAGENT-BRIEF.md` § SA-5）
- bugbot の指摘をそのまま提出 OK にしない — **本 Skill L0-L3 を必ず実行**
- submit は引き続きユーザー明示 OK 後のみ

---

## ワークフロー

### トリガー

- LB 提出の直前
- `my-submitted-notebook/` へコピーする直前
- ユーザー「提出していい？」

### Step 1: 読む

1. `docs-ja/submission-rules.md`
2. `docs-ja/comp-timeline.md`
3. 成果物パス

### Step 2: L0-L1 をスクリプト実行

**Code Competition（csv / notebook-output）は先に kernel 検査:**

```powershell
.\.venv\Scripts\python.exe .\scripts\check-codecomp-submit-kernel.py -p "path/to/kernel-dir"
```

- exit ≠ 0 → **提出禁止**（固定成果物コピー専用 NB の疑い）
- 続けて:

```powershell
.\scripts\validate-submission.ps1 `
  -ArtifactPath "path/to/artifact" `
  -Profile lora `
  -LogPath "docs-ja/submission-validations/auto-check.md"
```

- exit code 0 以外は提出禁止
- profile は `AGENTS.md` の `submission-profile` を使う
- **L0 PASS だけでは不十分** — L2（E2E / 形式不変）も必須

### Step 3: L2（手動）

`docs-ja/submission-rules.md` を読み、スクリプトが扱わない固有制約を確認する。

**必須チェック（Code Comp · 推測で飛ばさない）:**

- [ ] 提出形式（列・ファイル名・ID）が Overview / submission-rules と **一致**（変更していない）
- [ ] 提出 kernel が **コンペデータから E2E 生成**（`check-codecomp-submit-kernel.py` PASS）
- [ ] 固定成果物 / Dataset コピー専用 NB ではない（`check-codecomp-submit-kernel.py`）
- [ ] 日次提出上限・UTC 日付・ユーザー「今日は提出しない」指示

**simulation:** 必ず **「提出枠・retry 規律」** 節を読む（日次5 · 有効2 · ERROR でも枠消費 · **明示 intent まで retry 禁止**）。数値は `comp-timeline.md`、強みは L2.5。

### Step 3b: L3（メダル/賞金狙い時）

1. `docs-ja/license-ledger.md` の BOM 全行を確認
2. Skill `kaggle-license-compliance` **Tier A+** を実行
3. FAIL → 提出禁止。PASS-WITH-WARNINGS → ユーザー確認後のみ

### Step 4: 検証ログ

`docs-ja/submission-validations/YYYY-MM-DD-submit-{NNN}.md`

| result | 動作 |
|---|---|
| **PASS** | 提出・`my-submitted-notebook/` 凍結可 · **`lifecycle-manifest.md` 更新可** |
| **PASS-WITH-WARNINGS** | ユーザー確認後に提出可（警告をログに） |
| **FAIL** | 提出禁止 |

### Step 5: 提出（ユーザー操作 · notebook 紐づけ優先）

| profile | 標準 |
|---|---|
| **notebook-output** · tabular NB | **方式 1** UI Submit · **方式 2** CLI `-k` / `-v`（Version 済み）· **方式 2b** `kernels push` → `-k` / `-v`（`NOTEBOOK-LINKED-SUBMIT.md`） |
| **simulation** | CLI `-k` / `-v`（zip 直 `-f` は多く拒否） |
| **csv / lora** | コンペ依存 — `submission-rules.md` · `NOTEBOOK-LINKED-SUBMIT.md` |

**403 on `-k`:** 他者 kernel への紐づけ試行。**zip-only に切り替えず** 自 fork 更新 → Version 作成（UI または `kernels push`）→ 再提出。詳細: `NOTEBOOK-LINKED-SUBMIT.md` §`-k` 制約。

**公式 CLI 参照:** [Kaggle CLI tutorials](https://github.com/Kaggle/kaggle-cli/blob/main/docs/tutorials.md)（本リポジトリでは `.\scripts\kaggle-cli.ps1` 経由）

検証ログに **`submit_mode: notebook-linked | zip-only`** を記録。`zip-only` はユーザー「NB 不要・緊急」明示時のみ。

### Step 6: 提出後

- **移動必須:** validator PASS 後、`my-submitted-notebook/{name}/` に成果物をコピーし、**`lifecycle-manifest.md` を `submitted` に更新**（`submit_ref` · `kernel` · `version` · path · artifact）。Skill `kaggle-notebook-folders`
- `exp/exp-infer.md` + `hyperparameter-table.md` 更新（履歴は `Notebook <title> | Version N` 形式）
- （任意）`kaggle-cli-fetch` で submissions 確認

---

## Agent 規則

1. **スクリプト FAIL で提出・凍結しない**（`validate-submission.ps1` **および** Code Comp 時は `check-codecomp-submit-kernel.py`）
2. L2 は `submission-rules.md` を根拠に判定し、推測で PASS しない
3. **提出形式をコンペ指定から変えない**（列追加・リネーム・独自 ID 禁止）
4. **L0 で成果物が綺麗でも、固定コピー専用 NB は提出禁止**（Code Comp · Scoring Error）
5. pretrain-gate FAIL の成果物は原則提出しない
6. dataset 大量 DL 禁止（既存ルール）— DL 前は Skill `kaggle-cli-ops` **ダウンロード前チェック** 表を通す
7. **simulation — submit / retry:** `submission-rules.md` **提出枠・retry 規律** に従う。提出後は submissions 確認。**ERROR でもユーザー明示 intent なし再 submit 禁止**
8. **`-k` は自 kernel のみ** — 他者 slug で **403** → **zip-only 禁止** · **自 fork 更新を先に**（`NOTEBOOK-LINKED-SUBMIT.md`）
9. **`submit_mode: zip-only`** はユーザーが「NB 不要・緊急」と明示した場合のみログに記録可
10. ユーザーが「今日は提出しない」等と指示したら **即停止**（完走済み GPU があっても submit しない）

---

## 検証ログテンプレ

```markdown
# Submission Validation — submit-001

> date: yyyy/mm/dd HH:MM UTC
> profile: lora
> artifact: path/to/submission.zip
> execution: none | kaggle | colab | local
> result: PASS | FAIL | PASS-WITH-WARNINGS
> submit_mode: notebook-linked | zip-only | n/a

## L0
## L0.5（Code Comp kernel · `check-codecomp-submit-kernel.py`）
## L1
## L2（形式不変 · E2E · コピー専用 NB 禁止）
## L3（license / Tier A+）
## 実行証跡（任意）
## ブロッカー / 警告

## 提出枠（simulation · L2）

- 本日残り枠 / 有効2枠への載せ方: `comp-timeline.md`
- retry 可否: `submission-rules.md` 提出枠・retry 規律（明示 intent まで再 submit 禁止）
```

---

## ユーザー依頼別

| 依頼 | 動作 |
|---|---|
| 「提出していい？」 | validator 実行 |
| 「zip を検証して」 | スクリプト + L2 + ログ |
| 「submission-rules 初期化」 | テンプレから作成 |

---

## 他 Skill

| Skill | 役割 |
|---|---|
| `kaggle-pretrain-gate` | 学習前（本 Skill は提出前） |
| `kaggle-kernels-runbook` | 実行ログの出所 |
| `kaggle-comp-timeline` | 締切・1日上限 · 残り枠 |
| `kaggle-git-security` | 秘匿 L0 |
| `kaggle-license-compliance` | L3 / BOM / Host 許可 |
| `kaggle-notebook-folders` | 凍結先 |

---

## テンプレート

`%USERPROFILE%\.cursor\kaggle-template\comp\docs-ja/`
