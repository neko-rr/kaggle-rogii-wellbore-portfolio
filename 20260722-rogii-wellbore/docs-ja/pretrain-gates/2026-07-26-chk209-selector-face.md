# Pretrain gate — CHK-209 tip-cv-sel-face-combo-h20

> date: 2026-07-26  
> job: `kazeneko77/tip-cv-sel-face-combo-h20` · Kaggle GPU · **提出なし**  
> 根拠: CHK-206 根因（phys 優先）· CHK-208 combo oracle PASS

## Tier 0

- [x] tip 同型 dataset_sources · Private · Internet OFF
- [x] 変更は selector 面強制 + init_spr/seeds のみ
- [x] STOP_AFTER_SELECTOR（learned/test-id 回避）
- [x] 提出禁止（F015）

## Tier 1

- [x] tip-cv hard20 Ver2 完走実績
- [x] 208 で同一 PF ノブの combo がローカル完走

## Tier 2

- [-] N/A（本ジョブ自体が hard20 screen）

## 判定

**PASS** — 見込み ~40–90 min（seeds 256）· 9h 以内

## 停止

- selector 面 RMSE が phys 14.87 より大幅悪化のみで提出しない（診断）
- OOM → seeds を 128 に戻して再試行を検討
