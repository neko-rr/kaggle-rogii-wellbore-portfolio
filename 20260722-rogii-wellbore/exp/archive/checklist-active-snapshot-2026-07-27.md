> type: checklist-archive-snapshot  
> archived: 2026-07-27  
> note: **作業キューではない。** Active は [`../experiment-checklist.md`](../experiment-checklist.md)。索引は [`../checklist-archive.md`](../checklist-archive.md)。

# experiment-checklist — rogii-wellbore（ARCHIVE SNAPSHOT）

> phase: **Wave-20 · OPS-LB-SUB1314 · OPS-FINAL2 · CHK-231 harvest**  
> updated: 2026-07-27（OPS-LB-SUB1314 · tip-cv≃LB）  
> participant: Kazeneko  
> metric: **RMSE（行単位 `tvt` · 低いほど良い）**  
> pre-strategy-gate: **PASS**（`exp/pre-strategy-gate.md`）

---

> **現在地（Best / tip / 次アクション）:** [`exp-index.md`](exp-index.md) ← **唯一の正**（本ファイルにスコア再掲禁止）  
> **別セッション引き継ぎ（Wave-20）:** [`docs-ja/discussion/wave20-session-handoff-2026-07-26.md`](../docs-ja/discussion/wave20-session-handoff-2026-07-26.md) ← **次チャットはここから**  
> **Wave-14 診断:** [`docs-ja/wave14-well-archetypes-2026-07-25.md`](../docs-ja/wave14-well-archetypes-2026-07-25.md)  
> **戦略 SSOT:** [`docs-ja/comp-strategy.md`](../docs-ja/comp-strategy.md)（B1–B5 閉鎖 · F011–F020）  
> **禁止仮説台帳:** [`improvement-loop-failures.json`](improvement-loop-failures.json)  
> ずれ検知: `scripts/check-exp-ssot.ps1`

## 使い方

- **Phase 2:** Active を **上から 1 項目**。重い実験前に hypothesis-ban gate。  
- 完了時: 当該行 + `hyperparameter-table.md` + `exp-train`/`exp-infer`。**exp-index は Best/次アクション変更時のみ**
- done/rejected は [`checklist-archive.md`](checklist-archive.md) へ

**評価との対応:** 採択は原則 **自前 well-group CV の RMSE**。  
**GPU:** tip 再推論・提出相当 = Kaggle GPU。物差し（CF/GroupKFold/hard-well）= **ローカル CPU**。

---

## 実行制約（ユーザー記入）

| 項目 | 方針 |
|---|---|
| 起動条件 | **ユーザー許可済み + 対象ジョブの実行指示あり** |
| Kaggle GPU | Wave-20 は **ジョブ明示時のみ**（CHK-203 tip dump 等）· 同時最大2 |
| Kaggle CPU | 診断・harvest · CHK-203 後処理可（最大5） |
| Private | 自作資産は必須 |
| 提出 | E2E自kernelのみ（F005禁止）· 乱打しない |

---

## Active Pending

> **OPS-LB-101112 DONE:** SUB-11/10/12 枠外 · 旧 Best=SUB-9  
> **OPS-LB-SUB1314 DONE:** Final=枠1 CV1位 / 枠2 Public1位（不変）· 現割当は両枠 SUB-14 · Public1位入れ替わり→枠2差替  
> **Wave-20:** tip-cvリーク確定 · selector baseline · lik_temp 軸確定（T0.15）· tip-cv14.87禁止  
> **Wave-17/18/19:** 中間 SOFT / 薄混ぜ NO-GO · 提出レバー閉じ

### Wave-20 — tip 上流 / generator 命中（2026-07-26）

> **目標（ユーザー確定）:** generator が出す候補集合に、**現状より良いスコアの予測が含まれる**ようにする（選択・SOFT ではなく **命中**）。  
> 物差し: hard20 **seed-oracle**（186/207/208/213）· **selector 面 tip-cv**（211 baseline=33.18）· tip FINAL は参照のみ。  
> **根因 SSOT:** [`wave20-tipcv-phys-leak-rootcause`](../docs-ja/discussion/wave20-tipcv-phys-leak-rootcause.md) — tip-cv 14.87 は **0.3·CF+0.7·phys(TVTリーク)**。本番純 test 井は PF/selector。  
> **公平比較:** [`chk211-selector-baseline-result`](../docs-ja/discussion/chk211-selector-baseline-result.md)  
> **別セッション引き継ぎ:** [`wave20-session-handoff-2026-07-26`](../docs-ja/discussion/wave20-session-handoff-2026-07-26.md) ← **次チャットはここから**  
> 作業: [`exp/work/wave20-upstream/`](work/wave20-upstream/) · 186: [`chk186-result`](../docs-ja/discussion/chk186-generator-ceiling-result.md)  
> 既閉: F013 · F015 · CHK-091 · **CHK-202** · soft 後段 Wave-17〜19 · combo tip面（209）

