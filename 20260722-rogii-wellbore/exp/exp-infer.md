# exp-infer — rogii-wellbore

> type: inference-submission-analysis  
> updated: 2026-08-06（**COMP CLOSED · Private 確定 · 新規提出なし**）  
> purpose: 推論、後処理、提出、LB、submission notebook の管理

**現在地:** [`exp-index.md`](exp-index.md) · **振り返り:** [`../retro/retro-private.md`](../retro/retro-private.md)  
**Private（CLI 2026-08-06）:** チーム最終 **9.142 · #596 / 6191**（採用面=**666** `55247672`）  
**Public（CLI）:** **6.190 · #144 / 6191**（farvol `55148128`）  
**Final2 LOCK:** 枠1=**666** priv **9.142** · 枠2=**farvol** priv **9.453** · [final2-ops](latest/final2-ops-20260805.md)  
**CLI 生データ:** [`work/post-comp-lb/`](work/post-comp-lb/)  

**締切提出ゲート:** 上振れ未提出 **0** · 新規 submit なし · 再提出禁止 · [deadline](latest/ops-deadline-submit-gate-2026-08-05.md)  
**L1 dual 新面:** 781/784/802 等 **すべて dual NOGO** · residual E2E **昇格なし**  
**CHK-666:** ref **55247672** · Public 6.509 · Private **9.142** · Trust 枠1（Final 採用）  
**farvol 0.95:** ref **55148128** · Public **6.190** · Private **9.453** · 枠2  

---

## Private 確定（事実のみ · 2026-08-06）

| 面 | ref | Public | Private | 備考 |
|---|---|---:|---:|---|
| **Final 採用** | 55247672（666） | 6.509 | **9.142** | チーム Private 順位 #596 |
| Final 枠2 | 55148128（farvol） | **6.190** | 9.453 | Public #144 |
| 履歴最良 Private* | 55252403（702） | 7.394 | **8.986** | Final 未採用 · *自提出ヒスト |

詳細・shake-up: [`../retro/retro-private.md`](../retro/retro-private.md)  
出典: `kaggle competitions submissions` · `leaderboard -s`

---

## 現在のBest提出

