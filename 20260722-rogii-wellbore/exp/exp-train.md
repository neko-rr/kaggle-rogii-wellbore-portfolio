# exp-train — rogii-wellbore

> type: train-analysis  
> updated: 2026-08-06（**COMP CLOSED · L1 dual 全 NOGO · 新規 train なし**）  
> purpose: 学習実験、CV、fold、データ処理、モデル、loss、特徴量の管理

**現在地 / 梯子:** [`exp-index.md`](exp-index.md) · [laws 最終](latest/l-improvement-laws-2026-08-05.md)  
**L1 dual hard Δ（悪化+）:** **781 +0.44** ≺ 688 +0.52 ≺ 804 +0.74 ≺ 802 +1.79 ≺ 782 +3.81 ≺ 761 +4.01 ≺ **784 +6.27** · 全 **NOGO**  
**F044** weight · **F045** Huber loss · **F046** residual-path live · **F043** α · **F015** 生 mid/L  
**CHK-781 residual-path:** COMPLETE dual · **NOGO_L1** · [report](work/out-t3-cpu-harvest/l-dual-CHK-781-kaggle-v1/report.md)  
**CHK-784 Huber:** COMPLETE dual · **NOGO · F045** · [ops](latest/ops-chk784-dual-nogo-2026-08-05.md)  
**CHK-777 reg↑:** body only · dual **未 · 締切停止** · [ops](latest/ops-chk777-regup-colab-2026-08-05.md)  
**CHK-802/804/761/782/688:** 既報告 NOGO · F044 帯  
**Trust residual 頭:** faces **041247** · **666** α0.35 pool **10.094**（新 L 未採用）  
**CHK-FINAL-T2 all773:** tip pool **10.8388** hard **26.829** · tip⊕ NOGO · [stage-group](latest/all773-stage-well-group-2026-08-05.md)  

**Wave-29 CLOSED:** B7(S1a/S1b) 門番未達 · B8 ノブ0 · [`close`](../docs-ja/discussion/wave29-close-2026-07-30.md) · [`checklist`](experiment-checklist.md)  
**Wave-28 CLOSED:** 提出可能直し方6仮説 T4 全NO-GO · **F040** · 次=OPS-FINAL2 · [`close`](../docs-ja/discussion/wave28-usable-fix-close-2026-07-30.md)  
**Wave-27 CLOSED:** ねじれ全ファミリー測定 · 360 NO-GO · **F039 形修正閉鎖** · [`close`](../docs-ja/discussion/wave27-twist-close-2026-07-30.md)  
**Wave-26 CLOSED:** A–D完了 · **F038 移す系閉鎖** · [`close`](../docs-ja/discussion/wave26-compass-close-2026-07-30.md)  
**Wave-25 CLOSED:** A PASS · B/C/D **F036–F037** · [`close`](../docs-ja/discussion/wave25-lane-close-2026-07-30.md)  
**Wave-24:** 283 PASS · 284/285/288 **NO-GO**（F033）· [`chk288`](../docs-ja/discussion/chk288-guided-proposal-result.md)  
**Wave-23:** CHK-279 **順位付け失敗** · F028–F032 · [`chk279`](../docs-ja/discussion/chk279-discontinuity-result.md)  
**Wave-20 tip 温度:** selector 面 **T=0.15 最良（29.899）** · [`chk222`](../docs-ja/discussion/chk222-lik-temp-0p15-result.md)  
**Wave-9 B5:** **F017 閉鎖** · [`chk130-nogo-memo.md`](work/chk130-heel-dtw/chk130-nogo-memo.md)  
**Wave-7 B1:** **F014 閉鎖** · [`wave7-status-2026-07-25.md`](../docs-ja/wave7-status-2026-07-25.md)  
**Wave-8 B4:** **F016 閉鎖** · [`chk120-kill-memo.md`](work/chk120-dual-final/chk120-kill-memo.md)


---

## 学習方針

