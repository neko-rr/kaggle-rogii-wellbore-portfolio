# Agent デバッグ — rogii-wellbore

> status: **inactive**  
> comp-type: （simulation のとき **active** — それ以外は **inactive** のまま）  
> participant: Kazeneko  
> comp-url: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction  
> last-updated: （yyyy/mm/dd UTC）

**目的:** シミュレーションコンペで **Error submission・Validation Episode・agent ログ** を解析する SSOT。  
**Skill は作らない** — `kaggle-simulation-tracker`（メタ追跡）と **ペア** で使う。

---

## 有効化（simulation 開始時）

`comp-type: simulation` にしたら:

1. 本ファイル先頭 `status: active` に更新
2. `sim-track/` を運用開始（bootstrap で生成済みなら中身を記入）
3. `comp-profile.md` の simulation 行を確認
4. `exp-infer.md` § simulation 提出 を使う

**inactive のとき:** 読まない。`comp-profile.md` の「使わない」参照。

---

## ログ取得

### 1. Kaggle CLI（提出ステータス）

```powershell
kaggle competitions submissions -c <competition-slug>
```

- `Error` / `Complete` を確認
- 出力は `exp/submissions-cli.log` に追記可（Skill: `kaggle-cli-fetch`）
- 正式記録は `exp/exp-infer.md` § simulation 提出

### 2. Notebook / Kernel ログ

| ソース | 置き場 |
|---|---|
| stderr・トレースバック | `my-ran-notebook/{nb}/run-log.md` |
| セル出力の一部 | 同上（ユーザー貼り付け可） |
| Output ファイル一覧 | `run-log.md` 成功時メモ |

### 3. Episodes / replay（コンペによる）

| 取得手段 | 備考 |
|---|---|
| Host Discussion / Rules | 公式手順を優先 |
| ユーザー貼り付け | Agent は推測で補完しない |
| 大量 DL | **ユーザー明示時のみ**（sim-tracker と同規則） |

---

## ローカル再現（`kaggle_environments`）

### 前提

- Python 環境に `kaggle_environments` をインストール（コンペ指定バージョンに合わせる）
- `main.py` の `agent(obs, config)` シグネチャを Rules と一致させる

### 最小手順

1. ローカルに `main.py`（または提出 NB から export）を置く
2. Validation Episode **1 本** を実行（pretrain-gate Tier 1 と同じ）
3. 失敗時: 例外全文を `run-log.md` に保存
4. PASS 後: Kaggle へ再提出 → `exp-infer` に記録

### pretrain-gate 連携

| Tier | simulation チェック |
|---|---|
| 0 | `main.py` import、obs/action 型 |
| 1 | Validation Episode 1 本完走 |
| 2 | 対 random win/tie または acceptance 基準、timeout なし |

---

## よくある失敗

| パターン | 典型原因 | 最初に見る場所 |
|---|---|---|
| **Error submission** | 実行時例外・import 失敗 | `run-log.md` + CLI status |
| **timeout** | 1 step 遅い・無限ループ | Episode ログ・`agent()` 内ループ |
| **空 action / 型不一致** | `action` shape・dtype | Rules の action space |
| **Validation のみ失敗** | 本番 episode と設定差 | `main.py` vs Notebook 内の差分 |
| **再現不能** | Internet ON 依存・パス違い | `kernels-runbook.md` Input 表 |

---

## 記録フォーマット

### `my-ran-notebook/{nb}/run-log.md`

- § **simulation 実行** を埋める（テンプレ: `run-log.md.template`）
- `registry_slug` で `sim-track/submitted-notebook-registry.md` と紐付け

### `exp/exp-infer.md` § simulation 提出

| 列 | 意味 |
|---|---|
| submit_id | 連番または CLI の提出 ID |
| status | `Complete` / `Error` |
| validation | Validation スコア or — |
| episode_notes | timeout・例外要約 |
| run-log | 相対パス |

### `sim-track/submitted-notebook-registry.md`

提出 NB 登録時に **ローカルパス ↔ Kaggle slug** を追記（Skill: `kaggle-simulation-tracker`）

---

## simulation-tracker との分担

| やること | 担当 |
|---|---|
| 公開 NB 一覧・score 時系列 | `kaggle-simulation-tracker` → `sim-track/` |
| **自チーム Error の原因** | **本ファイル** → `run-log.md` |
| 上位 bot の推移 | simulation-tracker |
| Validation ローカル再現 | **本ファイル** |

---

## 更新履歴（changelog）

| updated_utc | source | 変更内容 |
|---|---|---|
| （初回） | bootstrap | status=inactive で作成 |

---

## 関連ファイル

| ファイル | 役割 |
|---|---|
| `comp-profile.md` | simulation ルーティング |
| `kernels-runbook.md` | Kaggle 実行・run-log |
| `pretrain-acceptance.md` | Tier 基準 |
| `sim-track/sim-track-index.md` | メタ追跡索引 |

