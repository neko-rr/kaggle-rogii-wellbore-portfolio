# hyperparameter-table — rogii-wellbore

> 詳細な表形式ログ。要約と考察は `exp-train.md` / `exp-infer.md` / `exp-intel.md` に書く。

---

## 学習実験

| exp_id | 日付 | モデル | データ / fold | 主要パラメータ | CV | 判断 |
|---|---|---|---|---|---|---|
| W0-ruler-cf | 2026-07-23 | carry-forward | train 773 · GroupKFold5 · seed42 | last known TVT_input | pooled **15.91** | 門番 · CHK-010/012 |
| W1-heel-gs0.85 | 2026-07-23 | heel affine proxy | 同上 | gs=0.85 | 32.60 | **NO-GO** |
| W1-heel-gs1.15 | 2026-07-23 | heel affine proxy | 同上 | gs=1.15 | 30.18 | **NO-GO** |
| W1-nbr150 | 2026-07-23 | neighbor copy | 同上 | max_ft=150 · heel shift | 15.95 | 非改善 · tip graft 要 |
| W1-nbr600 | 2026-07-23 | neighbor copy | 同上 | max_ft=600 | 18.97 | **NO-GO** |
| W1-hedge-deg | 2026-07-23 | midpoint±15 | 同上 | α=0.5 sep=15 | =CF | **NO-GO**（退化） |
| W2-phys-drift | 2026-07-23 | MD linear | 同上 | known-zone lstsq | ~1400 | **NO-GO** |
| tip-cv-hard20 | 2026-07-23 | tip luck (train eval) | hard20 wells · TIP_CV | tip-train-cv Ver3 | tip **14.87** vs CF同井 **49.56** · cover 1.0 | **PASS** · CHK-014 |
| F-050 | 2026-07-24 | Ridge CV audit | 200wells sample | Group vs Random · ±tops | Random楽観 · tops楽観 | **F003** · CHK-050 |
| F-051 | 2026-07-24 | tip nondet | hard20 seed42 vs 123 | preds identical | **spread 0** | CHK-051 done |
| F-052 | 2026-07-24 | error map | hard20 tip | az×MD×bimodal | NW_N worst · MD遠方 | CHK-052 |
| F-053 | 2026-07-24 | tip↔Sunny | hard20 · Sunny PF 8×200 | pearson **0.999** | NCC本命 | CHK-053 |
| （済）CHK-040 | 2026-07-24 | heel+窓 NCC+drift | hard20 | Ver1 GPU | OOF 45.96 · tip corr 0.999 | **F011 NO-GO** |
| （予定）CHK-041 | — | 多峰 posterior hedge | tip CV 物差し | tip `_BH_*` · 退化代理禁止 | — | pending · lit P2 · 023後継 |
| CHK-060 | 2026-07-24 | CF fold multi-seed | 773 · seeds 42/123/2026 | worst_fold band≈0.51 | pooled **15.91** | done · 門番安定 |
| CHK-061a | 2026-07-24 | T2 allowlist | hard20+az sample60 | 方位均等 | n=80 | done · T2準備 |
| CHK-061 | 2026-07-24 | tip T2 CV | balanced 80井 | tip-train-cv Ver4 · GPU 1.5h | tip **8.33** vs CF同井 **27.77** | **PASS** |
| CHK-062 | 2026-07-24 | tip T3 multi-seed | balanced 80 · seeds 42/123/2026 | seed42=T2 · GPU seed123+2026 | pooled **8.330** · band **0.0** · identical | **GO** · done |
| CHK-090 | 2026-07-24 | tip vp_conservative_final | E2E vs default | tip-vp-conservative-final | ≡default（max_abs0） | **NO-GO** · F013 |
| CHK-091 | 2026-07-24 | tip SP45 0.50/0.50 | hard20 TIP_CV | tip-cv-sp45-h20 | pooled **24.78** ≫ tip14.87 | **NO-GO** · F013 |
| CHK-092 | 2026-07-24 | T2 winners | — | — | 勝者なし | **cancelled** |
| CHK-093 | 2026-07-24 | tip bimodal_guarded | E2E vs default | tip-bimodal-guarded-profile | ≡default | **NO-GO** · F013 |
| CHK-031-smoke | 2026-07-24 | NCC+drift LGBM | smoke 3wells | self-contained · CPU | pooled **11.39** | smoke OK · hard20へ |
| CHK-031-h20 | 2026-07-24 | NCC+drift LGBM | hard20 | `chk031-ncc-hard20` | pooled≈38 · tip corr≈0.999 | **F007 NO-GO** |
| CHK-031-pure | 2026-07-24 | pure multi-scale NCC | hard20 | `rogii-ncc-pure-hard20` | pooled≈560 · tip corr≈0.72 | **F008 NO-GO** |
| CHK-020-pp | 2026-07-24 | NW_N last_anchor blend | tip T2 preds | strength 0.25 | 8.33→**10.93** | **F006 NO-GO** |
| CHK-020-nwn-bh | 2026-07-24 | tip内 NW_N BH=0.90 | hard20 | `tip-cv-nwn-bh-h20v2` | pooled **14.883**（基準14.869）· NW_N悪化 | **F009 NO-GO** |
| CHK-070 | 2026-07-24 | CatBoost residual GPU | hard20 · GroupKFold5 | romanrozen Private | OOF **31.80** · tip corr **0.999** | **F010 NO-GO** |
| CHK-070-full | 2026-07-24 | CatBoost residual GPU | 773 wells | full train | pooled **15.14** · tip corr≈0.999 | 参考のみ · Final2不可 |
| CHK-040-feat-train | 2026-07-24 | heel+窓 NCC + CatBoost drift | hard20 · GroupKFold | window±25ft · GPU Ver1 | OOF **45.96** · tip corr **0.999** · unconst 72.24 | **F011 NO-GO** |
| CHK-040-w40-ablate | 2026-07-24 | 同上 ±40ft（v2_fast） | hard20 | GPU Ver2 · ~10min | OOF **44.58** · tip corr **0.999** | **F011再確認** · 採択不可 |
| CHK-080 | 2026-07-24 | 着床/二峰 層別 | hard20 tip | local T4 | EGFDL 15.1 vs BUDA 13.0 · bim0 | **done** · 切断面弱 |
| CHK-081-v4 | 2026-07-24 | soft 近傍 GR·距離 | hard20 | GPU Ver5（chk071車両） | OOF **49.59** · 適用3/20 · tip corr **0.999** | **F012 NO-GO** |
| tip-filler-T2 | 2026-07-24 | tip T2 再走 | balanced 80 | allowlist Ver6 | pooled **8.330** · preds≡T2 | **再確認のみ** |
| tip-filler-h20s2 | 2026-07-24 | tip hard20 seed2 再走 | hard20 | seed2 Ver4 | pooled **14.870** · preds≡基準 | **再確認のみ** |
| CHK-100 | 2026-07-24–25 | B1 az-split ridge-sub1 | hard20 | tip-cv-az-split-h20 | hard20 **未確定** · ERROR/OOM | **blocked** |
| CHK-101 | 2026-07-24–25 | Best T2 Trust CV | T2 80井 | best-cv-t2-allowlist | 未完走 | **blocked** |

---

## 推論・提出実験