| 項目 | 値 |
|---|---|
| Public LB（表示） | **6.190** farvol · 618c **6.231** · **660 6.239** · 558b **6.238** · tip 6.269 · **711 6.359** · **641 6.472** · **666 6.509** · **710 6.613** · **702 7.394** |
| Public LB（実質内容） | **SUB-14** `55006677` · T=0.15 · **6.269**（Trust主成果物） |
| 公式 Rank | （要再取得） |
| Notebook / Script | **Trust主:** SUB-14 `kazeneko77/tip-gated-lik-temp-0p15` Ver1 · **表示診断Best:** farvol **0.95/0.05** · **枠2候補:** 55148128 / 55148294（ユーザー選択） |
| **CHK-420 tip×compound 0.90/0.10** | Ver1 · **55118585** · Public **6.284** · **NO-GO** |
| **CHK-420 tip×farvol 0.95/0.05** | Ver1 · **55148128** · Public **6.190** · **表示Best · 枠2第1候補** |
| **CHK-420 tip×farvol 0.80/0.20** | Ver1 · **55148294** · Public **6.197** · 枠2第2候補 |
| **CHK-420 tip×farvol 0.90/0.10** | Ver1 · **55118587** · Public **6.226** · 旧診断Best |
| **CHK-420 tip×farvol 0.88/0.12** | Ver1 · **55148271** · Public **6.273** · **NO-GO** |
| **CHK-420 tip×farvol 0.85/0.15** | Ver1 · **55148153** · Public **6.314** · **NO-GO**（最悪） |
| **CHK-420 tip×SUB-13 0.80/0.20** | Ver1 · **55122006** · Public **6.247** · ≡14×13 0.90/0.10 · 枠差替なし |
| **CHK-437 tip-post-unlock-r1-t015** | Ver1 · **55118915** · Public **6.250** · **NO-GO**（unlock未発火+ノイズ） |
| **OPS probe 14×13 0.90/0.10** | Ver1 · **55117902** · Public **6.247** · C未満 · 枠差替なし |
| **OPS probe C×13 0.90/0.10** | Ver1 · **55117901** · Public **6.353** · **NO-GO** · 三重blend禁止 |
| tip smoke | `…/rogii-luck-is-all-you-need-private-tip-fork` · **54920651** · Public **6.569** |
| 旧 Best（Contact） | top-repro Ver2 · **54914222** · **6.524** · 別CSV保険 |
| **SUB-20 T0.10** | Ver1 · **55066862** · Public **6.241** · 表示Best · SHA≡14 |
| **OPS-C 14×9 0.90/0.10** | Ver1 · **55094041** · Public **6.237** · 表示Public1 · SHA≠14 · 改善主張なし |
| **OPS-D 14×9 0.75/0.25** | Ver1 · **55094043** · Public **6.276** · C未満 |
| **OPS-B BH=0** | Ver1 · **55093492** · Public **6.274** · SHA≡14 · 効果なし |
| **OPS-A T0.08** | Ver1 · **55093490** · Public **6.323** · SHA≡14 · F025追認 |
| **SUB-19 blend** | Ver3 · **55066793** · Public **6.277** · 枠外 |
| **CHK-458 mid残存** | Ver1 · **55161873** · Public **7.781** · **NO-GO · F042**（重複55161881=**7.760**） |
| **SUB-18 E2E** | Ver1 · **55066050** · Public **7.705** · 枠禁止（重複55066056=7.768） |
| **SUB-14 T0.15** | Ver1 · **55006677** · Public **6.269** · **実質 Best / 枠1** |
| **SUB-13 T0.5** | Ver1 · **55001828** · Public **6.419** · Final保険 |
| **SUB-9 gated** | Ver1 · **54972467** · Public **6.484** · Trust候補 |
| **SUB-11 gated s05** | Ver1 · **54986210** · Public **6.530** · 強度軟化 NO |
| **SUB-10 CHK-184** | Ver1 · **54983914** · Public **6.541** · 枠外 |
| **SUB-12 portable 複合** | Ver1 · **54986214** · Public **6.556** · Trust≠Public |
| **SUB-8 SOFT** | Ver1 · **54970975** · Public **6.582** · 打ち切り |
| VISUALS | Frontier Lab Ver2 · **54958520** · Public **6.581** · Best未満 |
| Sunny SUB-1 | **54935410** · **9.150** · **F004** |
| SUB-2 BH-off | **54937708** · **6.599** · 枠2不採用 |
| SUB-3 mpkg020 copy | **54937788** · Scoring Error · **F005** |
| SUB-4 gated_010 | **54958356** · **6.718** · **F015** |
| SUB-5 pre-BH | **54958359** · **6.653** · **F015** |
| SUB-6 gated_020 | **54958970** · **6.621** · **F015**（中間面では最良だが tip より悪化） |
| SUB-7 mpkg-only | **54958971** · **20.067** · **F015** 壊滅 |
| 作者 tip 公開 | opencv411 · **6.478** |
| 後処理 | tip: `vp_balanced_modelpkg_005` · `_BH_*` hedge（**触らない**）· SOFT は別 kernel |
| 提出ファイル | submission.csv（Notebook 紐づけ） |

**tip CV:** T1 hard20 pooled **14.87** · T2/T3 **8.330** · gated self_dev>8 T2 **8.246**（samp −0.043）· SOFT f33-s08 T2 **8.261**（samp −0.076）· [`tip-cv-report-t2.json`](work/wave0-ruler/tip-cv-report-t2.json)

**読み（2026-08-05 · 660/666 Public）:** 660 **6.239**（tip近傍・枠2未達）· 666 **6.509**（Public NO-GO · 641より悪）· mid residual α↑=Public悪化 · tip residual は Public を壊さない · Final2=枠1 Trust666 / 枠2 farvol 不変 · 次=L · [`ops-660-666`](latest/ops-lb-chk660-666-public-2026-08-05.md)。

