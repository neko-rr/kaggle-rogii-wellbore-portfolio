# checklist-archive — rogii-wellbore

> type: checklist-archive  
> updated: 2026-08-06（**コンペ終了 · L1 全 dual 結果凍結**）  
> participant: Kazeneko

**役割:** 終了した CHK（done / rejected / NO-GO）と旧 Wave 表の保管。  
**作業キューではない。** 現在地: [`exp-index.md`](exp-index.md) · checklist Active は空。

---

## 移設ルール

- Active で `done` / `rejected` / **NOGO_L1 確定** になった行は本ファイルへ
- 行には hypothesis 要約・結果1行・リンクを残す
- 抽象禁止は failures 台帳にも（再掲で Active に戻さない）

---

## 2026-08-06 移設 — コンペ終了 · residual-path / Huber / 777 停止

> 数値: [781 dual](work/out-t3-cpu-harvest/l-dual-CHK-781-kaggle-v1/report.md) · [784 ops](latest/ops-chk784-dual-nogo-2026-08-05.md) · [laws](latest/l-improvement-laws-2026-08-05.md) · **F044 · F045**

| 帯 | CHK | 結果1行 | ref |
|---|---|---|---|
| **L1 residual-path** | **781** | Kaggle FAST2 · hard Δ**+0.44** · hybrid **+0.19** · d\|L−mid\| **−0.97** · Q4 **+0.21** · **NOGO_L1 · F046 · E2E 禁止** · Pack D 天井は live 未再現 | [report](work/out-t3-cpu-harvest/l-dual-CHK-781-kaggle-v1/report.md) · [post](latest/ops-chk781-post-pipeline-2026-08-05.md) · [kernel](https://www.kaggle.com/code/kazeneko77/tip-cv-chk781-resid-path-h20) |
| **L1 Huber loss** | **784** | Colab FAST2 · hard Δ**+6.27** · hybrid **+2.86** · d\|L−mid\| **−4.06** · raw L hard **26.9** · **NOGO · F045** | [ops](latest/ops-chk784-dual-nogo-2026-08-05.md) · run `20260805-143010-chk784-huber-hard20-fast2` |
| **L1 reg↑** | **777** | body / gate pre のみ · dual **未実施** · **締切停止 · incomplete** | [ops](latest/ops-chk777-regup-colab-2026-08-05.md) · body `exp/work/colab-final-t2/_colab_main_body_chk777.py` |
| **Final2** | **OPS** | 枠1 **666** · 枠2 **farvol** · LOCK | [final2](latest/final2-ops-20260805.md) · [exp-index](exp-index.md) |

**終了読み:** weight（F044）· residual-path live · Huber loss はいずれも dual 悪化。Trust 提出面は **旧 666** のまま。Public は **farvol**。

---

## 2026-08-05 移設 — L1 dual NOGO · mid-collapse（688 / 761 / 782 / 804 / **802**）

> 数値: dual reports · [ops-804](latest/ops-l1-chk804-colab-dual-2026-08-05.md) · [ops-802](latest/ops-chk802-dual-nogo-2026-08-05.md) · [post-802](latest/ops-chk802-post-pipeline-2026-08-05.md) · [ops-761-782](latest/ops-l1-chk761-782-harvest-dual-2026-08-05.md) · [laws](latest/l-improvement-laws-2026-08-05.md) · **F044**

| 帯 | CHK | 結果1行 | ref |
|---|---|---|---|
| **L1 MD-Q4 行** | **802** | Colab FAST2 · OOF **9.38** · hard Δ**+1.79** · hybrid **+0.79** · B_Q4 **+1.02** · d\|L−mid\| **−4.24** · **moderate collapse · E2E ABORT · F044 閉** | [dual](work/out-t3-cpu-harvest/l-dual-CHK-802-colab-fast2/report.md) · [ops](latest/ops-chk802-dual-nogo-2026-08-05.md) · [post](latest/ops-chk802-post-pipeline-2026-08-05.md) |
| **L1 known×Q4** | **804** | Colab v1c · hard Δ**+0.74** · hybrid **+0.33** · d\|L−mid\| **−1.43** · OOF 9.13 でも NOGO · **mild mid-collapse · F044 · 再学習禁止** | [dual](work/out-t3-cpu-harvest/l-dual-CHK-804-colab/report.md) · [ops](latest/ops-l1-chk804-colab-dual-2026-08-05.md) · [face](work/out-t3-cpu-harvest/chk804-colab-face-20260805/) |
| **L1 fold-driver** | **761** | hard Δ**+4.01** · hybrid **+1.81** · **mid-collapse** \|L−mid\| **−7.93** · **NOGO_L1 · 再実行禁止** | [dual](work/out-t3-cpu-harvest/l-dual-CHK-761-harvest/report.md) · [ops](latest/ops-l1-chk761-782-harvest-dual-2026-08-05.md) · [harvest](work/out-t3-cpu-harvest/watch-v2-20260805/harvest-761/) |
| **L1 resid-drag** | **782** | hard Δ**+3.81** · hybrid **+1.71** · 同 mid-collapse · 688hurt **+4.18** · **NOGO_L1 · 再実行禁止** | [dual](work/out-t3-cpu-harvest/l-dual-CHK-782-harvest/report.md) · 同上 · [harvest](work/out-t3-cpu-harvest/watch-v2-20260805/harvest-782/) |
| **L1 baseline retrain** | **688** | hard Δ**+0.52** · hybrid **+0.23** · **NOGO_L1** · この帯最良の失敗 | [dual](work/out-t3-cpu-harvest/l-dual-auto-688/report.md) |
| **監視** | **WATCH-V2** | 761/782 harvest+dual 完了 · 804 Kaggle CANCEL | [dir](work/out-t3-cpu-harvest/watch-v2-20260805/) |
| **tip-e2e 診断** | **669** | tip-e2e 診断 · 提出禁止 | harvest-669 |
| **CPU** | **CPU-GAP-b · P0P1 · expert-C · L-CPU-EDA · Pack D** | map/oracle · oracle 順は **壊れ方**のみ · Pack D 781 設計 | [gap-b](work/out-t3-cpu-harvest/cpu-cv-gap-20260805b/) · [p0p1](work/out-t3-cpu-harvest/cpu-parallel-p0p1-20260805/) · [C](work/out-t3-cpu-harvest/cpu-expert-pack-c-20260805/) · [PackD](latest/ops-cpu-pack-d-residual-path-2026-08-05.md) |
| **CV ops pack** | **790 · 791 · 796–801** | dual 平面/8seed · mid-pull NOGO · GO_ops | pack reports |
| **Public 診断（同日）** | **711 · 710ssot · 702** | Pub **6.359 / 6.613 / 7.394** · 再提出禁止 · residual 梯子 | [ops](latest/ops-lb-chk711-710-702-public-2026-08-05.md) |

**失敗モード要約（F044）:** hard/Q4/drag/**MD-Q4 行** **sample_weight** retrain → L が mid に吸い寄せ residual 悪化。OOF/offline 改善は dual と非対応。dual NOGO 後の residual E2E も禁止。  
**次（当時）:** 781 residual-path → **live も NOGO（上節 2026-08-06）**。

---

## 2026-08-05 移設 — Final Push 薄化（643–766 done / 定規 A）

> Active から一括。数値 SSOT: `hyperparameter-table` · `within-stage-comparisons` · faces **041247**

| 帯 | CHK | 結果1行 | ref |
|---|---|---|---|
| mid ladder | **643 · 677 · 697(=673)** | blend **w0.50** mid 材料 · tipdist 3.298 map · 生 mid FINAL 禁止 | [ladder](work/colab-final-t2/out-643-ladder-v2-local/report.md) · [697e2e](work/wave31-neural-proposal/out-697-702-e2e-analysis/report.md) |
| residual mid上 | **676 · 702 · 710** | w050 residual tipdist **≥4.14 NOGO** · FIXED3 空 · 固定α閉鎖 | [cascade](work/wave31-neural-proposal/out-710-downstream-cascade/report.md) |
| soft residual | **695 · 704 · 712 · 715** | tipdist/T2 割れ · soft 置換不可 | [wave](work/colab-final-t2/out-695-704-712-wave/report.md) · [1h](work/out-t3-cpu-harvest/session-1h-cv-20260805/report.md) |
| F043 α政策 | **736 · 737 WATCH · 741 · 745 · 746 · 738** | 特徴α 予測不能 · tipdist dual 全敗 · 現 L α言い換え閉 | [745](work/colab-final-t2/out-745-well-alpha-policy/report.md) |
| tip⊕ / blend | **711 · 697b · 735 · 758** | tip-close map only · Trust 外 · w0.45 NOGO | [711](work/wave31-neural-proposal/out-711-e2e-analysis/report.md) |
| 666 CV wave | **730–735 · 742 · 744 · 725** | α0.35 lock · Final2 LOCK · composite no-auto | [730](work/colab-final-t2/out-730-cv-from-666/report.md) |
| T3-A/B 定規 | **747–755 · 760 · 763 · 748–751 · 754** | 三点制 · 041247 再測 · band filter · flip0 | [750](work/out-t3-cpu-harvest/catalog-faces-041247/report.md) · [752](work/out-t3-cpu-harvest/chk752-755-763/report.md) |
| 1h diagnostics | **765 · 766 · 739 · 749 · 757 design** | oracle gap 3.53 · resid>L 41 · L win 17/20 · weights v2 | [1h](work/out-t3-cpu-harvest/session-1h-cv-20260805/report.md) · [insights](work/out-t3-cpu-harvest/chk754-757-763-insights/report.md) |
| candgen 診断A | **683–687 · 722 · 694** | ceiling OPEN · SP45 非≡ | [diagA](work/colab-final-t2/out-candgen-diag-a-20260804/report.md) |
| Public 梯子 | **664 · 618c · 558b · 541 · 579 · 641 · 660 · 666** | 枠2=farvol · mid residual Public NO · 660=6.239 枠2NO · 再提出禁止 | [ops 660/666](latest/ops-lb-chk660-666-public-2026-08-05.md) |
| residual 候補 | **668 · 644 · 661–663** | map/E2E 済 · 提出しない | harvest 系 |
| soft mid | **620 · 621 · 717** | 注入閉 · dump のみ | — |
| 上流ルール | **670–682 · 678–680 · 721** | applied | — |
| 面マップ | **CV gaps fill · T3-catalog** | done | [fill](work/colab-final-t2/out-cv-gaps-fill-20260804/report.md) |
| **666** | 提出1回 · Public **6.509** | **Public NO-GO · Trust only** · 再提出禁止 · [ops](latest/ops-lb-chk660-666-public-2026-08-05.md) | [val](../docs-ja/submission-validations/2026-08-05-chk666-submit.md) |
| **660** | tip residual diversify 1回 | Public **6.239** · farvol+0.049 · **枠2NO** · 再提出禁止 · 同上 | [val](../docs-ja/submission-validations/2026-08-05-chk660-submit.md) |

**Active 本命（薄化後）:** Colab **802** or **781 path loss** · Final2 · OPS-FINAL2  
**L 詳細 status:** [`l-relearn-session-guide.md`](l-relearn-session-guide.md) §5  

---

## 2026-08-04 移設 — Final Push 済 / rejected / 方針

> Active から移動。詳細は各 report · 数値 SSOT は hyperparameter-table / exp-index。

| CHK | 仮説（短） | 結果 | ref |
|---|---|---|---|
| **642** | tip\|mid 井 oracle 天井 | **STOP** Δ+0.062≪0.15 · 切替R&D禁止 | [`640-642`](work/colab-final-t2/out-640-642-climb/report.md) |
| **640** | 固定3井 tip | **GO_small** 12.217 ≡oracle · 継続不要 | 同上 |
| **641** | mid+α(L−m) 格子 | **GO_t2** best α0.30 **10.309** · 提出禁止 · 追試は Active **641f** | 同上 |
| **645** | H-D救済/frac減廃止 | **done_stop** Explicit | t2-stage-climb |
| **625** | 井切替一般化 | **closed→642** | t2-climb |
| **579** | tip⊕row Public診断 | Public **6.277** ≈tip · 枠2NO-GO · **再提出禁止** | [`ops-lb`](latest/ops-lb-chk579-public-2026-08-04.md) |
| **615 / 631 / 632** | 579分岐 · rowSTOP · 枠2方針 | **applied / done_policy** · farvol固定 | 同上 · [`615`](work/wave31-neural-proposal/out-615-branch-table/chk615-579-branch.md) |
| **636** | soft_diag/618c を Public主策 | **方針NOGO** · Trust専用 | t2-public |
| **618b/618c** | tip⊕soft_diag agree | **GO_e2e** · tipdist 11.933 · **提出禁止** | [`618c`](work/wave31-neural-proposal/out-618c-e2e-analysis/report.md) |
| **612** | tip×partner α表 | **done** tipdist多様性 | [`612`](work/wave31-neural-proposal/out-612-601-bath2h/report.md) |
| **603–607** | Soft/ESS ゲート注入 | **done** soft注入GO · mid注入のみNOGO | [`603-607`](work/wave31-neural-proposal/out-603-607-bath2h/report.md) · [`604-606`](work/wave31-neural-proposal/out-604-606-bath2h/report.md) |
| **604–606** | ESS/合意/absMid | **done** Trust 19–21帯 | 同上 |
| **600 / 602** | Soft→ゲート · peaky tip固定 | **rejected** · Soft FINAL禁止 | [`600-602`](work/wave31-neural-proposal/out-600-602-soft-peaky/report.md) |
| **592** | agree∧\|L−tip\|≥3 | **rejected** · sample FAIL · ≡591 | [`592`](work/wave31-neural-proposal/out-592-agree-micro/report.md) |
| **610 / 611 / 616 / 617** | 逆井HD · 安定/BL | **rejected** | [`610-613`](work/wave31-neural-proposal/out-610-613-reverse-safe/report.md) · bath2h |
| **613** | frac≤0.15 cap | **done** · 558b 既に安全帯 | 同上 |
| **595/596** | Trust≠Public 確認 · 診断優先 | **resolved→630** · 541/558b 提出済 | ops-lb · submit vals |
| **S1S2 / 590–591** | digest · 同時帯 | **済** · 同時帯NOGO | s1s2 backlog |

**運用メモ（2026-08-04）:** Active に done/rejected を残さない。score_wait（630/558b）と blocked/pending のみ。

---

## 全文スナップショット（2026-07-27）

Wave-0〜20 の詳細表・Stop 全文・Parked・EDA 突合は次に保存した（Active スリム化時）:


- [`archive/checklist-active-snapshot-2026-07-27.md`](archive/checklist-active-snapshot-2026-07-27.md)

---

## Archived CHK（索引 · Wave-12 以降を優先）

| CHK | 仮説（短） | 結果 | ref |
|---|---|---|---|
| CHK-160–162 | 難易度ゲート SOFT | GO · SUB-9 | wave12 |
| CHK-150–151 | tip 遠MD 自己線 | F020 · SUB-8 打ち切り | wave11 |
| CHK-170–178 · 191 | gated 洗練 · portable · s05 | Public 枠外 / Best 維持 | wave13 · ops-lb-101112 |
| CHK-180–184 | 井型 A/B · farvol | 183 GO screen · 184 Public NO | wave14 |
| CHK-185–189 | 候補天井 · generator | 185 GO · 186 mixed · 188/189→W20 | wave15–16 |
| CHK-192–198 | mid soft / tip_std | tip_std 軸 · farvol≻twostage | wave17 |
| CHK-199–201 · 195r | F 狭帯監査 | 新規レバーなし | wave18 |
| CHK-202 | tip×mid 薄混ぜ | NO-GO | wave19 |
| CHK-203–204 | upstream dump / stage gap | ERROR / NO-GO | wave20 |
| CHK-205–222 | lik_temp · selector | **T0.15 Best** | wave20 · ops-lb-sub1314 |
| CHK-207–217 | generator / spr | oracle↑ · tip 面 spr12 NO | wave20 |
| CHK-223–230 | T≤0.10 · topk · PF aux 等 | 全 NO-GO | wave20 |
| CHK-231 | weight/variant | NO-GO · F022 | chk231ac |
| **CHK-232–253** | Wave-21 上流/中間 | **全 rejected**（254/255 absorbed） | [wave21-handoff](../docs-ja/discussion/wave21-session-handoff-2026-07-28.md) |
| CHK-236 | (A)/(B) 分割 | done · **(B)14:6** | chk236 |
| CHK-241 | cascade | oracle↑ tip↓ | chk241 |
| CHK-245/252 | mid-bank 偽陽性 | F023 | chk245 · chk252 |
| **CHK-256–270** | Wave-22 A/B/C | **全 NO-GO** | [harvest](../docs-ja/discussion/wave22-cpu-harvest-2026-07-29.md) |
| CHK-256 | tip 内部面 | done · gold≡selector | chk256 |
| CHK-261/268 | 近傍クリップ | tip↓ / ≈0 | chk261 · chk268 |
| **CHK-271–282** | Wave-23 天井→tip橋渡し | **CLOSED**（選択・再生成・校正全滅） | [handoff](../docs-ja/discussion/wave20-session-handoff-2026-07-26.md) |
| CHK-279 | 断絶診断 | 順位付け失敗が主因 | [result](../docs-ja/discussion/chk279-discontinuity-result.md) |
| CHK-271 | ラベル無し選択 | tip超え0 · NO-GO | [result](../docs-ja/discussion/chk271-selector-screen-result.md) |
| CHK-273/274/278 | 再初期化・再校正・焼なまし | NO-GO · F028–F030 | discussion |
| CHK-276/277 | hedge固定・簡易ランカー | NO-GO · F031/F032 | discussion |
| CHK-272/275/280–282 | 分岐前提なし | skipped | Wave-23 |
| **CHK-283–296** | Wave-24 生成器再設計 | **CLOSED**（hard20全滅） | [handoff](../docs-ja/discussion/wave20-session-handoff-2026-07-26.md) |
| CHK-283/287 | 診断 | PASS（md_late/anchor · residual-guided） | discussion |
| CHK-284/285 | 観測尤度 screen | NO-GO · GPU-A skip | discussion |
| CHK-288–290 | guided/learned/ESS+MCMC | NO-GO · **F033–F035** | discussion |
| CHK-286/291–295 | tip-cv/E2E | skipped · PASSなし | Wave-24 |
| CHK-296 | Final更新判断 | done · 更新なし | Wave-24 |
| **CHK-297–320** | Wave-25 難井専用 | **CLOSED**（AのみPASS · F036–F037） | [close](../docs-ja/discussion/wave25-lane-close-2026-07-30.md) |
| **CHK-321–340** | Wave-26 コンパス→条件付き移動 | **CLOSED**（移す系 F038 · OPS-FINAL2へ） | [close](../docs-ja/discussion/wave26-compass-close-2026-07-30.md) |
| **CHK-341–362** | Wave-27 ねじれ分解 | **CLOSED**（形修正 F039 · OPS-FINAL2へ） | [close](../docs-ja/discussion/wave27-twist-close-2026-07-30.md) |
| CHK-341–350 | パック·カタログ·全screen·混合 | done · 欠測観察優勢 | [work](work/wave27-twist-taxonomy/) |
| CHK-351–360 | 検出·天井·薄い実装 | 360 NO-GO · 359閉鎖 | [close](../docs-ja/discussion/wave27-twist-close-2026-07-30.md) |
| **CHK-363–368** | Wave-28 提出可能直し方 | **CLOSED**（全NO-GO · **F040**） | [close](../docs-ja/discussion/wave28-usable-fix-close-2026-07-30.md) |
| **CHK-369–373** | Wave-29 B7 別面 S1a/S1b | **CLOSED**（370/373 NO-GO · **F041**） | [close](../docs-ja/discussion/wave29-close-2026-07-30.md) |
| **CHK-380–382** | Wave-29 B8 FINAL後段 | **CLOSED**（380 STOP · 候補0 · **F041**） | [close](../docs-ja/discussion/wave29-close-2026-07-30.md) |
| **CHK-390–394** | Wave-30 B9 Soft-Preserve | **CLOSED**（392 生Pearson NO-GO · **F041**） | [close](../docs-ja/discussion/wave30-close-2026-07-30.md) |
| **CHK-395** | 生Pearson門番監査 | **GO_gate_reopen_candidate** | [audit](work/wave30-soft-preserve/chk395-gate-audit.md) · [caveat](../docs-ja/gate-pearson-caveat.md) |
| **CHK-397** | Soft-Preserve E2E/リーク | **FAIL**（soft≡final · F015） | [397](work/wave30-soft-preserve/chk397-e2e-leak-audit.md) |
| **CHK-401** | tip PF pack×20 non-hard20 | **GO**（20/20） | [401](work/wave30-soft-preserve/chk401-pack-report.json) |
| **CHK-398** | hard20→外井 transfer CV | **NO-GO**（final>soft · tip CSV無し） | [398](work/wave30-soft-preserve/chk398-exhard-cv.md) |
| F001–**F041** | 失敗型 | 台帳 | `improvement-loop-failures.json` |
| **CHK-411–413** | W31-A selector崖 · 介入点→smoke→proxy | done · GO_proxy（synth） | [cliff](work/wave31-selector-cliff/) |
| **CHK-415–416** | W31-B 第2生成器 | 416 tip-clone · **417–418 skip** | [alt](work/wave31-alt-generator/) |
| **CHK-419–420** | W31-C 非soft薄ブレンド | 420 farvol Public診断Best · compound NO-GO | [blend](work/wave31-nonssoft-blend/) · [overnight](latest/ops-lb-wave31-overnight-public-2026-07-31.md) |
| **CHK-422–423** | W31-D intelハント→dedupe | done · D1–D3移植済 | [hunt](../docs-ja/discussion/wave31-intel-hunt-2026-07-31.md) · [dedupe](../docs-ja/discussion/wave31-chk423-dedupe-2026-07-31.md) |
| **CHK-424–426** | W31-E selector定義置換 | done · GO_proxy（synth PF+real y） | [replace](work/wave31-selector-replace/) |
| **CHK-428–430 / 430b** | W31-F soft蒸留 | 430 NO-GO · 430b caveat OK / long TIP_CLONE | [distill](work/wave31-soft-distill/) |
| **CHK-432–434** | W31-G 神経提案 | 434 Optuna最良 TIP_CLONE | [neural](work/wave31-neural-proposal/) |
| **CHK-436–437** | W31-H post-unlock | 437 Local未発火 · Public NO-GO · **438–439 skip** | [unlock](work/wave31-post-unlock/) |
| **CHK-440–442** | W31-I 二段残差 | 442 Trust悪化 · **443 skip** | [resid](work/wave31-two-stage-resid/) |
| **CHK-444–446** | W31-J tip全面再実装 | 446 tip-clone · **447 skip** | [rewrite](work/wave31-tip-rewrite/) |

Wave-0〜11: スナップショット参照。

## Archived Waves

| Wave | 主題 | 状態 | 詳細 |
|---|---|---|---|
| **Wave-31（A〜J 閉レーン）** | B10–B19 並列探索 | **部分閉鎖** · Active→Wave-31b（414/421/427/448/449 + F/G HOLD） | [plan](../docs-ja/discussion/wave31-plan-2026-07-31.md) · [checklist](experiment-checklist.md) |
| **Wave-30** | B9 Soft-Preserve Ranker | **CLOSED**（F041）· 402A NO-GO · 403–408診断完了（408は提出不可の天井） | [close](../docs-ja/discussion/wave30-close-2026-07-30.md) · [work](work/wave30-soft-preserve/) |
| **Wave-29** | B7 別面 + B8 FINAL後段 | **CLOSED**（F041） | [close](../docs-ja/discussion/wave29-close-2026-07-30.md) |
| **Wave-28** | 提出可能直し方ハント | **CLOSED**（F040） | [close](../docs-ja/discussion/wave28-usable-fix-close-2026-07-30.md) |
| **Wave-27** | ねじれ種類分解 | **CLOSED**（F039） | [close](../docs-ja/discussion/wave27-twist-close-2026-07-30.md) |
| **Wave-26** | コンパス監査→条件付き移動 | **CLOSED**（F038 · OPS-FINAL2） | [close](../docs-ja/discussion/wave26-compass-close-2026-07-30.md) |
| CHK-322 | lik vs tip-soft 方向 | **H1 PASS**（rf逆70%） | [r](work/wave26-compass-audit/chk322-report.json) |
| CHK-323 | soft⊥FINAL | ρ=+0.074 · soft≈argmax0.97 | [r](work/wave26-compass-audit/chk323-report.json) |
| CHK-324 | 質量寄せ/平均幾何 | coldT微 · oracle混はラベル依存 | [r](work/wave26-compass-audit/chk324-report.json) |
| CHK-325 | cascade/mode 向き | F028再確認 · casΔ−1.77 | [r](work/wave26-compass-audit/chk325-report.json) |
| CHK-326 | MD帯 平行/ねじれ | 局所平行なし | [r](work/wave26-compass-audit/chk326-report.json) |
| CHK-327 | tip-soft 代理 LOO | **NO-GO**（≦lik） | [r](work/wave26-compass-audit/chk327-report.json) |
| CHK-328–330 | FINAL代理·合意·単純統計 | 転用不可 · 合意25% · tip_stdのみ | audit |
| CHK-331–335 · 338–340 | 平行移動 / tip-cv | **skipped** | F038 |
| CHK-336–337 | 局在 / 打ち切り | 局在28%不可 · **レーン閉鎖** | [close](../docs-ja/discussion/wave26-compass-close-2026-07-30.md) |
| **CHK-341–362** | Wave-27 ねじれ分解 | **CLOSED**（形修正 F039） | [close](../docs-ja/discussion/wave27-twist-close-2026-07-30.md) |
| CHK-341–350 | パック·screen·混合 | 欠測観察優勢 · single=missing | [work](work/wave27-twist-taxonomy/) |
| CHK-351–360 | 検出·天井·薄い実装 | 360 NO-GO · 359閉鎖 | [close](../docs-ja/discussion/wave27-twist-close-2026-07-30.md) |
| F001–**F041** | 失敗型 | 台帳 | `improvement-loop-failures.json` |

Wave-0〜11: スナップショット参照。

## Archived Waves

| Wave | 主題 | 状態 | 詳細 |
|---|---|---|---|
| **Wave-30** | Soft-Preserve Ranker + 追試 | **CLOSED**（F041） | [close](../docs-ja/discussion/wave30-close-2026-07-30.md) · [work](work/wave30-soft-preserve/) |
| **Wave-29** | 別面 B7 + FINAL後段 B8 | **CLOSED**（F041） | [close](../docs-ja/discussion/wave29-close-2026-07-30.md) |
| **Wave-28** | 提出可能直し方ハント | **CLOSED**（F040） | [close](../docs-ja/discussion/wave28-usable-fix-close-2026-07-30.md) |
| **Wave-27** | ねじれ種類分解 | **CLOSED**（F039） | [close](../docs-ja/discussion/wave27-twist-close-2026-07-30.md) |
| **Wave-26** | コンパス監査→条件付き移動 | **CLOSED**（F038 · OPS-FINAL2） | [close](../docs-ja/discussion/wave26-compass-close-2026-07-30.md) |
| **Wave-25** | 難井専用 · 易井凍結 | **CLOSED**（F036–F037） | [close](../docs-ja/discussion/wave25-lane-close-2026-07-30.md) |
| **Wave-24** | 生成器（観測/proposal/SMC） | **CLOSED**（全滅 · F033–F035） | [handoff](../docs-ja/discussion/wave20-session-handoff-2026-07-26.md) |
| **Wave-23** | 天井→tip橋渡し | **CLOSED**（全滅 · F028–F032） | [handoff](../docs-ja/discussion/wave20-session-handoff-2026-07-26.md) |
| **Wave-22** | 近傍/内部面/二経路/弱後処理 | **CLOSED**（全滅 · F027） | [harvest](../docs-ja/discussion/wave22-cpu-harvest-2026-07-29.md) |
| **Wave-21** | 上流/中間候補 | **CLOSED** | [handoff](../docs-ja/discussion/wave21-session-handoff-2026-07-28.md) |
| Wave-20 | tip 上流 / lik_temp | CLOSED（T0.15 Best） | スナップショット §Wave-20 |
| Wave-19–0 | soft〜ruler | CLOSED | スナップショット |

---

## 2026-08-03 移設 — Final Push ローカル/済レーン

> Active スリム化。詳細は各 out-*/report。単一セッション SSOT: [`latest/single-session-ssot-2026-08-03.md`](latest/single-session-ssot-2026-08-03.md)

| CHK | 仮説（短） | 結果 | ref |
|---|---|---|---|
| 466–470 · 472 | P-456 cascade / tip-cv | GO · Trust **28.920** · 提出禁止 | wave31-selector-replace |
| 473 · 473b · 477–484 | tip×mid 薄ブレンド screen | GO_screen · **485 で Public 反証** | wave31-nonssoft-blend · [`485-LB`](latest/ops-lb-chk485-public-2026-08-03.md) |
| 475 · 478 | P-461 tip-cv | **28.920** ≡472 | out-475-tipcv-err |
| 485 | SE blend Public診断 | se060 **NO-GO** · se040≈tip | ops-lb-chk485 |
| 489–495 · 497–499 | 上流 aggregator / 297 dual | 490b/495 GO · 297=18.11 | wave31-neural-proposal |
| 491 · 494 · 496 | S0′ / 297dual E2E | GO 診断 · FINAL≡tip | out-491/494/496-e2e |
| 492b | tip-cv ess1.0 | COMPLETE · STOP_AFTER_SELECTOR | out-492b-tip-cv |
| 500–503 | 勝ち分·行ゲート·段崩れ | **本命 `signed_pos∨absd≥2`=28.901** | out-500…503 |
| 505–506 | 誤解掘り返し·復活実体化 | GO · 親468/461 · H-D本線 | out-505/506 |
| 507 | CPU Trust revival | GO · 行ゲート再確認 | out-507-cpu |
| 508–511 | pre-400監査·gate sweep·多様性 | GO · pre-400掘り返し禁止 | out-508…511 |
| 512–513 | H-D 井ゲート + LOO | GO · Trust **28.283** · thr=0.7 | out-512/513 |
| 516–518 | H-B combo · 井スライス · 504 mid | HOLD / EQUIV_507 · H-G打ち止め | out-516…518 |
| OPS-NIGHT | 3h harvest/push | done · 514/515 submit-ready | wake-submit-ready |
| 458 Public | 全面 mid FINAL | **NO-GO F042** | ops-lb-chk458 |

---

## 移設メモ

- 2026-08-04: Final Push スリム化 · 579/592/600–618/625/631–632/636/640–642/645 等 → archive · Active=621/620本命+score_wait+余力
- 2026-08-03b: 505–518 · 485 · 496/492b · OPS-NIGHT → archive · Active=待ち盤のみ（[`final-board`](latest/final-board-2026-08-03.md)）
- 2026-08-03: 466–484 · 489–503（GPU未完の492/492b/496除く）→ archive · Active=GPU待ち+504設計+HOLD
- 2026-08-01: Wave-31 閉レーン（411–447 done/rejected/skip）→ archive · Active=Wave-31b（414/421/427/448/449 + 431/435 HOLD）
- 2026-07-31: Soft-Preserve追試（395–410）· CHK-396カタログ → archive · Active=OPS-FINAL2のみ
- 2026-07-30: Wave-30 / Wave-29 → archive（F041）
- 2026-08-05c: L1 **688/761/782** NOGO · WATCH-V2 · CPU packs · 711/710/702 → archive · Active= **804** 本線 · [checklist](experiment-checklist.md)
- 2026-08-05d: **804 Colab dual NOGO** · **F044** · laws · Active= **802/781** · [ops-804](latest/ops-l1-chk804-colab-dual-2026-08-05.md) · [laws](latest/l-improvement-laws-2026-08-05.md)
- 2026-07-30: Wave-28 → archive（F040）· Active = Wave-29（B7/B8）+ OPS-FINAL2
- 2026-07-30: Wave-29 plan 追加（CHK-369–373 · 380–382）
- 2026-07-30: Wave-27 → archive（F039）· Active = OPS-FINAL2 のみ
- 2026-07-30: Active = **Wave-27**（ねじれ種類分解）· Wave-26 は F038 のまま archive
- 2026-07-30: Wave-26 → archive（F038）· 一時 OPS-FINAL2 のみ
- 2026-07-30: Wave-25 → archive · Active = **Wave-26**
- 2026-07-30: Wave-24 → archive
- 2026-07-29: Wave-23 → archive
- 2026-07-28: Wave-21 → archive