| submit_id | 日付 | Notebook / Script | 学習元 | 推論・後処理 | Public LB | 判断 |
|---|---|---|---|---|---|---|
| 55093490 | 2026-07-29 | tip-gated-lik-temp-0p08 Ver1 | tip E2E | OPS-A · LIK_TEMP=0.08 · local SHA≡SUB-14 | **6.323** | **NO-GO** · F025追認 |
| 55093492 | 2026-07-29 | tip-gated-bh-strength-0 Ver1 | tip E2E | OPS-B · BH=0 · applied=0 · local SHA≡SUB-14 | **6.274** | **NO-GO** · 効果なし |
| 55094041 | 2026-07-29 | tip-blend-sub14-sub9-090-010 Ver1 | tip E2E + SUB-9 | OPS-C · 0.90/0.10 · local RMSE差0.110 | **6.237** | **Public1運用GO** · 改善GOではない |
| 55094043 | 2026-07-29 | tip-blend-sub14-sub9-075-025 Ver1 | tip E2E + SUB-9 | OPS-D · 0.75/0.25 · local RMSE差0.276 | **6.276** | **NO-GO** · C未満 |
| 54914222 | 2026-07-22 | top-reproducible-pf… Ver2 | Contact-Gated conservative | branch conservative | **6.524** | **暫定 Best** |
| tip-smoke | 2026-07-23 | **rogii-luck-is-all-you-need-private-tip-fork** Ver1 | opencv411 tip | Notebook 紐づけ smoke | **6.569** | 再現OK · Best未満 · 作者6.478差+0.091 |
| 54935410 | 2026-07-23 | **Sunny physical Ver1** | physical+PF | Final2狙い SUB-1 | **9.150** | **F004 Final除外** |
| 54937708 | 2026-07-23 | **tip-bh-strength-off Ver1** | tip · BH=0 | SUB-2 hedge OFF | **6.599** | 枠2不採用 |
| 54937788 | 2026-07-23 | **tip-mpkg020-as-submission Ver1** | tip · mpkg gated 0.020 コピー | SUB-3 | **Scoring Error** | 無効 · copy-kernel 禁止 |
| 54958356 | 2026-07-24 | **tip-e2e-promote-mpkg010 Ver1** | tip E2E · gated_010 | SUB-4 | **6.718** | **F015** tip+0.149 |
| 54958359 | 2026-07-24 | **tip-e2e-promote-pre-bh Ver1** | tip E2E · before_BH | SUB-5 | **6.653** | **F015** tip+0.084 |
| 54958970 | 2026-07-24 | **tip-e2e-promote-mpkg020 Ver1** | tip E2E · gated_020 | SUB-6 | **6.621** | **F015** tip+0.052 |
| 54958971 | 2026-07-24 | **tip-e2e-promote-mpkg-only Ver1** | tip E2E · mpkg only | SUB-7 | **20.067** | **F015** 壊滅 |
| 54958520 | 2026-07-24 | VISUALS Ver2 | Frontier Lab | — | **6.581** | Best未満 |
| CHK-120 | 2026-07-25 | tip FINAL vs Best FINAL harvest | dual-final diagnose | max_abs **0** · SHA一致 | — | **F016 KILL** |
| CHK-130 | 2026-07-25 | heel-constrained-dtw hard20 | Sakoe-Chiba | pooled **371** | — | **F017 NO-GO** |
| CHK-143 | 2026-07-25 | low heel-corr → CF | thr 0.7–0.9 | best pooled **25.4** | — | **F018 NO-GO** |
| CHK-144 | 2026-07-25 | far-MD heel line/blend | frac 0.25–0.5 | best pooled **609** | — | **F019 NO-GO** |
| CHK-145 | 2026-07-25 | spatial density &lt;150ft | train 773 | hard20 nbr=**0%** · all=**1.7%** | — | F012 強化 |
| CHK-150-h20 | 2026-07-25 | tip_self_line far-MD | hard20 | far0.5 s0.25 | pooled **13.76**（Δ+1.11） | screen PASS |
| CHK-150-T2 | 2026-07-25 | tip_self_line graft T2 | balanced 80 | 厳格 sample 悪化 | pool 最良+0.30 だが samp+0.63 | 厳格 NO-GO |
| CHK-150-soft | 2026-07-25 | tip_self_line weak | T2 f33-s08 | far0.33 s0.08 | pool **8.261**（+0.069）· samp −0.076 | SOFT · **F020** |
| CHK-160 | 2026-07-25 | SOFT Δ × meta | T2 80 | self_dev corr **+0.45** | feasible gates | **GO→161** |
| CHK-161 | 2026-07-25 | gated SOFT f33-s08 | T2 exact | **self_dev>8** | pool **8.246**（+0.084）· samp −0.043 | **厳格 PASS** |
| CHK-151 | 2026-07-25 | tip-soft-selfline-f33s08 | tip E2E + post | Kaggle GPU Ver1 · **SUB-8** | Public **6.582**（tip+0.013） | **打ち切り** |
| CHK-162 | 2026-07-25 | tip-gated-selfline-selfdev8 | tip E2E + gate | GPU Ver1 · **SUB-9** | Public **6.484**（新Best） | **GO · Final仮枠1** |
| OPS-LB-89 | 2026-07-26 | SUB-8/9 Public 読取 | — | gated GO · SOFT NO | Final仮更新 · [`ops-lb-89`](../docs-ja/ops-lb-89-sub89-public-2026-07-26.md) |
| CHK-174 | 2026-07-25 | self_dev grid | T2 graft | t∈{6,8,10,12,15} f33-s08 | 最良 **>10** · +0.085 / samp −0.024 | **GO** |
| CHK-170 | 2026-07-25 | compound gate | T2 graft | `(>10)∧(heel&lt;0.85)` n=14 | +0.082 / samp **−0.0078** | **GO · gate選定** |
| CHK-171 | 2026-07-25 | strength retune | 選定ゲート | s∈{0.05,0.08} f33 | **s=0.05** · +0.053 / samp −0.0036 | **GO** |
| CHK-175 | 2026-07-25 | far_frac grid | 選定ゲート s05 | f∈{0.25,0.33,0.40} | f40 pool↑だが samp悪化 | **NO-GO · f33維持** |
| CHK-173 | 2026-07-25 | continuous strength | T4 screen | clip(0.004·dev+0.02) | 悪化井で strength↓せず | **NO-GO** |
| CHK-176 | 2026-07-25 | two-stage strength | T2 · k=3/5 | 悪化井 strength半減 | k5 · +0.063 / samp **+0.0005** | **GO · oracle制限** |
| CHK-177 | 2026-07-25 | hard20 diag | hard20 | portable + two-stage | tip14.87→14.76/14.74 | **診断のみ** |
| CHK-180 | 2026-07-25 | well archetype map | T2 80 · multi-cut | A/B/E… × soft variants | A +0.17 / B −0.07 / E ungated−0.08 | **GO 診断** |
| CHK-181 | 2026-07-25 | SOFT-hurt proxy | portable gate n=14 | az_nwn_affinity | prec0.5 · rec1.0 | **GO 境界** |
| CHK-182 | 2026-07-25 | exclude az proxy graft | T2 | skip 10 wells | pool +0.040 · samp +0.004 | **NO-GO** |
| CHK-183 | 2026-07-25 | A/B tip shape sep | A/B 30 + portable T2 | `tip_std_far/prox`≥0.842 | AUC **0.978** · T2 +0.072/+0.004 · =oracle k5 | **GO screen** |
| CHK-184 | — | portable+farvol exclude | tip-cv / E2E | thr固定 · Public後 | — | **pending** |
| CHK-185 | 2026-07-25 | tip candidate ceiling | T2 80 · hard20 | tip seeds / soft / BH | soft oracle **+0.155** · tip最良64/80 · oracle>6 **23井** | **GO · generator不足** |
| CHK-186 | 2026-07-25 | lik-PF seed-oracle | T2 80 · 128×500 | tip FINAL vs min-seed | FINAL **8.33** · oracle **8.13** · hit≤4.5 **46%** · hard oracle **12.9** | **mixed** · 188自動なし |
| CHK-187 | 2026-07-26 | stage/soft oracle | T2 80 · hard knobs | soft / PF dump / tip-fork | soft **+0.14** · tip64/80 · knobs gap0 · F015 | **GO · 昇格禁止** |
| CHK-202 | 2026-07-26 | tip×SP45 thin blend | hard20 · Type A | α≤0.05 · no promote | 最良 **Δpool −0.093** | **NO-GO** · F015 |
| CHK-207 | 2026-07-26 | PF knob screen | hard20 seed-oracle | init_spr/seeds/gs/PN/N | 最良 **init_spr=9** 11.94（Δ**+0.94**）· seeds256 +0.53 | **PASS** · →206 |
| CHK-206 | 2026-07-26 | tip init_spr=9 | hard20 tip-cv | literal 9 · selector-stop | ≡baseline 14.8695 | **誤物差し** · tip-cv=0.3CF+0.7phys(TVTリーク) · [`rootcause`](../docs-ja/discussion/wave20-tipcv-phys-leak-rootcause.md) |
| CHK-208 | 2026-07-26 | combo oracle | hard20 seed-oracle | init_spr9×seeds256 | **11.63** Δ**+1.25** | **PASS** · [`result`](../docs-ja/discussion/chk208-combo-oracle-result.md) |
| CHK-209 | 2026-07-26 | selector-face combo | hard20 tip-cv | 9×256 · USE_SELECTOR_FACE | **33.541** vs 211 | **NO-GO** · Δ−0.36 · [`比較`](../docs-ja/discussion/chk211-selector-baseline-result.md) |
| CHK-211 | 2026-07-26 | selector-face baseline | hard20 tip-cv | 4.5×128 · USE_SELECTOR_FACE | **33.178** | **GO·物差し** · [`result`](../docs-ja/discussion/chk211-selector-baseline-result.md) |
| CHK-210 | 2026-07-26 | tip-cv 物差し修正 | builder | TIP_CV で phys 無効を既定 | **GO** | [`ruler`](../docs-ja/discussion/chk210-tipcv-ruler.md) |
| CHK-205 | 2026-07-26 | lik_temp T=0.5 / 2.0 | hard20 tip-cv | selector-face · GPU | T0.5 **32.276**（**+0.90**）· T2 **33.696** | **PASS / NO-GO** · [`result`](../docs-ja/discussion/chk205-lik-temp-result.md) |
| CHK-205b | 2026-07-26 | lik_temp 局所 pf_scale + 209×208 | hard20 local | T∈{0.5,1,2} · 128×500 | T0.5 **+1.68** · T2 **−2.5** | [`result`](../docs-ja/discussion/chk205b-wait-screen-result.md) · tip↔oracle corr≈0 |
| CHK-212 | 2026-07-26 | Best tip + LIK_TEMP=0.5 | tip E2E · **SUB-13** | gated+T0.5 · GPU | Public **6.419** | Final保険 · ref **55001828** · [`SUBMIT`](../my-submitted-notebook/tip-gated-lik-temp-0p5/SUBMIT.md) |
| CHK-213 | 2026-07-26 | generator diversity | hard20 oracle | spr{6..15} · mix · seeds384 | **spr12=10.38（+2.50）** | **PASS** · tip面未検証 · [`result`](../docs-ja/discussion/chk213-generator-diversity-result.md) |
| CHK-214 | 2026-07-26 | init_spr=12 ± T0.5 tip-cv | hard20 selector | spr12 · T=1.0/0.5 · GPU | **33.413 / 33.428** vs 211 | **NO-GO** · [`result`](../docs-ja/discussion/chk214-spr12-tipcv-result.md) |
| CHK-216 | 2026-07-26 | hardwell 1b1eba53 | local PF autopsy | spr/gs/pn | oracle≈31 · lik rank 120/128 | **GO_CLOSE** · [`result`](../docs-ja/discussion/chk216-hardwell-1b1eba53-result.md) |
| CHK-217 | 2026-07-26 | spr fine {10..14} | hard20 oracle | ×128 | best 13=12.11 ≺ spr12 | **NO-GO** · 12固定 · [`result`](../docs-ja/discussion/chk217-spr-fine-grid-result.md) |
| CHK-203b | 2026-07-26 | upstream dump fix | T2 tip-cv GPU | learned skip | **running** t2b | harvest待ち |
| CHK-204 | 2026-07-26 | stage gap gate | T2 selector vs sp45 | portable feats | Δpool **0**（≡） | **NO-GO** · [`result`](../docs-ja/discussion/chk204-stage-gap-result.md) |
| CHK-218 | 2026-07-26 | lik_temp fine+entropy | hard20 local PF | T∈{0.3..1} · T2 | **T0.3=17.85** vs T0.5 +0.56 | **PASS** · entropy NO-GO · [`result`](../docs-ja/discussion/chk218-liktemp-fine-result.md) |
| CHK-219 | 2026-07-26 | lik_temp=0.3 tip-cv | hard20 selector | T=0.3 · GPU | **30.827** vs211 +2.35 · vsT05 +1.45 | **PASS** · [`result`](../docs-ja/discussion/chk219-lik-temp-0p3-result.md) |
| CHK-221 | 2026-07-26 | colder+topk+scale | hard20 local PF | T2 | **T0.15=17.24** · topk5=17.13 · sc2=17.21 | **PASS** · [`result`](../docs-ja/discussion/chk221-colder-topk-result.md) |
| CHK-222 | 2026-07-26 | lik_temp=0.15 tip-cv | hard20 selector | T=0.15 · GPU | **29.899** vs219 +0.93 | **PASS_best** · [`result`](../docs-ja/discussion/chk222-lik-temp-0p15-result.md) |
| CHK-223 | 2026-07-27 | lik_temp=0.10 tip-cv | hard20 | T=0.10 | **29.848** vs222 +0.05 | **NO-GO** · [`result`](../docs-ja/discussion/chk223-lik-temp-0p1-result.md) |
| CHK-224 | 2026-07-27 | T0.15+topk5 tip-cv | hard20 | topk5 | **49.526** | **NO-GO** · [`result`](../docs-ja/discussion/chk224-topk5-result.md) |
| CHK-227 | 2026-07-27 | lik_temp=0.08 tip-cv | hard20 | T=0.08 · Force | **29.841** vs222 +0.06 | **NO-GO** · [`result`](../docs-ja/discussion/chk227-lik-temp-0p08-result.md) |
| CHK-228 | 2026-07-27 | T0.15 seeds256 tip-cv | hard20 | s256 · Force | **29.872** vs222 +0.03 | **NO-GO** · [`result`](../docs-ja/discussion/chk228-seeds256-result.md) |
| CHK-229 | 2026-07-27 | best-of-temps tip-cv | hard20 | oracle blend | **29.639** vs222 +0.26 | **NO-GO** · [`result`](../docs-ja/discussion/chk229-temp-blend-result.md) |
| CHK-230 | 2026-07-27 | PF gs/pn/particles @T0.15 | hard20 local | Force | base **17.59** · 全悪化 | **NO-GO** · [`result`](../docs-ja/discussion/chk230-pf-aux-knobs-result.md) |
| CHK-231a | 2026-07-27 | tip-cv weight=0.55 | hard20 GPU | T0.15 | **33.573** vs29.899 | **NO-GO** · [`result`](../docs-ja/discussion/chk231a-gpu-w055-result.md) · **F022** |
| CHK-231c | 2026-07-27 | tip-cv pf_scale_5 | hard20 GPU | T0.15 | **29.899** ≡baseline | **NO-GO** · [`result`](../docs-ja/discussion/chk231c-gpu-var-s5-result.md) · **F022** |
| CHK-231b/d/e | 2026-07-27 | weight/variant 他 | — | GPU 未起動 | — | **cancelled** · CPU2 参考のみ |
| CHK-197 / SUB-15 | 2026-07-27 | portable twostage s05 | tip E2E Public | 診断 · 二重提出 | **6.494** / 重複 **6.564** | **NO（Best外）** · [`ops-lb-sub15`](../docs-ja/ops-lb-sub15-twostage-public-2026-07-27.md) |
| CHK-232 | 2026-07-27 | upstream diversity≠spr12 | hard20 T0.15 screen | 最良 spr8 −0.51 | oracle↑ tip↓ | **rejected** · GPU skip · [`chk232`](../docs-ja/discussion/chk232-diversity-result.md) |
| CHK-233 | 2026-07-28 | heel錨定/多峰 init | hard20 T0.15 | 最良 tight1.5 −1.60 | hit↑ tip↓ | **rejected** · GPU skip · [`chk233`](../docs-ja/discussion/chk233-heel-multimode-result.md) |
| CHK-234 | 2026-07-28 | BIN→force hold0.2 | tip-cv GPU | **30.223 (−0.32)** | **rejected** · [`234`](../docs-ja/discussion/chk234-force-global-result.md) |
| CHK-234b | 2026-07-28 | BIN4/5 hold→0.10 | tip-cv GPU | **30.426 (−0.53)** | **rejected** · [`234b`](../docs-ja/discussion/chk234b-hold010-result.md) |
| CHK-239 | 2026-07-28 | 216型 / stretch gate | hard20 | 1b1 stretch効・全体 tip−5 | **rejected** · [`chk239`](../docs-ja/discussion/chk239-obs-break-result.md) |
| CHK-235 | 2026-07-28 | lik特徴≠weight | mid-bank | 最良 −0.24 | **rejected** · GPU skip · [`chk235`](../docs-ja/discussion/chk235-lik-feat-result.md) |
| CHK-236 | 2026-07-27 | hit有誤選択 vs hit無 分割 | hard20 診断 | T4 · 186/205b | **B14:A6** · 上流厚 | **done** · [`chk236`](../docs-ja/discussion/chk236-ab-split-result.md) |
| CHK-237 | 2026-07-28 | lik→oracle校正 LOWO | mid-bank | nonleak +0.02〜0.07 · leak上限+1.66 | **rejected** · [`chk237`](../docs-ja/discussion/chk237-lik-calib-result.md) |
| CHK-238 | 2026-07-28 | 遠MD PN密度 | hard20 T0.15 | 最良 −3.23 · far微改善 | tip↓ | **rejected** · GPU skip · [`chk238`](../docs-ja/discussion/chk238-far-md-result.md) |
| CHK-240 | 2026-07-28 | 候補散らばり→井別T | mid-bank | −0.70 | **rejected** · [`chk240`](../docs-ja/discussion/chk240-well-t-spread-result.md) |
| CHK-241 | 2026-07-28 | 粗→細2段 | hard20 | oracle 8.44≪12.88 · tip −2〜3 | **rejected** · [`chk241`](../docs-ja/discussion/chk241-cascade-result.md) |
| CHK-242 | 2026-07-28 | 多ラン候補バンク結合 | hard20 | tip −1.15〜−1.33 · 2x128 oracle+0.29 | **rejected** · [`chk242`](../docs-ja/discussion/chk242-multirun-merge-result.md) |
| CHK-243 | 2026-07-28 | 難井提案予算↑ tip_std | hard20 | tip −2.32 | **rejected** · [`chk243`](../docs-ja/discussion/chk243-budget-gate-result.md) |
| CHK-244 | 2026-07-28 | 同一バンクT soft混合 | mid-bank | −0.30 | **rejected** · [`chk244`](../docs-ja/discussion/chk244-t-mix-result.md) |
| CHK-245 | 2026-07-28 | 多様性prune→soft lik | tip-cv GPU | 29.951 (−0.05) · mid-bank偽+0.32 | **rejected** · F023 · [`chk245`](../docs-ja/discussion/chk245-diversity-prune-result.md) |
| CHK-246 | 2026-07-27 | ±15ft 二峰 init（候補） | hard20 PF screen | s8@T0.15 17.59→21.39 | **−3.80** · hit0.30→0.25 | **rejected** · GPU skip · [`chk246`](../docs-ja/discussion/chk246-bimodal-init-result.md) |
| CHK-247 | 2026-07-28 | Typewell 極性反転 | hard20 | tip −20.6 · hit不変 | **rejected** · [`chk247`](../docs-ja/discussion/chk247-polarity-result.md) |
| CHK-248 | 2026-07-28 | タイからの扇状提案分散 | hard20 | tip −2.26 | **rejected** · [`chk248`](../docs-ja/discussion/chk248-fan-spread-result.md) |
| CHK-249 | 2026-07-28 | Buda/強ピーク lik 重み | mid-bank | −0.09 | **rejected** · [`chk249`](../docs-ja/discussion/chk249-buda-lik-result.md) |
| CHK-250 | 2026-07-28 | jitter GR lik ダウンウェイト | mid-bank | −0.19 | **rejected** · [`chk250`](../docs-ja/discussion/chk250-jitter-lik-result.md) |
| CHK-251 | 2026-07-28 | dip/incl PF state | mid-bank partial | s5〜58 | **rejected** · [`chk251`](../docs-ja/discussion/chk251-dip-state-result.md) |
| CHK-252 | 2026-07-28 | ESS≤10.35→heel spr1.5 | tip-cv GPU | **29.921 (−0.02)** · mid偽+0.225 | **rejected** · F023 · [`chk252`](../docs-ja/discussion/chk252-ess-heel-result.md) |
| CHK-253 | 2026-07-28 | fault jump / teleport | mid-bank | tip −0.12〜−4.4 · teleport P2 | **rejected** · [`chk253`](../docs-ja/discussion/chk253-fault-jump-result.md) |
| SUB-16/17/18 | 2026-07-28 | T0.3 / before_hedge / learned_traj | Public diag | 16=**6.385** · 17/18 F005 | [`ops-lb-sub161718`](../docs-ja/ops-lb-sub161718-night-2026-07-28.md) · **F025** |
| SUB-18 E2E | 2026-07-28 | learned_trajectory E2E promote | Public diag | **7.705**（重複 **7.768**） | 枠禁止 · F015追認 · [`ops-lb-pend`](../docs-ja/ops-lb-pend-public-2026-07-29.md) |
| SUB-19 blend | 2026-07-28 | SUB-14×13 0.85/0.15 E2E | Public diag | **6.277** `55066793` | 枠外 · Δ+0.008 |
| SUB-20 T0.10 | 2026-07-28 | tip E2E LIK_TEMP=0.10 | Public diag | **6.241** `55066862` | 表示Best · **SHA≡SUB-14** · ノイズ |
| CHK-254 | 2026-07-28 | landing window prior | mid-bank | Δ=0（不発火） | **absorbed** · [`chk254`](../docs-ja/discussion/chk254-landing-prior-result.md) |
| CHK-255 | 2026-07-27 | MD vs TST軸 照合診断 | hard20 known GR | TVT 14.50 ≪ TST 35.86 | **absorbed** | **done** · [`chk255`](../docs-ja/discussion/chk255-md-tst-result.md) |
| CHK-256 | 2026-07-28 | tip内部面 tip-cv 診断 | hard20 tip-cv T0.15 | gold≡before_hedge≡selector **30.089** | **done** · 案C天井なし · [`result`](../docs-ja/discussion/chk256-faces-result.md) |
| CHK-261 | 2026-07-28 | cascade∩tip近傍→T0.15 | hard20 local | 最良k0.5 **Δ−0.25** | **rejected** · [`result`](../docs-ja/discussion/chk261-near-clip-result.md) |
| CHK-268 | 2026-07-28 | spr12∩tip近傍→T0.15 | hard20 local | 最良k0.25 **Δ+0.024** | **rejected** · [`result`](../docs-ja/discussion/chk268-near-clip-result.md) |
| CHK-257 | 2026-07-28 | 内部面→候補選択 | tip-cv | 案C | **skipped** · 256 | Wave-22 |
| CHK-258 | 2026-07-28 | tip近傍クリップ enrichment | hard20 local | 案B/A · ≠F026 | **rejected** · k0.5 Δ−0.47 | Wave-22 · [`258`](../docs-ja/discussion/chk258-near-clip-result.md) |
| CHK-259 | 2026-07-28 | F025 hedge×温度 | hard20 local | 横断 | **rejected** · h>0悪化 | Wave-22 · [`259`](../docs-ja/discussion/chk259-hedge-temp-result.md) |
| CHK-260 | 2026-07-28 | 多run 安定/選定 | hard20 local | 横断 | **rejected** · mean Δ−1.73 | Wave-22 · [`260`](../docs-ja/discussion/chk260-multirun-result.md) |
| CHK-263 | 2026-07-28 | 最良内部面 E2E 昇格 | tip-cv E2E | 案C · ≠F005 | **skipped** · 256 | Wave-22 |
| CHK-265 | 2026-07-28 | tip_stdゲート弱後処理 | hard20 local | 案A/B · ≠F020 | **rejected** · Δ−0.015 | Wave-22 · [`265`](../docs-ja/discussion/chk265-std-gate-result.md) |
| CHK-266 | 2026-07-28 | 易井維持·難井だけA経路 | tip-cv | 案B | **skipped** · 261/268 | Wave-22 |
| CHK-267 | 2026-07-28 | A経路を後工程まで tip-cv | tip-cv | 案A セット | **skipped** · 261/268 | Wave-22 |
| CHK-269 | 2026-07-28 | 差し替え井だけ後工程sweep | tip-cv | 案A · 上流固定 | **skipped** · 267 | Wave-22 |
| CHK-270 | 2026-07-28 | 難井だけ弱い後処理 | hard20 local | 案B · ≠F020 | **rejected** · β0.05 Δ−0.10 | Wave-22 · [`270`](../docs-ja/discussion/chk270-weak-pp-result.md) |
| CHK-279 | 2026-07-29 | 天井≠tip 断絶タイプ診断 | hard20 | 186/205b/241 突合 | 断絶18 · ranking-like13 | **done·GO** · 順位付け失敗 · [`279`](../docs-ja/discussion/chk279-discontinuity-result.md) |
| CHK-271 | 2026-07-29 | ラベル無し選択ルール screen | cascade±近傍 | argmax/soft/median/… | tip超え **0** · 最良 tip_nearest Δ−0.36 | **NO-GO** · →273 · [`271`](../docs-ja/discussion/chk271-selector-screen-result.md) |
| CHK-272 | 2026-07-29 | 271ルールで tip soft 置換 | tip-cv | ≠F027 | — | **skipped** · 271全滅 |
| CHK-275 | 2026-07-29 | 単一シード選択 | tip-cv | ≠soft混ぜ | — | **skipped** · 271全滅 |
| CHK-273 | 2026-07-29 | cascade→tip PF 再初期化 | tip soft hard20 | ls_offset modes | 最良 Δ**−1.04** | **NO-GO·F028** · [`273`](../docs-ja/discussion/chk273-tip-reinit-result.md) |
| CHK-274 | 2026-07-29 | cascade バンク専用 soft(T,scale) LOO | tip soft hard20 | ≠F022/F027 | LOO Δ**−1.39** | **NO-GO·F029** · [`274`](../docs-ja/discussion/chk274-bank-lik-refit-result.md) |
| CHK-278 | 2026-07-29 | 温→冷焼なまし+段階刈り込み | tip soft hard20 | ≠F027/F029 | 最良 Δ**−1.25** | **NO-GO·F030** · [`278`](../docs-ja/discussion/chk278-anneal-select-result.md) |
| CHK-276 | 2026-07-29 | hedge 前確定／後差替 | tip soft hard20 | ≠259 | 最良 tip_soft Δ**0.00** · nearest Δ−0.36 | **NO-GO·F031** · [`276`](../docs-ja/discussion/chk276-hedge-lock-result.md) |
| CHK-277 | 2026-07-29 | シード ridge LOO ランカー | tip soft hard20 | 過学習監視 | 最良 argmax Δ**−1.16** | **NO-GO·F032** · [`277`](../docs-ja/discussion/chk277-seed-ranker-result.md) |
| CHK-281 | 2026-07-29 | spr12 同型橋渡し | tip-cv | ≠214 | — | **skipped** · 橋渡し全滅 |
| CHK-280 | 2026-07-29 | PASS 後の弱い後処理 | tip-cv | ≠F020 · 前提PASS | — | **skipped** · PASS なし |
| CHK-282 | 2026-07-29 | Final 更新判断文書 | tip-cv | OPS-FINAL2 | — | **skipped** · PASS なし |
| CHK-283 | 2026-07-29 | 現行lik逆転の項別分解 | hard20 tip128@4.5 | level/grad/corr/anchor/MD | culprits **md_late·anchor** 63.6% | **PASS** · [`283`](../docs-ja/discussion/chk283-lik-term-decomp-result.md) |
| CHK-284 | 2026-07-29 | robust multi-scale likelihood screen | existing particles · LOO | Student-t/Huber · 遠MD | RF↑ pooled**−13** · LOO≡pf | **NO-GO** · [`284`](../docs-ja/discussion/chk284-robust-lik-screen-result.md) |
| CHK-285 | 2026-07-29 | heteroscedastic + 難井ゲート | LOO · pf×late_het | texture/ent/heel | RF改善 **27%** · Δpool+0.03 | **NO-GO** · [`285`](../docs-ja/discussion/chk285-hetero-lik-screen-result.md) |
| CHK-287 | 2026-07-29 | proposal innovation診断 | hard20 packs | MD帯 bias/scale | fix=**residual-guided** | **PASS** · [`287`](../docs-ja/discussion/chk287-proposal-diag-result.md) |
| CHK-288 | 2026-07-29–30 | innovation-guided proposal | hard20 GPU-B | γ×gmax+clip · spr4.5 | 最良Δ**−23.9** | **NO-GO·F033** · [`288`](../docs-ja/discussion/chk288-guided-proposal-result.md) |
| CHK-289 | 2026-07-30 | learned conditional proposal | hard20 unseen GPU | ridge ΔTVT · α混合 | 最良Δ**−12.8** | **NO-GO·F034** · [`289`](../docs-ja/discussion/chk289-learned-proposal-result.md) |
| CHK-290 | 2026-07-30 | ESS resample + MCMC rejuvenation | hard20 GPU | resamp×mcmc格子 | 最良Δ**−0.51** | **NO-GO·F035** · [`290`](../docs-ja/discussion/chk290-ess-mcmc-result.md) |
| CHK-286 | 2026-07-29 | 観測モデル組込PF生成 | hard20 GPU-A | 284/285勝者 | — | **skipped** · 284/285 PASSなし |
| CHK-291 | 2026-07-30 | 観測×proposal 2×2統合 | hard20 GPU | A/B PASS前提 | — | **skipped** · Wave-24全滅 |
| CHK-292 | 2026-07-30 | 勝者の層別頑健性 | hard20 | 難井/方位/MD | — | **skipped** · PASSなし |
| CHK-293 | 2026-07-30 | 生成器 tip-cv | well-group GPU | 勝者凍結 | — | **skipped** · PASSなし |
| CHK-294 | 2026-07-30 | 独立seed/粒子数再現 | tip-cv GPU | 2設定 | — | **skipped** · PASSなし |
| CHK-295 | 2026-07-30 | 勝者E2E | tip-cv GPU | branch_hedgeまで | — | **skipped** · PASSなし |
| CHK-296 | 2026-07-30 | Final更新判断 | document | OPS-FINAL2 | 更新なし | **done** · 枠維持 |
| CHK-297 | 2026-07-30 | ラベル無し hard/easy ゲート | LOO · hard20∪easy45 | ridge zscore · tip_std* | recall**0.95** FPR**0.022** AUC**0.986** | **PASS** · [`297`](../docs-ja/discussion/chk297-hard-easy-gate-result.md) |
| CHK-298 | 2026-07-30 | easy tip 非回帰 harness | CI · easy45 | STRICT1e-6 / SOFT0.02 | self-test PASS | **PASS** · [`298`](../docs-ja/discussion/chk298-easy-freeze-harness-result.md) |
| CHK-299 | 2026-07-30 | 難井地図+ノブ割当 | hard20 · 19cells | MD×disc×GR×az | 型≥1仮説 | **PASS** · [`299`](../docs-ja/discussion/chk299-hardwell-map-result.md) |
| CHK-300 | 2026-07-30 | hard-only 遠MD尤度再重み | packs | late_het/late_w | Δ**−7.5** | **F036 NO-GO** |
| CHK-301 | 2026-07-30 | hard-only anchor緩和 | packs | heel_w/anch_lam | Δ≈0 | **NO-GO** |
| CHK-302 | 2026-07-30 | hard-only短長窓混合 | packs | window mix | Δ**−7.5** | **F036 NO-GO** |
| CHK-303 | 2026-07-30 | hard-onlyスパイクマスク | packs | mask | Δ**−12** | **F036 NO-GO** |
| CHK-304 | 2026-07-30 | hard-only TW局所スケール | packs | lstsq | Δ**−7.9** | **F036 NO-GO** |
| CHK-305 | 2026-07-30 | 観測勝者GPU統合 | — | upstream全滅 | — | **skipped** |
| CHK-306–309 | 2026-07-30 | PN/regime/budget/rate | hard20 GPU | tip PF regen | best Δ**0** | **F037 NO-GO** · [`306`](../docs-ja/discussion/chk306-309-dynamics-result.md) |
| CHK-310 | 2026-07-30 | 小区間独立PF接続 | hard20 GPU | seg2/3/4 | Δ**−1.74** | **F037 NO-GO** · [`310`](../docs-ja/discussion/chk310-segment-pf-result.md) |
| CHK-311–319 | 2026-07-30 | 統合〜tip-cv | — | upstream無し | — | **skipped** |
| CHK-320 | 2026-07-30 | Final判断 | document | OPS-FINAL2 | 枠維持 | **done** · [`close`](../docs-ja/discussion/wave25-lane-close-2026-07-30.md) |
| CHK-321 | 2026-07-30 | soft−oracle 平行 vs ねじれ分解 | hard20 packs | 成分比 | **twist 90%** (P2/T18) · mean_pfrac=0.287 | **GO · ねじれ優勢→C原則skip** · [`r`](work/wave26-compass-audit/chk321-report.json) |
| CHK-322 | 2026-07-30 | lik/GR vs tip-soft 方向相関 | 微小変位 FD | H1 | rf rev**70%** cos**−0.40** · all55% | **GO · H1 PASS** · [`r`](work/wave26-compass-audit/chk322-report.json) |
| CHK-323 | 2026-07-30 | soft vs FINAL 二面 | chk279+packs | ρ | soft↔FINAL **+0.074** · soft≈argmax **0.973** | **GO · 面別必須** · [`r`](work/wave26-compass-audit/chk323-report.json) |
| CHK-324 | 2026-07-30 | 質量寄せ×平均幾何 | T梯子+oracle α | 曲線 | coldT Δ+0.02 · α1 Δ**+4.36**（ラベル） | **GO診断** · 誤寄せが本丸 · [`r`](work/wave26-compass-audit/chk324-report.json) |
| CHK-325 | 2026-07-30 | cascade/mode vs tip-soft | chk279+packs | 向き | cas meanΔ**−1.77** · F028 YES | **GO · cascade再禁止強化** · [`r`](work/wave26-compass-audit/chk325-report.json) |
| CHK-326 | 2026-07-30 | MD帯別 平行/ねじれ | 層別 | 局所可否 | near5%/mid40%/far40% 平行 | **GO · 局所平行なし→332skip** · [`r`](work/wave26-compass-audit/chk326-report.json) |
| CHK-327 | 2026-07-30 | tip-soft 代理 LOO | 雲特徴 T4 screen | LOO ρ=+0.13 ≦ lik · tip_std ρ=+0.46 | **NO-GO** · [`r`](work/wave26-compass-audit/chk327-report.json) |
| CHK-328 | 2026-07-30 | tip-FINAL 代理 | LOO | FINAL ρ−0.30 · soft転用≈0 | **GO診断 · 転用不可** · [`r`](work/wave26-compass-audit/chk328-report.json) |
| CHK-329 | 2026-07-30 | soft∩FINAL代理合意 | 介入候補 | 合意 **25%** | **GO診断 · 薄い** · [`r`](work/wave26-compass-audit/chk329-report.json) |
| CHK-330 | 2026-07-30 | 単純統計代理 | tip_std/ESS | tip_std ρ=+0.46 · 学習不要 | **GO · リスク≠コンパス** · [`r`](work/wave26-compass-audit/chk330-report.json) |
| CHK-331–335 | 2026-07-30 | N固定平行移動 | — | 入口未達 | **skipped** · F038 |
| CHK-336 | 2026-07-30 | ねじれ局在マップ | MDピーク | 局在28% · タッチ不可 | **GO診断** · [`r`](work/wave26-compass-audit/chk336-report.json) |
| CHK-337 | 2026-07-30 | 移す系打ち切り | 文書 | **閉鎖 · OPS-FINAL2** | **done · F038** · [`close`](../docs-ja/discussion/wave26-compass-close-2026-07-30.md) |
| CHK-338–340 | 2026-07-30 | tip-cv·再現·Final | — | C未達 | **skipped** |
| CHK-341 | 2026-07-30 | ねじれ残差パック定義 | soft−oracle等 | 20/20 packs | **GO** · [`r`](work/wave27-twist-taxonomy/chk341-report.json) |
| CHK-342 | 2026-07-30 | ねじれファミリーカタログ | ≥6種 | 7種 · 指標固定 | **GO** · [`cat`](work/wave27-twist-taxonomy/chk342-family-catalog.json) |
| CHK-343 | 2026-07-30 | 位相説明力 | hard20 | mean0.02 · ≥0.5=**0%** | **GO診断** |
| CHK-344 | 2026-07-30 | 振幅説明力 | hard20 | mean0.08 · ≥0.5=**0%** | **GO診断** |
| CHK-345 | 2026-07-30 | 欠測/マスク説明力 | hard20 | mean0.70 · ≥0.5=**90%** | **GO診断**（観察優勢） |
| CHK-346 | 2026-07-30 | 局所ワープ追加 | vs位相 | 追加0.04 · 有意10% | **GO診断** |
| CHK-347 | 2026-07-30 | 区分構造追加 | ≠F038 | 追加0.21 · 有意65% | **GO診断** |
| CHK-348 | 2026-07-30 | soft vs FINAL | 二面 | TV0.08 · 面近い | **GO診断** |
| CHK-349 | 2026-07-30 | 混合ウェイト | 決め打ち禁止 | single16/20≈missing | **GO診断** |
| CHK-350 | 2026-07-30 | 粒子間一致 | soft平均病か | スパイク一致85% | **GO · soft固有ではない** |
| CHK-351–353 | 2026-07-30 | 位相/振幅/欠測検出 | LOO | **FAIL** | 実装禁止寄り |
| CHK-354 | 2026-07-30 | warp/piece検出 | LOO AUC0.62 | **PASS** | 候補ゲート |
| CHK-355–357 | 2026-07-30 | 天井probe | ラベル教師 | phase/amp/miss PASS | 欠測は検出FAIL |
| CHK-358 | 2026-07-30 | 候補選抜 | データ | 候補=piece/warp | missing除外 |
| CHK-360 | 2026-07-30 | 薄いラベル無しprobe | median寄せ | Δ**−1.08/−0.04** | **NO-GO** |
| CHK-359 | 2026-07-30 | 形修正打ち切り | 文書 | **閉鎖** | **done · F039** · [`close`](../docs-ja/discussion/wave27-twist-close-2026-07-30.md) |
| CHK-361–362 | 2026-07-30 | 頑健/tip-cv | — | 360未達 | **skipped** |
| CHK-363 | 2026-07-30 | H-A1 heel自己相関ラグ | T4 MD位相 | 最良Δ**0.0** | **NO-GO** |
| CHK-364 | 2026-07-30 | H-A4 PS連続拘束 | T4 | median gap0.07 · Δ≈0 | **NO-GO** |
| CHK-365 | 2026-07-30 | H-A2 整合特徴 residual LOO | T4 · ≠F007 | pearson≈0.9999 · Δ+2.55 | **NO-GO** |
| CHK-366 | 2026-07-30 | H-A3 last-anchor/NCC単独 | T4 | 最良+6.6 vs tip | **NO-GO** |
| CHK-367 | 2026-07-30 | H-B2 dZ rate prior | T4 | pooled−0.26だが15/20悪化 | **NO-GO** |
| CHK-368 | 2026-07-30 | H-B1 GR窓再重み | T4 | Δ0 | **NO-GO** |
| Wave-28 | 2026-07-30 | 提出可能直し方ハント | T4×6 | 全NO-GO | **closed · F040** · [`close`](../docs-ja/discussion/wave28-usable-fix-close-2026-07-30.md) |
| CHK-369 | 2026-07-30 | S1a PF設計+1井smoke | T3 · (tvt,lag)+Pearson | CF微超え · tip非クローン | **done** |
| CHK-370 | 2026-07-30 | S1a hard20門番 | T3 · local4well | 1/4 CF超え | **NO-GO** · 371 skip |
| CHK-372 | 2026-07-30 | S1b last-anchor Ridge smoke | T4 · tip-free | 2/5 CF · smoke PASS | **done** → 373 |
| CHK-373 | 2026-07-30 | S1b TinyTCN GroupKFold | T3 · CPU Ver2 | pooled 55.55 > CF 49.56 · 8/20 | **NO-GO** |
| CHK-380 | 2026-07-30 | soft→FINAL段マップ | T3 | destroy=soft→selector · 候補0 | **STOP_no_knob** · 381/382 skip |
| CHK-390 | 2026-07-30 | soft候補バンク仕様+1井smoke | T4 · chk284-packs | soft45.2 · sel61.1 · no submission | **GO** · [`s0`](work/wave30-soft-preserve/s0-design-memo.md) |
| CHK-391 | 2026-07-30 | Soft-Preserve ranker設計+4井LOO | T4 · Ridge τ=3 bias_soft=-2 | finite · tip非混合 · pool≈25.7 | **GO** · [`s1`](work/wave30-soft-preserve/s1-ranker-memo.md) |
| CHK-392 | 2026-07-30 | hard20 Soft-Preserve門番1回 | T3 · local-CPU packs | CF/tipcv/sample OK · pearson**0.9995** | **NO-GO** · [`gate`](work/wave30-soft-preserve/chk392-gate-report.json) |
| CHK-393 | 2026-07-30 | E2E | — | 392未達 | **skipped** |
| CHK-394 / Wave-30 | 2026-07-30 | Soft-Preserve閉鎖 | T4 | F041追記 · Active=OPS-FINAL2 | **closed** · [`close`](../docs-ja/discussion/wave30-close-2026-07-30.md) |
| CHK-395 | 2026-07-30 | 生Pearson門番監査（再学習なし） | T4 · frozen 392 | raw0.999 · err0.689 · centered0.895 · 20/20改善 | **GO_gate_reopen_candidate** · [`audit`](work/wave30-soft-preserve/chk395-gate-audit.md) · 常設: [`gate-pearson-caveat`](../docs-ja/gate-pearson-caveat.md) |
| CHK-396 | 2026-07-31 | 過去 tip-corr NO-GO カタログ | T4 · frozen preds | 4件再計算 · 全件 metric_suspect だが tip非改善 · ban維持 | **GO_catalog** · [`396`](work/wave30-soft-preserve/chk396-tip-corr-catalog.md) |
| CHK-397 | 2026-07-30 | Soft-Preserve E2E/リーク監査 | T4 · Force | soft≡final · pack=hard20のみ | **FAIL** · [`397`](work/wave30-soft-preserve/chk397-e2e-leak-audit.md) |
| CHK-401 | 2026-07-30 | tip PF pack×20 non-hard20 | T4 · Force · knobs=chk284 | 20/20 OK | **GO** · [`401`](work/wave30-soft-preserve/chk401-pack-report.json) |
| CHK-398 | 2026-07-30 | hard20→外井 transfer CV | T4 · Force | final14.81 · soft14.58 · CF15.44 · tip CSV無し | **NO-GO** · [`398`](work/wave30-soft-preserve/chk398-exhard-cv.md) |
| CHK-402 | 2026-07-30 | matched tip full-pipeline CV（401と同20井） | T4 · GPU Ver1 · fork chk256 | **ERROR** audit UnboundLocal · tip FINAL pool **10.6568** | **PARTIAL_USABLE** · [`分析`](../docs-ja/discussion/chk402-error-partial-2026-07-30.md) |
| CHK-402A | 2026-07-30 | tip FINAL vs ranker 同一20井 | T4 · local · tip=402部分 | tip **10.66** · ranker **14.73** · soft **14.51** · soft≡ranker | **NO-GO** · [`比較`](work/wave30-soft-preserve/chk402a-compare.md) |
| CHK-405 | 2026-07-30 | 398同型再発チェック | T4 · 402A | soft≡final · final>soft · tip負け | **done · F015門番どおり** |
| CHK-403 | 2026-07-31 | 402A vs 392/395/398 門番突合 | T4 | tip負け+F015で閉鎖正しい | **GO · 門番どおり棄却** · [`403`](../docs-ja/discussion/chk403-gate-reconcile-2026-07-31.md) |
| CHK-404 | 2026-07-31 | Pearson caveat 文書判定 | T4 | caveat維持 · F041維持 · 392自動PASS禁止 | **GO** · [`404`](../docs-ja/discussion/chk404-pearson-caveat-decision-2026-07-31.md) |
| CHK-406 | 2026-07-31 | label-free tip\|soft 選択 | T4 · 402同20井 | oracle 8.29 · LOO acc0.50 · ゲート悪化 | **NO-GO** · [`406`](work/wave30-soft-preserve/chk406-report.md) |
| CHK-407 | 2026-07-31 | tip内部特徴ゲート | T4 | acc0.60だが pool悪化 | **NO-GO** · [`407`](work/wave30-soft-preserve/chk407-report.md) |
| CHK-408 | 2026-07-31 | tip×soft 固定αブレンド天井 | T4 · 診断 | α0.2 pool **10.52**（tip比−0.14）· 提出禁止 | **GO_screen** · [`408`](work/wave30-soft-preserve/chk408-tip-soft-blend-screen.md) |
| CHK-409 | 2026-07-31 | 402生成段階の変化見落とし再監査 | T4 · local · 井bootstrap | selector〜before同一 · FINALは1井6958行だけ移動 · before 10.5985 vs FINAL 10.6568 | **NO-GO** · 新面なし · [`409`](work/wave30-soft-preserve/chk409-stage-change-report.md) |
| CHK-410 | 2026-07-31 | tip×新面再実験 | — | 409で独立新面なし | **cancelled** |
| CHK-399–400 | 2026-07-30 | Kaggle完走 / 診断提出 | — | 402A NO-GO | **skipped** |
| OPS-PROBE-C13 | 2026-07-31 | OPS-C×SUB-13 | E2E Ver1 | 0.90/0.10 · 実質14/9/13=0.81/0.09/0.10 | Public **6.353** · **NO-GO** · ref **55117901** |
| OPS-PROBE-1413 | 2026-07-31 | SUB-14×SUB-13 | E2E Ver1 | 0.90/0.10 | Public **6.247** · C未満・枠差替なし · ref **55117902** |
| CHK-420 / blend-compound | 2026-07-31 | tip×portable-compound | E2E tip face A · GPU | SUB-14 T0.15 × SUB-12 **0.90/0.10** · soft=0 | Public **6.284** · **NO-GO** · ref **55118585** · [`overnight`](latest/ops-lb-wave31-overnight-public-2026-07-31.md) |
| CHK-420 / blend-farvol | 2026-07-31 | tip×portable-farvol | E2E tip face A · GPU | SUB-14 T0.15 × SUB-10 **0.90/0.10** · soft=0 | Public **6.226** · 旧診断Best · ref **55118587** |
| CHK-420 / blend-sub13-080 | 2026-07-31 | tip×SUB-13 T0.5 | E2E tip face A · GPU | SUB-14 T0.15 × SUB-13 **0.80/0.20** · soft=0 | Public **6.247** · ≡14×13 · 枠外 · ref **55122006** |
| CHK-420 / farvol-α-grid | 2026-08-01 | tip×farvol α∈{0.05,0.12,0.15,0.20} | E2E · Public診断 | tip-cvはα0.15推し | **0.05=6.190 Best · 0.20=6.197 · 0.12/0.15 NO-GO** · [`LB`](latest/ops-lb-wave31-farvol-alpha-public-2026-08-01.md) · 追加α禁止 |
| CHK-421 | 2026-08-01 | farvol 枠2候補化 | T3 · Public確定 | SHA≠ · soft=0 | **GO** · 枠2第1=55148128 · 第2=55148294 · 差替はユーザー |
| CHK-429 / soft-distill-smoke | 2026-07-31 | Soft教師蒸留 GPU smoke | T3 · numpy/GPU | baseline · infer soft禁止 | **done** · L1 PASS · [`429`](work/wave31-soft-distill/out-smoke-v6/chk429-smoke-report.json) |
| CHK-430 / soft-distill-train | 2026-07-31 | Soft絶対TVT 本学習 | T3 · numpy | Trust proxy 3514 ≫ CF | **NO-GO** · [`430`](work/wave31-soft-distill/out-train-v3/chk430-report.json) |
| CHK-430b / tip-resid | 2026-07-31 | tip_linear残差+clip · Optuna | T3 Force · Trust CV | Optuna best 42.52 · caveat OK · long TIP_CLONE | **HOLD** · [`430b`](work/wave31-soft-distill/out-430b-long-cpu/chk430b-long-report.json) |
| CHK-434 / neural-optuna | 2026-07-31 | P1-shift Optuna最良 | T3 · Trust CV | beats tip proxy · raw/err Pearson≈1.0 | **TIP_CLONE · HOLD** · [`434-best`](work/wave31-neural-proposal/out-434-best/chk434-optuna-best-report.json) |
| CHK-437 / post-unlock-r1 | 2026-07-31 | post崩壊無効化 E2E | T3 · tip face · T0.15 | R1 unlock · hedge identity 候補 | Public **6.250** · **NO-GO** · submit **55118915** · unlock未発火+ノイズ |
| CHK-416 / alt-gen | 2026-07-31 | hierarchical SMC stub hard20 | T3 | CF超え · tip-clone | **rejected** · 417–418 skip |
| CHK-442 / two-stage | 2026-07-31 | tip→GPU残差 hard20 | T3 | Trust 23.21 > tip 22.94 | **rejected** · 443 skip |
| CHK-446 / tip-rewrite | 2026-07-31 | tip全面再実装 hard20 | T3 | tip-clone · Trust≡tip | **rejected** · 447 skip |
| CHK-448 | 2026-08-01 | 本番 tip soft 上 selector tip-cv | T3 · hard20 packs | new **27.431** · tipCSV **29.899** · leg **30.025** · soft **17.236** | **NO-GO** · sample `57f05c51` · [`448`](work/wave31-selector-replace/out-448-v1/chk448-report.md) |
| CHK-450 | 2026-08-01 | 448失敗分解→ゲート固定 | T4 · CPU | peak_and_sep ess≤1.2∧mode≥3 | **GO** · [`450`](work/wave31-selector-replace/out-450-decomp/chk450-report.md) |
| CHK-451 | 2026-08-01 | 条件付き selector tip-cv | T3 · packs | gated **23.760** < tip **29.899** | **GO** · [`451`](work/wave31-selector-replace/out-451-v1/chk451-report.md) |
| OPS-E2E-451/456 | 2026-08-01 | tip E2E GPU Ver1 | T3 · Private | FINAL≡SUB-14 · graft生存·overlap全置換が崩壊点 | **NO-GO Final** · 診断訂正 [`457`](work/wave31-selector-replace/out-457-v1/chk457-collapse-diagnosis.md) |
| CHK-457 | 2026-08-01 | overlap preserve α=0.50 + 451 | T3 · GPU Ver1 | self_v≠tip · before_hedge≡tip · FINAL≡SUB-14 | **PARTIAL/NO-GO** · [`harvest`](work/wave31-selector-replace/out-457-e2e/chk457-e2e-harvest.md) |
| CHK-458 | 2026-08-01–02 | gold=self_verified 固定 + 457 | T3 · GPU Ver1 | E2E mid残存GO · Public **7.781/7.760** | **Public NO-GO · F042** · [`458-LB`](latest/ops-lb-chk458-public-2026-08-02.md) · [`harvest`](work/wave31-selector-replace/out-458-e2e/chk458-e2e-harvest.md) |
| CHK-459 | 2026-08-01 | 後段崩壊中間面棚卸し | T4 | SL/α/SP45w 本命 · learned=型B | **GO_design** · [`459`](work/wave31-selector-replace/out-459-v1/chk459-post-collapse-inventory.md) |
| CHK-460 | 2026-08-01 | selfline OFF on 458 | T3 · GPU Ver1 | FINAL≡hedge · ≠SUB-14 | **GO** · [`harvest`](work/wave31-selector-replace/out-460-e2e/chk460-e2e-harvest.md) |
| CHK-461 | 2026-08-01 | overlap α=0.75 on 460 | T3 · GPU Ver1 | before_ov rmse 0.77≪460 | **GO** · [`harvest`](work/wave31-selector-replace/out-461-e2e/chk461-e2e-harvest.md) |
| CHK-462 | 2026-08-01 | SP45 w screen | T4 | w↓=learned寄り | **GO_screen · E2E DEFER** · [`462`](work/wave31-selector-replace/out-462-v1/chk462-sp45-weight-screen.md) |
| CHK-449 | 2026-08-01 | tip×451 α0.05/0.10 | T2 · tip-cv | α0.10 **29.032**（Δ−0.87） | **GO** · E単体の方が強い · [`449`](work/wave31-nonssoft-blend/out-449-v1/chk449-report.md) |
| CHK-452 | 2026-08-01 | tip×456 α0.05/0.10 | T2 · tip-cv CPU | α0.10 **28.906**（Δtip −0.99 · vs449 −0.13） | **GO** · 提出保留 · [`452`](work/wave31-nonssoft-blend/out-452-v1/chk452-report.md) |
| cascade-SSOT | 2026-08-01 | 親ごとデット · S0′先頭 · 不足分のみ | T4 · design | P-456=466–473 · P-461不足=474–476 | **GO_design** · [`cascade`](work/wave31-selector-replace/pipeline-cascade-retest.md) |
| CHK-466 | 2026-08-02 | S0′: 456 E2E mid残存 | T3 · 既存E2E | w0.60≠tip · FINAL≡tip | **GO** · [`466`](work/wave31-selector-replace/out-466-v1/chk466-s0prime-harvest.md) |
| CHK-467 | 2026-08-02 | S3: w ①0.60②0.55③0.50 | T4 · local | 採用 w0.60 · w↓ DEFER | **GO_screen** · [`467`](work/wave31-selector-replace/out-467-v1/chk467-w-screen.md) |
| CHK-468 | 2026-08-02 | S4: α0.75 on P-456 (+self_v+SL off) | T3 · GPU Ver1 | before_hedge≠tip · FINAL≠SUB-14 | **GO · 提出禁止** · [`468`](work/wave31-selector-replace/out-468-e2e/chk468-e2e-harvest.md) |
| CHK-469 | 2026-08-02 | S5: gold self_v（468同梱） | T3 · GPU | ≡468 | **GO**（同梱） |
| CHK-470 | 2026-08-02 | S8: SL OFF（468同梱） | T3 · GPU | FINAL≡hedge | **GO**（同梱） |
| CHK-471 | 2026-08-02 | S4×S8 2×2 | T3 · HOLD | 472優先 | **HOLD** |
| CHK-472 | 2026-08-02 | S9: Trust tip-cv P-456/468 | T3 · GPU Ver2 | Ver1 mpkg ERROR · Ver2再走 | **in-progress** · `tip-cv-chk472-456-h20` |
| CHK-473 | 2026-08-02 | B0: tip×461 tip-cv α0.05/0.10 | T2 · Trust | α0.10 **29.772**（Δ−0.13） | **GO_small · 提出保留** · [`473`](work/wave31-nonssoft-blend/out-473-v1/chk473-report.md) |
| CHK-474 | 2026-08-01 | P-461: S4×S8 不足のみ | T3 · pending | 済工程再実行禁止 | **pending** |
| CHK-475 | 2026-08-02 | P-461: S9 Trust tip-cv hard20 | T3 · GPU | **28.920**（Δ−0.98）· 提出禁止 | **GO_partial** · [`475`](work/wave31-selector-replace/out-475-tipcv-err/chk475-harvest.md) |
| CHK-477 | 2026-08-02 | farvol vs 468/461 幾何 | T4 · local | farvol≈tip · 468遠い · 枠2分離 | **GO_screen** · [`477`](work/wave31-nonssoft-blend/out-477-v1/chk477-report.md) |
| CHK-473b | 2026-08-02 | tip×461 Trust α0.05–0.30 | T2 · local | α0.30 **29.537** · sample3弱い | **GO_small · 提出保留** · [`473b`](work/wave31-nonssoft-blend/out-473-v1/chk473b-report.md) |
| CHK-478 | 2026-08-02 | 475井内訳 | T4 · local | +11/−5井 · SE_S改善大 | **GO_screen** · [`478`](work/wave31-selector-replace/out-475-tipcv-err/chk478-report.md) |
| CHK-479 | 2026-08-02 | 井ゲート tip×461 | T2 · local | oracle29.353 · lf29.599 | **GO_screen** · [`479`](work/wave31-nonssoft-blend/out-479-v1/chk479-report.md) |
| CHK-480 | 2026-08-02 | test lf井ゲート tip×468 | T2 · local | tip距離0.491 | **GO_screen** · [`480`](work/wave31-nonssoft-blend/out-480-v1/chk480-report.md) |
| CHK-481 | 2026-08-02 | soft\|Δ\|比例ブレンド | T2 · local | 0.30/0.5→29.586 · tip距0.589 | **GO_screen** · [`481`](work/wave31-nonssoft-blend/out-481-v1/chk481-report.md) |
| CHK-482 | 2026-08-02 | SE_Sブースト薄ブレンド | T2 · local | se0.50+oth0.10 **29.301** | **GO_screen · 提出HOLD** · [`482`](work/wave31-nonssoft-blend/out-482-v1/chk482-report.md) |
| CHK-483 | 2026-08-02 | 472着弾後再ブレンド | T2 · Trust | se0.60 Trust **29.190** | Trust-best · **Publicで485反証** |
| CHK-485 | 2026-08-03 | tip×468 SE Public診断 | T2 · submit | se040 **6.265**≈tip · se060 **6.304** | **done** · se060 NO-GO · [`485-LB`](latest/ops-lb-chk485-public-2026-08-03.md) |
| CHK-514 | 2026-08-03 | tip×468 H-D gate E2E | T3 · submit | Public **6.335** | **NO-GO** · [`514-LB`](latest/ops-lb-chk514-public-2026-08-03.md) |
| CHK-515 | 2026-08-03 | tip×468 row gate E2E | T3 · submit | Public **6.249**≈tip | **done** · 枠外 · 同上 |
| CHK-476 | 2026-08-01 | P-461: B0本番（449版） | T2 · pending | 473重複ならskip | **pending** |
| CHK-453 | 2026-08-01 | 残差蒸留 設計メモ | T4 | soft−tip · 推論soft禁止 | **GO_design** · [`453`](work/wave31-soft-distill/chk453-residual-distill-design.md) |
| CHK-454 | 2026-08-01 | 残差蒸留 hard20 LOO Ridge | T3 · CPU | 30.07 > tip · tip-clone | **NO-GO** · [`454`](work/wave31-soft-distill/out-454-v1/chk454-report.md) |
| CHK-455 | 2026-08-01 | anti-clone提案 設計メモ | T4 | ≠F033–F035 | **GO_design** · [`455`](work/wave31-neural-proposal/chk455-anticlone-proposal-design.md) |
| CHK-456 | 2026-08-01 | anti-clone push + 451ゲート | T3 · CPU | gated **23.450** < tip · 非clone | **GO** · [`456`](work/wave31-neural-proposal/out-456-v1/chk456-report.md) |
| CHK-490 | 2026-08-02 | multi-amp keep-original push | T3 · CPU | gated **23.355** · ≤21.5未達 | **GO_weak** · [`490`](work/wave31-neural-proposal/out-490-v1/chk490-report.md) |
| CHK-490b | 2026-08-02 | topk5_soft + 451 gate | T3 · CPU | gated **20.437** ≤21.5 · 非clone | **GO** · [`490b`](work/wave31-neural-proposal/out-490-v2/chk490-v2-report.md) |
| CHK-491 | 2026-08-03 | P-490b E2E S0′ | T3 · GPU | w0.60≠tip · FINAL≡tip | **GO** · [`491`](work/wave31-neural-proposal/out-491-e2e/chk491-s0prime-harvest.md) |
| CHK-493 | 2026-08-03 | topk×TEMP grid | T4 · CPU | best≡490b | **NO-GO** · [`493`](work/wave31-neural-proposal/out-493-v1/chk493-report.md) |
| CHK-495 | 2026-08-03 | ess_thr 1.0 + topk5 | T3 · CPU | gated **17.136** · sample OK | **GO pack** · [`495`](work/wave31-neural-proposal/out-495-v1/chk495-report.md) |
| CHK-500 | 2026-08-03 | win-parts + policy screen | T4 · local | hard20 mid 20/20 · best deploy all_mid **17.14** / p297 **18.11** | **GO** · [`rank`](work/wave31-neural-proposal/out-500-winparts/chk500-ranked-promising.md) |
| CHK-501 | 2026-08-03 | tip×472 win-parts tip-cv proxy | T4 · local | `lf_absd_ge_1` **28.920** ≈ all_mid · oracle行 **28.013** | **GO** · [`501`](work/wave31-neural-proposal/out-501-tipcv-winparts/chk501-report.md) |
| CHK-501b | 2026-08-03 | 491/494 stage collapse map | T4 · local | FINAL≡tip · before_* Δrmse≈0.97 | **GO** · [`501b`](work/wave31-neural-proposal/out-501-tipcv-winparts/chk501b-e2e-collapse.md) |
| CHK-502 | 2026-08-03 | 475≡472 + alt row gates | T4 · local | best `signed_pos∨absd2` **28.901** · signed_pos **28.908** | **GO** · [`502`](work/wave31-neural-proposal/out-502-alt-rowgates/chk502-report.md) |
| CHK-503 | 2026-08-03 | 491×signed_pos tip距離 | T4 · local | before_* raw0.97 · ∨absd2→0.91 · signed→0.28 · FINAL無効果 | **GO_diag** · [`503`](work/wave31-neural-proposal/out-503-signed-on-491/chk503-report.md) |
| CHK-505 | 2026-08-03 | 誤解NO-GO掘り返し | T4 · local | **468/461 親復活** · 483 Trust順 · 458全面は死のまま | **GO** · [`505`](work/wave31-neural-proposal/out-505-revival-audit/chk505-misread-revival-audit.md) |
| CHK-506 | 2026-08-03 | 復活実体化 | T4 · local | gated FINAL CSV · Trust再順位 · 504 NB planned | **GO** · [`506`](work/wave31-neural-proposal/out-506-revival/chk506-report.md) |
| CHK-517 | 2026-08-03 | 井スライス + H-G/H-B Trust proxy | T4 · local | HD **28.283** 維持 · 更新0 · win5/lose2 | **HOLD** · [`517`](work/wave31-neural-proposal/out-517-wellslice-hg/chk517-report.md) |
| CHK-518 | 2026-08-03 | 504 train mid Trust 採点 | T4 · local | before_hedge≡mid507 · HD同値 | **EQUIV_507** · [`518`](work/wave31-neural-proposal/out-518-504face-trust/chk518-report.md) |
| CHK-519–523 | 2026-08-03 | S1/S2 診断 T4 | T4 · local | learned tipdist大 · SP45直交 · pack伝播弱 | **GO_screen** · [`s1s2`](work/wave31-neural-proposal/out-s1s2-t4-20260803/report.md) |
| CHK-524/525/537 | 2026-08-03 | SP45/learned ゲート Trust | T4 · local | SP45≡468 · learned欠 | **NOGO/BLOCKED** · 同上 |
| CHK-571 | 2026-08-03 | Pack495 Trust tip-cv | T3 · harvest | Trust **26.761** ≪ tip 29.899 | **GO** · [`571`](work/wave31-neural-proposal/out-571-492b-trust/tipcv-trust-report.md) |
| CHK-578 | 2026-08-03 | tip⊕row/HD on P-495 | T4 · local | row **26.768** · HD **27.577** ≻ HD468 | **GO** · row優先 · [`578`](work/wave31-neural-proposal/out-578-p495-hd-trust/report.md) |
| CHK-579 | 2026-08-04 | tip⊕row P-495 E2E Public | T3 · GPU | Public **6.277** · tip+0.008 · Trust 26.768 · tipdist 0.907 | **完了 · 枠2NO-GO** · ref 55206184 · 再提出禁止 · [`ops-lb`](latest/ops-lb-chk579-public-2026-08-04.md) |
| CHK-533 | 2026-08-03 | learned TRAIN dump tip-cv | T3 · GPU | n=107478 · tipdist≈22.96 | **GO** · [`533`](work/wave31-neural-proposal/out-533-learned-dump-harvest/) |
| CHK-541 | 2026-08-03 | tip⊕agree∧row P-495 E2E | T3 · GPU · submit | Public **6.256** · tip−0.013 · tipdist **0.278** · Trust **26.655** · ref **55221459** | **Public_GO_noise** · 枠2NO · 再提出禁止 · [`ops`](latest/ops-lb-chk541-558b-public-2026-08-04.md) · [`541`](work/wave31-neural-proposal/out-541-e2e-analysis/report.md) |
| CHK-558b | 2026-08-03 | tip⊕agree-only P-495 E2E | T3 · GPU · submit | Public **6.238** · tip−0.031 · tipdist **0.382** · Trust **26.629** · ref **55221471** | **Public_GO_thin** · 枠2NO（≪farvol） · 再提出禁止 · 同上 · [`558b`](work/wave31-neural-proposal/out-558b-e2e-analysis/report.md) |
| CHK-FINAL-T2 all773 | 2026-08-05 | full 773 Trust A/B/C + **工程×井戸グループ** | T4 · local · 提出禁止 | A tip **10.8388**/hard **26.829** · B≡C · **hard SSE≈20% · top100 SSE≈62%** · mid **win25/hurt21/タイ94%** · 非hard tip mean **8.0** · tip⊕ **NOGO** | **GO_baseline + GO_group_insight** · [cv](latest/chk-final-t2-all773-cv-2026-08-05.md) · [stage-group](latest/all773-stage-well-group-2026-08-05.md) · [run](work/colab-final-t2/runs/20260804-115307/) |
| CHK-813 | 2026-08-05 | dual SSE top50/100 WATCH | T4 ops | all773 top100 SSE≈62% → pool希釈防衛 | **ops NEW** · [handoff §4b](l-cv-hypothesis-handoff-2026-08-05.md) |
| CHK-814 | 2026-08-05 | non-hard Q4e 半 hard weight | T3 map | tip mean≈15.6 帯を hard∪ | **map design** · after 804 |
| CHK-815 | 2026-08-05 | hard tip-stick unlock dual | T4 ops | hard resid/\|L−mid\| 移動診断 | **ops NEW** · dual 必須 |
| CHK-816 | 2026-08-05 | Q1e bulk protect weight≤1 | T3 map | 易井 mean≈3.3 過学習防衛 | **map** · with 804/789 |
| CHK-FINAL-T2 | 2026-08-04 | T2 80井 再dump + ローカル採点（分析用） | T2 · Colab | winner **T_agree_only_495** pooled **12.344** · hard_mean **18.642** · tip 17.030 · row/agree∧row/579 **12.395** · prior 12.279 | **GO_t2** · 提出禁止 · [`041247`](work/colab-final-t2/runs/20260804-041247/t2-catalog-report.md) · pointer [`CURRENT-T2-FACES`](work/colab-final-t2/CURRENT-T2-FACES.md) |
| CHK-FINAL-T2 | 2026-08-03 | Final候補カタログ同一物差し（T2≈80井） | T2 · Colab | winner **T_agree_only_495** pooled **12.279** · hard_mean **18.521** · tip 17.030 · 579/541/row **12.331**タイ · mid468 skip · agree frac1.0≡Pack | **GO_t2** · 提出禁止 · [`t2-catalog`](work/colab-final-t2/t2-catalog-report.md) · run `20260803-114917` |
| T2-stage-well | 2026-08-04 | T2工程×井分解（S0 tip / S1 learned / S9 mid·gates） | T2 · local | mid win**77**/hurt**3** · pooled tip17.03→mid12.28 · HD13.89 · S2–S6未dump | **done** · [`t2-stage`](latest/t2-stage-well-map-2026-08-04.md) |
| CHK-FINAL-T2 all773 | 2026-08-03 | T2勝者 agree-only を全773確認 | T4 · Colab | → **2026-08-05 COMPLETE** · 上行列へ移管 | **superseded** · 旧 run `20260803-162733` 停止 / 新 `20260804-115307` |
| CHK-621 | 2026-08-04 | soft_diag T2 80井 dump（PF scale5 temp0.15） | T3 · Kaggle CPU | rows **397333** · wells **80** · packs ok | **GO** · [`t2-missing-cv`](work/colab-final-t2/out-t2-missing-cv-kaggle/report.md) · kernel `t2-missing-cv-cpu` v1 |
| CHK-620 | 2026-08-04 | tip⊕soft_diag agree on T2 | T3 · Kaggle CPU | pooled **12.907** · Δvs mid **−0.628** · hard20 mean **13.78**≪18.52 · help24/hurt56 | **NOGO_t2** · hard20だけだと改善誤読 · Soft FINAL禁止 · 同上 |
| CHK-644 | 2026-08-04 | 640 tip3 + 641 α0.3(L−m) | T3 · Kaggle CPU | pooled **10.185** · Δvs 641 **+0.125** · hard20 **14.86** | **GO_small** · tipdist↑注意 · 同上 |
| CHK-622/623 | 2026-08-04 | soft_diag ゲート絞り | — | 620 NOGOで打ち切り | **rejected** |
| CHK-642 | 2026-08-04 | tip\|mid well-oracle 天井 | T4 · local T2 | oracle **12.217** · Δ vs mid **+0.062** ≪0.15 · **切替STOP** | **done_stop** · [`640-642`](work/colab-final-t2/out-640-642-climb/report.md) |
| CHK-640 | 2026-08-04 | 固定3井 tip mid-hurt | T3 · local T2 | pooled **12.217** · sample help3/hurt0 · ≡oracle | **GO_small** · 同上 |
| CHK-641 | 2026-08-04 | mid+α0.30 L resid E2E | T3 · GPU · submit | T2 **10.309** · tipdist **1.743** · Public **6.472** · tip+0.203 | **Public_NOGO** · Trust only · 再提出禁止 · [`ops-641`](latest/ops-lb-chk641-public-2026-08-04.md) |
| CHK-645 | 2026-08-04 | T2 H-D救済/frac減設計廃止 | T4 policy | Explicit Stop 確定 · 追加実験0 | **done_stop** |
| CHK-640–645 | 2026-08-04 | 工程分解後バッチ | T3/T4 | 642/645 STOP · 640小 · 641 GO | **batch done** · [`t2-stage-climb`](t2-climb-stage-hypotheses.md) |
| CHK-650–657 | 2026-08-04 | **T2×地質** match層別 · lateral self-GR · known-TVT warp · dip prior · residual層別 | T3/T4 | **657 GO_sep** · **650 NOGO** · **655 NOGO_layer** · 651/652次 | **geo partial** · [`657`](work/colab-final-t2/out-657-typewell-match/report.md) · [`650`](work/colab-final-t2/out-650-655-match-layer/report.md) |
| CHK-665 | 2026-08-04 | tip+α(mid−tip) ゲート格子 | T3 | α1=mid注入 · 部分α無益 | **GO_confirm_a1** · [`665`](work/colab-final-t2/out-665-tip-mid-alpha/report.md) |
| CHK-660–665 | 2026-08-04 | **合法残差** tip土台·clip·薄α·cascade | T3 · T2 + GPU E2E | **660** tipdist **1.923** · Public **6.239** · tip−0.030 · 枠2NO · ref **55248920** | **Public_GO_noise · 枠2NO** · 再提出禁止 · [`ops`](latest/ops-lb-chk660-666-public-2026-08-05.md) · [`660-e2e`](work/wave31-neural-proposal/out-660-e2e-harvest/report.md) |
| CHK-676 | 2026-08-04 | mid 更新後 residual α 再格子 | T3 | ≡ **702** · pooled改善も sample3 割れ | **NOGO_sample** · [697](work/colab-final-t2/out-697-blend-w050-local/report.md) |
| CHK-677 | 2026-08-04 | 643 主工程に改修スコープ固定 | T3 | scope=**S3 blend weight** · S5–S8 触らない | **GO_lock** · [ladder](work/colab-final-t2/out-643-ladder-v2-local/report.md) |
| CHK-678–680 | 2026-08-04 | flip監査 · residual Public禁止 · tip/farvol固定 | T4 | applied | **applied** · 同上 |
| CHK-630–636 | 2026-08-04 | **T2→Public** tip近い薄い差分 · 541+558b着弾 | T4/T2 | 579=6.277 · **541=6.256 · 558b=6.238** · 枠2 farvol | **630 Public_GO_noise** · 枠2NO · [`ops-541-558b`](latest/ops-lb-chk541-558b-public-2026-08-04.md) |
| CHK-592–599 | 2026-08-03 | **傾向仮説** Trust/Public分離 · Final2規律 | T4→T3 | 未実施 · フル表 | **pending** · [`final-push-trend-hypotheses`](final-push-trend-hypotheses.md) |
| CHK-603 | 2026-08-03 | softW/massBal ゲート+soft注入 | T3 · local | Trust **19.55** help18/hurt0 | **GO_screen** · [`603-607`](work/wave31-neural-proposal/out-603-607-bath2h/report.md) |
| CHK-607 | 2026-08-03 | Soft signゲート · mid vs soft注入 | T3 · local | mid注入NOGO · soft注入19.50 | **GO_screen**（注入面=Softが本体）· 同上 |
| CHK-618b | 2026-08-03 | tip⊕soft_diag agree（pack） | T3 · local | Trust **19.54** · help18/hurt0 · Soft FINAL17.24禁止 | **GO_screen** · [`618b`](work/wave31-neural-proposal/out-618b-soft-diag-inject/report.md) |
| CHK-618c | 2026-08-04 | tip⊕soft_diag agree E2E | T3 · GPU · submit | Public **6.231** · tip−0.038 · tipdist **11.933** · Soft FINAL False · ref **55222561** | **Public_GO_risky** · 枠2NO · 再提出禁止 · [`ops-618c`](latest/ops-lb-chk618c-public-2026-08-04.md) · [`618c`](work/wave31-neural-proposal/out-618c-e2e-analysis/report.md) |
| CHK-604 | 2026-08-03 | ESS/softAbs→ゲート+soft注入 | T3 · local | Trust **21.37** help17/hurt1 | **GO_screen** · [`604-606`](work/wave31-neural-proposal/out-604-606-bath2h/report.md) |
| CHK-605 | 2026-08-03 | soft-mid合意でsoft注入 | T3 · local | Trust **19.49** help18/hurt0 | **GO_screen** · 同上 |
| CHK-606 | 2026-08-03 | absMid hard∩soft注入 | T3 · local | Trust **21.62** help16/hurt2 | **GO_screen** · 同上 |
| CHK-611/616/617 | 2026-08-03 | 安定/Agree∧Stable/HD-BL | T3 · local | mid注入系はNOGO · soft系はhurt混在 | **NOGO** · [`bath2h`](work/wave31-neural-proposal/out-bath2h-cpu-20260803/report.md) |
| CHK-612 | 2026-08-03 | tip×partner α0.05/0.10 | T2 · local | 579多様性最大 · ops_cほぼtip | **GO_screen** · [`612`](work/wave31-neural-proposal/out-612-601-bath2h/report.md) |
| CHK-615 | 2026-08-04 | 579着弾分岐適用 | T4 | Δ=+0.008 ≈tip · farvol固定 · row連打STOP | **applied** · [`615`](work/wave31-neural-proposal/out-615-branch-table/chk615-579-branch.md) |
| CHK-610 | 2026-08-03 | 逆井: HD tip固定+非HD薄注入 | T3 · local | Trust **29.13**（agree+2.5）· HDがTrust寄与本体 | **NOGO** · [`610-613`](work/wave31-neural-proposal/out-610-613-reverse-safe/report.md) |
| CHK-613 | 2026-08-03 | 515安全 frac≤0.15 on row/agree | T3 · local | 追加cap Trust28.5+ · agree_only TEST frac**0.127**既達 | **GO_confirm=558b** · 同上 |
| CHK-600 | 2026-08-03 | Soft残差→ゲート特徴（mid注入） | T3 · local | 最良26.95 · Soft FINAL diag **24.62**（F041禁止） | **NOGO** · [`600-602`](work/wave31-neural-proposal/out-600-602-soft-peaky/report.md) |
| CHK-602 | 2026-08-03 | peaky ESS≈1 tip固定 | T3 · local | Trust27.53 · peaky井悪化 | **NOGO** · 同上 |
| CHK-592 | 2026-08-03 | agree∧\|L−tip\|≥3 | T3 · local | Trust26.621だが hurt12/help6 · ≡591 | **NOGO** · [`592`](work/wave31-neural-proposal/out-592-agree-micro/report.md) |
| CHK-600–607 | 2026-08-03 | **S0残** Soft/温度/beam→ゲートのみ | T4/T3 | 600/602 NOGO · 604+後回し | **partial** · [`s0-residual`](s0-residual-hypotheses.md) |
| S1S2-pending | 2026-08-03 | backlog 529–570 pending digest | T4 · local | 20件 · GO少数 · 多NOGO | **done** · [`digest`](work/wave31-neural-proposal/out-s1s2-pending-digest-20260803/report.md) |
| CHK-558 | 2026-08-03 | agree-only / same_sign mid495 | T4 · local | Trust **26.629** | **GO_screen** · [`558`](work/wave31-neural-proposal/out-558-555-pack-absd/report.md) |
| CHK-544 | 2026-08-03 | anti-promote validator | T4 · local | 541/579 PASS | **GO** · [`544`](work/wave31-neural-proposal/out-544-anti-promote/report.md) |
| CHK-524/528 | 2026-08-03 | learned gates mid468 | T4 · local | agree∧row **28.062** | **GO_screen** · [`524-536`](work/wave31-neural-proposal/out-524-536-learned-trust/report.md) |
| CHK-572 | 2026-08-03 | P-495 S0′ tipdist | T4 · local | mid残 · FINAL≡tip | **GO** · [`572`](work/wave31-neural-proposal/out-572-495-s0prime/report.md) |
| CHK-495 E2E | 2026-08-03 | ess1.0 mid面 | T3 · GPU | Ver1 **COMPLETE** · 579入力 | **done** · [harvest](work/wave31-neural-proposal/out-495-e2e-harvest/) |
| CHK-514 / 584 | 2026-08-03 | H-D Public 診断 | T4 · LB | Public **6.335** | **NO-GO Final** · [`514-LB`](latest/ops-lb-chk514-public-2026-08-03.md) |
| CHK-515 / 584 | 2026-08-03 | row Public 診断 | T4 · LB | Public **6.249**≈tip | **枠外** · 同上 |
| CHK-504 / 581 | 2026-08-03 | tip⊕H-D tip-cv 親468 | T3 · GPU | Ver3 UnboundLocalError · Ver4 pushed · 局所 HD≡28.283 | **running** · [run-log](../my-notebook/tip-cv-chk504-468-gated-h20/run-log.md) |
| CHK-492b | 2026-08-03 | tip-cv ess1.0 STOP_AFTER_SELECTOR | T3 · GPU | COMPLETE · =571入力 | **done** · [run-log](../my-notebook/tip-cv-chk492b-ess1p0-h20/run-log.md) |
| CHK-492 | 2026-08-03 | tip-cv ess1.2 allowlist fix | T3 · GPU | 枠待ち自動 push | **queued** · [`note`](work/wave31-neural-proposal/out-492-tipcv/chk492-error-note.md) |
| CHK-496 | 2026-08-03 | 297 dual E2E | T3 · GPU | Ver4 **RUNNING** | **running** · 提出禁止 |
| CHK-212 / SUB-13 | 2026-07-27 | Best tip + LIK_TEMP=0.5 | tip E2E | gated+T0.5 | Public **6.419** | Final保険 · ref **55001828** |
| CHK-220b / SUB-14 | 2026-07-27 | Best tip + LIK_TEMP=0.15 | tip E2E | gated+T0.15 | Public **6.269** | **実質 Best / 枠1** · ref **55006677** · [`ops-lb`](../docs-ja/ops-lb-sub1314-public-2026-07-27.md) |
| CHK-184 | 2026-07-26 | portable+farvol SUB-10 | tip E2E | f33-s05 · 可視 apply0 | Public **6.541** | **NO · 枠外** |
| CHK-191 | 2026-07-26 | gated>8 s05 SUB-11 | tip E2E | Best同ゲート軟化 | Public **6.530** | **NO · s08維持** |
| CHK-178 | 2026-07-26 | portable複合 s05 SUB-12 | tip E2E | Trust Δpool+0.053 | Public **6.556** | **NO · Trust≠Public** |
| tip-fork | 2026-07-23 | **rogii-luck-is-all-you-need-private-tip-fork** | opencv411 tip | vp_balanced_modelpkg_005 · `_BH_*` | **6.569** | tip 基準 |
|（履歴）| 2026-07-21 | hahaha-nondet-agi Ver2 | 公開 contact-gated fork | nondet PF+GBM | 6.644 | 旧 Best |