| 優先 | ID | 仮説（手法 × 期待） | action | acceptance | 状態 |
|---|---|---|---|---|---|
| G0 | **CHK-207** | PF ノブで hard20 **seed-oracle** が ≥0.30 改善 | T4 | ローカル · **提出なし** | **done（PASS）** · init_spr=9 Δ**+0.94** · [`result`](../docs-ja/discussion/chk207-pf-knob-result.md) |
| G1 | **CHK-206** | tip CFG `init_spr=9` で tip-cv 面が動く | T4 | tip-cv hard20 · **提出なし** | **done（誤物差し）** · ≡14.87 は phys面 · [`rootcause`](../docs-ja/discussion/wave20-tipcv-phys-leak-rootcause.md) |
| G1b | **CHK-208** | init_spr9×seeds256 で oracle が単独最良+0.10 | T4 | ローカル · **提出なし** | **done（PASS）** · **11.63** Δ**+1.25** · [`result`](../docs-ja/discussion/chk208-combo-oracle-result.md) |
| G2 | **CHK-209** | selector 面強制+combo で PF tip 面が改善 | T4 | vs **211** baseline · **提出なし** | **done（NO-GO）** · 33.54 vs 33.18（Δ−0.36）· [`result`](../docs-ja/discussion/chk209-selector-face-result.md) · [`比較`](../docs-ja/discussion/chk211-selector-baseline-result.md) |
| G2b | **CHK-211** | selector-face baseline（4.5×128）を確立し 209 と公平比較 | T4 | USE_SELECTOR_FACE · **提出なし** | **done（GO·物差し）** · RMSE **33.178** · [`result`](../docs-ja/discussion/chk211-selector-baseline-result.md) |
| G3 | **CHK-210** | tip-cv 既定を **本番同型**（phys 無効）にし物差しを固定 | T4 | ビルダー既定 · 文書 · **提出なし** | **done（GO）** · [`ruler`](../docs-ja/discussion/chk210-tipcv-ruler.md) |
| G4 | **CHK-205** | 尤度温度 T∈{0.5,2.0} で selector 面を ≥0.30 改善 | T4 | vs **211** 33.178 · **提出なし** | **done（PASS T0.5 / NO-GO T2）** · 32.276（**+0.90**）· [`result`](../docs-ja/discussion/chk205-lik-temp-result.md) |
| G4b | **CHK-205b** | 待ち時間: 局所 pf_scale×T + 209×208 井別 | T4 | ローカル · **提出なし** | **done** · T0.5 **+1.68** · corr tip↔oracle **0.04** · [`result`](../docs-ja/discussion/chk205b-wait-screen-result.md) |
| G5 | **CHK-212** | 本番 Best tip に **LIK_TEMP=0.5** を載せて E2E smoke | T4 | GPU COMPLETE · sub 形 | **done（SUB-13 · Public 確定）** · ref **55001828** · [`SUBMIT`](../my-submitted-notebook/tip-gated-lik-temp-0p5/SUBMIT.md) · [`ops-lb`](../docs-ja/ops-lb-sub1314-public-2026-07-27.md) |
| G6 | **CHK-213** | generator 多様性（init_spr細/混合/seeds384）で oracle↑ | T4 | hard20 seed-oracle ≥+0.30 · **提出なし** | **done（PASS）** · **init_spr=12 → 10.38（+2.50）** · [`result`](../docs-ja/discussion/chk213-generator-diversity-result.md) |
| G7 | **CHK-214** | tip-cv selector 面で **init_spr=12** ± T0.5 を測る | T4 | vs **211** 33.178 · **提出なし** | **done（NO-GO）** · 33.413 / 33.428 · [`result`](../docs-ja/discussion/chk214-spr12-tipcv-result.md) |
| G8 | **CHK-216** | 難井 `1b1eba53` は散布では閉じず観測/尤度破綻 | T4 | 1文断定 · 次ノブ1つ | **done（GO_CLOSE）** · [`result`](../docs-ja/discussion/chk216-hardwell-1b1eba53-result.md) |
| G9 | **CHK-217** | spr {10,11,13,14} が spr12 を ≥+0.30 | T4 | hard20 oracle · **提出なし** | **done（NO-GO）** · spr12 固定 · [`result`](../docs-ja/discussion/chk217-spr-fine-grid-result.md) |
| G10 | **CHK-218** | lik_temp 細格子 / エントロピーゲートが T0.5 超 | T2 | 局所 PF · **提出なし** | **done（PASS T0.3 / entropy NO-GO）** · [`result`](../docs-ja/discussion/chk218-liktemp-fine-result.md) |
| G11 | **CHK-219** | tip-cv selector で **T=0.3** が T0.5 と 211 を超える | T2 | vs 211 · vs 32.276 · **提出なし** | **done（PASS）** · **30.827** · [`result`](../docs-ja/discussion/chk219-lik-temp-0p3-result.md) |
| G12 | **CHK-221** | T&lt;0.3 / top-k / scale が局所 soft T0.3 を ≥0.30 | T2 | 局所 PF hard20 · **提出なし** | **done（PASS）** · T0.15/topk5/sc2 · [`result`](../docs-ja/discussion/chk221-colder-topk-result.md) |
| G13 | **CHK-222** | tip-cv **T=0.15** が 211·T0.5·(219) を超える | T2 | tip-cv hard20 · **提出なし** | **done（PASS_best）** · **29.899** · [`result`](../docs-ja/discussion/chk222-lik-temp-0p15-result.md) |
| G14 | **CHK-220b** | Best tip + **LIK_TEMP=0.15** E2E smoke | T2 | GPU COMPLETE · 提出は別 | **done（SUB-14 · Public Best）** · ref **55006677** · [`SUBMIT`](../my-submitted-notebook/tip-gated-lik-temp-0p15/SUBMIT.md) · [`ops-lb`](../docs-ja/ops-lb-sub1314-public-2026-07-27.md) |
| G15 | **CHK-223** | tip-cv **T=0.10** が T0.15(29.899) を ≥0.30 | T2 | tip-cv · **提出なし** | **done（NO-GO）** · 29.848（+0.05）· [`result`](../docs-ja/discussion/chk223-lik-temp-0p1-result.md) |
| G16 | **CHK-224** | tip-cv **T0.15+topk5** が soft T0.15 を ≥0.30 | T2 | tip-cv · **提出なし** | **done（NO-GO）** · 49.53 · [`result`](../docs-ja/discussion/chk224-topk5-result.md) |
| G17 | **CHK-227** | tip-cv **T=0.08** 天井 | T4·Force | tip-cv · **提出なし** | **done（NO-GO）** · 29.841（+0.06）· [`result`](../docs-ja/discussion/chk227-lik-temp-0p08-result.md) |
| G18 | **CHK-228** | tip-cv T0.15 **seeds256** | T4·Force | tip-cv · **提出なし** | **done（NO-GO）** · 29.872（+0.03）· [`result`](../docs-ja/discussion/chk228-seeds256-result.md) |
| G19 | **CHK-229** | tip-cv best-of-temps オラクル | T4·Force | tip-cv dump · **提出なし** | **done（NO-GO）** · 29.639（+0.26）· [`result`](../docs-ja/discussion/chk229-temp-blend-result.md) |
| G20 | **CHK-230** | 局所 PF gs/pn/particles @ T0.15 | T4·Force | ローカル CPU · **提出なし** | **done（NO-GO）** · base最良 · [`result`](../docs-ja/discussion/chk230-pf-aux-knobs-result.md) |
| G21 | **CHK-231a–e** | tip-cv weight/variant | T4·Force | GPU×2 + CPU2×5 | **running** · [`handoff`](../docs-ja/discussion/wave20-session-handoff-2026-07-26.md) |
| U0 | **CHK-203** | 同一ランで sp45/learned/gold vs FINAL dump | T4 | **提出なし** · F015 | **done（ERROR）** · learned=test id |
| U0b | **CHK-203b** | learned skip + train-id dump で完走 | T4 | selector+≥1 upstream ok | **done（ERROR）** · gold length · [`result`](../docs-ja/discussion/chk203b-dump-error.md) |
| U1 | **CHK-204** | 上流ギャップをゲート特徴のみ | T4→T0 | Δpool≥+0.05 | **done（NO-GO）** · sp45≡selector · [`result`](../docs-ja/discussion/chk204-stage-gap-result.md) |

**Active（別セッション継続用）:**

| 優先 | ID | 仮説 / 作業 | 状態 | 次の一手 |
|---|---|---|---|---|
| 1 | **OPS-FINAL2** | 枠1=CV1位 · 枠2=Public1位（現 SUB-14×2） | **pending** | Public1位入れ替わり→枠2差替 · [`prep`](../docs-ja/ops-final2-prep-2026-07-26.md) |
| 2 | **CHK-231** | tip-cv weight/variant | **running** | harvest → ≤29.599 なら E2E |
| 3 | **OPS-LB-SUB15** | twostage Public 記録 | **PENDING** | 診断のみ · Best 戦場外 |
| 4 | **OPS-LB-SUB1314** | SUB-14/13 Public 確定 | **done** | [`ops-lb`](../docs-ja/ops-lb-sub1314-public-2026-07-27.md) |

**Pending（承認後のみ）:**

| ID | 仮説 | 再開条件 |
|---|---|---|
| **CHK-215** | tip CFG に **init_spr=12** | **cancelled**（214 NO-GO） |
| **CHK-220（仮）** | Best tip に **LIK_TEMP=0.3** E2E | **superseded** by 220b |
| （判断） | Public 1位入れ替わり時の枠2差替 | **方針確定** · UIはユーザー · Agentは記録+通知のみ |

**分岐:**

| 結果 | 次 |
|---|---|
| **214 NO-GO（確定）** | spr12 は命中専用 · tip は lik_temp 軸 · 215 作らない |
| **217 NO-GO** | spr 軸打ち切り（12 固定） |
| **204 NO-GO** | 上流薄混ぜ再発明禁止 |
| **SUB-14 Best（確定）** | tip-cv≃LB · Final=枠1 CV1 + 枠2 Public1（現は両枠 SUB-14）· Public入れ替わりで枠2更新 |
| tip-cv 14.87 / phys | **禁止** |

**Explicit Stop:** F015 · F013/CHK-202 · tip-cv phys 誤認 · **combo/spr12 tip 採用（214）** · spr 細格子再スイープ · Public 乱獲 · 日次枠の無駄撃ち（本日 2/5 済）· F011–F020 言い換え。

**引き継ぎ全文:** [`wave20-session-handoff-2026-07-26`](../docs-ja/discussion/wave20-session-handoff-2026-07-26.md)

### Wave-19 — tip×mid 薄混ぜ（2026-07-26 · 提出なし）

> 結果: [`chk202-thin-blend-result`](../docs-ja/discussion/chk202-thin-blend-result.md) · 作業: [`exp/work/wave19-thin-blend/`](work/wave19-thin-blend/)

| ID | 仮説 | 状態 |
|---|---|---|
| **CHK-202** | Type A のみ tip FINAL に α≤0.05 で SP45/learned 面を薄混ぜ（昇格せず） | **done（NO-GO）** · 最良 α0.02 TypeA **Δpool −0.093** |

### Wave-18 — F閉鎖の井型狭帯監査（2026-07-26 · 提出なし）

> 結果: [`wave18-f-narrow-result`](../docs-ja/discussion/wave18-f-narrow-result.md) · 作業: [`exp/work/wave18-f-narrow/`](work/wave18-f-narrow/)