| 項目 | 値 |
|---|---|
| CV設計 | **GroupKFold by well ID**（5-fold）· **用途別 Tier:** [`docs-ja/cv-tiers.md`](../docs-ja/cv-tiers.md) |
| fold数 | 5 · fold-seed 安定幅: 42/123/2026（CHK-060） |
| validation単位 | well |
| 門番 | **carry-forward（anchor-hold）** pooled RMSE ≈ **15.91**（multi-seed でも同一） |
| tip 採用物差し | T1=hard20 · **T2=方位層化≈80井** · T3=3 seed |
| 主モデル / tip | Contact-Gated luck tip（GPU）· ローカルは CF/Bet 代理 |
| 主なloss / metric | **RMSE** |

データ実測: [`docs-ja/dataset.md`](../docs-ja/dataset.md) · ruler: [`exp/work/wave0-ruler/`](work/wave0-ruler/)

---

## データスナップショット（2026-07-23）

| 項目 | 値 |
|---|---|
| train wells | 773 |
| train rows | ~5.09M（eval ~73%） |
| CF pooled OOF（Wave-0） | **15.91**（5-fold 14.83–17.92） |
| CF well-median | 10.67 |
| hard-wells | 20（`hard-wells.json`） |

---

## 学習実験ログ

| exp_id | 日付 | 変更点 | CV | fold詳細 | 判断 |
|---|---|---|---|---|---|
| CHK-610 | 2026-08-03 | 逆井ゲート HD tip固定 | hard20 tip⊕mid495 | Trust 29.13 ≫ agree 26.63 | **NOGO** · [`610-613`](work/wave31-neural-proposal/out-610-613-reverse-safe/report.md) |
| CHK-613 | 2026-08-03 | frac≤0.15 cap / 515安全確認 | hard20 · TEST tipdist | 追加cap NOGO · 558b frac0.127確認 | **GO_confirm** · 同上 |
| CHK-600 | 2026-08-03 | Soft→ゲート特徴 mid注入 | hard20 · T2 soft面 | 最良26.95 · Soft FINAL diag24.62 | **NOGO** · [`600-602`](work/wave31-neural-proposal/out-600-602-soft-peaky/report.md) |
| CHK-602 | 2026-08-03 | peaky ESS tip固定 | hard20 · 492b ess | Trust27.53 · 86454悪化 | **NOGO** · 同上 |
| CHK-592 | 2026-08-03 | agree∧\|L−tip\|≥3 | hard20 | 26.621 · hurt12/help6 · ≡591 | **NOGO** · [`592`](work/wave31-neural-proposal/out-592-agree-micro/report.md) |
| CHK-390 | 2026-07-30 | soft候補バンク+1井smoke | chk284-packs · F015禁止 | soft45.2 · no submission | **GO** · [`s0`](work/wave30-soft-preserve/s0-design-memo.md) |
| CHK-391 | 2026-07-30 | Soft-Preserve Ridge設計 | 4井LOO · label-free | finite · tip非混合 | **GO** · [`s1`](work/wave30-soft-preserve/s1-ranker-memo.md) |
| CHK-392 | 2026-07-30 | hard20 Soft-Preserve門番 | local packs · 1回 | CF/tipcv OK · pearson0.9995 | **NO-GO** · [`gate`](work/wave30-soft-preserve/chk392-gate-report.json) |
| CHK-395 | 2026-07-30 | 生Pearson門番監査 | frozen 392 · 再学習なし | raw0.999 · err0.689 · centered0.895 | **GO_gate_reopen_candidate** · [`audit`](work/wave30-soft-preserve/chk395-gate-audit.md) |
| CHK-397 | 2026-07-30 | Soft-Preserve E2E/リーク | hard20 packs | soft≡final · pack不足 | **FAIL** · [`397`](work/wave30-soft-preserve/chk397-e2e-leak-audit.md) |
| CHK-401 | 2026-07-30 | tip PF pack×20 non-hard20 | knobs=chk284固定 | 20/20 OK | **GO** · [`401`](work/wave30-soft-preserve/chk401-pack-report.json) |
| CHK-398 | 2026-07-30 | hard20→外井 transfer CV | hard20 train · 401 packs | final14.81 > soft14.58 · tip CSV無し | **NO-GO** · [`398`](work/wave30-soft-preserve/chk398-exhard-cv.md) |
| CHK-402 | 2026-07-30 | matched tip FINAL部分取得 | 401と同20井 · Ver1 ERROR | tip pool 10.66 | **PARTIAL** · [`分析`](../docs-ja/discussion/chk402-error-partial-2026-07-30.md) |
| CHK-402A | 2026-07-30 | tip FINAL vs Soft-Preserve ranker | 同一20井 · local | tip 10.66 ≪ ranker 14.73 · soft≡ranker | **NO-GO** · [`比較`](work/wave30-soft-preserve/chk402a-compare.md) |
| CHK-406 | 2026-07-31 | label-free tip\|soft 選択診断 | 同一20井 · LOO | oracle 8.29だが選択pool 12.98 | **NO-GO** · [`406`](work/wave30-soft-preserve/chk406-report.md) |
| CHK-407 | 2026-07-31 | tip内部特徴ゲート | 同一20井 · LOO | acc0.60–0.65だがpool 12.8–13.6 | **NO-GO** · [`407`](work/wave30-soft-preserve/chk407-report.md) |
| CHK-408 | 2026-07-31 | tip×soft固定ブレンド天井 | 同一20井 · 診断 | α0.2 pool10.52 · 提出不可 | **GO_screen** · [`408`](work/wave30-soft-preserve/chk408-tip-soft-blend-screen.md) |
| CHK-409 | 2026-07-31 | 402生成変化の見落とし再監査 | 同一20井 · 井bootstrap | 1井hedgeのみ · before10.5985 < final10.6568 · CI上端0 | **NO-GO** · [`409`](work/wave30-soft-preserve/chk409-stage-change-report.md) |
| CHK-396 | 2026-07-31 | 過去 tip-corr≈1 NO-GO カタログ | T4 · frozen · 再学習なし | 070/040/w40/Sunny 再計算 · raw≈0.999だが err/cen低下 · 全件 tip非改善 | **GO_catalog** · ban維持 · [`396`](work/wave30-soft-preserve/chk396-tip-corr-catalog.md) |
| CHK-369 | 2026-07-30 | S1a PF設計凍結+1井smoke | (tvt,lag)+窓Pearson · tip非クローン | CF微超え（25050f63） | **done** · [`memo`](work/wave29-alt-face/s1a-design-memo.md) |
| CHK-370 | 2026-07-30 | S1a hard20門番 | local4well screen · N48×4 | 1/4 CF超えのみ | **NO-GO** · 371 skip · [`screen`](work/wave29-alt-face/chk370-4well-local-screen.json) |
| CHK-372 | 2026-07-30 | S1b last-anchor Ridge smoke | LOO 5井 · tip-free | 2/5 CF | **done** · TCN本学習へ · [`report`](work/wave29-alt-face/chk372-smoke-report.json) |
| CHK-373 | 2026-07-30 | S1b TinyTCN GroupKFold5 | hard20 · CPU Ver2 | pooled **55.55** > CF **49.56** · 8/20 | **NO-GO** · B7閉鎖 · [`report`](work/wave29-alt-face/chk373-out/chk373-report.json) |
| CHK-380 | 2026-07-30 | soft→selector→hedge→FINAL段マップ | hard20 · chk284+chk256 | destroy=soft→selector · 候補0 | **STOP** · 381/382 skip · [`report`](work/wave29-final-pipeline/chk380-report.md) |
| CHK-321 | 2026-07-30 | soft−oracle→平行/ねじれ | hard20 · pfrac thr0.5 | twist **90%** | **GO診断** |
| CHK-322 | 2026-07-30 | lik vs soft 方向 | FD h=1 | rf rev70% · H1 PASS | **GO** |
| CHK-323–326 | 2026-07-30 | 二面·幾何·cascade·MD帯 | packs+chk279 | ρ_sf=+0.07 · F028 · 局所Pなし | **GO · A完了 C skip** |
| CHK-327 | 2026-07-30 | tip-soft 代理 LOO | 雲特徴 | LOO≦lik | **NO-GO** |
| CHK-328–330 | 2026-07-30 | FINAL代理·合意·単純統計 | LOO/tip_std | 転用不可·合意25% | **GO診断** |
| CHK-336–337 | 2026-07-30 | 局在/打ち切り | 文書 | 局在28%不可 · **F038** | **閉鎖 · OPS-FINAL2** |
| CHK-331–335 · 338–340 | 2026-07-30 | 平行移動/昇格 | — | 入口未達 | **skipped** |
| EDA-001 | 2026-07-23 | 公式 data 実測 · CF 代理 | CF med 10.67 | 773 | 下限把握 |
| W0-ruler | 2026-07-23 | GroupKFold CF + Bet 代理 | CF pooled 15.91 | 5-fold | **物差し確立** · CHK-010/012/024 |
| W1-proxy | 2026-07-23 | heel gs / nbr / hedge 代理 | 下記 | — | 素朴代理は **rejected**（tip graft へ） |
| F-050–053 | 2026-07-24 | 基礎ギャップ T4 | 下記 | hard20 | Random禁止(F003) · NW_N · NCC本命 |
| CHK-060 | 2026-07-24 | CF fold multi-seed | pooled **15.91** · worst_fold band≈**0.51** | seeds 42/123/2026 | 門番安定幅確定 |
| CHK-061a | 2026-07-24 | T2 allowlist | n=80 方位層化 | hard20+sample60 | tip T2 準備 |
| CHK-051 | 2026-07-24 | tip hard20 seed123 再推論 | pooled **14.87** · preds≡seed42 | hard20 | **nondet band≈0** |
| CHK-061 | 2026-07-24 | tip T2 balanced 80井 | tip pooled **8.33** vs CF同井 **27.77** | Ver4 · 1.5h | **T2 PASS** · 採用物差し確立 |
| CHK-FINAL-T2 | 2026-08-03 | Final候補カタログ T2≈80井 | winner agree-only **12.279** · hard_mean **18.521** · tip 17.030 · 579/541/row 12.331 | Colab · faces済 | **GO_t2** · all773待ち · [`t2-catalog`](work/colab-final-t2/t2-catalog-report.md) |
| CHK-062 | 2026-07-24 | tip T3 3seed | pooled **8.330** · band **0** · preds identical | 80井 | **GO** · seed非依存 |
| CHK-020 | 2026-07-24 | NW_N graft | F006 postprocess · F009 tip内 BH-up | hard20/T2 | **rejected** |
| CHK-041 | 2026-07-24 | BH=0.30 hedge | pooled 14.874（基準14.869） | hard20 | **NO-GO** · T2不実施 |
| CHK-070 | 2026-07-24 | CatBoost residual GPU | hard20 **31.80** · tip corr0.999 | GroupKFold | **F010** · Final2不可 |
| CHK-071 | 2026-07-24 | LGBM TrackA proxy | hard20 **214.8** | GroupKFold GPU | **NO-GO** |
| CHK-040 | 2026-07-24 | heel+窓 NCC→CatBoost drift | hard20 **45.96** · tip corr≈0.999 · unconst 72.24 | GroupKFold GPU | **F011 NO-GO** · Final2不可 |
| CHK-100 | 2026-07-25 | B1 方位2群 Track A early-ridge | hard20 early | az-split-h20-ee | pooled **31.82** vs 対照 **31.28** | **F014 NO-GO** |
| CHK-103 | 2026-07-25 | az-as-feature early-ridge | hard20 early | az-feat-h20-ee | ≈対照 Δ0.003 | **F014 NO-GO** |
| CHK-101 | 2026-07-25 | Best T2 Trust CV（graft） | T2 80井 | best-cv-t2-allowlist | pooled **8.330** ≡ tip · Best固有未分離 | **done（注意）** · memo |
| Wave-13-A | 2026-07-25 | gated soft 洗練（ローカル graft） | T2 portable Δpool **+0.053** · two-stage samp **+0.0005** | 複合+f33-s05 | **A完了** · [`wave13-a-best`](work/wave13-gated-refine/wave13-a-best.json) |
| Wave-14 | 2026-07-25 | 井型×後処理 · A/B=`tip_std_far/prox` | AUC0.978 · T2 screen +0.072/+0.004 | farvol thr0.842 | **screen GO** · 本採点は CHK-184 · [`wave14`](../docs-ja/wave14-well-archetypes-2026-07-25.md) |
| CHK-186 | 2026-07-25 | tip lik-PF 128-seed oracle | T2 FINAL **8.33** vs oracle **8.13**（+0.20）· hit≤4.5 46% | hard20 oracle **12.9** | **mixed** · 188/189 自動なし · [`chk186-result`](../docs-ja/discussion/chk186-generator-ceiling-result.md) |
| CHK-187 | 2026-07-26 | tip stage/soft oracle | soft **+0.14** · tip64/80 · BH knobs gap0 | F015 再確認 | **done** · [`chk187-result`](../docs-ja/discussion/chk187-stage-oracle-result.md) · [`wave14×186`](../docs-ja/discussion/wave14-x-chk186-join-2026-07-26.md) |
| CHK-236 | 2026-07-27 | hard20 A/B 分割 | B14:A6 | 上流厚 | **done** · [`chk236`](../docs-ja/discussion/chk236-ab-split-result.md) |
| CHK-256 | 2026-07-28 | tip内部面 tip-cv 診断 | hard20 tip-cv T0.15 | gold≡before_hedge≡selector **30.089** · final+0.017 | **done** · 案C天井なし · [`result`](../docs-ja/discussion/chk256-faces-result.md) |
| CHK-255 | 2026-07-27 | MD vs TST GR 軸 | TVT 14.5 ≪ TST 35.9 | absorbed | **done** · [`chk255`](../docs-ja/discussion/chk255-md-tst-result.md) |
| CHK-246 | 2026-07-27 | ±15ft 二峰 PF init | s8@T0.15 −3.8 · hit↓ | early-kill | **rejected** · [`chk246`](../docs-ja/discussion/chk246-bimodal-init-result.md) |
| CHK-232 | 2026-07-27 | spr≠12 多様性 screen | 最良 spr8 T0.15 −0.51 | oracle↑ tip↓ | **rejected** · [`chk232`](../docs-ja/discussion/chk232-diversity-result.md) |
| CHK-233 | 2026-07-28 | heel錨定/多峰 | 最良 −1.60 | hit↑ tip↓ | **rejected** · [`chk233`](../docs-ja/discussion/chk233-heel-multimode-result.md) |
| CHK-238 | 2026-07-28 | 遠MD PN密度 | tip −3.23 | far微↑ tip↓ | **rejected** · [`chk238`](../docs-ja/discussion/chk238-far-md-result.md) |
| CHK-205 | 2026-07-26 | lik_temp T∈{0.5,2} tip-cv selector | hard20 **T0.5=32.276**（vs211 +0.90）· T2 NO-GO | selector-face | **PASS T0.5** · [`chk205`](../docs-ja/discussion/chk205-lik-temp-result.md) |
| CHK-211 | 2026-07-26 | selector-face baseline T=1 | hard20 **33.178** | USE_SELECTOR_FACE | **GO·物差し** · [`chk211`](../docs-ja/discussion/chk211-selector-baseline-result.md) |
| CHK-213 | 2026-07-26 | generator spr/seeds oracle | seed-oracle spr12 **10.38**（+2.50） | hard20 · tip非採用 | **PASS oracle** · tip面は214 NO-GO |
| CHK-218 | 2026-07-26 | lik_temp 細格子+entropy（局所PF） | s5 **T0.3=17.85** vs T0.5 +0.56 · entropy NO-GO | hard20 local | **PASS T0.3** · [`chk218`](../docs-ja/discussion/chk218-liktemp-fine-result.md) |
| CHK-219 | 2026-07-26 | tip-cv **T=0.3** | hard20 selector **30.827**（vs211 +2.35 · vsT05 +1.45） | tip-cv GPU | **PASS** · [`chk219`](../docs-ja/discussion/chk219-lik-temp-0p3-result.md) |
| CHK-221 | 2026-07-26 | colder T / topk / scale（局所） | T0.15=17.24 · topk5=17.13 · sc2=17.21 | hard20 local | **PASS** · [`chk221`](../docs-ja/discussion/chk221-colder-topk-result.md) |
| CHK-222 | 2026-07-26 | tip-cv **T=0.15** | hard20 selector **29.899**（vs219 +0.93） | tip-cv GPU | **PASS_best** · [`chk222`](../docs-ja/discussion/chk222-lik-temp-0p15-result.md) |

