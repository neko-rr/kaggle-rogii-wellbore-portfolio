# L / Trust CV 仮説ハンドオフ — 2026-08-05

> **用途:** 別セッション Agent が **Trust residual CV 向上** を回すときの拡張 SSOT  
> **親 Active:** [`experiment-checklist.md`](experiment-checklist.md)  
> **L 手順:** [`l-relearn-session-guide.md`](l-relearn-session-guide.md)  
> **L 法則:** [`latest/l-improvement-laws-2026-08-05.md`](latest/l-improvement-laws-2026-08-05.md)  
> **804 ops:** [`latest/ops-l1-chk804-colab-dual-2026-08-05.md`](latest/ops-l1-chk804-colab-dual-2026-08-05.md)  
> **LB 着弾:** [`latest/ops-lb-chk660-666-public-2026-08-05.md`](latest/ops-lb-chk660-666-public-2026-08-05.md)  
> **metric:** residual `mid+α0.35(L−mid)` · **pool ∧ mean_worst ∧ max_band** (+ worst8 WATCH)  
> **提出:** ユーザー明示時のみ · residual Public 禁止 · α いじり禁止（F043）· **F044 weight mid-collapse**  
> **ドメイン:** GR 欠損・水平揺動 = **機器制限** · [gr-instrument-limits-cv](../docs-ja/discussion/gr-instrument-limits-cv.md) · Host wiggle 無料（727171）

---

## 0. 別セッション開始（必読 2 分）

1. `exp-index.md` 現在地  
2. `experiment-checklist.md` Active + 本ファイル  
3. `l-relearn-session-guide.md` §3 dual · §5 status  
4. faces: `work/colab-final-t2/CURRENT-T2-FACES.md`（`20260804-041247`）  
5. 661/666 Public: **666=6.509 Public NO · Trust only** · **660=6.239 枠2NO** · Best/枠2=farvol  
6. **GR:** 機器制限 → **GR 本命特徴・高周波合わせ 禁止**（811 GR 二次 · L residual 本命）

**禁止の再確認:** F015 生 L/mid · F043 residual-α · **F044 weight L mid-collapse 言い換え** · mid 先改修 · L1 未 GO で POST-L · 自律提出 · **GR 本命** · **TVT-OOF 単独 L1 GO**

---

## 0b. ドメイン補強（2026-08-05 · GR 機器制限）

> 詳細: [`docs-ja/discussion/gr-instrument-limits-cv.md`](../docs-ja/discussion/gr-instrument-limits-cv.md)

| 事実 | CV・仮説への影響 |
|---|---|
| GR 欠損多 = 機器制限 | 欠測充填・GR 単体特徴を GO 根拠にしない |
| 水平 GR 揺動 = 計測制限 | 高周波 wiggle 合わせ再開禁止（Host: 誤差は低周波） |
| 811 mean_GR ρ≈0 | **確認済み** · 本命は \|L−mid\|+md · weight/loss |
| Active 順 | **差し替えなし**（761→804…→781） |

---

## 1. 数値の床（いじらない基準）

| 面 | pool | mean_worst3 | 備考 |
|---|---:|---:|---|
| tip S0 **T2 80** | 17.03 | ~20 | 土台（カタログ尺） |
| tip S0 **all773** | **10.84** | hard mean **26.83** | フル人口尺 · [all773](latest/chk-final-t2-all773-cv-2026-08-05.md) · **tip⊕ NOGO** |
| mid S9 T2 resid | 12.34 | ~14.6 | 材料 · win**77**/hurt**3** · 生 FINAL 禁止 |
| mid all773 tip-cv | ≈tip（tipdist **0.20**） | — | label **win25/hurt21/タイ727** · T2 mid と混同禁止 · [stage-group](latest/all773-stage-well-group-2026-08-05.md) |
| **666 resid α0.35** | **10.09** | **11.91** | **Trust 合法頭** · Public 6.509 |
| L 生 T2 | 6.92 | 8.92 | F015 · 天井見映え |
| perfect-L residual | **~8.02** | — | ceil gap pool **~2.07** |
| 641 α0.30 | 10.40 | 12.28 | Public 6.472 |
| 660 tip+α0.5 | T2 11.17 | — | Public 6.239 · Trust 外 |