| ID | 仮説 | 状態 |
|---|---|---|
| **CHK-199** | F011–F020 を井型で狭めれば残 EV がある | **done（GO監査）** · 新規レバーなし · 有効狭帯は farvol/twostage に吸収済 |
| **CHK-200** | 近傍を密度通過井だけにすれば有効（F012 狭帯） | **done（NO-GO）** · 3/20 · Δ悪化 |
| **CHK-201** | 低整合井だけ CF（F018 狭帯） | **done（NO-GO）** · T2 で CF>tip が **0/80** |
| **CHK-195r** | 段食い違い代理で SOFT ゲート（昇格せず） | **done（NO-GO）** · portable を超えず |

### Wave-17 — 中間改善探索（2026-07-26 · 採点待ち並行 · 提出なし）

> 目的: soft oracle +0.155 の残り ~0.07〜0.10 を **ラベル無し**でどこまで取るか  
> 制約: **F015**（中間面を submission にしない）· F020 · 188/189 触らない  
> 物差し: [`intermediate-improvement-ledger`](../docs-ja/discussion/intermediate-improvement-ledger-2026-07-26.md)  
> 作業: [`exp/work/wave17-mid-improve/`](work/wave17-mid-improve/)

| 優先 | ID | 仮説（手法 × 期待） | action | acceptance | 状態 |
|---|---|---|---|---|---|
| W0 | **CHK-192** | soft が tip を勝つ井を推論時特徴だけで分離できる（AUC≥0.75） | T4 | AUC·prec/rec · 提出なし | **done（GO）** · `tip_std` AUC **0.978** |
| W1 | **CHK-193** | two-stage 半減井を portable 代理し T2 厳格（Δpool≥+0.05 · samp≥0） | T0 | tip-cv 厳格 · 井名ハードコード禁止 | **done（GO）** · tip_std hi-k5 ≡ oracle · +0.063/+0.0005 |
| W1b | **CHK-193b** | farvol × two-stage 結合 | T0 | 結合が farvol 単独を超える | **done（farvol単独勝）** · 重ねない · +0.072/+0.004 |
| W2 | **CHK-194** | 入れ子遠MD 弱い SOFT | T0 | strength≤0.08 · far≤0.40 · T2 厳格 | **done（NO-GO）** |
| W3 | **CHK-195** | tip FINAL vs `before_*` 食い違いゲート | T4→T0 | portable · F015 厳守 | **skipped**（EV低） |
| W4 | **CHK-196** | W0–W3 最良を1設定に固定し ledger 追記 · 次提出 0/1 | T4 | ledger + GO/NO-GO | **done** · [`wave17-result`](../docs-ja/discussion/wave17-mid-improve-result.md) |

**次提出候補（承認後）:** **原則なし**（SOFT/portable/s05 打ち切り）· Wave-20 generator が selector-baseline を明確に超えたときのみ再検討 · twostage は低優先。  
**Kaggle CPU:** `wave17-gate-audit-cpu` Ver3 COMPLETE。  
**Kaggle GPU:** `tip-portable-twostage-s05`（CHK-197 smoke · 提出なし）。

| ID | 仮説 | action | 状態 |
|---|---|---|---|
| **CHK-197** | portable + tip_std hi-k5 two-stage を tip E2E で smoke（可視 apply/halve 確認） | T0 | **done（GO · 提出なし）** · Ver1 COMPLETE · 可視 halve=`00bbac68` s=0.025 · [`result`](../docs-ja/discussion/chk197-twostage-e2e-result.md) |
| **CHK-197b** | gated>8 + tip_std two-stage が sample を守る | T0 | **done（NO-GO）** · samp −0.014〜−0.024 |
| **CHK-198** | tip_std 連続 strength が hard two-stage を超える | T0 | **done（NO-GO）** · 最良≈two-stage 同等 |

**Explicit Stop（Wave-17）:** 中間面昇格（F015）· 全井SOFT/攻撃的 self-line（F020）· 188/189 · Final UI 差し替え · ラベル井リスト直提出 · farvol+two-stage 重ね · gated×twostage（197b）。

### Wave-16 — tip generator 天井（2026-07-25）

> 設計: [`chk186-plan`](../docs-ja/discussion/chk186-generator-ceiling-plan.md) · 結果: [`chk186-result`](../docs-ja/discussion/chk186-generator-ceiling-result.md)  
> 前提: CHK-185 tip+SOFT +0.15 → tip lik-PF 128-seed  
> 制約: 新予測面禁止 · F015 禁止 · **188/189 は自動開始しない**

| 優先 | ID | 仮説（手法 × 期待） | action | acceptance | 状態 |
|---|---|---|---|---|---|
| G0 | **CHK-186** | tip `lik_pf` / `_pf_lik_allseeds` の **シード軌跡集合**に、真値に近い候補（例: oracle RMSE≤4.5 or ≤6）が入る井が一定割合ある。入るなら「選択」、入らないなら「generator不足」が確定する | T4 | T2 allowlist seed-oracle · `frac_hit` · gap · **提出なし** | **done（mixed）** · pooled FINAL **8.33** vs oracle **8.13**（+0.20）· hit≤4.5 **46%** · hard20 oracle **12.9** · [`result`](../docs-ja/discussion/chk186-generator-ceiling-result.md) |
| G1 | **CHK-187** | tip パイプライン **中間面**（pre-mpkg / pre-BH / FINAL 等）のラベル付き oracle が FINAL より有意に良い（診断のみ。提出昇格はしない） | T4 | 段ごと per-well RMSE · pooled gap · F015 再提出禁止を明記 | **done（GO · F015再確認）** · soft oracle **+0.14** · tip最良64/80 · PF混入の大gapは提出不可 · [`result`](../docs-ja/discussion/chk187-stage-oracle-result.md) |
| G2 | **CHK-188** | **186 が hit高・gap大**のときだけ: 尤度温度/シード重みの **微小変更**で seed-oracle に近づく（新面なし · プロファイル大切替は F013 禁止） | T4→T0 | 186 PASS分岐のみ · T2 厳格 · sample 非悪化 · 承認後 | **parked → Wave-20 CHK-205 に吸収** |
| G3 | **CHK-189** | 粒子数・`gs`・窓の **大改修**で generator 命中が上がり 4.8 帯に近づく | T3 | **既定 Park** · 明示承認時のみ · pretrain-gate · F013/乱獲禁止と両立する設計が必要 | **parked → Wave-20 CHK-206 に吸収** |

**分岐（CHK-186 確定）:**

| 186 の読み | 次 | 判定 |
|---|---|---|
| `frac_hit_le_4.5` 高 · `gap` 大 | **CHK-188** | **否**（mean_gap≈0 · pooled +0.20） |
| `frac_hit_le_6` 低 · `gap` 小 | Park 189 · **OPS-FINAL2** | hard20 は近い |
| 井型で混在 | Wave-14 結合 · 易井維持 / 難井受容 | **採用** |

**Explicit Stop（Wave-16）:** 近傍コピー · 方位分割学習 · NCC/DTW 新面 · 学習 ranker 新規 · 中間面の submission 昇格（F015）· seed 乱獲で Public を追うこと。

### Wave-15 — 別系統天井（CHK-185 · 2026-07-25 · ローカル CPU）

> 計画: [`chk185-candidate-ceiling-plan`](../docs-ja/discussion/chk185-candidate-ceiling-plan.md) · 作業: [`exp/work/chk185-candidate-ceiling/`](work/chk185-candidate-ceiling/)  
> 制約: 既存 tip 家系ディスク成果物のみ · NCC/近傍/方位新面禁止

| ID | 仮説（手法 × 期待） | action | acceptance | 状態 |
|---|---|---|---|---|
| **CHK-185** | tip 内部候補の oracle gap で「選択ボトルネック」vs「generator 不足」を分離できる | T4 | 報告 JSON · 解釈1行 · 提出なし | **done（GO）** · 選択残差 **+0.15** のみ · **generator不足支配** · [`result`](../docs-ja/discussion/chk185-candidate-ceiling-result.md) |

### Wave-14 — 井アーキタイプ + A/B分離（2026-07-25）

> 作業: [`exp/work/wave14-well-archetypes/`](work/wave14-well-archetypes/) · 文書: [`wave14`](../docs-ja/wave14-well-archetypes-2026-07-25.md)

