# Kernels Runbook — rogii-wellbore

> skill: kaggle-kernels-runbook  
> participant: Kazeneko  
> comp-url: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction  
> last-updated: 2026-07-23 UTC

Kaggle / Colab 実行の環境メモ **SSOT**。

---

## 実行場所の方針

| 用途 | 場所 |
|---|---|
| 短時間（推論・軽い検証） | ローカル or Kaggle Notebook（多くは CPU） |
| Kaggle CPU | **最大5枠を並列実行可能**。ユーザー許可 + 対象ジョブ指示の両方がある場合のみ |
| Kaggle GPU | **最大2枠を並列実行可能**。ユーザー許可 + 対象ジョブ指示 +（長時間なら）pretrain-gate PASS |
| 長時間 / GPU 必要 | Kaggle（**公式 9h 上限**）または Colab — **ユーザーが A/B 選択**。未指示ジョブで空き枠を埋めない |
| 提出 rerun | Kaggle Notebook · **Internet OFF** · 出力 **`submission.csv`** |
| スモーク・gate | ローカル or Kaggle 短時間 |

**起動の前提:** ユーザー許可済み **かつ** 対象ジョブの実行指示あり。全自作 Kaggle 資産は **Private**。  
**長時間実行の追加前提:** `kaggle-pretrain-gate` PASS

---

## Input 固定（Kaggle）

| Input | slug | version | 備考 |
|---|---|---|---|
| Competition Data | `rogii-wellbore-geology-prediction` | （DL 後に固定） | 公式コンペデータ |
| Dataset（自作派生） | — | — | 使う場合は Private |
| Models | — | — | 公開 pretrained は可（license-ledger 追記） |

Internet: **OFF**（提出必須。開発時の一時 ON は notes に理由）

---

## Kaggle 設定メモ

| 項目 | 値 |
|---|---|
| Accelerator | CPU / GPU — **どちらもユーザー指示後**（CPU最大5枠 / GPU最大2枠） |
| Internet | **OFF**（提出） |
| 実行時間上限 | **9h**（CPU/GPU とも） |
| 提出成果物 | `/kaggle/working/submission.csv` |
| 時間見積 | 可視 test は **約 3 wells**。hidden ≈ **200 wells** → 単純比例で数十倍。提出前に大規模推論ベンチ必須（Discussion 728152） |

---

## Colab 設定メモ

| 項目 | 値 |
|---|---|
| ランタイム | （T4 / A100 等） |
| ドライブ保存先 | — |

---

## 関連

| ファイル | 役割 |
|---|---|
| `my-ran-notebook/{nb}/run-log.md` | デバッグ共有ログ |
| `pretrain-gates/` | 学習前ゲート |
| `submission-validations/` | 提出前検証 |


## Private 必須

- 自作 Notebook / Dataset / Model: `is_private` / `isPrivate: true`
- CLI: `check-kaggle-cli.ps1` → metadata/path確認 → `assert-kaggle-private.ps1` → `kaggle-cli.ps1`
- `kernels push` は `-p <folder>` を必ず明示（wrapper が private/metadata を自動検査）
- `datasets create --public` 禁止