### Wave-20 tip 温度ラダー（selector hard20 · RMSE↓が良い）

| T | RMSE | CHK | メモ |
|---:|---:|---|---|
| 1.0 | 33.178 | 211 | baseline |
| 0.5 | 32.276 | 205 | SUB-13 根拠 |
| 0.3 | 30.827 | 219 | — |
| **0.15** | **29.899** | **222** | **tip面既定候補 · SUB-14 根拠** |

※ 旧 tip-cv **14.87** は phys(TVTリーク)面 · **禁止物差し**（[`rootcause`](../docs-ja/discussion/wave20-tipcv-phys-leak-rootcause.md)）。

### Wave-0 CF folds（OOF RMSE）

| fold | n_wells | n_eval | oof_rmse |
|---|---|---|---|
| 1 | 155 | 751824 | 15.773 |
| 2 | 155 | 773474 | 17.922 |
| 3 | 155 | 768452 | 14.826 |
| 4 | 154 | 741764 | 15.726 |
| 5 | 154 | 748475 | 15.071 |

### Hard-well セット

`86454a6f` + CF worst19 → `exp/work/wave0-ruler/hard-wells.json`。以降の変更は hard-set 悪化 >0.1 なら rejected。

---

## 効いた学習変更

- well-GroupKFold 物差しを固定したこと（採用基準が LB 感覚から数値へ）