> 詳細: `exp-infer.md` · [`sub-4-7-lb-analysis.md`](../docs-ja/sub-4-7-lb-analysis.md) · 採用は **checklist acceptance** 優先。

## 2026-08-04 session (643 / geo / residual now)

| ID | 日付 | 内容 | レーン | 主数値 | 結果 |
|---|---|---|---|---|---|
| CHK-643 | 2026-08-04 | T2 hard20_balanced S0–S9 stage dump ladder | tip-cv GPU Ver2 | tip_collapse=**false** · tip **16.69**→mid_w060 **12.00** · **S1→S2 SP45 リセット** · primary net=**S3 blend** · report cell SyntaxError 後 ladder ローカル | **GO_local_harvest** · [ladder](work/colab-final-t2/out-643-ladder-v2-local/report.md) · [NB](../my-notebook/tip-cv-chk643-stage-dump-t2/) |
| CHK-685/677 | 2026-08-04 | 643 主工程ロック | T4 | スコープ=**S1–S3 blend のみ** · S5–S8 Δ≈0 · gold path train 未適用 | **GO_lock** · 同上 |
| CHK-683–687·722 | 2026-08-04 | 診断入口A oracle/L井/3way/Q/wellRMSE | T4 local | 666→L-oracle gap **3.72** · L cluster help63 · SP45≢tip/mid | **GO_diag** · [candgen-A](work/colab-final-t2/out-candgen-diag-a-20260804/report.md) |
| CHK-694 | 2026-08-04 | SP45 ≡判定 | T4 | maxabs_vs_tip **22.8** · ≢mid468 · **非≡→材料可** | **GO_non_equiv** · 同上 |
| CHK-697 (=673) | 2026-08-04 | S3 blend **w0.60→0.50** 1機構 | T3 local T2 | mid eqwell **10.940** < w060 **11.997** · < ssot mid | **GO_t2** · [697](work/colab-final-t2/out-697-blend-w050-local/report.md) |
| CHK-702/676 | 2026-08-04 | 新 mid(w050) 上 residual α | T3 local | α0.35 row **9.423**&lt;666 · **sample3 全悪化**（70925e23 14.3→17.7） | **NOGO_sample** · mid GO 先行 · residual は **710 井α** · 同上 |
| CHK-651 | 2026-08-04 | heel typewell affine warp screen | T2 local | meanΔheel≈0 | **NOGO_screen** · [651](work/colab-final-t2/out-651-heel-warp-screen/report.md) |
| CHK-652 | 2026-08-04 | lateral-self GR on neg dTVT | T2 local | best≈14.24 | **NOGO** · [652-654](work/colab-final-t2/out-652-654-geo/report.md) |
| CHK-654 | 2026-08-04 | neighbor dip prior blend | T2 local | Δmid +0.005 · hurt≫help | **NOGO_small** · 同上 |
| CHK-644-E2E | 2026-08-04 | fixed3 tip on test E2E | GPU E2E | fixed3∩test=∅ | **skip_reE2E** · T2 only GO · [err](work/wave31-neural-proposal/out-644-e2e-error/) |
| CHK-667 | 2026-08-04 | soft residual mid/tip +α(S−base) | T2 local | best mid+0.50 soft **11.62** ≫641 10.31 | **NOGO_vs_641** · [soft-634](work/colab-final-t2/out-t2-parallel-soft-634/report.md) |
| CHK-634 | 2026-08-04 | mid468 T2 face (proxy tip-cv-504) | T2/h20 | mid≡tip · face無し | **blocked_face** · 同上 |
| CHK-666 | 2026-08-04 | mid+α(L−m) α0.35 E2E | T2 + GPU E2E + LB | T2 **9.998** · tipdist **1.985** · Public **6.509** · tip+0.240 · ref **55247672** | **Public_NOGO · Trust only** · 再提出禁止 · [ops](latest/ops-lb-chk660-666-public-2026-08-05.md) · [666](work/wave31-neural-proposal/out-666-e2e-harvest/report.md) |
| CHK-668 | 2026-08-04 | mid+α0.30+β0.05 soft | T2 + local face dual | T2 **10.206** · tipdist **2.552** · kernel ERROR(wid) | **GO_e2e_map** · 提出禁止 · [668-local](work/wave31-neural-proposal/out-668-e2e-local-from-faces/report.md) |
| CHK-664 | 2026-08-04 | Public 診断梯子 | LB | farvol **6.190** · … · **641 6.472 NO-GO** · 664 **done** | **done** · [664](latest/ops-lb-chk664-public-branch-2026-08-04.md) · [641](latest/ops-lb-chk641-public-2026-08-04.md) |
| CHK-669 | 2026-08-04 | 661 β tipdist map（agree∧row） | T2 + E2E | E2E tipdist β0.10 **0.58** · β0.20 **0.88** · β0.30 **1.19** · T2 agree frac=1 注意 | **GO_e2e_map** · Public薄候補 · [resid-now](work/colab-final-t2/out-t2-parallel-residual-now/report.md) |
| CHK-697 E2E | 2026-08-04 | SP45 blend **0.50** mid FINAL E2E | T3 · GPU Ver1 | COMPLETE · tipdist **3.298** · final≡w0.50 · w0.60 tipdist **2.866** · mid_before_hedge **0.968** · n=14151 | **GO_e2e_map** · 提出禁止 · [analysis](work/wave31-neural-proposal/out-697-702-e2e-analysis/report.md) · [harvest](work/out-697-e2e-harvest/) |
| CHK-702 E2E | 2026-08-04 | w0.50 mid + residual α**0.35** E2E | T3 · GPU Ver1 | COMPLETE · tipdist **4.223** ≫666 **1.985** · Public **7.394** | **Public_壊滅 · 再提出禁止** · [702](work/out-702-e2e-harvest/) · [ops](latest/ops-lb-chk711-710-702-public-2026-08-05.md) |
| CHK-710 feat | 2026-08-04 | label-free hurt ( |L−m| 等) → α↓ | T3 · local | hurt AUC 低 · top-k hit≈0 · T2 悪化 | **NOGO_label_free** · [feat](work/colab-final-t2/out-710-feature-proxy-local/report.md) |
| CHK-710 s3zero | 2026-08-04 | residual FIXED3 α=0 | T3 · T2 local + CPU + GPU E2E | w050 tipdist **4.142** · ssot **2.017** · Public **6.613** | **Public_NOGO** · [cascade](work/wave31-neural-proposal/out-710-downstream-cascade/report.md) · [ops](latest/ops-lb-chk711-710-702-public-2026-08-05.md) |
| w050-downstream | 2026-08-04 | 新mid上 residual/α/tip⊕/blend 網羅 | local+E2E faces | residual tipdist≥3.4 · tip⊕ g0.05 tipdist0.16 · blend dual T2≠tipdist | **done_cascade** · 同上 · [blend](work/colab-final-t2/out-blend-weight-dual-cascade/report.md) |
| CHK-697b | 2026-08-04 | blend **0.45** mid map E2E | GPU COMPLETE | tipdist **3.705** ≻ w0.50 3.298 | **NOGO_map** · 0.50 固定 · [697b](work/wave31-neural-proposal/out-697b-e2e-analysis/report.md) · [harvest](work/out-697b-e2e/) |
| CHK-711 | 2026-08-04 | tip⊕w050 mid g=0.10 | GPU + submit | tipdist **0.327** · Public **6.359** | **GO_map · Public_NO** · [711](work/wave31-neural-proposal/out-711-e2e-analysis/report.md) · [ops](latest/ops-lb-chk711-710-702-public-2026-08-05.md) |
| CHK-730–735/742/744 | 2026-08-04 | 666 発展 CV 尺子 wave（faces 041247） | T4/T3 local | composite L上位→auto禁止 · α nested **NOGO**·lock0.35 · leaveout flip0 · 725 Final2 LOCK | **wave_done** · [730](work/colab-final-t2/out-730-cv-from-666/report.md) · [proto](chk-730-cv-from-666.md) |
| CHK-725 | 2026-08-04 | Final2 枠凍結表 | T4 | Public=farvol · Trust=666 · material=697 | **LOCK** · 同上 |
| CHK-688 light | 2026-08-04 | oracle well-alpha residual ceiling | T4 local | oracle T2 **5.12–5.89** · gap **~4–5** · 特徴予測不能 | **GO_ceiling OPEN** · 本学習必須 · [745+688](work/colab-final-t2/out-745-well-alpha-policy/report.md) |
| CHK-695 softβ | 2026-08-04 | mid+αL+β soft tipdist dual | local faces E2E | β0.05 tipdist **2.817** · β0.10 **3.667** · 666=1.985 | **NOGO_tipdist** · [wave](work/colab-final-t2/out-695-704-712-wave/report.md) |
| CHK-704 σ-rew | 2026-08-04 | residual α×σ shrink (absLm / softagree / well) | T3 local + tipdist E2E | T2 全悪化 · tipdist↓地図 | **NOGO_Trust** · ≠F033 · 同上 |
| CHK-712 ridge | 2026-08-04 | OOF ridge residual + TEST coef redeploy | T3 local | train OOF~4.9 · TEST tipdist **4.42** | **NOGO_tipdist_E2E** · [712e2e](work/colab-final-t2/out-695-704-712-wave/chk712_e2e_summary.json) |
| CHK-745 well-α | 2026-08-04 | LOO knn/ridge meta residual α | T4 local | corr **0.08–0.17** · tipdist deploy **~6** | **NOGO_tipdist** · **F043** · [745](work/colab-final-t2/out-745-well-alpha-policy/report.md) |
| CHK-741 2α | 2026-08-04 | absLm thr a_lo/a_hi | T4 | T2 9.26 · tipdist **2.83** | **NOGO** · F043 |
| CHK-736 MD α | 2026-08-04 | early/late residual α | T4 | tipdist E2E **+0.17** near-miss | **NOGO dual** · F043 |
| CHK-746 clip α | 2026-08-04 | meta clip [0.2,0.45] | T4 | 一律0.45 · tipdist≥2.54 | **NOGO** · F043 |
| tip-cv-cpu-w050 | 2026-08-04 | CPU tip-cv blend 0.50 | CPU | COMPLETE · FINAL≡tip tipdist0 · mid 面なし | **NOGO_selector_only** · [w050](work/out-tip-cv-cpu-w050/) |
| CPU fill others | 2026-08-04 | var-s5 / w060 / w055 | CPU | **ERROR** (w055 KeyError wid) · dual screen 1井のみ | 参考弱 |
| CHK-750 | 2026-08-04 | T3-B catalog on SSOT faces **041247** | T3 local · 25 policies | 666 pool **10.094** worst **11.905** band **4.144** · vs114917 Δpool **+0.096** · head SAME | **GO_remeasure** · [report](work/out-t3-cpu-harvest/catalog-faces-041247/report.md) · [cmp](work/out-t3-cpu-harvest/catalog-faces-041247/compare_report.md) |
| CHK-748 | 2026-08-04 | pool↔worst Spearman | T3 local | ρ_pool_worst **0.999** · flip≥2 本数 **0** | **GO_rule** · dual 単独 GO は禁止継続 · [diag](work/out-t3-cpu-harvest/chk748-751-diag/chk748_751_report.md) |
| CHK-751 | 2026-08-04 | hard20 vs pool rank flip | T3 local | soft 系が hard20 楽観（max flip **7**） | **GO_rule** · hard20-only GO 再禁止 · 同上 |
| CHK-749 | 2026-08-04 | 666 worst-fold top wells | T3 local · 041247 | top=`1b1eba53` rmse **37.0** · top20 hard20=**14** | **GO_diag** · [749](work/out-t3-cpu-harvest/chk748-751-diag/chk749_report.md) |
| CHK-761 design | 2026-08-04 | well weight map for L retrain | design | top10×**2.0** · 11–20×**1.25** | **ready_after_688** · [weights](work/out-t3-cpu-harvest/chk748-751-diag/chk761_well_weights.json) |
| CHK-747/758/760 | 2026-08-04 | Trust 三点 · tip⊕除外 · Δvs666 列 | process | applied on catalog + Stop | **applied** · [session](work/out-t3-cpu-harvest/chk748-751-diag/session-20260804-t3b-ruler.md) |
| CHK-752 | 2026-08-05 | max_band second filter + name ban | T3 local | survivors **6**（resid α0.35–0.80, a035_s3）· tip⊕/soft drop | **GO_filter** · [752](work/out-t3-cpu-harvest/chk752-755-763/report.md) |
| CHK-755 | 2026-08-05 | tipdist×worst lane assign | T3 local | trust_candidate=666/a035_s3 · public_map=711系 · L=t2_good_tipdist_bad | **GO_map_rule** · 同上 |
| CHK-763 | 2026-08-05 | field leave-out flip=0 ops | process | 731 運用 JSON | **ops_ready** · 同上 |
| CHK-761 NB | 2026-08-05 | worst-well weighted L retrain NB | GPU ready | top10×2 · sample_weight in train_stack | **ready · wait 688** · [nb](../my-notebook/tip-cv-chk761-weighted-h20/) |
| CHK-761 L1 push | 2026-08-05 | v2 fold-driver + FAST L1 GPU Ver1 | **ERROR** | IndentationError In[36] · no learned | **ERROR** · [harvest](work/out-t3-cpu-harvest/autopilot-3h-20260805/harvest-761/) |
| CHK-688 full | 2026-08-05 | full retrain hard20 learned | COMPLETE · dual | resid pool **16.82** vs old **16.30** · Δ**+0.52** · worst +0.89 | **NOGO_L1** · [dual](work/out-t3-cpu-harvest/l-dual-auto-688/report.md) · [harvest](work/out-t3-cpu-harvest/autopilot-3h-20260805/harvest-688/) |
| CHK-782 weights | 2026-08-05 | resid>L drag sample_weight | design | n=41 · top10×2 / next×1.5 / rest×1.35 | **nb_ready** · [w](work/out-t3-cpu-harvest/session-1h-cv-20260805/chk782_resid_drag_weights.json) · [nb](../my-notebook/tip-cv-chk782-resid-drag-h20/) |
| CHK-782 L1 | 2026-08-05 | resid-drag L1 | **COMPLETE NOGO** | hard Δ**+3.81** · dual done | [ops](latest/ops-l1-chk761-782-harvest-dual-2026-08-05.md) · [kernel](https://www.kaggle.com/code/kazeneko77/tip-cv-chk782-resid-drag-h20) |
| T3 formal 041247 | 2026-08-05 | promising policies 5-seed | local+Kaggle COMPLETE | resid_a035 pool **10.094** ≡ SSOT | **GO_catalog** · [report](work/out-t3-cpu-harvest/t3-formal-041247/report.md) |
| CPU-WAIT pack | 2026-08-05 | dual+weight+anti-promote+ceiling | local T4 + Kaggle CPU | pool≡SSOT **10.094** · 783 **RUN** · anti-promote PASS · 782 ceil −0.88 | **GO_map** · [report](work/out-t3-cpu-harvest/session-cpu-wait-20260805/report.md) · [kernel](https://www.kaggle.com/code/kazeneko77/cpu-l-wait-cv-pack) |
| CHK-783 set | 2026-08-05 | 761 vs hard top vs 782 set | T4 local | top10_761∈hard **1/10** · 782-only **27** | **RUN_783 after 782** |
| CHK-724 faces | 2026-08-05 | residual a0.35 anti-promote | T4 local | PASS · not raw mid/L | **GO_local** |
| CHK-769 L1 | 2026-08-05 | LGB-only FAST screen | GPU queued | FAST=1 · L_FAST_LGB_ONLY · ban pre PASS | **nb_ready · wait GPU** · [nb](../my-notebook/tip-cv-l-fast-h20/) |
| CHK-762 script | 2026-08-05 | new L dual T2+T3-B | local harness | no 688 dump → exit2 | **ready · wait 688** · [py](work/out-t3-scratch/run_chk762_dual_new_L.py) |
| 1h-session | 2026-08-05 | CV loop 55min while 688 RUNNING | T3/T4 local | 765/739/715/766/737/764/761-impact | **done** · [report](work/out-t3-cpu-harvest/session-1h-cv-20260805/report.md) |
| CHK-765 | 2026-08-05 | oracle well-α residual ceiling | T4 diagnostic | oracle pool **6.57** vs a035 **10.09** gap **3.53** · mean α* **0.91** | **GO_ceiling** · ≠deploy F043 · [765](work/out-t3-cpu-harvest/session-1h-cv-20260805/chk765_summary.json) |
| CHK-739 | 2026-08-05 | 第2 seed pack T3 | T4 | rank flip **0** · a035 worst 11.91→**12.48** band↑ | **GO_stable** · 同上 |
| CHK-761 v2 | 2026-08-05 | fold-driver weights | design | v1 overlap**1**→ v2 worst-fold top10 | **refined** · [weights](work/out-t3-cpu-harvest/chk748-751-diag/chk761_well_weights.json) |
| CHK-766 | 2026-08-05 | resid−L drag map | T4 | resid>L+1 **41**/80 · L≺mid **90%** | **GO_map** · mid drag |
| CHK-715 | 2026-08-05 | soft residual screen | T4 | best≡mid_a035 · soft 負け | **NOGO** 置換不可 |
| CHK-737 screen | 2026-08-05 | conf\|L-m\| α gate | screen | pool **9.52** worst **11.21** · tipdist未 · F043近 | **WATCH · 昇格禁止** · 688優先 |
| CHK-764 | 2026-08-05 | mid hurts L design | design | mid≺L by2 **38** wells · defer | **defer_after_688** |
| L-relearn SSOT | 2026-08-05 | multi-session L flow | process | L0→L1→L2 · dual α0.35 · F043/F015 | **applied** · [guide](l-relearn-session-guide.md) |
| CHK-767 | 2026-08-05 | L0/L1 FAST NB 雛形 | ops | FAST=1 · LGB-only · stop-after-learned | **nb_ready** · [nb](../my-notebook/tip-cv-l-fast-h20/) |
| dual local L | 2026-08-05 | residual dual new vs old L | harness | L1: pool/worst ≤old−0.05 · band≤old+0.5 | **ready** · [py](work/out-t3-scratch/run_l_residual_local_dual.py) |
| CHK-769–780 | 2026-08-05 | L improve queue（Kaggler案） | design | LGB-only · early-stop · known-zone · residual-y · 特徴 · seed · 帯切替 | **pending** · [§5](l-relearn-session-guide.md) |
| CHK-781–788 | 2026-08-05/06 | L1 追加キュー | closed | 781/784 dual NOGO · 他 dual 未 · 締切 | **COMP CLOSED** · F044–F046 · [laws](latest/l-improvement-laws-2026-08-05.md) |
| recon-688 | 2026-08-05 | residual dual hard20 reconfirm | local T4 | new resid 16.82 vs old 16.30 · Δ+0.52 | **NOGO_L1 confirm** · [r](work/out-t3-cpu-harvest/l-dual-session-reconcile-688/report.md) |
| recon-ssot-L | 2026-08-05 | dual harness idemp SSOT L | local T4 | pool **10.094** ≡666 · 80 wells | **ssot_ok** |
| Public snap | 2026-08-05 | 660/666 LB | COMPLETE | **660=6.239** · **666=6.509 NOGO** · farvol=6.190 Best · 641=6.472 | **再提出禁止** · [ops](latest/ops-lb-chk660-666-public-2026-08-05.md) |
| CV-handoff | 2026-08-05 | 工程×井 · CHK-807–812 · 実行順 | handoff MD | residual win≈mid · Q4 主戦場 · mid-hurt3 除外 · weight3→781 | **applied_map** · [handoff](l-cv-hypothesis-handoff-2026-08-05.md) |
| CHK-807 | 2026-08-05 | residual early-stop / OOF 選抜 | design | 688 型 L良resid悪防止 · 781 隣接 | **design** · handoff §4 |
| CHK-808 | 2026-08-05 | weight 3 NOGO→即781 | ops | 帯粘り禁止 | **applied** |
| CHK-809 | 2026-08-05 | attack − mid-hurt3 | map | 3 井除外 weight | **map pending** |
| CHK-810–812 | 2026-08-05 | タイプ dual 表 · Q4/mid-hurt WATCH · 直交特徴 | design/ops | dual 拡張 | **pending** |
| CHK-660 submit | 2026-08-05 | tip+α0.50 L resid agree | Ver1 · once | ref **55248920** · Public **6.239** · tipdist 1.923 | **枠2NO · no resubmit** · [val](../docs-ja/submission-validations/2026-08-05-chk660-submit.md) |
| CHK-666 submit | 2026-08-05 | mid+α0.35 residual · notebook-linked | Ver1 · once | ref **55247672** · Public **6.509** · tip+0.240 | **Public_NOGO · Trust only · no resubmit** · [val](../docs-ja/submission-validations/2026-08-05-chk666-submit.md) |
| CHK-711 submit | 2026-08-05 | tip⊕w050 mid g0.10 | Ver2 · once | ref **55251125** · Public **6.359** · tip+0.090 · tipdist 0.327 | **Public_NO · map_only · no resubmit** · [ops](latest/ops-lb-chk711-710-702-public-2026-08-05.md) |
| CHK-710ssot submit | 2026-08-05 | residual α0.35 s3zero SSOT | Ver1 · once | ref **55252402** · Public **6.613** | **Public_NOGO · 666より悪 · no resubmit** · 同上 |
| CHK-702 submit | 2026-08-05 | w050 mid + α0.35 residual | Ver1 · once | ref **55252403** · Public **7.394** · tipdist 4.223 | **Public_壊滅 · no resubmit** · 同上 |
| CHK-761 Ver2 attempt | 2026-08-05 | indent-fixed re-push | GPU blocked | Max batch GPU=2 · 占有 782+669 | **queued day-watch** · [log](../my-ran-notebook/tip-cv-chk761-weighted-h20/run-log.md) |
| day-watch | 2026-08-05 | 782 harvest+761 push autowatch | ops 3h | includes 669 in GPU count | **RUNNING** · [dir](work/out-t3-cpu-harvest/session-day-watch-20260805/) |
| CV-789–795 | 2026-08-05 | dual plane·8seed·drag·field·known·midhurt | T4 local pack | 790/791 ops · 794 elev771 · 795 mid SSE87% | **done screen** · [pack](work/out-t3-cpu-harvest/cv-improve-pack-20260805/report.md) |
| dual-v2 | 2026-08-05 | hard_plane+hybrid80+worst8 | harness | 688 hard Δ+0.52 · hybrid Δ+0.23 とも NOGO | **applied** · [py](work/out-t3-scratch/run_l_residual_local_dual.py) |
| CHK-782 Ver1 | 2026-08-05 | resid-drag L1 | **ERROR** | Indent `_ns` · learned無し · PFは完了 | [harvest](work/out-t3-cpu-harvest/harvest-782-error/) · **FIX local** |
| CHK-761 Ver2 | 2026-08-05 | weighted L1 COMPLETE | GPU COMPLETE · dual | hard Δ**+4.01** · hybrid **+1.81** · mid-collapse | **NOGO_L1** · [dual](work/out-t3-cpu-harvest/l-dual-CHK-761-harvest/report.md) · [ops](latest/ops-l1-chk761-782-harvest-dual-2026-08-05.md) |
| CHK-782 Ver2 L1 | 2026-08-05 | resid-drag n41 L1 | GPU COMPLETE · dual | hard Δ**+3.81** · hybrid **+1.71** · 688hurt **+4.18** | **NOGO_L1** · [dual](work/out-t3-cpu-harvest/l-dual-CHK-782-harvest/report.md) · 同上 |
| CHK-804 Kaggle | 2026-08-05 | known-q4 push try | **CANCEL_ACK** | 政策: Kaggle L1 停止 | Colab 本線のみ |
| CV-796–801 | 2026-08-05 | MD-Q · seed ruler · weight · mid-pull · rank | T4 pack2 | Q4 worst · 5seed worst+0.51 · mid-pull NOGO | **done** · [pack2](work/out-t3-cpu-harvest/cv-improve-pack2-20260805/report.md) |
| CPU-GAP-b | 2026-08-05 | Jaccard·oracle v1b/809·offline L | T4 local | **792≡803** · 761 midhurt · 804帯 | **done** · [gap-b](work/out-t3-cpu-harvest/cpu-cv-gap-20260805b/report.md) |
| CPU-P0P1 local | 2026-08-05 | 761v2b·803/804·Q4·811·781·field | T4 local 27s | J**0.608** · Q4sse**0.46** · L\* d−3.03 | **done** · [p0p1](work/out-t3-cpu-harvest/cpu-parallel-p0p1-20260805/report.md) |
| CPU-P0P1 Kaggle×5 | 2026-08-05 | 5 Private CPU V1 parallel | **COMPLETE** | harvest≡local pool**10.094** | [kaggle](work/out-t3-cpu-harvest/kaggle-cpu-p0p1-20260805/report.md) · 提出禁止 |
| CPU-expert-C | 2026-08-05 | coverage·688∩·bias·pseudoPub·805·807·804v1c | T4 local 223s | 804v1c n43≈full · 805 L\*Q34 · 782∩688 49% · C5 ρ=1 | **GO_ops** · [C](work/out-t3-cpu-harvest/cpu-expert-pack-c-20260805/report.md) |
| CHK-804 v1c | 2026-08-05 | 804_v1b knee prune + demote 688nontop | map | n**43** · d_worst≈full+0.006 | **map only · live は下** · [json](work/out-t3-cpu-harvest/l-hyp-weights-20260805/chk804_known_q4_weights_v1c_pruned.json) |
| **CHK-804 Colab L1** | 2026-08-05 | known×Q4 v1c retrain FAST3 | **Colab L4** · dual α0.35 | OOF stack **9.701** · tip-cv TVT **9.131** · hard Δ**+0.74** · hybrid **+0.33** · d\|L−mid\| **−1.43** · 688hurt **+0.93** | **NOGO_L1 · mild mid-collapse · F044 · 再学習禁止** · [ops](latest/ops-l1-chk804-colab-dual-2026-08-05.md) · [dual](work/out-t3-cpu-harvest/l-dual-CHK-804-colab/report.md) · [laws](latest/l-improvement-laws-2026-08-05.md) · face [harvest](work/out-t3-cpu-harvest/chk804-colab-face-20260805/) |
| **CPU Pack D** | 2026-08-05 | residual-path D1–D7 design screen | T4 local + **Kaggle CPU Ver3 COMPLETE** | L* all β0.30 d_pool **−3.03** ≡Kaggle · protect excl midhurt · 807 resid stop **1.0** · path **\|L−mid\|↑** vs weight **↓** | **GO_ops design · ≡ local** · [ops](latest/ops-cpu-pack-d-residual-path-2026-08-05.md) · [local](work/out-t3-cpu-harvest/cpu-expert-pack-d-20260805/) · [kaggle *-v3](work/out-t3-cpu-harvest/kaggle-cpu-pack-d-20260805/) · 提出禁止 |
| **CHK-802 Colab FAST2** | 2026-08-05 | MD-Q4 行 weight · residual mid+α0.35(L−m) | Colab L4 · dual α0.35 | OOF **9.3765** · hard Δ**+1.79** · hybrid **+0.79** · B_Q4 **+1.02** · d\|L−mid\| **−4.24** · 813/815 fail | **NOGO_L1 · F044 · E2E ABORT · 再学習禁止** · [dual](work/out-t3-cpu-harvest/l-dual-CHK-802-colab-fast2/report.md) · [ops](latest/ops-chk802-dual-nogo-2026-08-05.md) · [post](latest/ops-chk802-post-pipeline-2026-08-05.md) · [laws](latest/l-improvement-laws-2026-08-05.md) |
| **CHK-781 Ver1 L1** | 2026-08-05/06 | residual-path soft L\* · FAST2 hard20 | **Kaggle COMPLETE · dual** | hard Δ**+0.44** · hybrid **+0.19** · d\|L−mid\| **−0.97** · Q4 **+0.21** · SSE50 **+0.25** | **NOGO_L1 · mild · E2E 禁止** · [dual](work/out-t3-cpu-harvest/l-dual-CHK-781-kaggle-v1/report.md) · [post](latest/ops-chk781-post-pipeline-2026-08-05.md) · [kernel](https://www.kaggle.com/code/kazeneko77/tip-cv-chk781-resid-path-h20) |
| **CHK-784 Huber FAST2** | 2026-08-05/06 | LGB objective=huber α0.9 · no weight | Colab L4 · dual α0.35 | hard Δ**+6.27** · hybrid **+2.86** · d\|L−mid\| **−4.06** · raw L hard **26.9** | **NOGO_L1 · F045 · loss 形禁止** · [ops](latest/ops-chk784-dual-nogo-2026-08-05.md) · run `20260805-143010-chk784-huber-hard20-fast2` |
| **CHK-777 reg↑** | 2026-08-05/06 | reg_λ30 · reg_α1 · min_child60 · FAST2 | body + gate pre only | dual **未** | **incomplete · 締切停止** · [ops](latest/ops-chk777-regup-colab-2026-08-05.md) |
| COMP END freeze | 2026-08-06 | Final2 + L ladder 凍結 | docs only | Final **666+farvol** · L1 dual **全 NOGO** | **done** · [exp-index](exp-index.md) |
| CHK-761 weights v2b | 2026-08-05 | midhurt3 protect ab3ced07→1.0 | map only | midhurt protect は dual で効かず | [v2b](work/out-t3-cpu-harvest/chk748-751-diag/chk761_well_weights.json) |