### all773 グループ床（2026-08-05 · tip A）

| 群 | n 井 | mean tip | SSE 寄与 |
|---|---:|---:|---:|
| hard20 | 20 | 26.83 | **≈20%** |
| 非 hard | 753 | 8.02 | ≈80% |
| top100 井（SSE） | 100 | — | **≈62%** |
---

## 2. 工程ごと知見 → 実験への接続

| 工程 | 事実 | 穴 | **CV で触る？** | 接続 CHK |
|---|---|---|---|---|
| **S0 tip** | T2 hard20≈29.9 · **all773 pool10.84 / 非hard mean8.0 / hard26.8** · Public 6.269 | 薄い | **触らない**（T0.15 固定） | フル尺 [all773](latest/all773-stage-well-group-2026-08-05.md) |
| **S1 L** | win77/hurt3 vs tip · raw 最良 · residual レバー · all773 dump L は tip 近傍 | 688 retrain で resid 悪化 | **本命 100%** | 761–806 · 781 · 807+ |
| **S2–S8**（blend/gate 内） | S3 blend w0.50 材料 · gate は mid に内包 | S2–S6 井別は dump 薄い | L1 GO 前は触らない | 643 ladder 済 archive |
| **S9 mid** | **T2** tip→mid **win77/hurt3** · pooled 12.3 · **all773 tip-cv mid win25/hurt21/タイ94%** | hurt 3 井（T2） | mid 改修は **L 後のみ** · **面を分けて読め** | POST-L 764/795 · all773 tip⊕ 禁止 |
| **S9 residual mid+αL** | help **77**/hurt **3**（mid と同集合）· hard20 **全 help** · Public 毒 | mean_worst · Q4 · L 質 | **α固定 · L だけ変える** | F043 閉 · L1 only |
| **S9 tip residual 660** | Public 安全 · T2 は mid residual より弱い | Trust 頭にならない | Trust 本命にしない | 再提出禁止 |
| **FINAL tip⊕** | 541/558b/618c は tip 近傍 Public · **all773 B≡C Δ−0.008** | 枠2 farvol 優位 | Trust 改善に使わない | archive · all773 NOGO |

### 工程読み（確定）

1. residual の **井 win 集合は mid とほぼ同一**（深度だけ深まる）→ mid を壊さず **L 方向を直す**。  
2. residual α↑ は Trust T2 では少し良くても **Public は悪化**（641→666）→ deploy α 閉鎖。  
3. soft を residual に足すと hurt↑（668）→ soft residual 再開禁止。  
4. **773 固有:** tip-cv mid 面は **T2 residual mid と別人**（win 率崩壊）· tip⊕ は full 尺で死 · **SSE の 6 割が top100 井** → dual/weight 必須 · [stage-group](latest/all773-stage-well-group-2026-08-05.md)。
---

## 3. 井戸の種類（タイプ）→ 重み / loss 設計

### 3.1 タイプ定義（operational）

| タイプ | 定義（機械） | 典型例 | 学習での扱い | **all773 での裏付け** |
|---|---|---|---|---|
| **A · Attack hard residual** | hard20 ∧ residual SSE/rmse 上位 · drag 大 | `1b1eba53` · `5f4d2a52` · … | sample_weight↑ · 804/782/806 | hard **2.6% 井で SSE≈20%** |
| **B · MD Q4 悪** | row MD 上位四半期 · gap_to_rstar 最大 | Q4 pool resid **12.83** | Q4 weight · **802 / 804** | residual 行帯 · **井 tip 半 hard は I/814** |
| **C · resid>L 拖** | residual RMSE > L | n≈41 | **782** weight | residual 面で測る（all773 L は tip 近傍） |
| **D · 688 hurt** | 688 retrain で resid 悪化 15 | `1b1eba53`… | **789 protect** | 未再測 · 仮説維持 |
| **E · mid-hurt（3 井）** | tip より mid が悪い（**T2 尺**） | `70925e23`… | **809 除外** | all773 tip-cv mid は **タイ94%** · 定義を all773 に持ち込むな |
| **F · L 既に強** | frac_L_beats_mid 高 | known 良側 | weight ≤1 | all773 sign_agree≈1 · L dump 情報薄 |
| **G · known vs unknown** | known40 gap | known 帯 | 804 known× | 尾 SSE と同一方向 |
| **H · field / pad** | leave-field | field プレフィックス | **785** | 尾がクラスタしうる → Group 意義残 |
| **I · 半 hard Q4e** | 非 hard · tip well-RMSE 上位帯 | — | **814 weight** | all773 Q4e mean **≈15.6** · hard 拡張 |
| **J · Q1e bulk** | 非 hard · tip 易帯 mean≈3.3 | — | **816 protect ≤1** | 易井過学習防衛 |
### 3.2 MD 四分位（行 · residual 現状）