**読み（2026-08-04 · 641 Public）:** residual α0.30 **6.472** · tip+0.203 · **Public NO-GO** · Trust dual は捨てない · 666 は予想通り更に悪化 **6.509** · [`ops-641`](latest/ops-lb-chk641-public-2026-08-04.md)。

**読み（2026-08-04 · 618c Public）:** **6.231** · farvol 次点だが +0.041 · tipdist 11.9 で **Private 危険** · 枠2NO · 620 soft→mid 再開しない · [`ops-618c`](latest/ops-lb-chk618c-public-2026-08-04.md)。

**読み（2026-08-04 · 541/558b Public）:** 558b **6.238** · 541 **6.256** · 枠2 farvol 固定 · [`541-558b`](latest/ops-lb-chk541-558b-public-2026-08-04.md)。

**読み（2026-08-01 farvol α）:** 表示Best **6.190**（0.95/0.05）· 第2 **6.197**（0.80/0.20）。中間α 0.12/0.15 は **6.273/6.314** で NO-GO（U字· tip-cvと逆）。Δ≈1.2σ · Trust枠1はSUB-14据え置き · 枠2差替はユーザー。詳細 [`farvol-α`](latest/ops-lb-wave31-farvol-alpha-public-2026-08-01.md) · [`421`](work/wave31-nonssoft-blend/chk421-farvol-candidate-2026-08-01.md)。

**読み（2026-08-01 Wave-31c）:** tip-cvの451/456はGOだが **E2E FINAL≡SUB-14**（before_hedgeのみ差分・後段崩壊）。提出不可。枠2は farvol/OPS-C。詳細 [`harvest`](work/wave31-selector-replace/out-451-e2e/chk451-e2e-harvest.md) · [`checklist`](experiment-checklist.md)。

**読み（2026-07-31 OPS-LB overnight）:** farvol **6.226** · C **6.237** · 14×13 **6.247** / 437 **6.250** はノイズ帯。compound **6.284** と C×13 **6.353** は明確 NO-GO。詳細 [`ops-lb-overnight`](latest/ops-lb-wave31-overnight-public-2026-07-31.md)。

**読み（2026-07-30 Wave-29）:** B7(S1a PF / S1b TCN) とも CF門番未達 · B8は soft→selector 支配悪化で安全ノブ0（F015）。**新規提出なし**。Final枠2は Public1 C のまま（別面差替なし）。

**読み（2026-07-30 OPS-LB-ABCD）:** C **6.237**が表示Public1だが旧Best差−0.004でノイズ。A/B/SUB-14/SUB-20の同一ローカル面は6.241–6.323（σ≈0.034）で、既知ノイズ床と整合。Cは枠2運用のみ、改善GOではない。A/B/DはNO-GO。詳細 [`ops-lb-abcd`](latest/ops-lb-abcd-public-2026-07-30.md)。

**読み（2026-07-29 OPS-LB-PEND）:** T0.10 表示 **6.241**だが最終 CSV **SHA≡SUB-14**（F025 が T=0.10 にも波及）→ Δ0.028=ノイズ帯。blend **6.277** 枠外。SUB-18 **7.705** 中間面 final 化は壊滅。詳細 [`ops-lb-pend`](../docs-ja/ops-lb-pend-public-2026-07-29.md)。

**読み（2026-07-27 OPS-LB-SUB15）:** twostage Public **6.494**（重複 **6.564**）。Best 6.269 / T0.5 6.419 / gated 6.484 をいずれも超えず → **portable/twostage 系は Public 閉鎖**。同一提出の Δ0.070 は非決定性の追認。詳細 [`ops-lb-sub15`](../docs-ja/ops-lb-sub15-twostage-public-2026-07-27.md)。

**読み（2026-07-27 OPS-LB-SUB1314）:** **SUB-14 Public 6.269**（T=0.15）。tip-cv（29.899≪32.276）と Public（6.269≺6.419）が **同符号**。同一 T0.5 kernel の 6.419 vs 6.530 は非決定性疑い。詳細 [`ops-lb-sub1314`](../docs-ja/ops-lb-sub1314-public-2026-07-27.md)。