| ID | 仮説（手法 × 期待） | action | acceptance | 状態 |
|---|---|---|---|---|
| **CHK-180** | 多切り口で型×後処理の効きが分離できる | T4 | 型表 + 効く変化マトリクス | **done（GO）** · A/B 各15 · E は ungated 有害 |
| **CHK-181** | ゲート内悪化井を方位メタで代理できる | T4 | prec≥0.5 · rec≥0.6 | **done（GO · 境界）** · `az_nwn_affinity` prec0.5/rec1.0 · **粗い** |
| **CHK-182** | 方位代理除外で portable より厳格改善 | T0 | T2 厳格 · samp 改善 | **rejected（NO-GO）** · samp↑だが pool +0.040&lt;0.05 |
| **CHK-183** | `tip_std_far/prox` が高ければ B（悪化）で、self_dev より A/B を分けられる | T4 | AUC≥0.9 · portable · T2 screen | **done（GO · screen）** · AUC **0.978** · thr≥0.842 · 除外=oracle k5 · T2 Δpool **+0.072** · Δsamp **+0.004** · [`ab-separation`](work/wave14-well-archetypes/ab-separation-report.json) |
| **CHK-184** | portable + farvol除外を本採点し、枠1候補にできる | T0 | 閾値固定 · tip E2E · SUB-10 | **done（NO · Public）** · **6.541** · [`ops-lb-101112`](../docs-ja/ops-lb-101112-public-2026-07-26.md) |

**確定知見（採点待ち中でも有効）:**

| 項目 | 内容 |
|---|---|
| A（助け） | 高 self_dev かつ **遠方 tip が相対的に滑らか** → 弱い gated SOFT が効く |
| B（悪化） | 高 self_dev でも **`tip_std_far/prox` 大** → SOFT 除外が正しい |
| 使わない | 方位だけの悪化代理（CHK-182）· oracle 井リスト直接提出 · self_dev 単体で A/B |
| 提出 | 当面 **Wave-13 portable** · farvol は CHK-184 後 |

### Wave-13 — gated soft 洗練 + Final 運用（2026-07-25 · A完了 · **OPS-LB-89 DONE**）

> 方針: 別予測面は作らない。Wave-12 の合法レバーだけを回す。

#### A. 採点待ち並行（Public 不要 · ローカル CPU）

> SUB-8/9 の採点を待たずに回せる。既存 tip T2 / hard20 予測への後処理 graft が主。GPU・提出なし。

| 優先 | ID | 仮説（手法 × 期待） | action | acceptance | 状態 |
|---|---|---|---|---|---|
| A1 | **CHK-170** | `self_dev>12` または複合ゲート（`>8`∧`heel_corr<0.85`）が `>8` 単体より sample を守り pool≥+0.05 を維持する | T0 | T2 厳格 · hard 非悪化 · CPU | **done（GO）** · 複合 `(>10)∧(heel&lt;0.85)` · Δpool +0.082 · Δsamp −0.0078 |
| A1 | **CHK-174** | 閾値グリッド `self_dev∈{6,8,10,12,15}` で厳格帯の最適点が `>8` 以外にある | T0 | 最良が厳格 PASS · 報告 JSON · CPU | **done（GO）** · 最良 `>10` · +0.085 / samp −0.024 · [`chk174`](work/wave13-gated-refine/chk174-report.json) |
| A2 | **CHK-171** | ゲート通過井だけ strength∈{0.05,0.08}（far=0.33）再調整で T2 厳格を改善する | T0 | 同上 · ≥0.15 禁止（F020）· 全井禁止 | **done（GO）** · **s=0.05** · Δsamp −0.0036 |
| A2 | **CHK-175** | ゲート固定（`self_dev>8`）のまま far_frac∈{0.25,0.33,0.40} を変えると sample が改善する | T0 | T2 厳格 · far≥0.5 禁止（F020）· CPU | **done（NO-GO）** · f40 pool↑だが samp悪化 · **far=0.33 維持** |
| A3 | **CHK-173** | strength∝clip(self_dev) 連続化がハード閾値より sample 平均悪化が小さい | T4→T0 | まず T4 · 厳格空なら reject | **rejected（NO-GO）** · 悪化井で cont strength↓せず · T0未実施 |
| A3 | **CHK-176** | 井別 SOFT Δ の上位悪化井だけ strength を下げる（二段 strength）と sample が回復する | T0 | T2 厳格 · 全井同一 strength より改善 · CPU | **done（GO · 条件付き）** · k=5 · Δsamp +0.0005 · oracle井は提出不可 |
| A4 | **CHK-177** | hard20 だけ見ると gated は tip より良く、T2 sample ゲートと矛盾しない候補が残る | T4 | hard20 報告 · 提出根拠にしない · CPU | **done（診断）** · soft +0.113 · two-stage +0.130 vs tip |
| A4 | **OPS-PREP-89** | SUB-8/9 比較表・forecast 更新テンプレ・sha/差分を先に用意する | — | テンプレ+compare 固定 · Public 欄は空 | **done** · [`ops-prep-89-compare`](work/wave13-gated-refine/ops-prep-89-compare.md) |

> **A 完了 · 引き継ぎ:** [`wave13-a-best.json`](work/wave13-gated-refine/wave13-a-best.json) · 安全側=portable **複合ゲート + f33-s05** · 候補=+farvol除外（CHK-183/184）· 次は **OPS-LB-89**

#### B. 採点後 / 承認後（Public または GPU）

| 優先 | ID | 仮説（手法 × 期待） | action | acceptance | 状態 |
|---|---|---|---|---|---|
| B0 | **OPS-LB-89** | SUB-8/9 Public を読み、gated 継続可否と forecast を更新する | T0 | Public 記入 · tip/Best 比 · 両方悪化なら提出系停止 | **done（GO）** · SUB-9 **6.484** · SUB-8 **6.582** · [ops-lb-89](../docs-ja/ops-lb-89-sub89-public-2026-07-26.md) |
| B1 | **CHK-184** | portable + `tip_std_far/prox` 除外を本採点し枠1材料にする | T0 | T2/T3 · tip 比 · 閾値リーク注意 | **done（NO）** · Public **6.541** · [ops-lb-101112](../docs-ja/ops-lb-101112-public-2026-07-26.md) |
| B2 | **CHK-178** | portable 複合+s05 を tip E2E 提出（farvol なし） | T0 | COMPLETE · Notebook 紐づけ | **done（NO）** · Public **6.556** · Trust≠Public |
| B2b | **CHK-191** | Best 同ゲート `self_dev>8` で strength **s05**（s08 軟化）を本採点 | T3 | COMPLETE · tip 比 · Private | **done（NO）** · Public **6.530** · 強度軟化禁止 |
| B0 | **OPS-FINAL2** | 締切前に枠1/枠2を UI 確定（仮: 枠1 SUB-9 · 枠2 旧Best） | — | timeline に記録 | **pending（締切前必須）** |
| B1 | **CHK-172** | tip-cv に選定 gated（±farvol）を載せ、枠1 Trust CV が tip を上回る | T0 | tip-cv T2/T3 · tip 比 · Final1 根拠 | **park（低優先）** · SUB-9 で枠1十分 · portable 再提出禁止 |

**分岐（OPS-LB-89 + OPS-LB-101112 確定）:**

| Public 読み | 判定 | 次 |
|---|---|---|
| gated（SUB-9）**6.484** 最良 | **採用 · Best 維持** | Final=枠1 SUB-9 / 枠2 旧Best |
| SUB-11 s05 **6.530** | **強度軟化 NO** | s08 固定 · 再軟化禁止 |
| SUB-10/12 portable 系 | **枠外** | portable/farvol 再提出しない |
| SOFT（SUB-8）**6.582** | **全井 SOFT 打ち切り** | 再強化禁止 |

### Wave-12 — 難易度ゲート付き SOFT（2026-07-25 · ローカル CPU · **厳格 PASS**）

> 作業: [`exp/work/chk160-difficulty-gate/`](work/chk160-difficulty-gate/) · [`exp/work/chk161-gated-soft/`](work/chk161-gated-soft/)

- [x] **CHK-160** | high | action:T0 | SOFT Δ × メタ分類 | **done（GO）** | self_dev 相関 +0.45 · 提出可能ゲート複数
- [x] **CHK-161** | high | action:T0 | 条件付き SOFT T2 厳格 | **PASS** | 最良 **self_dev>8**: pool **+0.084** · hard +0.203 · samp **−0.043** · `chk161-report.json`
- [x] **CHK-162** | high | action:T0 | tip fork `self_dev>8` + smoke | **done（GO · SUB-9）** | Ver1 COMPLETE · ref **54972467** **PENDING** · [SUBMIT](../my-submitted-notebook/tip-gated-selfline-selfdev8/SUBMIT.md) · 枠1自動差し替えなし

