---
name: kaggle-kernels-runbook
description: >-
  Kaggle Notebook / Google Colab の実行手順・環境設定・デバッグログの残し方。
  GPU 実行場所が不明・9h 超の見込み・quota 逼迫時はユーザーに A/B 確認。完走は提出前提にしない。
  Kaggle 実行、Colab、Internet OFF、GPU、Output commit、デバッグログと言ったときに使う。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| 短時間 smokes · kaggle-cli（読取） | Kaggle / Colab（ユーザー実行中心） | — | docs-ja/kernels-runbook.md · my-ran-notebook/ · lifecycle-manifest.md | my-ran-notebook/ · run-log.md · lifecycle-manifest.md |

**要ユーザー明示 OK:** 長時間 Notebook · GPU 学習

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle Kernels Runbook

**全コンペ共通。** GPU 実行の **手順書**。提出とは切り離す。

- **短時間** → Kaggle Notebook（多くは CPU で可）
- **長時間** → Kaggle（**9h/セッション** 上限）または Colab。**どちらかは Agent が勝手に決めない**（下記 §GPU 実行場所の確認）
- **エージェント単体・zip** → ローカル整形 → `kaggle-submission-validator`

**pretrain-gate PASS 後** に本番の長時間実行へ進む。

---

## 実行レーンの承認（必須 · Agent）

**Kaggle GPU と Google Colab の選択権はユーザーにある。** Agent は一方を勝手に固定しない。

**起動条件:** 「その環境を使ってよいというユーザー許可」と「対象ジョブを実行するユーザー指示」が **両方ある場合だけ**起動する。過去の包括許可・空き枠・CPU 実行であることだけでは起動しない。

| Kaggle 並列枠 | 運用上限 | Agent の扱い |
|---|---:|---|
| CPU Notebook | **最大5枠** | 指示済み CPU ジョブだけを上限内で並列化 |
| GPU Notebook | **最大2枠** | 指示済み GPU ジョブだけを上限内で並列化 · 長時間は pretrain-gate 必須 |

上限は「使える最大数」であり「常に全枠を埋める命令」ではない。指示済み候補がなくなった場合、acceptance 未達の場合、停止基準に該当した場合は **空き枠を未指示ジョブで埋めず**、停止・harvest・ユーザー報告を行う。

| トリガー | 確認 |
|---|---|
| GPU が必要だが Kaggle / Colab のどちらがよいか不明 | **A) Kaggle GPU** · **B) Google Colab** |
| 見込みが Kaggle **9h/セッション** に近い、または超えそう | **A) Kaggle（分割・checkpoint）** · **B) Colab（長時間向き）** |
| Kaggle GPU **quota 逼迫**（`kaggle quota` で残量が少ない） | **A) 残 quota で実行** · **B) Colab** |
| `experiment-checklist.md` **§実行制約** に今週方針がある | 方針に従う。無い・曖昧なら上記と同様に確認 |

**質問に含めるもの:** ① 目的（CHK-id / 作業）② 見込み時間・GPU 要否 ③ **A) Kaggle GPU**（quota 残 · 9h 制限）④ **B) Colab**（長時間 · Compute Unit）⑤ 選択後 `run-log.md` に記録

**指示後の空回し禁止:** ユーザーが明示したジョブ群は、許可範囲内で待ち時間を減らし、完了後すぐ harvest / status 確認を行う。ただし次ジョブへの自動継続は、次ジョブもユーザー指示済みの場合だけ。**許可だけで CPU/GPU/Colab を起動しない**（Rule `kaggle-private-assets.mdc`）。

**環境の再確認が不要（ただし対象ジョブのユーザー指示は必要）:**

- ローカル CPU で足りる（verify · gate · 短い compile）
- Kaggle **CPU** を使うことと対象ジョブが直前に明示されている
- ユーザーが直前ターンで環境を **明示**した
- §実行制約 で環境が **固定**されている

**コンペ固有の工程分離**（例: コンパイル=ローカル · ORT 探索=GPU）は `docs-ja/` の手順書または `experiment-checklist.md` §実行制約 に書く（Skill には固定しない）。

---

## 3段ゲート内の位置

```
pretrain-gate (PASS) → ② kernels-runbook → submission-validator
```

---

## サブエージェント連携（SA-4）

- 長時間・反復 shell は **`kaggle-subagent-delegate`** → Task `shell`
- 親は runbook 手順 · `my-ran-notebook/run-log.md` · lifecycle 更新
- 完走を提出前提にしない（従来どおり）