**読み（2026-07-26 OPS-LB-101112）:** 当時 Best=SUB-9 6.484。s05/portable は枠外。詳細 [`ops-lb-101112`](../docs-ja/ops-lb-101112-public-2026-07-26.md)。

---

## Final 2 候補方針（2026-07-30 · OPS-LB-ABCD 後）

| 枠 | 候補 | 家系 | 備考 |
|---|---|---|---|
| 枠1 | **CV 1位** → **SUB-14** | tip+lik_temp T0.15 | tip-cv 29.899 凍結（T0.10 は +0.051 未達） |
| 枠2 | **Public最良候補** → **farvol 55148128**（0.95/0.05）または **55148294**（0.80/0.20）· 旧OPS-C可 | tip×farvol / 14×9 | ユーザーUI選択 · 表示Best 6.190（≈1.2σ）· Agent差替なし |
| 却下 | A/B/D · C×13 · compound · 437 · SUB-19 · SUB-18 · portable/SOFT/Sunny | — | overnightでC×13/compound/437追認 NO-GO |

**予測台帳:** [`docs-ja/cv-public-private-forecast.md`](../docs-ja/cv-public-private-forecast.md)

---

## 提出履歴

| submit_ref | 日付 UTC | Notebook | 変更の要約 | Public LB | 判断 |
|---|---|---|---|---|---|
| **55248920** | 2026-08-05 | **tip-e2e-chk660-tip-alpha-l-resid** | CHK-660 tip+α0.50 L resid agree | **6.239** | tip−0.030 · farvol+0.049 · **枠2NO** · diversify · 再提出禁止 · [`ops`](latest/ops-lb-chk660-666-public-2026-08-05.md) |
| **55247672** | 2026-08-05 | **tip-e2e-chk666-mid-a035-l-resid** | CHK-666 mid+α0.35 residual | **6.509** | tip+0.240 · **Public NO-GO** · Trust only · 641より悪化 · 再提出禁止 · 同上 |
| **55223002** | 2026-08-03 | **tip-e2e-chk641-mid-alpha-l-resid** | CHK-641 mid+α0.30 residual | **6.472** | tip+0.203 · **Public NO-GO** · Trust only · [`ops-641`](latest/ops-lb-chk641-public-2026-08-04.md) |
| **55222561** | 2026-08-03 | **tip-e2e-chk618c-soft-diag-agree** | CHK-618c tip⊕soft_diag | **6.231** | tip−0.038 · **枠2NO** · tipdist11.9 · [`ops-618c`](latest/ops-lb-chk618c-public-2026-08-04.md) |
| **55221471** | 2026-08-03 | **tip-e2e-chk558b-agree-only-p495** | CHK-558b tip⊕agree-only P-495 | **6.238** | tip−0.031 · **枠2NO** · [`541-558b`](latest/ops-lb-chk541-558b-public-2026-08-04.md) |
| **55221459** | 2026-08-03 | **tip-e2e-chk541-agree-p495** | CHK-541 tip⊕agree∧row P-495 | **6.256** | tip−0.013 · **枠2NO** · 同上 |
| **55206184** | 2026-08-03 | **tip-e2e-chk579-row-p495** | CHK-579 tip⊕row P-495 | **6.277** | 枠2NO-GO · [`ops-lb-579`](latest/ops-lb-chk579-public-2026-08-04.md) |
| **55195981** | 2026-08-02 | **tip-submit-chk515-row-signed-or-absd2** | CHK-515 tip×468 before · row gate | **6.249** | **≈tip** · Best未達 · 枠外 · [`514-LB`](latest/ops-lb-chk514-public-2026-08-03.md) |
| **55195975** | 2026-08-02 | tip-submit-chk514（誤再送） | CHK-514 二重 | **6.346** | 枠浪費 · 再送禁止 |
| **55195968** | 2026-08-02 | **tip-submit-chk514-hd-fracSpos07** | CHK-514 tip×468 before · **H-D** | **6.335** | **NO-GO** · tip+0.066 · Trust≠Public · 同上 |
| **55193007** | 2026-08-02 | **tip-blend-chk485-468-se040** | CHK-485 SE a0.40/o0.10 | **6.265** | **≈tip（ノイズ）** · 枠外 · [`485-LB`](latest/ops-lb-chk485-public-2026-08-03.md) |
| **55192995** | 2026-08-02 | **tip-blend-chk485-468-se060** | CHK-485 SE a0.60/o0.10 | **6.304** | **NO-GO** · tip+0.035 · Trust≠Public · 同上 |
| **55148294** | 2026-08-01 | **tip-blend-sub14-farvol-080-020** | farvol α0.20 · CHK-420 grid | **6.197** | 枠2第2候補 · [`farvol-α`](latest/ops-lb-wave31-farvol-alpha-public-2026-08-01.md) |
| **55148271** | 2026-08-01 | **tip-blend-sub14-farvol-088-012** | farvol α0.12 · CHK-420 grid | **6.273** | **NO-GO** · 中間α毒 |
| **55148153** | 2026-08-01 | **tip-blend-sub14-farvol-085-015** | farvol α0.15 · CHK-420 grid | **6.314** | **NO-GO** · tip-cv推しαが最悪 |
| **55148128** | 2026-08-01 | **tip-blend-sub14-farvol-095-005** | farvol α0.05 · CHK-420 grid | **6.190** | **表示Best · 枠2第1候補** · CHK-421 GO |
| **55122006** | 2026-07-31 | **tip-blend-sub14-sub13-080-020 Ver1** | tip×SUB-13 **0.80/0.20** · CHK-420 | **6.247** | ≡55117902 · C+0.010 · 枠差替なし · SUB-13比率追加禁止 |
| **55118915** | 2026-07-30 | **tip-post-unlock-r1-t015 Ver1** | CHK-437 post-unlock E2E | **6.250** | **NO-GO** · C+0.013ノイズ · unlock未発火 · [`overnight`](latest/ops-lb-wave31-overnight-public-2026-07-31.md) |
| **55118585** | 2026-07-30 | **tip-blend-sub14-compound-090-010 Ver1** | CHK-420 tip×portable-compound **0.90/0.10** | **6.284** | **NO-GO** · tip+0.015 · portableパートナー失敗 |
| **55118587** | 2026-07-30 | **tip-blend-sub14-farvol-090-010 Ver1** | CHK-420 tip×portable-farvol **0.90/0.10** | **6.226** | 旧診断Best · αグリッドで降格 · [`overnight`](latest/ops-lb-wave31-overnight-public-2026-07-31.md) |
| **55117902** | 2026-07-30 | **tip-blend-sub14-sub13-090-010 Ver1** | SUB-14×SUB-13 **0.90/0.10** | **6.247** | C+0.010 · 枠差替なし · SUB-13比率追加スイープ禁止 |
| **55117901** | 2026-07-30 | **tip-blend-ops-c-sub13-090-010 Ver1** | OPS-C×SUB-13 **0.90/0.10** · 実質14/9/13 | **6.353** | **NO-GO** · C+0.116 · 三重blend禁止 |
| **55094043** | 2026-07-29 | **tip-blend-sub14-sub9-075-025 Ver1** | OPS-D · 14×9 **0.75/0.25** | **6.276** | **NO-GO** · Cより+0.039 · ノイズ帯 |
| **55094041** | 2026-07-29 | **tip-blend-sub14-sub9-090-010 Ver1** | OPS-C · 14×9 **0.90/0.10** | **6.237** | **表示Public1 / 枠2暫定** · 改善主張なし |
| **55093492** | 2026-07-29 | **tip-gated-bh-strength-0 Ver1** | OPS-B · T0.15 · BH=0 diagnostic | **6.274** | **NO-GO** · SHA≡14 · hedge効果なし |
| **55093490** | 2026-07-29 | **tip-gated-lik-temp-0p08 Ver1** | OPS-A · T=0.08 diagnostic | **6.323** | **NO-GO** · SHA≡14 · F025追認 |
| **55066862** | 2026-07-28 | **tip-gated-lik-temp-0p1 Ver1** | **SUB-20** T=0.10 diagnostic | **6.241** | 表示Best · **SHA≡SUB-14** · ノイズ · [`ops-lb-pend`](../docs-ja/ops-lb-pend-public-2026-07-29.md) |
| **55066793** | 2026-07-28 | **tip-blend-sub14-sub13-e2e Ver3** | **SUB-19** 14×13 0.85/0.15 | **6.277** | 枠外 · Δ+0.008 |
| **55066050** | 2026-07-28 | **tip-e2e-learned-traj Ver1** | **SUB-18** E2E learned_trajectory（F005 remake） | **7.705** | 枠禁止 · 誤重複 **55066056**=**7.768** · [`ops-lb-pend`](../docs-ja/ops-lb-pend-public-2026-07-29.md) |
| **55037034** | 2026-07-27 | **tip-gated-lik-temp-0p3 Ver1** | **SUB-16** T=0.3 梯子 | **6.385** | Best外 · F025 |
| **55012195** | 2026-07-26 | **tip-portable-twostage-s05 Ver1** | **SUB-15** CHK-197 診断 | **6.494** | Best外 · 重複55012192=**6.564** · [`ops-lb-sub15`](../docs-ja/ops-lb-sub15-twostage-public-2026-07-27.md) |
| **55006677** | 2026-07-26 | **tip-gated-lik-temp-0p15 Ver1** | **SUB-14** CHK-220b T0.15 | **6.269** | **実質 Best / 枠1** · [`SUBMIT`](../my-submitted-notebook/tip-gated-lik-temp-0p15/SUBMIT.md) |
| **55001828** | 2026-07-26 | **tip-gated-lik-temp-0p5 Ver1** | SUB-13 CHK-212 Best+T0.5 | **6.419** | Final保険 · notebook-linked |
| **55001822** | 2026-07-26 | tip-gated-lik-temp-0p5 Ver1 | SUB-13 重複 | **6.530** | 同kernel · 非決定性 · 枠浪費 |
| **54986214** | 2026-07-25 | **tip-portable-compound-s05 Ver1** | SUB-12 portable 複合+s05 | **6.556** | Trust≠Public · 枠外 |
| **54986210** | 2026-07-25 | **tip-gated-selfline-selfdev8-s05 Ver1** | SUB-11 gated>8 s05 | **6.530** | Best+0.046 · 強度軟化 NO |
| **54983914** | 2026-07-25 | **tip-chk184-portable-farvol Ver1** | SUB-10 portable+farvol | **6.541** | tip帯 · 枠外 |
| **54972467** | 2026-07-25 | **tip-gated-selfline-selfdev8 Ver1** | SUB-9 gated self_dev>8 | **6.484** | 旧 Public Best |
| **54970975** | 2026-07-25 | **tip-soft-selfline-f33s08 Ver1** | SUB-8 SOFT f33-s08 | **6.582** | tip+0.013 · 打ち切り |
| 54958971 | 2026-07-24 | **tip-e2e-promote-mpkg-only Ver1** | SUB-7 model_package_only | **20.067** | **F015** 壊滅 |
| 54958970 | 2026-07-24 | **tip-e2e-promote-mpkg020 Ver1** | SUB-6 gated_020 | **6.621** | tip+0.052 · **F015** |
| 54958520 | 2026-07-24 | **VISUALS Ver2** | Frontier Lab | **6.581** | Best未満 |
| 54958359 | 2026-07-24 | **tip-e2e-promote-pre-bh Ver1** | SUB-5 before_BH | **6.653** | tip+0.084 · **F015** |
| 54958356 | 2026-07-24 | **tip-e2e-promote-mpkg010 Ver1** | SUB-4 gated_010 | **6.718** | tip+0.149 · **F015** |
| 54937788 | 2026-07-23 | tip-mpkg020-as-submission | SUB-3 コピー | **Scoring Error** | **F005** |
| 54937708 | 2026-07-23 | tip-bh-strength-off | SUB-2 BH=0 | **6.599** | 枠2不採用 |
| 54935410 | 2026-07-23 | Sunny physical | SUB-1 | **9.150** | **F004** |
| 54920651 | 2026-07-23 | luck-private-tip-fork | tip smoke | **6.569** | tip 基準 |
| 54914222 | 2026-07-22 | top-reproducible-pf… Ver2 | Contact-Gated | **6.524** | **旧 Best · 枠2保険** |
| 54888184 | 2026-07-21 | hahaha-nondet-agi Ver2 | nondet | 6.644 | 旧 Best |
| 54863463 | 2026-07-20 | det-mha180sep3 Ver2 | hedge α=1.8 | 6.906 | |
| 54837764 | 2026-07-19 | det-mha140sep4 Ver2 | α=1.4 | 6.979 | |
| 54814286 | 2026-07-18 | det-mha120sep4mpkg10 | α=1.2+mpkg | 7.003 | package 不利 |

