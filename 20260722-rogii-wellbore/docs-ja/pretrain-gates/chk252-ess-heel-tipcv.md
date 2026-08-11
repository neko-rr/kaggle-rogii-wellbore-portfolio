# Pretrain gate — CHK-252 tip-cv ESS heel

> profile: tabular · tip-cv GPU · 2026-07-28

## Tier 0

- [x] tip-cv base `tip-cv-sel-face-temp0p15-h20` から派生 · allowlist / dataset_sources 継承
- [x] `is_private: true` · `enable_gpu: true` · internet off
- [x] 提出セルなし（TIP_CV_STOP_AFTER_SELECTOR）
- [x] patch: `init_spr` 引数 + ESS ゲート追加シードのみ（≠230 全域 gs/pn/N）

## Tier 1

- [x] builder 後静的 assert（flag / pf / ens）PASS
- [ ] Kaggle 実行 smoke（ジョブ開始時）

## Tier 2

- mid-bank soft Δ **+0.225**（参考のみ · **F023**: 採択根拠にしない）
- tip-cv hard20 直測で判定

## Verdict

**PASS**（GPU tip-cv 起動可）· 採択は tip-cv スコア次第