---

## 出力ファイル

```
docs-ja/kernels-runbook.md           # コンペ環境メモ SSOT（Input version 等）
my-ran-notebook/{nb-name}/run-log.md # デバッグ共有用（成功・失敗どちらも）
my-ran-notebook/{nb-name}/*.ipynb    # 実行した ipynb（あれば）
```

テンプレ: `kaggle-template/comp/docs-ja/kernels-runbook.md.template`  
`my-ran-notebook/run-log.md.template`

---

## 実行場所の判定

| 条件 | 推奨 | 記録先 |
|---|---|---|
| 見込み > 1〜2h / **9h 近い** | **ユーザーに A/B 確認**（Kaggle 分割 vs Colab） | `exp-train.md` · `run-log.md` |
| **GPU 必要・場所不明** | **ユーザーに A/B 確認**（Kaggle GPU vs Colab） | `run-log.md` |
| 短時間推論・軽い検証 | **Kaggle**（通常 CPU） | `run-log.md` |
| Tier 0〜1 スモーク | ローカル or Kaggle 短時間 | `pretrain-gates/` |
| 提出のみ（zip/csv/py） | ローカル検証 → Version 作成（UI または **`kernels push`**）→ **NB 紐づけ提出**（**自 kernel** `-k` / `-v`） | validator へ。**403 時 zip-only 禁止**（`NOTEBOOK-LINKED-SUBMIT.md` §2b） |

---

## Kaggle Notebook チェックリスト

### Before

- [ ] **ユーザー許可 + 対象ジョブの実行指示**が両方ある
- [ ] CPU 最大5枠 / GPU 最大2枠の範囲内（未指示ジョブで空きを埋めない）
- [ ] `.\scripts\check-kaggle-cli.ps1` PASS（CLI 使用時）
- [ ] `kernel-metadata.json` の `id` / `title` / `code_file` / Accelerator を確認
- [ ] `.\scripts\assert-kaggle-private.ps1 -KernelDir <folder>` PASS
- [ ] Internet: **OFF**（必要データは Input で固定）
- [ ] Accelerator: GPU 種別を `run-log.md` に記録
- [ ] Input: Dataset / Models の **slug + version** を `kernels-runbook.md` に固定
- [ ] `comp-timeline.md`: 締切・1日提出上限
- [ ] **pretrain-gate PASS**（長時間の場合）

### During

- [ ] セル順・再実行要否をメモ
- [ ] 9h 制限に近づいたら checkpoint / 中断方針

### After（完走しなくても必須）

- [ ] **成功:** Version N 確定 — **UI Save Version** または **`kernels push`**（stdout の `Kernel version N` を `run-log.md` に記録）
- [ ] **CLI push 時:** `scripts/kaggle-cli.ps1` のみ使用 · `kernels status` → **COMPLETE** · `kernels output` で実体を取得して出力サイズ/hash確認（`kernels files` の表示だけを信用しない）
- [ ] **失敗:** エラー全文・stderr・セル番号を `run-log.md` に貼る
- [ ] **移動必須:** 実行成果物（ipynb または simulation の bot ディレクトリ）→ `my-ran-notebook/{name}/` + **`lifecycle-manifest.md` を `ran` に更新**（Skill `kaggle-notebook-folders`）
- [ ] 提出は **別判断** → `kaggle-submission-validator` → **Notebook 紐づけ提出**（`NOTEBOOK-LINKED-SUBMIT.md` 方式 1 / 2 / **2b** · 自 kernel `-k` / `-v` · 403 時 zip-only 禁止）

### Version 作成（Save Version 相当）

| 経路 | コマンド / 操作 |
|---|---|
| **UI** | Run All → Save Version |
| **CLI** | `kernels pull -m` → 編集 → `kernels push -p <folder>/` |

