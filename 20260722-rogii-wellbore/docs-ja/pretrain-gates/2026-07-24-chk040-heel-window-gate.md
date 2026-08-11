# Pretrain Gate — CHK-040 heel+window NCC + CatBoost drift head

> skill: kaggle-pretrain-gate  
> chk: CHK-040  
> date: 2026-07-24  
> profile: tabular

## Scope

- Heel last_anchor tie + windowed multi-scale NCC features
- Train CatBoost GPU on **drift** (not XYZ residual = F010 avoid)
- Unconstrained soft-argmax exported as control only (F008 avoid as main)
- hard20 · GroupKFold · outputs `tip_train_preds.csv`

## Tier checks

- [x] Competition data only · Private · Internet OFF · GPU ON
- [x] GroupKFold(well)
- [x] Hypothesis keywords avoid F007–F010 banned phrases
- [x] Unconstrained control for acceptance (3)

**結果:** PASS → GPU push 可
