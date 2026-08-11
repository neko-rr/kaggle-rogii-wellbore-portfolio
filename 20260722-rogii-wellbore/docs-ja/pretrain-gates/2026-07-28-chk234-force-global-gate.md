# pretrain-gate — CHK-234 force selector GLOBAL variant tip-cv GPU

> skill: kaggle-pretrain-gate  
> date: 2026-07-28  
> chk: CHK-234  
> profile: tabular  
> lane: Kaggle GPU（ユーザー: 次実験指示）

## Tier 0

- [x] tip-cv ベース fork · Private · GPU · Internet OFF · dataset_sources 継承
- [x] T4 audit: tip-cv は BIN routing（hard20 の 13/20 が hold=0.05）· GLOBAL パッチは実質無効（231c 説明）
- [x] graft: 全 `SELECTOR_BIN_VARIANTS` → `pf_scale_8_hold_0.2`（選択のみ · generator 不変 · F015）
- [x] ≠F022 weight · ≠F023 mid-bank proxy · 提出なし

## Tier 1

- [x] builder patch verify · BIN 6 キー全て同一 variant

## Tier 2

- [x] acceptance: tip-cv hard20 ≤29.599（vs 29.899 ≥+0.30）

## Verdict

**PASS** → `tip-cv-gpu-sel-force-global-h20` push 可
