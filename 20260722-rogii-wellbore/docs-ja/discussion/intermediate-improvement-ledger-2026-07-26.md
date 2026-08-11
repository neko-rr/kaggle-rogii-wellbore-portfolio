# 中間地点改善レジャー — 実測Δ × oracle（2026-07-26）

> 目的: 「選択・中間面で 4.8 に届かない」の先に、**どれだけ改善できるか**を実測と理論上限で並べる  
> 用途: 今後の gated / soft / 段選択の模索時の **参照 SSOT**（再発明防止）  
> 提出: 本ファイルは診断。昇格は F015/F020 と Trust CV 厳格を別途通すこと

---

## 1 行

**ラベル無しで実際に取れる T2 改善は、だいたい Δpool +0.05〜0.08（厳格帯）。**  
SOFT ラベル oracle 上限は **+0.155** → 実測は上限の **約 1/3〜1/2**。  
4.8 までの距離（CV tip 8.33→4.8 = **3.53**）に対し、実測は **約 1.5〜2.3%** しか埋めない。

---

## 物差し

| 項目 | 値 | 出典 |
|---|---|---|
| tip T2 FINAL（行重み） | **8.330** / hard **14.870** / sample **3.624** | `tip-cv-report-baseline.json` |
| SOFT ラベル oracle | **8.175**（Δ **+0.155**） | CHK-185 B |
| PF seed-oracle（診断） | **8.132**（Δ **+0.198**） | CHK-186 · **提出段ではない** |
| 4.8 までの距離（CV） | **3.53** | 8.330 − 4.8 |
| tip Public | **6.569** | SUB tip smoke |
| Δ の符号 | **正 = tip より良い**（RMSE 低下） | — |

---

## 表 A — 実測（ラベル無し） vs oracle

基準: tip T2 FINAL。Δ = tip − candidate（大きいほど良い）。

| 候補 | 種別 | pool | Δpool | hard Δ | samp Δ | 厳格感* | oracle対比 |
|---|---|---:|---:|---:|---:|---|---|
| **SOFT ラベル oracle** | 理論上限 | 8.175 | **+0.155** | — | — | （ラベル見ている） | **100%** |
| **PF seed-oracle** | 診断上限 | 8.132 | **+0.198** | hard +1.99 | samp **悪化** | 提出不可 | （別軸） |
| portable 複合+`f33-s05` | **実測・推奨** | 8.277 | **+0.053** | +0.113 | **−0.004** | PASS | oracle の **34%** |
| farvol 除外（A/B） | 実測 screen | 8.258 | **+0.072** | +0.146 | **+0.004** | screen PASS | **46%** |
| compound `>10`∧heel | 実測 | 8.249 | **+0.082** | +0.174 | −0.008 | PASS 寄り | **53%** |
| selfdev8 ungated寄り | 実測 | 8.246 | **+0.084** | +0.203 | **−0.044** | sample 悪化 | 上限近いが危険 |
| selfdev10 | 実測 | 8.245 | **+0.085** | +0.192 | −0.024 | sample 悪化 | 同上 |
| two-stage k5 | 実測（リーク注意） | 8.267 | **+0.063** | +0.130 | +0.001 | PASS だが井リスト要代理 | **40%** |
| **two-stage tip_std hi-k5** | **Wave-17 CHK-193 · portable** | 8.267 | **+0.063** | +0.130 | **+0.001** | **PASS · oracle一致** | **40%** |
| farvol+two-stage | Wave-17 193b | ≤farvol | **劣後** | — | +0.004 | 重ねない | — |
| nested far MD | Wave-17 CHK-194 | — | **NO-GO** | — | — | ref 超えず | — |
| tip×SP45 薄混ぜ α≤0.05 | Wave-19 CHK-202 · Type A | hard20 | **−0.093〜−0.50** | — | （sample空） | **NO-GO** | 0% |
| gated s05 / portable Public | OPS-LB-101112 | Public | Best未達 | — | — | **枠外** | Trust≠Public |
| BH / NW_N ノブ | 実測 | ≡tip | **0** | 0 | — | 無意味 | 0% |
| tip 多シード CSV | 実測 | ≡tip | **0** | 0 | — | 無意味 | 0% |

\*「厳格」= T2 で sample 非悪化を重視する運用（Wave-13）。正確な gate 定義は各 tip-cv-report。

### 読み（表 A）

