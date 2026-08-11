# rogii-geoanchor — 日本語要約

> analyzed: 2026-07-25  
> source: `lucifer19/rogii-geoanchor`  
> 原文: `others-notebook/public-useful-refresh-20260725/rogii-geoanchor/`  
> コード: `docs-en/others-notebook/rogii-geoanchor-Ver-latest.py`  
> 索引: [public-useful-refresh-20260725.md](public-useful-refresh-20260725.md)

## 家系判定（1行）

**Dual-Champion Suffix Arbiter** — 二本の champion を固定し、hidden suffix だけ合意付きで動かす。エンジンは dual-track / SP45 / fleongg **同家系**（別予測面ではない）。

## 使用するデータ

- 公式コンペ + 公開 artifacts / model-package（任意マウント）
- model-package が無い・非互換なら prefix-verified champion を保ったまま arbiter へ

## 前処理

- heel 校正（α,β）· GR→typewell スケール合わせ
- visible prefix を偽ホールドアウト（cut 0.50/0.65/0.75）にして候補選択
- contact 再構成は **prefix RMSE ≤ 1.0 ft · 比較行≥50** 等のガード付き（主に EGFDU）

## モデルの定義

1. residual（tree + PF）  
2. physical selector（likelihood PF / beam）  
3. ridge/selector アンカー + U=T+Z 投影  
4. learned blend  
5. **suffix arbiter**: surface drift · GR novelty · package/PF/learned 残差の **符号合意** + ramp + ステップ上限  
6. well 単位 rollback · 全体 audit rollback

代表コントロール例: `α=1.0`, `τ=85`, `w_pf=0.15`, SP45 0.30/0.70, projection blend 0.75。

## 学習の設定

- 提出モードでは重い CV / ablation OFF（`RUN_CV_REPORT=False` 等）
- プロファイル例: `dual_track_prefix_balanced` · `…_modelpkg_005/010`

## その他

| 項目 | 内容 |
|---|---|
| 強み | 「いつ動かすか」の叙述が明確 · 監査成果物が多い |
| 弱み | tip と同情報面 · Final2 多様性には弱い |
| 自チーム | arbiter **条件設計**の参考のみ。丸写し・新規 CHK は開かない |
| 優先 | **A（叙述）** |