---

## 効かなかった学習変更・罠

- Typewell 無しの heel `gs` スイープ（0.85/1.15）→ RMSE 大幅悪化
- 近傍 600ft 素朴コピー → 悪化（Discussion と一致）
- 近傍 150ft 素朴コピー → pooled 非改善（シフト合わせ品質不足）
- CF±15 の単純中点 hedge → 数学的に CF と同一（退化）
- 絶対 TVT への線形 MD 外挿を「物理」扱い → 崩壊（Sunny 経路を別途）
- 手元 `test/`（3 wells）でのスコアを LB とみなすこと
- NW_N postprocess blend / tip内 BH 上げ（F006/F009）
- LGBM+NCC（tip高相関）· 素の pure NCC（F007/F008）
- TIP_CV early-exit 後の `_BH_*` セルは走らない → BH 実験は early-exit 前注入必須
- CatBoost residual tabular（CHK-070）は CF超えでも tip corr≈1 → Final2不可（F010）
- ±15ft 二峰を **候補 init** に載せる（CHK-246）→ tip 代理面悪化 · FINAL hedge（F013）とは別だが同方向 NO-GO
- 素朴 LGBM 絶対TVT（CHK-071）は hard20 で CFより大幅悪化
- Wave-24 learned ridge ΔTVT→PF rate（CHK-289）→ tip soft 最良Δ−12.8（F034）
- Wave-24 Newton GR-guide PF（CHK-288）→ tip soft 最良Δ−23.9（F033）
- Wave-24 ESS+MCMC in-gen（CHK-290）→ tip soft 最良Δ−0.51（F035）· ESS↑≠tip改善
- Wave-29 S1a 自前PF（CHK-370）→ local4wellで CF超え1/4のみ · 門番未達
- Wave-29 S1b TinyTCN last-anchor（CHK-373）→ hard20 pooled 55.55 > CF 49.56 · B7閉鎖
- Wave-29 B8 soft→FINAL監査（CHK-380）→ 支配悪化は soft→selector · soft復帰はF015 · ノブ0