1. **実測で安全に取れるのは +0.05〜0.07 級**（portable / farvol）。  
2. **+0.08〜0.09 は sample を削りやすい**（selfdev 広め）→ LB では裏目になりやすい。  
3. oracle +0.155 の **残り ~0.07〜0.10 は「ラベル選択」でしか取れない** → 提出時には使えない。  
4. PF seed +0.20 は **tip FINAL 後段と別物**。易井では tip が既にシードより良い。

---

## 表 B — Public での「実際に取れた」改善（参考）

| 提出 | Public | vs tip 6.569 | 備考 |
|---|---:|---:|---|
| tip smoke | 6.569 | 0 | 枠1家系 |
| Best top-repro | **6.524** | **+0.045** | 枠2 |
| SUB-9 gated（`wave13-a-best` / OPS-LB-89） | **6.484** | **+0.085** | 実測 Public · 新Best |
| SUB-8 SOFT ungated寄り | 6.582 | −0.013 | soft_NO · 打ち切り |
| 中間面昇格 F015 | 6.62〜6.72 / 20+ | **悪化** | 昇格禁止 |

Public の +0.05〜0.09 は、T2 Δpool +0.05〜0.08 と同オーダー。**CV の微小改善が Public でも同帯で出た例**として残す。

---

## 表 C — 改善の「質」チェックリスト（次回の中間模索用）

新しい soft / 段 / ゲートを試すときは、この順で書く。

| # | 問い | 合格の目安 | 不合格例 |
|---|---|---|---|
| 1 | tip FINAL からの **Δpool** は？ | ≥ **+0.05**（T2） | +0.01 未満はノイズ帯 |
| 2 | **sample Δ** は非悪化か？ | ≥ **−0.01** 目安 · 厳格は ≥0 | selfdev8 の −0.04 |
| 3 | hard だけ見て採択していないか？ | hard 改善は参考のみ | CHK-177 診断 |
| 4 | ラベル oracle との差は？ | 実測 ≤ oracle · 残りを「取れない分」と書く | oracle を提出期待にしない |
| 5 | テスト時特徴だけか？ | portable = inference のみ | two-stage 井リスト直書き |
| 6 | 中間面を FINAL にしていないか？ | F015 | pre-BH / mpkg 昇格 |
| 7 | Public 1 発の前に Trust CV は？ | tip-cv-report PASS | 盲提出 |

---

## 層別の感覚（CHK-186 × Wave-14）

| 層 | tip FINAL | やること | やらないこと |
|---|---:|---|---|
| sample60 | **3.62**（既に強い） | tip FINAL 維持 | 強い SOFT / 中間面 |
| hard20 | 14.87 | 弱い gated のみ検討 | hard だけ最適化 |
| soft-hurt × hard | oracle 相対良でも | farvol 除外候補 | ラベルで井を選んで提出 |

詳細: [`wave14-x-chk186-join-2026-07-26.md`](wave14-x-chk186-join-2026-07-26.md)

---

## ソース一覧（再現）

| 役割 | パス |
|---|---|
| tip 基準 | `exp/work/wave13-gated-refine/tip-cv-report-baseline.json` |
| portable / gated 実測 | `tip-cv-report-chk170/171/174/175/176-*.json` |
| farvol | `exp/work/wave14-well-archetypes/tip-cv-report-absep-exclude-farvol.json` |
| SOFT oracle | `exp/work/chk185-candidate-ceiling/chk185-report.json` · [`chk185-result`](chk185-candidate-ceiling-result.md) |
| seed oracle | `exp/work/chk186-generator-ceiling/chk186-report.json` · [`chk186-result`](chk186-generator-ceiling-result.md) |
| 段・中間 | [`chk187-result`](chk187-stage-oracle-result.md) |
| Wave-13 選定 | `exp/work/wave13-gated-refine/wave13-a-best.json` |
| 機械表 | [`actual-vs-oracle-table.json`](../../exp/work/chk187-stage-oracle/actual-vs-oracle-table.json) |

---

## 次回テンプレ（コピペ）

```text
仮説: <ゲート/段> で tip FINAL より T2 Δpool ≥ +0.05 かつ sample 非悪化
実測: pool=__ hard=__ samp=__  (vs tip 8.330/14.870/3.624)
oracle対比: soft上限+0.155 の __% / seed上限+0.198 は提出に使わない
禁止: F015 中間昇格 · ラベル井リスト直書き · sample 犠牲の hard 稼ぎ
判断: GO / NO-GO / screen-only
```
