# hahaha-nondet-agi — Ver2（分析）

> kernel: `kazeneko77/hahaha-nondet-agi`  
> Public LB: **6.644**（2026-07-21 · Version 2）  
> 取得: latest（Ver2 提出と一致）  
> 原文コード: `docs-en/others-notebook/hahaha-nondet-agi-latest.py`

## 使用するデータ

- 公式: `rogii-wellbore-geology-prediction`
- 外部 Dataset（metadata）:
  - `phongnguyn23021656/koolbox-offline`
  - `nina2025/rogii-03`
  - `pilkwang/rogii-model-package`
  - `thbdh5765/rogii-v10-fresh-artifacts`
  - `fleongg/rogii-claude-models-pub`
  - `needless090/rogii-tabicl-mirror`
  - `ravaghi/wellbore-geology-prediction-artifacts`

## 前処理

- Contact-Gated Stratigraphic Alignment 系
- heel / visible-prefix 校正
- Typewell GR との整合（PF・beam）
- bimodal detector（hedge 用）

## モデルの定義

- **Track A:** LightGBM / CatBoost + Ridge（well GroupKFold）
- **Track B:** Particle filter（複数 seed/scale）+ selector
- fleongg / model package 補正パスあり（プロファイル依存）

## 学習の設定

- GPU ON · Internet OFF
- `VARIANT = 'pf_scale_8_hold_0.2'` 系セレクタ
- タイトル通り **nondet**（決定論 det-* よりランタイム揺らぎありうる）

## その他

- コード hash `315bd90addfe249b`（同フォルダ内で一意）
- **自チーム提出の最良 Public**
- 本質は公開スタックの設定違い。独自理論は薄い

## 採用可否（次実験）

| 判断 | 理由 |
|---|---|
| **ベースとして維持** | 現状 Best LB |
| そのまま Final 唯一にはしない | 公開系と相関が高い可能性 |
| 要実施 | 自前 well-group CV · 難井リストでの内訳 · 方位分割の有無確認 |
