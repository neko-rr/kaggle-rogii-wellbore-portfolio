# rogii-det-mha* 家系 — Ver2（分析）

> kernels: `rogii-det-mha180sep3` · `mha140sep4` · `mha120sep4mpkg10`  
> 取得: latest（各 Version 2 提出と一致）  
> コード: `docs-en/others-notebook/rogii-det-mha*-latest.py`

## 使用するデータ

共通:

- 公式コンペ
- `koolbox-offline` · `fleongg/rogii-claude-models-pub` · `ravaghi/...-artifacts`
- **mha120sep4mpkg10 のみ** `pilkwang/rogii-model-package` を明示 ON

## 前処理 / モデル

タイトルどおり **Deterministic dual-track**:

1. **Track A (learned):** LGBM/CatBoost per-row delta + grouped Ridge · seed 固定
2. **Track B (trajectory):** 128-seed likelihood-weighted **particle filter** + beam · guarded contact · prefix cal
3. **Post:** global bias · **bimodal-datum midpoint hedge**

`ROGII_GOLD_PROFILE = "conservative"`（コメント: balanced 7.549 vs conservative 7.178）

## 学習の設定 — 唯一の制御差分

```text
_MH_ALPHA, _MH_MINMASS, _MH_SEPLO, _MH_SEPHI, _MH_CAP = ...
```

| variant | α | seplo | sephi | min mass | model package | Public LB |
|---|---|---|---|---|---|---|
| **mha180sep3** | **1.8** | **3.0** | 40 | 0.22 | OFF | **6.906** |
| mha140sep4 | 1.4 | 4.0 | 40 | 0.22 | OFF | 6.979 |
| mha120sep4mpkg10 | 1.2 | 4.0 | 40 | 0.22 | **ON (max_w=0.01)** | 7.003 |

解釈: PF が二峰（質量≥0.22 · 峰間隔 seplo–40 ft）のとき、予測を中点方向へ α だけ寄せる（Discussion 711878 の midpoint と一致）。

## その他

- mha140 と mha180 はコード長ほぼ同一（~199k）で **後処理定数だけ差**
- mha120 は package 補正セル追加で長い
- 公開 LB では **α を上げ seplo を下げた mha180 が最良**（この3兄弟内）

## 採用可否

| 判断 | 理由 |
|---|---|
| hedge グリッドの知見は **再利用価値あり** | 自 CV で α/seplo を再スイープすべき |
| package ON は LB 悪化 | この3点では不要寄り |
| 本体アーキは fork | 独自化なしでは Private 同時沈没リスク |
