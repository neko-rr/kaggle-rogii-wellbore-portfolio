# rogii-luck-is-all-you-need — tip 分析（opencv411 · Public 6.478）

> analyzed: 2026-07-23 · **refresh確認: 2026-07-25**  
> source: `opencv411/rogii-luck-is-all-you-need`  
> Private fork WIP: `my-notebook/rogii-luck-is-all-you-need/`（`kazeneko77/...` · `is_private: true` · GPU）  
> 原文: `docs-en/others-notebook/rogii-luck-is-all-you-need-Ver-latest.py`  
> 2026-07-25: `hjyact/ultimate-pf-…` · `youill0317/…gs130…` と **コード同一**（SHA一致）

## 家系判定（1行）

**dual-track / Contact-Gated 同家系**（別メカニズムではない）。見出しは「ROGII Contact-Gated Stratigraphic Alignment」。Ver2 `hahaha-nondet-agi` と同スタック（ravaghi / koolbox / fleongg / pilkwang）。

## 使用するデータ

- 公式コンペ + metadata DS（Ver2 と同型7本）
- コードが主に触る: ravaghi artifacts · koolbox · fleongg · pilkwang model-package

## 前処理 / パイプライン

- ridge/PF anchor → projection → fleongg blend → guarded contact → VP cal → model-package → PF seed-branch midpoint hedge
- 既定プロファイル: **`vp_balanced_modelpkg_005`**（bimodal detector OFF · model package ON）

## 決定性（"Luck"）

- `CFG.seed=42` · PF 多シード（128）· VP seeds 24/48
- numba PF 内 `np.random` → **nondet 寄り**（タイトルの Luck ≈ 多シード/ランタイム揺らぎ）
- **取り込み後の seed/α 乱獲は禁止**（計画 Stop）

## GPU 要否

| 作業 | GPU |
|---|---|
| 物差しのみ（CF · GroupKFold RMSE · hard-well） | **不要（ローカル CPU）** |
| tip 提出相当の再推論 / smoke / 200well 時間 | **GPU 推奨**（metadata `enable_gpu: true` · 再学習時 LGBM/CatBoost GPU）。提出パスは artifacts ロード主体で PF は numba CPU |

## 主要ハイパラ（Ver2 差分メモ）

- 分岐 hedge: `_BH_STRENGTH=0.60` · `_BH_SEP_LOW=4`（det-mha の `_MH_ALPHA/_MH_SEPLO` とは別名）
- SP45 0.30/0.70 · blend 0.60 · package `max_w=0.00425`
- **PF GR noise:** `gs = clip(nanstd(GR−tw), 10, 60) * 1.3`（Discussion [728712](../discussion/728712-gs-noise-scale-public-nb.md) と同内容・**既に tip 内**）
- 実行約 **13 min**（papermill）

## Final 2 含意

同家系のため Final は [`comp-strategy`](../comp-strategy.md): 枠1=Trust CV · 枠2=Public最良（別経路探索は F011/F012 で閉鎖）。  
`gs*1.3` の再スイープや ultimate-pf の再 fork は **枠1/枠2 を変えない**（既実装の確認のみ）。