---

## tip 後処理 ablation（Public）

| 面 | Public | tip final 比 | 含意 |
|---|---|---|---|
| tip final（mpkg005+BH） | **6.569** | — | **現状 tip の最終面を維持（枠1）** |
| gated tip_self_line self_dev>8 | **6.484** | tip−0.085 | 旧Best · Trust候補 |
| SOFT tip_self_line f33-s08 | **6.582** | tip+0.013 | **打ち切り** |
| gated_020 as final | 6.621 | +0.052 | package 強化は悪化 |
| pre-BH / BH-off | 6.653 / 6.599 | +0.084 / +0.030 | hedge は残す |
| gated_010 as final | 6.718 | +0.149 | さらに悪化 |
| mpkg-only | 20.067 | +13.5 | 絶対禁止 |

---

## 次アクション

- [x] tip smoke · SUB-1–7 Public 反映
- [x] F015 台帳追記
- [x] SUB-8 提出 · Public **6.582**（打ち切り）
- [x] SUB-9 gated 提出 · Public **6.484**（新Best）
- [x] OPS-LB-89: Public 確定 · forecast/本表更新
- [x] CHK-184 / SUB-10 · Public **6.541**（枠外）
- [x] CHK-191 / SUB-11 · Public **6.530**（強度軟化 NO）
- [x] CHK-178 / SUB-12 · Public **6.556**（Trust≠Public）
- [x] OPS-LB-101112 · Final 仮更新 · [`ops-lb-101112`](../docs-ja/ops-lb-101112-public-2026-07-26.md)
- [x] SUB-13 CHK-212 Public **6.419**（ref 55001828）
- [x] SUB-14 CHK-220b Public **6.269 Best**（ref 55006677）· [`ops-lb-sub1314`](../docs-ja/ops-lb-sub1314-public-2026-07-27.md)
- [x] CHK-231 weight/variant **NO-GO（F022）** · 提出なし
- [x] SUB-15 twostage Public **6.494**（重複 6.564）· Best外 · [`ops-lb-sub15`](../docs-ja/ops-lb-sub15-twostage-public-2026-07-27.md)
- [x] OPS-LB-PEND: T0.10 **6.241** · blend **6.277** · SUB-18 **7.705** · [`ops-lb-pend`](../docs-ja/ops-lb-pend-public-2026-07-29.md)
- [x] Wave-29 B7/B8 **CLOSED**（別面門番未達 · 後段ノブ0）· 提出なし
- [ ] **OPS-FINAL2 UI:** 枠1=**SUB-14** · 枠2=**Public1 farvol 0.95/0.05**（`55148128`）または 0.80/0.20 / 旧C · ユーザー操作 · [`prep`](../docs-ja/ops-final2-prep-2026-07-26.md)
- [ ] Parked CHK-110–112 は **承認後のみ**
- [ ] T0.10–0.3 最終≡再提出 · blend · learned_traj · portable **再提出しない**

---

## 禁止（提出）

- Sunny 再提出（F004）· `kernel_sources` コピー（F005）
- BH-off / pre-BH / gated_mpkg / mpkg-only の再提出（**F015**）
- tip `SUBMISSION_PROFILE` だけの再提出（最終≡tip · F013）
- 攻撃的 tip_self_line 再スイープ（**F020**）· SOFT の枠1自動昇格