**公式:** [Kaggle CLI — Update a Kernel](https://github.com/Kaggle/kaggle-cli/blob/main/docs/tutorials.md) · [kernel-metadata.json](https://github.com/Kaggle/kaggle-cli/blob/main/docs/kernels_metadata.md)

### Private 必須（自作資産）

- 自作 Notebook / Dataset / Model は **常に Private**（意図しないリーク防止）
- `kernel-metadata.json`: `"is_private": true` · `dataset-metadata.json` / `model-metadata.json`: `"isPrivate": true`
- push 前: `scripts/assert-kaggle-private.ps1` · Rule: `.cursor/rules/kaggle-private-assets.mdc`
- **禁止:** `datasets create --public` / `-u`（`kaggle-cli.ps1` が拒否）
- Day 0: `comp-start-checklist.md` の Private 項 · bootstrap Skill `kaggle-comp-bootstrap`

**Agent:** `kernels push` はユーザー明示 OK 後のみ（`PERMISSIONS.md`）

---

## Colab チェックリスト（簡易）

**接続手順 SSOT:** Skill **`cursor-colab-runtime`** — ユーザーが「Colab アクセス方法」と言ったら Skill の **ユーザー向けアクセス手順** をそのまま出力。

- [ ] `.ipynb` を開き Select Kernel → **Colab**（Sign in 済みなら Auto Connect 可）
- [ ] 長時間 GPU は **pretrain-gate PASS** 後
- [ ] CSV 等: `Mount Server to Workspace` → `sample_data/`（Skill `cursor-colab-runtime`）
- [ ] 終了時 **Disconnect**（Compute Unit 節約）
- [ ] ランタイム・GPU を `exp-train.md` と `run-log.md` に記録
- [ ] export パス・checkpoint を記録
- [ ] 提出用 artifact → **submission-validator**
- [ ] 実行後: **移動必須** → `my-ran-notebook/` + `run-log.md` + manifest `ran`

---

## run-log.md（デバッグ共有の要）

ユーザーが「ログしか共有できない」場合の **主な置き場**。

```markdown
# Run Log — {notebook-name}

> started: yyyy/mm/dd HH:MM UTC
> environment: kaggle | colab
> gpu: ...
> result: success | fail | partial
> output_version: N（成功時）
> kernel_slug: username/notebook-slug（提出紐づけ用）

## Input 固定
- dataset: slug @ version
- models: slug @ version

## エラー / ログ
（貼り付け）

## メモ
```

失敗でも **必ず** 作成。Agent はここを読んでデバッグ継続。

**simulation:** `run-log.md` の § simulation 実行 を埋める。手順 SSOT は `docs-ja/agent-debug.md`（comp-type=simulation かつ status=active）。

---

## Notebook ライフサイクル（runbook 視点）

```
my-notebook/
    ├─ [実行] ──→ my-ran-notebook/{nb}/ + run-log.md
    │                 ├─ デバッグのみで終了 OK
    │                 └─ 成果物あり ──→ submission-validator
    └─ [成果物のみ] ──→ submission-validator（実行ログ不要）
```

`my-submitted-notebook/` は validator **PASS 後のみ**。

---

## Agent 規則

1. **Kaggle 完走を提出の前提にしない**
2. 失敗 run も `my-ran-notebook/` + `run-log.md` を残す
3. **Kaggle/Colab の全起動は「ユーザー許可 + 対象ジョブ指示」の両方が必要**
4. 長時間 GPU 実行は **pretrain-gate PASS 後のみ**（Kaggle / Colab 共通）
5. Kaggle は **CPU最大5枠・GPU最大2枠**。指示済みジョブだけを並列化し、未指示ジョブで空きを埋めない
6. 自作 Notebook / Dataset / Model は **Private 必須**。push 前 private assert FAIL なら停止
7. CLI は preflight → metadata/path → private assert → wrapper の順。生の `kaggle` を使わない
8. Internet ON で秘匿 API を叩かない（Kaggle OFF 前提）
9. dataset 大量 DL 禁止（ユーザー指示時のみ）

---

## ユーザー依頼別

| 依頼 | 動作 |
|---|---|
| 「Kaggle で実行する」 | Before チェック → 実行後 run-log |
| 「エラーが出た」 | run-log 更新 → pretrain-gate 再判定（simulation なら `agent-debug.md` 参照） |
| 「Colab で学習」 | Colab checklist + exp-train |
| 「GPU で実行したい」 | §GPU 実行場所の確認 → ユーザー選択後に runbook 手順 |
| 「runbook 初期化」 | `kernels-runbook.md` テンプレ |

---

## 他 Skill

| Skill | 役割 |
|---|---|
| `kaggle-pretrain-gate` | 本番実行の前提 |
| `kaggle-submission-validator` | 提出前 |
| `docs-ja/agent-debug.md` | simulation: Error/Validation（Skill なし） |
| `kaggle-notebook-folders` | フォルダ移動 |
| `kaggle-comp-timeline` | 締切 |

---

## テンプレート

`%USERPROFILE%\.cursor\kaggle-template\comp\`
