# Contact-Gated / Dual-Track 兄弟 — Ver2（分析）

> kernels: `rogii-kim-om020` · `top-reproducible-pf-config-branch-conservative` · `rogii-dual-track-prefix-calibrated-geosteering`  
> コード: `docs-en/others-notebook/{slug}-latest.py`

## 共通

- タイトル系: **ROGII Contact-Gated Stratigraphic Alignment** または **Dual-Track Prefix-Calibrated Geosteering**
- 部品: koolbox · ravaghi artifacts · fleongg ·（多くで）pilkwang / nina / thbdh / tabicl
- Track A tabular + Track B PF + prefix cal + bimodal hedge
- GPU ON（dual-pipeline 以外）

## 個別

### rogii-kim-om020 — LB 7.132

- Contact-Gated 同型
- hash `71139d11e2144ecf`（hahaha とは別）
- hahaha より約 **0.5** 悪い → 設定/乱数/プロファイル差

### top-reproducible-pf-config-branch-conservative — PENDING

- Contact-Gated + **BRANCH conservative**
- `ROGII_GOLD_PROFILE` / visible-prefix ブリッジあり
- 提出は Scoring PENDING（2026-07-22）— hidden 時間に注意

### rogii-dual-track-prefix-calibrated-geosteering

- **注意:** API で Ver2 単体取得不可（403）。取得は **最新**（提出履歴上 Ver3–6 が 7.06–7.12）
- Dual-Track 本流タイトル · Dataset セットが最充実
- Ver2 時点の正確な差分は UI で Version History を確認すること

## 使用するデータ / 前処理 / モデル

det-mha 家系・hahaha と同じ骨格（上記索引参照）。

## 採用可否

| 判断 | 理由 |
|---|---|
| kim / dual-track 単体の追提出は低優先 | 最良 hahaha・mha180 より劣る |
| top-reproducible は結果待ち | PENDING 解消後に CV 比較 |
| 全体 | **1 家系の乱獲** — 次は別メカニズム（方位・近傍転写・自前整合）が必要 |