### Wave-11 — tip 遠MD 自己線（2026-07-25 · **F020 + SUB-8**）

> 作業: [`exp/work/chk150-far-md-uncertainty/`](work/chk150-far-md-uncertainty/) · NB: `my-notebook/tip-soft-selfline-f33s08/` · ran: `my-ran-notebook/tip-soft-selfline-f33s08/`

- [x] **CHK-150** | high | action:T0 | tip 遠MD 不確実性（自己線） | **conditional → F020** | hard20 PASS · T2 厳格 NO-GO（sample 悪化）· SOFT `f33-s08` のみ · 攻撃的 strength≥0.15 禁止
- [x] **CHK-151** | high | action:T0 | tip fork SOFT f33-s08 smoke+提出 | **done（SUB-8）** | Ver1 · ref **54970975** Public **6.582**（tip+0.013 · 打ち切り）

### Wave-10 — 手がかりスタック（2026-07-25 · ローカル CPU）

> 作業: [`exp/work/chk140-clue-stack/`](work/chk140-clue-stack/)

- [x] **CHK-140** | high | action:T0 | tip hard20 誤差×メタ | **done** | 遠MD悪化 · heel_gr_tw_corr −0.34 · `chk140-report.json`
- [x] **CHK-141** | medium | action:T0 | tip 中間面サンプル診断 | **done（警告）** | サンプルは中間面が過適合 · Public F015 と矛盾 → 提出根拠にしない
- [x] **CHK-142** | medium | action:T0 | 公開NB差分 | **done** | pfcfg/Frontier 再掲のみ · 新機構なし
- [x] **CHK-143** | high | action:T0 | 低整合井→CF | **rejected（F018）** | pooled 25.4 ≫ tip 14.87
- [x] **CHK-144** | high | action:T0 | 遠MD heel直線 | **rejected（F019）** | pooled 609 ≫ tip
- [x] **CHK-145** | medium | action:T0 | 空間密度&lt;150ft | **done** | hard20=0% · 全train=1.7% · F012 強化

### Wave-9 — Heel 拘束 DTW（2026-07-25 · **F017 で閉鎖**）

> 作業: [`exp/work/chk130-heel-dtw/`](work/chk130-heel-dtw/) · [`wave9-status`](../docs-ja/wave9-status-2026-07-25.md)

- [x] **CHK-130** | high | bet:B5 | action:T4 | heel拘束 DTW hard20 | **rejected（NO-GO · F017）** | pooled **371** ≫ tip **14.87** · pearson≈0.95 · `chk130-report.json`
- [x] **CHK-131** | high | bet:B5 | action:T3 | tip上条件付き置換 | **cancelled** | 130 NO-GO
- [x] **CHK-132** | high | bet:B5 | action:T0 | T2 | **cancelled** | GPU 申請なし
- [x] **CHK-133** | medium | bet:B5 | action:T1 | 提出 | **cancelled** | CV PASS 未達

### Wave-8 — Private 防衛梯子（2026-07-25 · **F016 で閉鎖**）

> 作業: [`exp/work/chk120-dual-final/`](work/chk120-dual-final/) · memo [`chk120-kill-memo.md`](work/chk120-dual-final/chk120-kill-memo.md)

- [x] **CHK-120** | high | bet:B4 | action:T4 | tip/Best 最終面の井別不一致ゲート | **rejected（KILL · F016）** | tip≡Best FINAL · max_abs **0** · SHA一致 · `chk120-disagree-report.json`
- [x] **CHK-121** | medium | bet:B4 | action:T4 | tip field-stress | **cancelled** | 120 KILL のため未到達
- [x] **CHK-122** | high | bet:B4 | action:T3 | mechanism:`dual-final-well-arbiter` | **cancelled** | 120 KILL · **F016**
- [x] **CHK-123** | high | bet:B4 | action:T0 | アービター T2 | **cancelled** | GPU 申請なし（PASS 条件未達）

### 運用キュー

- [x] **OPS-SUB** | SUB-4–7 · VISUALS · **SUB-8 SOFT smoke PENDING** · [`forecast`](../docs-ja/cv-public-private-forecast.md) · **F015** · Final2=枠1 tip / 枠2 Best
- [ ] **OPS-SUB8-LB** | SUB-8 `54970975` Public 確定後に forecast / exp-infer 更新（待ち）
- [ ] **OPS-BEST-T2** | **低優先（任意）** · CHK-101 で tip≡Best preds · EDA上も同家系。**枠1選抜に必須ではない** · ユーザーが「Best 固有 CV を数値で残したい」と承認したときのみ
- [ ] **OPS-FINAL2** | 締切前 UI で枠1 tip · 枠2 Best を選択（**唯一の必須運用**）

### 駐車仮説（Parked · **Active 外**）— **2026-07-25 EDA監査で優先度改定**

> 監査根拠: [`strategy-from-eda`](../docs-ja/others-notebook/eda/strategy-from-eda.md) · Connor/geoanchor/A016 · **F015**（中間面 Public 悪化）  
> **結論:** EDA は「新 Active CHK を増やす」方向ではない。下表は **凍結／吸収** を明示し、別セッションの誤昇格を防ぐ。  
> **昇格条件（共通・さらに厳格）:** ユーザー明示承認 · gate PASS · **かつ** 下表の「再開してよいとき」を満たす · Bet 追加なら先に `comp-strategy`

| id | hypothesis（手法 × 期待） | 監査後 status | 再開してよいとき | EDA / 失敗との関係 |
|---|---|---|---|---|
| **CHK-110** | tip 上に geoanchor 流 suffix arbiter 条件だけ載せ T2 非悪化 | **frozen（低優先）** | 枠1の **CV 防衛**が危機（T2 大崩れ）かつユーザー承認。**Public 追い・Final2 差し替え目的では再開禁止** | EDA: tip 同面飽和 · #8 Public双子。F015: tip 面いじりは Public 悪化。別予測面ではない |
| **CHK-111** | tip 上で guarded contact OFF（A016）を hard20 screen | **rejected as score-hyp（凍結）** | **スコア目的では再開しない**。理解用にコードを読むだけ可 | EDA/geoanchor: prefix ガード付き contact が安全側。guard OFF は安全設計に逆行。盲提出は既存 Stop |
| **CHK-112** | Connor 幾何 drift/kappa を診断物差し化 | **absorbed（実行不要）** | 新 Bet（幾何経路）を戦略に戻す設計承認時のみ再掲 | EDA #3 + Connor NB 自体が診断完了（幾何天井〜10ft）。再測定の限界効用低 |
| **CHK-072** | well vs field-CV 差の監視 | **cancelled（条件付き再掲のみ）** | **空間特徴を入れる CHK の直前のみ** | EDA #7。B3/F012 閉鎖中は単独実行しない |

**吸収済み（CHK 不要）:** Discussion 728712 の PF `gs`×1.3 — tip 既実装。再乗算・再 fork は Stop。

**別セッション向け 1 行判断木:**

1. tip 同家系の fork / pfcfg / MHA / VISUALS / `gs` 再スイープ？ → **Stop**  
2. tip 中間面昇格 / mpkg 単独・強化提出？ → **F015**  
2b. tip×Best 井単位アービター？ → **F016**（CHK-120 tip≡Best）  
2c. heel 拘束 DTW / Sakoe-Chiba TVT？ → **F017**  
2d. 低整合→CF / 遠MD heel直線？ → **F018 / F019**  
2e. 攻撃的 tip_self_line（strength≥0.15 · sample 非悪化無視）？ → **F020**（SOFT f33-s08 は診断提出済 · 枠1自動差し替え禁止）  
3. 整合学習・ゲート近傍・方位学習の言い換え？ → **F011/F012/F014**  
4. geoanchor / A016 / Connor を「新しい勝ち筋」にしたい？ → **EDA監査済 · 110 frozen / 111 score-hyp 禁止 / 112 absorbed** · Active 化しない  
5. EDA 構造事実（tops独立 · U持ち越し · test/ · 二峰尖鋭 · 行ML）？ → **明示 Stop**（仮説ではない）  
6. それ以外の新機構？ → 先に `comp-strategy` + ユーザー承認 · **Active は空のまま**

### EDA × checklist 突合（検証サマリ）

