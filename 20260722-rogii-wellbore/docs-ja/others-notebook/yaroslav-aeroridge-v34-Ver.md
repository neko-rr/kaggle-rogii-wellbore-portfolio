# yaroslav AeroRidge v34 — 日本語分析

> analyzed: 2026-08-04 eve  
> source: [`yaroslavkholmirzayev/reproduce-strongest-reference-aeroridge-v34`](https://www.kaggle.com/code/yaroslavkholmirzayev/reproduce-strongest-reference-aeroridge-v34)  
> 原文 pull: `others-notebook/public-useful-refresh-20260804-eve/aeroridge-v34/`  
> コード抜粋: `docs-en/others-notebook/aeroridge-v34-Ver-latest.py`  
> 関連: [Contact+U Restore](yaroslav-contact-u-restore-Ver.md) · [evansussex Q0522](rogii-public-score-frontier-lab-visuals-evansussex-Ver1.md)  
> lastRun: **2026-08-04** · votes ≈43 · GPU T4 · Internet OFF

## 1 行結論

タイトルは **AeroRidge** だが、マークダウン本文は **「Contact and U Restore · Codex Q2522 Consensus Gate（experiment 98）」**。  
**Q0522 / tip 同家系**の上に residual weight 0.120 · row cap **0.50 ft** · consensus feature を載せた再パッケージ。**Final / Active 不可**。

## 使用するデータ

- コンペ `rogii-wellbore-geology-prediction`
- 公開 artifacts: `koolbox-offline` · `nina2025/rogii-03` · `pilkwang/rogii-model-package` · `fleongg/rogii-claude-models-pub` · `needless090/rogii-tabicl-mirror` · `ravaghi/...artifacts`

## 前処理

1. 基線は **Q branch total 2.522 ft**（Q0522 制御）  
2. feature mode=**consensus** · residual weight **0.120** · row correction cap **0.50 ft**  
3. 補正は downloaded submission の再再生ではない、と明記（元 Contact+U 叙述と同一系統）  
4. heel 校正 · bimodal hedge · contact guard · learned_trajectory · GS1.30/Q0522 VISUALS ブロック等の tip 定番層

## モデルの定義

新規の独自物理モデル名ではなく、**Contact-Gated / dual-track PF + model package** エコシステムの profile 選択（vp_balanced / conservative / contact_gated_anchor 等）。

## 学習の設定

GPU 提出向け。診断用の all-train CV sweep は提出パスで無効、という叙述あり（他 tip NB と同様）。

## その他

- 出力に `model_package_*` · `gold_prefix_*` · `learned_trajectory_submission.csv` · `gs130q0522_*` 等（tip 生態）  
- 同作者 Contact+U の改題・パラメータ微調整と読むのが安全

## 自チーム

| する | しない |
|---|---|
| 「終盤公開=Q0522 改題」として監視リストに載せる | Active / Final / residual 政策への移植 |
| Public 人気と混同しない | AeroRidge という名称だけで新経路と扱わない |