| Q | n | resid | r* | gap | 読み |
|---|---:|---:|---:|---:|---|
| Q1 | 11k | 3.21 | 2.55 | 0.66 | 余裕小 · 過学習しやすい |
| Q2 | 121k | 6.45 | 4.89 | 1.55 | 中 |
| Q3 | 133k | 10.10 | 7.96 | 2.14 | residual-path loss 帯（805） |
| **Q4** | **133k** | **12.83** | **10.35** | **2.48** | **最悪 · L1 主戦場** |

### 3.3 mid-hurt 3 井（特別）

| well | mid vs tip | L vs mid | 読み |
|---|---|---|---|
| `70925e23` | mid 悪化 | L も mid より悪い帯 | residual 載せると sample 全滅パターン（702）の元 · **ここを weight↑ すると毒** |
| `ab3ced07` | mid 悪化 | L 悪め | 同上 |
| `19871e7f` | mid 悪化 | tip 易しい井 | 軽く触らない |

→ **attack リストに mid-hurt を混ぜない**（789 とは別ルール）。

### 3.4 Attack 優先（EDA · top）

出典: `l-cpu-eda-20260805/attack_priority_wells.csv` · 先頭 hard20 中心:  
`5f4d2a52` · `1b1eba53` · `91db7070` · `206b6193` · `86454a6f` · `fef8af96` · `f88ddb26` · …

---

## 4. Public 着弾から足した CV 仮説（新規 CHK）

| ID | type | 仮説（手法 × 期待） | source | acceptance | L段 |
|---|---|---|---|---|---|
| **CHK-807** | T3 | **学習停止・OOF 選抜を residual RMSE（α0.35）主**にし、L-TVT RMSE 改善だけでは止めない → 688 型の「L良・resid悪」を防ぐ | 688 hurt · 799 corr · 781 拡張 | L1 dual GO と同基準 · 機構=early_stop/selector のみ（weights 同時不可） | L1 |
| **CHK-808** | T3 | **weight 帯で連続 3 NOGO**（761·782·804 など weight 系）したら中間 weight を飛ばし **即 781 residual-RMSE** へ帯切替 | H-R5 · 768 | ログに jump 記録 · GPU 1本 | ops+T3 |
| **CHK-809** | T3 | attack 集合から **中 mid-hurt3 を明示除外**（＋789 hurt 低 weight）した weight map 1 本で dual が 804 より良い | §3.3 · 789 | dual vs 804 · hurt 井 d_resid | L1 |
| **CHK-810** | T4 | 新 L dual 時に **タイプ別（A–G）d_resid 表を自動出力**し GO 条件に「Q4 非悪化」「mid-hurt3 非悪化」を記録 | 工程×井 | dual report に表があれば GO_ops | ops |
| **CHK-811** | T3 | L 入力に **mid 誤差と直交する観測特徴 1 群のみ**（**\|L−mid\|+md_frac** · **GR 禁止**） | 666 · mid バイアス · **GR=機器制限** | dual · soft注入禁止 · 1群のみ · [gr-inst](../docs-ja/discussion/gr-instrument-limits-cv.md) | L1 after 781 |
| **CHK-812** | T4 | タイプ別 dual（hard20-only / non-hard / Q4-row-agg）の **3 スライス残差**を L1 採否の WATCH にする | 798 seed · 791 | WATCH 文書化 · 単独 GO 禁止 | ops |

