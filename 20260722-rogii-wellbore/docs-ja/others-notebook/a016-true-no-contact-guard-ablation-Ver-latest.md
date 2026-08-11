# a016-true-no-contact-guard-ablation — 日本語要約

> analyzed: 2026-07-25  
> source: `zongzishuang/a016-true-no-contact-guard-ablation`  
> 原文: `others-notebook/public-useful-refresh-20260725/a016-true-no-contact-guard-ablation/`  
> コード: `docs-en/others-notebook/a016-true-no-contact-guard-ablation-Ver-latest.py`  
> 索引: [public-useful-refresh-20260725.md](public-useful-refresh-20260725.md)

## 家系判定（1行）

**公開 7.091 系（A013）の ablation**。意図変更は `DISABLE_GUARDED_CONTACT_OVERRIDE = True` のみ。tip（`gs*1.3` 入り Contact-Gated）とは別世代。

## 使用するデータ

- 公式 + 公開 dual-track 系 metadata（ravaghi / koolbox / fleongg 近縁の A013 パイプライン）

## 前処理 / パイプライン

- A013 本体を維持: blend w0.60 · gold conservative · micro guard
- **Guarded contact override を無効化**（true no-contact-guard）
- 終端で `submission.csv` 必須（複数フォールバック）

## モデルの定義

- 公開 7.091 スタック（ridge/PF · projection · fleongg · contact）のまま
- 大きな後処理変更はしない（conservative score policy）

## 学習の設定

- 本 NB は学習スイープではなく **提出安全な ablation / rebuild**
- 環境変数でも `DISABLE_GUARDED_CONTACT_OVERRIDE` を上書き可

## その他

| 項目 | 内容 |
|---|---|
| 目的 | A012 が submission を残せず失敗 → A013/A016 で artifact 保証 |
| tip との差 | tip は `gs*1.3` あり · A016 は無し · guard OFF が主差分 |
| 自チーム | guard の効き理解用。**盲目 OFF 提出はしない**（既存 tip は guard 前提） |
| 優先 | **A（ablation 参照）** |
