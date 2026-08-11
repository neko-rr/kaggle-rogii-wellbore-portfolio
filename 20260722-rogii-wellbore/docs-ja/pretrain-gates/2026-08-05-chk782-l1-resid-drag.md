# Pretrain Gate — CHK-782 resid-drag weighted L1

- **Date:** 2026-08-05
- **CHK:** CHK-782
- **NB:** `my-notebook/tip-cv-chk782-resid-drag-h20/`
- **Status:** **PASS** 静的 · ban-gate pre PASS · **push は GPU 空き後**
- **Lane:** Kaggle GPU · Colab 不可セッション

## Tier 0

- [x] weights from 766 drag map · n=41
- [x] sample_weight train_stack · FAST L1
- [x] assert-private PASS · submit ban
- [x] ≠ 761 fold-driver（井集合・重み差）

## ban-gate pre

PASS · T3 · residual-α なし · F015 遵守
