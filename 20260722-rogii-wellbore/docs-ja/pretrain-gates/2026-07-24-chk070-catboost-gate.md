# Pretrain Gate — CHK-070 CatBoost drift/residual GPU train (hard20)

> skill: kaggle-pretrain-gate  
> chk: CHK-070  
> date: 2026-07-24  
> profile: tabular

## Scope

- Private fork of `romanrozen/catboost-baseline` concept
- Target: residual on linear baseline (≈drift family) · GroupKFold(well)
- Mode: hard20 wells · CatBoost `task_type=GPU`
- Output: `tip_train_preds.csv` / `chk070_oof_preds.csv` (`id,tvt`)

## Tier checks

- [x] Competition data only · Private · Internet OFF · GPU ON
- [x] No Random KFold (F003)
- [x] Not pure soft-argmax NCC (F008)
- [x] Not thin NCC+LGBM absolute TVT (F007) — CatBoost residual + trajectory/GR features
- [x] Prior CatBoost baseline completed publicly (~99s debug / full GPU ok)
- [x] hard20 filter baked · OOF export added

**結果:** PASS → Kaggle GPU push 可
