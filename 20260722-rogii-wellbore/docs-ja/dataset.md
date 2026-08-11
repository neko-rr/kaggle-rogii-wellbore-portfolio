# データセット要約 — rogii-wellbore

> skill: dataset-summary  
> participant: Kazeneko  
> last-updated: 2026-07-23 UTC（**ローカル実測**）  
> sources: Data タブ + `dataset/` CLI DL  
> 実測 JSON: [`../exp/work/dataset-eda-20260723.json`](../exp/work/dataset-eda-20260723.json)  
> well 一覧: [`../exp/work/dataset-train-wells-light-20260723.csv`](../exp/work/dataset-train-wells-light-20260723.csv)  
> 原文メモ: [`../docs-en/dataset.md`](../docs-en/dataset.md)

---

## データの概要

水平坑井の軌道・検層と垂直参照ログ（Typewell）から、評価区間の **TVT（True Vertical Thickness, ft）** を予測する。評価指標は行単位 **RMSE**。

| 項目 | 内容（実測） |
|---|---|
| ローカル配置 | `20260722-rogii-wellbore/dataset/`（2026-07-23 確認） |
| train wells | **773**（各 `__horizontal_well.csv` + `__typewell.csv` + `.png`） |
| 手元 test wells | **3**（いずれも train と **同一 ID** · 例示のみ） |
| train 行数合計 | **約 509 万**（horizontal） |
| 評価区間行（`TVT_input` NaN） | **約 378 万**（全体の **~73%**） |
| 既知区間行 | **約 131 万** |
| TVT 値域（train） | **9245.19〜12893.89** ft |
| sample_submission | **14,151** 行 · wells=**3**（手元 test 用） |
| ライセンス | **Competition use only**（再配布・Git 禁止） |
| 本番 hidden test | **約 200 wells**（提出 rerun 時に差替 · 手元に無し） |
| **Public / Private 採点** | Public ≈ hidden の **26%** · 最終順位は残り **74%**（Private）。公式文は [`conditions.md`](conditions.md) |

**重要:** 手元 `test/` でスコアを本番とみなさない。`sample_submission` も手元 3 wells 用。画面の Public LB も **最終順位ではない**（約4分の1の試験）。

---

## 各ファイルの詳細な説明

### `train/{WELLNAME}__horizontal_well.csv`

井 ID は **ファイル名**（8 文字ハッシュ）。CSV 内に `WELLNAME` 列は **無い**（実測）。

| 列 | dtype（例） | 欠損（120 wells 合算サンプル） | 備考 |
|---|---|---|---|
| `MD` | float | 0 | Measured Depth (ft) |
| `X`, `Y` | float | 0 | Easting / Northing |
| `Z` | float | 0 | TVD |
| `ANCC` | float | あり（サンプルで ~2e4） | 地層深度 · **train only** |
| `ASTNU`, `ASTNL`, `EGFDU`, `EGFDL`, `BUDA` | float | サンプルでは 0 | 同上 · **train only** |
| `TVT` | float | 0 | **目的変数** |
| `GR` | float | **多**（サンプルで ~2.3e5） | NaN 補間が重要（Sunny NB 指摘） |
| `TVT_input` | float | **評価区間で NaN** | 既知 heel のコピー |

典型: 1 well あたり行数中央値 **~6576**、評価区間中央値 **~4840** 行、MD span 中央値 **~6575** ft。

### `train/{WELLNAME}__typewell.csv`

| 列 | 意味 |
|---|---|
| `TVT` | 垂直深度インデックス（水平井 TVT と対応） |
| `GR` | 垂直 GR |
| `Geology` | 地層ラベル（欠損行あり） |

**Geology 出現（typewell・80 wells サンプル、多い順）:** ANCC → EGFDL → ASTNL → BUDA → ASTNU → EGFDU → OLMOS → …（少数: MNSS, LBHL 等）

### `train/{WELLNAME}.png`

断面可視化 × **773**。EDA 用（提出必須ではない）。

### `test/`（手元 = 例示）

| well | 行数 | 評価行 | train と同一 ID | 列 |
|---|---|---|---|---|
| `000d7d20` | 5278 | 3836 | yes | `MD,X,Y,Z,GR,TVT_input` のみ |
| `00bbac68` | 7559 | 6014 | yes | 同上 |
| `00e12e8b` | 6384 | 4301 | yes | 同上 |

- **`TVT` 無し** · **formation tops 無し**
- 本番 hidden は別集合（~200）。ローカル test 最適化は無効

### `sample_submission.csv`

| 列 | 内容 |
|---|---|
| `id` | `{WELLNAME}_{row_index}`（例: `000d7d20_1442`） |
| `tvt` | 予測（サンプルは 0.0 埋め） |

手元は 3 wells 分のみ。本番は hidden の評価行すべて。

### `AI_wellbore_geology_prediction_task_en.pptx`

タスク説明スライド（~28 MB）。

### zip 控え

展開後の `rogii-wellbore-geology-prediction.zip` は **2026-07-23 削除済**（必要なら CLI で再 DL）。
---

## ベースライン実測（train ラベル · carry-forward）

評価区間で **最後の既知 `TVT_input` を定数外挿**した per-well RMSE（773 wells）:

| 統計 | RMSE (ft) |
|---|---|
| mean | **12.81** |
| median | **10.67** |
| p10 / p90 | 5.03 / 22.97 |
| max | **70.64** |

Discussion の Public「last TVT → 15.883」は **hidden/Public 集合**の話で、この train 代理値と一致しなくてよい。

**CF が特に悪い井（上位）:** `1b1eba53`, `86454a6f`, `a959858c`, …（`86454a6f` は Discussion 難井とも一致）

評価区間の (TVT − last_known) 残差（120 wells サンプル）: 中央値 ≈0、std≈17、|残差|平均≈11.9。裾が長い（±15 ft 二峰仮説と整合しうる）。

---

## モデリング上の注意（リーク・CV）

| リスク | 対策 |
|---|---|
| 同一 well 内リーク | **GroupKFold by well ID（ファイル名）** |
| `TVT_input` 評価区間 | 入力で NaN 扱いを明示 · 既知区間は教師 |
| 地層 tops（ANCC 等） | **test に無い**（手元 test で確認済）。本番特徴にそのまま使わない |
| GR 欠損 | 補間必須（高 NaN 井あり） |
| 手元 test = train twin | local「test スコア」を LB とみなさない |
| CF 難井 | hard-set を固定して平均だけの改善を rejected（CHK-024） |

---

## ローカル配置

```text
dataset/
├─ README.md
├─ sample_submission.csv
├─ AI_wellbore_geology_prediction_task_en.pptx
├─ train/          # 773 wells × (hw, tw, png)
├─ test/           # 3 example wells
├─ derived/        # 自前加工のみ
└─ *.zip           # 任意（展開済なら削除可）
```

- 公式ファイルは **編集禁止**（加工は `derived/`）
- Git にコミットしない

## 関連

| ファイル | 役割 |
|---|---|
| [`conditions.md`](conditions.md) | 評価・制限 |
| [`metric-repro.md`](metric-repro.md) | RMSE |
| [`../exp/experiment-checklist.md`](../exp/experiment-checklist.md) | CHK-010 以降 |
| [`../docs-en/dataset.md`](../docs-en/dataset.md) | English notes |