**既存との重複回避**

- 781 = residual **loss** · 807 = residual **early-stop / モデル選抜**（隣接だが同時実行禁止 · 781 実装時に 807 を内包可）  
- 806 = attack+protect map · 809 = mid-hurt 除外の別 map  
- 790/791 = 既 apply · 810 はその拡張 · **812** Q4 WATCH

---

## 4b. all773 後の仮説 Δ（2026-08-05 · CV 改善）

> **結論:** 本命レーン（L dual · residual 041247）は **差替なし・証拠強化**。  
> **閉:** tip⊕ full · mid 面読み替え · agree 再発明 · S0 再設計。  
> **増:** CHK-**813–816**（ops 2 + weight map 2）。  
> 画面SSOT: checklist [`§all773 CV仮説の変化`](experiment-checklist.md#all773-cv仮説の変化) · 数値 [`stage-group`](latest/all773-stage-well-group-2026-08-05.md)

### 不変 · 強化

- L retrain dual · hard/Q4 weight · 688 protect · α閉 · tip 凍結

### 閉鎖 / 降格（言い換え再開禁止）

| 仮説 | 状態 |
|---|---|
| all773 tip⊕ / mid ゲートで Trust 改善 | **closed** · Δ≪0.01 · Final NO |
| T2 mid win77 → 人口面に外挿 | **prohibited** |
| hard を mid 注入で unlock | **downgraded** · tip stick · L only |
| pool 単独 dual GO | **ban 強化** → 813 |
| full faces 上 agree ゲート追加 | **downgraded** · B≡C |

### 新規 CHK

| ID | type | 仮説 | acceptance |
|---|---|---|---|
| **CHK-813** | T4 ops | dual 報告に **tip-SSE top50/100 井**（または SSE 重み residual）の Δ を必須 · all773 で top100≈62%SSE | dual JSON/report に欄 · **単独 GO 禁止** · 812 と併記 |
| **CHK-814** | T3 | non-hard **Q4e**（all773 tip RMSE 最悪帯 · mean≈15.6）を hard∪weight に加えた **1 map**（804 拡張 or 802 接点） | dual vs 804v1c · d_worst または Q4 非悪化 · mid-hurt3 非混入 |
| **CHK-815** | T4 ops | dual に **hard tip-stick unlock**: hard20 の resid と \|L−mid\|（または tipdist_L proxy）が baseline より動いたか | hard resid 改善なしで pool だけ良い → **NOGO 候補** · 812 併記 |
| **CHK-816** | T3 | **Q1e bulk protect**: all773 tip 易井帯（mean≈3.3）weight ≤1 · attack 混入禁止 | dual · 易 band 非悪化 + 尾非悪化 · 789 と併用可 |

### タイプ追加

| タイプ | 定義 | CHK |
|---|---|---|
| **I · 半 hard Q4e** | 非 hard · tip well-RMSE 上位 Q（≈15.6） | 814 |
| **J · Q1e bulk** | 非 hard · tip 下位 Q（≈3.3） | 816 protect |

### 実行順への差込

```text
DUAL 常時:  810 + 812 + **813 + 815**（ops · GPU/local 問わず）
weight 次:  804（±816）→ **814** or 802 → 809 …
禁: tip⊕ · all773 mid で residual 再定義 · GR 本命 · α
```

---

## 5. 実行順（別セッション標準）

> **GPU 必読短縮版:** [`latest/session-bridge-cpu-to-gpu-2026-08-05.md`](latest/session-bridge-cpu-to-gpu-2026-08-05.md)

```text
DONE:    688 · 761 · 782 · **804** = NOGO · **F044** · [laws]
NOW:     Colab **802**（任意 1 本）or **781 residual-path**（推奨）
DUAL:    810 + 812 + **813 + 815** · OOF 単独 PASS 禁止
             ├─ GO → POST-L: 779 → 762 → 756 → 764/795
             └─ NOGO → 809 optional → **808→781(+805·807)** → 811
提出: ユーザー明示のみ
```

### weight oracle 順位（再学習成功後の期待ではない · 地図）

`804(v1b≈v1c) ≳ 803/792 ≳ 802 ≳ 806 ≳ 789 ≫ 761`  
（**809** は oracle 弱めだが midhurt 防衛機構 · dual 監査用）

### CPU で済んだこと（GPU で繰り返さない）

- GAP-b · P0P1 · expert-C · Kaggle CPU×5 harvest  
- 804 **v1c map 生成済** · 次 push 時に NB へ焼くだけ

---

## 6. acceptance 統一（Trust レーン）

| 条件 | 値 |
|---|---|
| 平面 | hard_plane 主 · hybrid80 地図 |
| pool | ≤ old − **0.05** |
| mean_worst3 | ≤ old − **0.05** |
| max_band | ≤ old + **0.5** |
| worst8 WATCH | ≤ old_8 + **0.10** で L2 可 |
| **新規 WATCH（812）** | Q4 resid 非悪化 · mid-hurt3 非悪化 |
| **新規 WATCH（813）** | tip-SSE top50/top100 帯 residual を報告 · 単独 GO 禁止 |
| **新規 WATCH（815）** | hard20 residual または \|L−mid\| が baseline から動いたか（tip stick 診断） |
| 禁止 | pool 単独 · L 生 FINAL · α 変更 · all773 tip⊕ · mid 面外挿 |

---

## 7. 参照パス早見

| 内容 | パス |
|---|---|
| **GPU 橋渡し** | `latest/session-bridge-cpu-to-gpu-2026-08-05.md` |
| L dual script | `work/out-t3-scratch/run_l_residual_local_dual.py` |
| 804 NB | `my-notebook/tip-cv-chk804-known-q4-h20/` |
| **804 v1c map** | `work/out-t3-cpu-harvest/l-hyp-weights-20260805/chk804_known_q4_weights_v1c_pruned.json` |
| 804 v1b map | `work/out-t3-cpu-harvest/l-hyp-weights-20260805/chk804_known_q4_weights_v1b.json` |
| 761 weights | `work/out-t3-cpu-harvest/chk748-751-diag/chk761_well_weights.json`（v2b） |
| 782 weights | `work/out-t3-cpu-harvest/session-1h-cv-20260805/chk782_resid_drag_weights.json` |
| 806 map | `work/out-t3-cpu-harvest/l-cpu-eda-20260805/chk806_attack_protect_weights.json` |
| CPU-C report | `work/out-t3-cpu-harvest/cpu-expert-pack-c-20260805/report.md` |
| well×resid | `work/out-t3-cpu-harvest/l-cpu-eda-20260805/well_residual_table.csv` |
| 688 hurt | `work/out-t3-cpu-harvest/l-cpu-eda-20260805/chk688_well_hurt.csv` |
| stage×井 | `latest/t2-stage-well-map-2026-08-04.md` · residual help/hurt · **all773** [`stage-group`](latest/all773-stage-well-group-2026-08-05.md) |
| all773 CV | `latest/chk-final-t2-all773-cv-2026-08-05.md` · faces `CURRENT-ALL773-FACES` |
| LB 660/666 | `latest/ops-lb-chk660-666-public-2026-08-05.md` |

---

## 8. 更新履歴

- 2026-08-05: 660/666 Public 後 · 工程×井タイプ · CHK-807–812 · 実行順統合
- 2026-08-05 **pm:** CPU-C · 804 **v1c** · 805/807 ops · **session-bridge** · GPU セッション共有向け更新
- 2026-08-05 **pm2:** **GR 機器制限** ドメイン追記（Active 順は不変 · GR 本命禁止強化）
- 2026-08-05 **pm3:** **all773 工程×群** · hard SSE≈20% · top100 SSE≈62% · mid win25/タイ94% · tip⊕ NOGO · [stage-group](latest/all773-stage-well-group-2026-08-05.md)
- 2026-08-05 **pm4:** **仮説 Δ** 明文化 · CHK-**813–816** · タイプ I/J · dual ops 強化 · 本命差替なし