| EDA 事実 | checklist への帰結 | 修正要否 |
|---|---|---|
| #1–4 評価区間・1面・U禁止・test/禁止 | 既に Stop · 運用済 | **修正不要** |
| #5–6 着床層・二峰 | CHK-080 done · 041 rejected | **修正不要** |
| #7 field-CV 差 | CHK-072 条件付きのみ | **修正不要**（空間 Bet 再開時のみ） |
| #8 Public 双子 | Final に載せない · F015 と整合 | **修正不要**（Stop 済） |
| #9 行 tabular | F010 · Stop | **修正不要** |
| B2/B3 閉鎖後の「別面」期待 | Active なしが正しい | **Active 再開不要** |
| Parked 110–112 | 公開NB材料の置き場としては妥当だが **昇格期待が過大** | **本節で優先度改定** |

### Wave-7 — B1 学習内方位分割（2026-07-24–25 · **F014 で閉鎖**）

> 途中〜最終: [`wave7-status-2026-07-25.md`](../docs-ja/wave7-status-2026-07-25.md) · early gate: `exp/work/chk100-b1/chk100-early-gate-memo.md`  
> 注: TIP_CV 後段は OOM → **early-ridge hard20** 対照比で判定

- [x] **CHK-100** | high | bet:B1 | action:T3 | mechanism:`azimuth-train-split` | **rejected（NO-GO）** | early-ridge pooled **31.82** vs 対照 **31.28**（+0.54）· well_mean +0.64 · `tip-cv-az-split-h20-ee`
- [x] **CHK-101** | high | bet:枠1 | action:T0 | Best T2 Trust CV | **done（注意）** | 報告 pooled **8.330** ≡ tip T2（preds max_abs0）· Best固有CVは未分離 · `chk101-best-t2-memo.md`
- [x] **CHK-102** | high | — | **cancelled** | 100 NO-GO のため未到達
- [x] **CHK-103** | medium | bet:B1 | action:T3 | mechanism:`azimuth-as-feature` | **rejected（NO-GO）** | early-ridge ≈対照（Δ≈0.003）· 改善なし · **F014**

### 実験提出（枠消化 · 2026-07-24/25 · Public 確定 · **F015**）

> 分析: [`sub-4-7-lb-analysis.md`](../docs-ja/sub-4-7-lb-analysis.md)

- [x] **SUB-4** promote gated_010 · ref **54958356** · Public **6.718** · tip+0.149 · **F015**
- [x] **SUB-5** promote pre-BH · ref **54958359** · Public **6.653** · tip+0.084 · **F015**
- [x] **SUB-6** promote gated_020 · ref **54958970** · Public **6.621** · tip+0.052 · **F015**
- [x] **SUB-7** promote mpkg-only · ref **54958971** · Public **20.067** · **F015** 壊滅
- （参考）VISUALS · **54958520** · Public **6.581** · Best未満

### Wave-6 — tip 離散プロファイル梯子（2026-07-24 · 完了）

> 計画: tip内部 `SUBMISSION_PROFILE` / SP45 · F001–F012 外 · Final選抜は [`comp-strategy`](../docs-ja/comp-strategy.md)

- [x] **CHK-090** | high | bet:枠1 | action:T0 | mechanism:`vp_conservative_final` | tip既定比で改善 | **rejected（NO-GO）** | E2E≡default tip（max_abs0）· tip-cv early-exitはVP非到達 · `chk090-e2e-compare`
- [x] **CHK-091** | high | bet:枠1 | action:T0 | mechanism:SP45 0.50/0.50 | tip hard20 非悪化 | **rejected（NO-GO）** | hard20 pooled **24.78** ≫ tip **14.87** · `tip-cv-report-chk091.json`
- [x] **CHK-092** | high | bet:枠1 | action:T0 | 090/091 勝者 T2 | — | **cancelled** | 勝者なし
- [x] **CHK-093** | medium | bet:枠1 | action:T4 | `bimodal_guarded` E2E screen | **rejected（NO-GO）** | E2E≡default tip · **F013** |

### 提出準備 CV（最優先）

- [x] **CHK-014** | high | bet:基盤 | action:T0 | tip 予測を well-group 物差しに載せ、CF 同井集合より良く・難井悪化≤0.1・カバー≥99%なら提出準備 CV PASS。併せて tip Notebook 紐づけ smoke 1回で再現確認する | source: docs-ja/submission-prep-cv.md · wave0-ruler | acceptance: (1) `tip-cv-report.json` PASS (2) smoke 提出が Notebook 紐づけで受理 (3) 追加提出は PASS 後のみ | **done** | tip pooled 14.87 · smoke **6.569**（作者6.478差+0.091 · Best6.524未満）

### 基礎ギャップ（CHK-020 前 · T4）

- [x] **CHK-050** | high | T4 | GroupKFold vs Random + tops リーク静的証明 + heel/eval 分布 | **done** | Ridge: Random が Group より楽観 · tops で train CV だけ改善 · F003 · `foundation-chk050-report.json`
- [x] **CHK-051** | high | T4 | tip hard20 非決定性 | **done** | 真の2-run（seed42 vs 123）· preds **identical** · pooled 14.87 · `tip-nondet-report.json`
- [x] **CHK-052** | high | T4 | 方位×MD×bimodal 残差地図 | **done** | 最悪=`NW_N` · MD遠方ほど残差大 · bimodal_active=0 → 041は `_BH_*` · `error-structure-report.json`
- [x] **CHK-053** | high | T4 | tip vs Sunny hard20 相関 | **done** | corr **0.999** だが Sunny RMSE≈24≫tip · SUB-1で **9.150** 実証 · Sunny Final除外（F004）· Final2方針は `comp-strategy`

### Wave-0 / tip

- [x] **CHK-013** | high | T1 | tip Private fork | **done** | `kazeneko77/rogii-luck-is-all-you-need-private-tip-fork`

- [x] **CHK-010** | high | T0 | well-GroupKFold + CF OOF 物差し確立（tip フル OOF は GPU 別） | **done** | CF 5-fold OOF ≈14.8–17.9 · pooled≈**15.91** · `exp/work/wave0-ruler/`

- [x] **CHK-011** | high | T4 | tip GPU 完走 wall-clock 記録 · ×200 外挿 | **done** | ≈13min / 3wells · scoring 外挿 **~14h > 9h** → 縮小案を run-log に記載

- [x] **CHK-012** | medium | T0 | CF well-group CV 門番 | **done** | pooled≈15.91 · well-median≈10.67 · これより悪い単独手法は rejected

- [x] **CHK-024** | medium | T4 | hard-well セット固定 | **done** | 20 wells（`86454a6f`+CF worst）· `exp/work/wave0-ruler/hard-wells.json`

### Wave-1 — tip 上 graft（代理は rejected · tip 実装待ち）

- [x] **CHK-020** | high | T3 | tip 上の方位分割 graft | **rejected（F006+F009）** | postprocess blend **F006** · tip内 NW_N BH=0.90 **F009**（pooled 14.869→14.883 · NW_N悪化）· 方位ビンだけ BH 上げ再実行禁止
- [x] **CHK-021** | high | T3 | 素朴 heel `gs` sweep（Typewell 無し） | **rejected** | gs≠1 で pooled 30–32（CF 15.9 より悪化）· 雑 affine NO-GO · failures F001
- [x] **CHK-022** | high | T3 | 素朴近傍コピー | **rejected（600ft）/ 150ft 非改善** | nbr_150 pooled 15.95 · nbr_600 **18.97** · F002
- [x] **CHK-023** | medium | T3 | 退化 midpoint hedge 代理 | **rejected** | CF±sep の中点=CF · tip の `_BH_*` graft が本実験

### Wave-2 — Final 多様性（同家系のため枠2必須）

- [x] **CHK-030** | high | T1 | 線形 MD drift 代理を物理経路扱い | **rejected（代理）** | pooled≈1400
- [x] **CHK-030b** | high | T1 | Sunny physical Private fork（CPU）完走 · tip 相関 | **rejected（Final）** | SUB-1 Public **9.150** · hard20 RMSE≈24≫tip · **F004** · Final/予備とも除外
- [ ] **CHK-031** | high | T3 | Mitch drift+NCC 特徴移植 | **superseded by CHK-070** | F007/F008 · 後継=CHK-070 drift 自前学習

### Wave-4 — GPU 学習メイン（2026-07-24）

- [x] **CHK-070** | high | T3 | drift/residual CatBoost GPU 学習で Final2 | **rejected（F010）** | hard20 OOF **31.80**（CF超え）だが tip corr **0.999** · tip14.87に大敗 · full773 pooled15.14も tip高相関
- [x] **CHK-071** | medium | T3 | LGBM TrackA proxy 再学習 | **rejected（NO-GO）** | hard20 OOF **214.8** ≫ CF · 枠1改善なし

---

> 方針: 文献・整合学習・近傍ゲート Active は **閉鎖（F011/F012）**。EDA拘束: [`strategy-from-eda`](../docs-ja/others-notebook/eda/strategy-from-eda.md) · Final選抜: [`comp-strategy`](../docs-ja/comp-strategy.md)

- [x] **CHK-040** | high | bet:B2 | action:T3 | heel+窓 NCC → drift 学習 | **rejected（F011 NO-GO）** | tip pearson≈0.999 · memo `chk040-final2-memo.md`

- [x] **CHK-041** | medium | bet:B2 | action:T3 | 多峰 hedge | **rejected（NO-GO）** | `_BH_=0.30` 微悪化

- [x] **CHK-072** | high | bet:B2 | action:T4 | well vs field-CV | **cancelled** | 040 F011 で前提消滅 · **空間特徴を入れる CHK の直前に再掲**

### Wave-5 — EDA 由来（F011 後 · 2026-07-24）

- [x] **CHK-080** | medium | bet:基盤 | action:T4 | **着床層（EGFDL vs Austin 等）· Buda 急崖品質 · 二峰フラグ**で hard20 / tip 残差を再層別し、次仮説の切断面を表にする | source: eda/decoding-eagle-ford · 15-ft-datum · strategy-from-eda S1b | acceptance: (1) 層別 RMSE 表 (2) 新 CHK の切断面を1行で提案 or 「層別しても単一戦略で足りる」と結論 (3) 本実験・提出なし | **done** | EGFDL_like tipRMSE≈15.1 vs BUDA≈13.0 · bim0/20 · cut=`exp/work/chk080-screen/chk080-report.json`

- [x] **CHK-081** | high | bet:B3 | action:T3 | mechanism:近傍井を **距離&lt;150ft かつ GR/照合類似度ゲート**で選び TVT プロファイルをシフト転写し、ゲート外は tip/CF にフォールバック | **ゲート付き近傍転写**は tip と同井で tip pearson **&lt;0.90** かつ CF より pooled≥0.05・hard悪化≤0.1 | source: eda · discussion/726465 · strategy-from-eda S2a · ≠F002素朴コピー | acceptance: (1) hard20 上記ゲート (2) tip corr&lt;0.90 (3) 無ゲート/600ft 対照より良い (4) **ユーザー承認後のみ GPU/本実験** | **rejected（F012 NO-GO）** | hard20 空間疎 · soft適用3/20 · OOF49.59≈CF · tip corr≈0.999 · memo `chk081-final2-memo.md`

---

## In progress

- **Final 運用 + 手がかり監視**（F011–**F019** · Active スコア仮説なし）
- Final 選抜仮: 枠1=tip Trust CV · 枠2=Public Best — [`forecast`](../docs-ja/cv-public-private-forecast.md)
- 必須は **OPS-FINAL2**。Wave-10 手がかり: [`wave10-clue-stack`](../docs-ja/wave10-clue-stack-2026-07-25.md)

---

### Wave-CV — 用途別 Tier 体制（基盤）

> SSOT: [`docs-ja/cv-tiers.md`](../docs-ja/cv-tiers.md) · T0/T1=hard20 · T2=方位層化80井 · T3=3seed · T4=空間は条件付き

- [x] **CHK-060** | high | T0 | CF GroupKFold fold-seed 3種（42/123/2026）で門番安定幅を確定 | **done** | pooled OOF **15.91**（seed不変）· worst_fold band **≈0.51** · fold_mean band **≈0.05** · `cf-multiseed-report.json`

- [x] **CHK-061a** | high | T0 | T2 allowlist（hard20_balanced · 方位層化 sample60）構築 | **done** | n=80 · 方位 sample 各15 · `tip-cv-allowlist-balanced.json`

- [x] **CHK-061** | high | T0 | tip T2 CV（balanced 80井 · GPU ≈6h）実測 | **done** | Ver4 · wall≈1.5h · tip pooled **8.33** vs CF同井 **27.77** · hard悪化なし · cover1.0 · `tip-cv-report-t2.json` **PASS**

- [x] **CHK-062** | medium | T0 | tip T3 multi-seed（同80井 · 3 seed）で Final 用バンド確定 | **done（GO）** | pooled **8.330** · band **0.0** · 3seed preds identical · CHK-051 と整合 · `tip-cv-report-t3.json`

---

## 既存 CHK × 論文語彙（裏打ちマップ · 新規実験ではない）

| 既存 CHK | 論文語彙（literature-survey） | いまの状態 | 読み替え |
|---|---|---|---|
| CHK-010 / 012 ruler · CF 門番 | 検証用 oracle / baseline | done | ローカル物差し |
| CHK-024 hard-set | 失敗ケースの明示 | done | 難井を平均に埋もれさせない |
| CHK-021 heel 校正 | P4 affine | **rejected** F001 | 雑 affine NO-GO |
| CHK-023 / 041 二峰 hedge | P2 multimodal | **rejected** | データ限界井は尖らせない |
| CHK-030b 物理 PF | P1 | **rejected** F004 | — |
| CHK-022 / 081 近傍 | offset prior | **rejected** F002/F012 | 近傍転写打ち切り |
| CHK-020 方位後処理 | — | **rejected** F006/F009 | — |
| CHK-031/070/040 整合·残差 | P3 | **rejected** F007–F011 | 整合系打ち切り |
| CHK-072 field-CV | leave-spatial-out | **cancelled→Parked再掲条件** | 空間 CHK 直前 |
| CHK-080 着床/二峰 | EDA | **done** | 単一戦略で足りる |
| Connor dz-dtvt | 幾何 drift / LOO | **absorbed（CHK-112）** | NB読了=診断 · 再実行低優先 |
| geoanchor arbiter | suffix 合意ゲート | **frozen（CHK-110）** | CV防衛以外再開禁止 |
| A016 guard OFF | contact ablation | **score-hyp 禁止（CHK-111）** | 読むだけ |
| tip `gs*1.3` | PF noise scale | **吸収済** | 728712 · CHK不要 |
| Final 選抜 | — | 方針済 | [`comp-strategy`](../docs-ja/comp-strategy.md) |

**禁止の再確認:** F001–**F019** · 無制約 DTW · RL · 有料 DB · Active 乱増禁止（新 CHK は承認後のみ · Parked の勝手昇格も禁止）。

---

## 明示 Stop（Active に載せない · 再提案禁止）

| 禁止 | 理由 | 根拠 |
|---|---|---|
| dual-track α·seplo·seed 乱獲 | Public 密集 · Private 同時沈没 | leaderboard · tip "luck" |
| 行単位 tabular のみ本命 | CF に負ける | 726751 |
| 有料地下 DB | Host 未回答 | 728022 |
| tops 絶対アンカー | 潰れる | 727149 |
| 素朴 heel affine（GR無し gs） | CHK-021 rejected | wave0-ruler · F001 |
| 遠井素朴コピー（~600ft） | CHK-022 rejected | wave0-ruler · F002 |
| Sunny physical を Final/予備 | F004 | SUB-1 · CHK-030b |
| kernel_sources コピーだけの提出 | F005 | SUB-3 |
| tip 中間面昇格 / mpkg 単独・強化提出 | F015 | SUB-4–7 · sub-4-7-lb-analysis |
| tip×Best dual-final 井単位アービター | F016 | CHK-120 tip≡Best |
| heel 拘束 band-limited DTW→TVT | F017 | CHK-130 pooled 371 |
| 低 heel整合 → CF フォールバック | F018 | CHK-143 |
| 遠MD heel 直線外挿/blend | F019 | CHK-144 |
| Public ±0.05〜0.3 を「枠1改善」扱い | seed バンド | cv-lb-private-relation |
| 枠1を Public 順位だけで決める | Private 耐性を捨てる | comp-strategy §Final2 |
| Random KFold / 行単位 CV を採択根拠 | well リークで楽観 | CHK-050 · F003 |
| 無制約 DTW 全面採用 | 文献でも破綻しやすい | literature-survey P3 |
| 他盆地公開 well log を学習混入 | ドメインずれ | literature-survey D4–D5 |
| RL 舵取りを RMSE 本命にする | タスク不一致 | literature-survey P5 |
| Active 乱増（承認なし新 CHK） | 方針済 · B2/B3閉鎖 | comp-strategy |
| heel+窓 NCC→drift 言い換え | tip 同面 | **F011** |
| tip 離散プロファイル（vp_cons / SP45 0.5 / bimodal）言い換え | 非改善 or 同一 | **F013** |
| U=TVT+Z 構造面持ち越し | CFより大幅悪化 | EDA tvt-identity |
| 6 tops を独立特徴化 | 1面 | EDA |
| Public 双子マッチを Final 戦略 | Private 無効 | EDA visual |
| 二峰分類ネットで平均超え | データ限界 | EDA 15ft |
| 他人の CV–LB ギャップで自モデル校正 | 個人ギャップは安定・流用不可 | 727570 |
| 手元 `test/` で学習検証 | train コピー（identity） | 727570 |
| tip 後処理の方位 blend / BH ビン上げ | 学習分割とは別物 · 悪化済み | F006 · F009 · 726465 |
| 横断 field slope 回帰を本命 | 合法特徴から学習困難 | 712037 |
| tip / ultimate-pf / gs130 の再 fork · `gs` 再乗算（×1.3 の二重適用） | tip に既実装 · 同家系 | refresh-20260725 · 728712 |
| pfcfg / Frontier VISUALS / shift / MHA\*sep\* 乱獲 | 票≠新規知見 · tip 同面 | refresh-20260725 |
| 純幾何梯子（Connor 型）を Final 本命 | LB~10 帯 · GR無し天井 | dz-dtvt-eda |
| geoanchor を「別予測面」として Final2 | dual-track 同家系 | rogii-geoanchor |
| A016 流 contact guard OFF を盲提出 / Final | ablation · submit-safe が本命 | a016… |
| A016 / guard OFF を **スコア改善仮説**として Active 化 | EDA: prefix ガードが安全側 · F015 | **CHK-111 改定** |
| geoanchor suffix を Public/Final2 目的で tip に載せる | tip 同面 · F015 | **CHK-110 frozen** |
| Connor 幾何の再測定だけを本実験にする | 天井既知 · 限界効用低 | **CHK-112 absorbed** |
| 「公開NBを読んだから Active に CHK 追加」 alone | 仮説×期待が無い | Skill checklist |

---

## 重複防止インデックス

| item-id | hypothesis（短） | status | exp / table ref | 結果要約 |
|---|---|---|---|---|
| CHK-014 | tip CV + smoke | **done** | tip-cv-report.json | tip 14.87 · smoke **6.569** |
| CHK-013 | tip luck fork | done | T022 · tip.md | Contact-Gated 同族 |
| CHK-010 | ruler + well CV | done | wave0-ruler | CF GKF pooled 15.91 |
| CHK-011 | 200well 時間 | done | run-ledger | ×200>9h リスク |
| CHK-012 | CF 門番 | done | wave0-ruler | 15.91 |
| **CHK-050** | Group vs Random · tops | **done** | foundation-chk050-report.json | F003 Random禁止 |
| **CHK-051** | tip nondet | **done** | tip-nondet-report.json | seed42≡123 · spread0 |
| **CHK-052** | 誤差地図 | **done** | error-structure-report.json | NW_N · MD遠方 |
| **CHK-053** | tip↔Sunny hard20 | **done** | tip-vs-sunny-hard20-corr.json | corr0.999 · Sunny禁止(F004) |
| CHK-020 | 方位 tip graft | **rejected** | F006+F009 | 学習内条件→040 |
| CHK-021 | heel gs | rejected | F001 | 悪化 |
| CHK-022 | 近傍 | rejected | F002 | 150非改善·600悪化 |
| CHK-023 | hedge 代理 | rejected | — | → CHK-041 |
| CHK-024 | hard-set | done | hard-wells.json | 20 wells |
| CHK-030 | phys 代理 | rejected | — | 1400 |
| CHK-030b | Sunny 物理 | **rejected Final** | F004 | 予備も除外 |
| CHK-031 | drift+NCC | **rejected** | F007+F008 | 後継 040 |
| CHK-032 | median CF×nbr | rejected | corr 0.98 | |
| CHK-033 | Final2 方針 | **superseded** | comp-strategy | 枠1 CV / 枠2 Public |
| CHK-070/071 | tabular 再学習 | **rejected** | F010 | — |
| **CHK-040** | heel+窓+drift | **rejected** | F011 | tip corr≈0.999 |
| **CHK-041** | 多峰 hedge | **rejected** | — | — |
| **CHK-072** | well vs field-CV | **cancelled** | — | 空間CHK前に再掲 |
| **CHK-080** | 着床/二峰 層別 screen | **done** | chk080-report.json | 単一戦略で足りる |
| **CHK-081** | ゲート近傍&lt;150 | **rejected** | F012 | 近傍打ち切り |
| **CHK-090–093** | tip離散プロファイル | **rejected** | F013 | 提出0 |
| **CHK-100** | B1 az-train-split hard20 | **rejected** | F014 | early-ridge +0.54 |
| **CHK-101** | Best T2 Trust CV | **done（≡tip）** | chk101 memo | Best固有は未測 |
| **CHK-102** | B1 T2 | **cancelled** | — | 100 NO-GO |
| **CHK-103** | az-as-feature hard20 | **rejected** | F014 | Δ≈0 |
| **SUB-4–7** | promote E2E 実験提出 | **rejected（F015）** | 6.718/6.653/6.621/20.067 | tip最終より悪化 |
| **CHK-120** | tip×Best 不一致ゲート | **rejected（KILL）** | F016 · max_abs0 | B4 閉鎖 |
| **CHK-130** | heel拘束 DTW hard20 | **rejected（F017）** | pooled 371≫tip14.87 | B5 閉鎖 |
| **CHK-131–133** | DTW置換 / T2 / 提出 | **cancelled** | — | 130 NO-GO |
| **CHK-121–123** | field-stress / arbiter / T2 | **cancelled** | — | 120 KILL |
| **CHK-110** | tip+suffix arbiter 条件 | **frozen** | EDA監査 07-25 | CV防衛以外禁止 |
| **CHK-111** | contact guard OFF screen | **rejected score-hyp** | EDA監査 07-25 | 読むだけ |
| **CHK-112** | 幾何 drift 診断物差し | **absorbed** | Connor NB | 再実行不要 |
| **gs×1.3** | PF noise scale | **absorbed** | tip 既実装 | CHK不要 |
| **CHK-060** | CF fold multi-seed | **done** | cf-multiseed-report.json | pooled 15.91 |
| **CHK-061a** | T2 allowlist | **done** | tip-cv-allowlist-balanced.json | 80井 |
| **CHK-061** | tip T2 CV | **done** | tip-cv-report-t2.json | pooled 8.33 |
| **CHK-062** | tip T3 multi-seed | **done** | tip-cv-report-t3.json | band 0 |

---

## Phase 1 完了チェック

- [x] pre-strategy PASS · ヘッダにスコア再掲なし
- [x] F011/F012 · B2/B3 閉鎖
- [x] Wave-6 tipプロファイル · **F013** · 提出0
- [x] Final 選抜方針確定（枠1 CV / 枠2 Public）
- [x] CV Tier 060–062 done
- [x] Wave-7 B1 承認 · Phase0–1 完了
- [x] Wave-7 Phase2（CHK-100/101/103）— **完了 · F014**（100/103 NO-GO · 101≡tip）
- [x] SUB-4–7 Public 確定 · **F015** · OPS-SUB 完了
- [x] 公開NB refresh → Parked CHK-110–112
- [x] **EDA×Parked 監査** → 110 frozen · 111 score-hyp禁止 · 112 absorbed · Active 再開なし
- [x] Wave-8 CHK-120 · **F016** · tip≡Best · B4 閉鎖 · CHK-121–123 cancelled
- [x] Wave-9 CHK-130 · **F017** · heel-DTW NO-GO · B5 閉鎖 · CHK-131–133 cancelled
- [x] Wave-10 CHK-140–145 · **F018/F019** · 手がかりスタック（新面未発見）
