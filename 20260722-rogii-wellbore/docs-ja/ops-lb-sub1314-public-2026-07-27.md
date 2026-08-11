# OPS-LB SUB-13/14 — Public 確定（2026-07-27）

> refs: SUB-13 **55001828** · SUB-14 **55006677** · 重複 T0.5 **55001822**  
> SSOT Best: [`exp/exp-index.md`](../exp/exp-index.md)

## 1 行

**SUB-14（LIK_TEMP=0.15）Public **6.269** が新 Best。**  
SUB-13（T=0.5）は **6.419**。tip-cv 順位（T0.15≻T0.5）と Public が一致した。

## 数値

| SUB | CFG | ref | Public | vs 旧Best(6.484) |
|---|---|---|---:|---:|
| **14** | Best tip + **T=0.15** | **55006677** | **6.269** | **−0.215（良化）** |
| **13** | Best tip + **T=0.5** | **55001828** | **6.419** | −0.065 |
| 9 | gated self_dev>8 | 54972467 | 6.484 | 0（旧 Best） |
| （重複） | T=0.5 同 kernel Ver1 | 55001822 | **6.530** | +0.046（悪化） |

## Kaggler 解釈

1. **温度を尖らせるほど Public が良い（この帯）**  
   tip-cv: 29.899（T0.15）≪ 32.276（T0.5）≪ 33.178（T1）。  
   Public: 6.269 ≺ 6.419 ≺ 6.484。**同符号** → 205→222→220b の軸は生きている。

2. **「CV≠LB」は一時的誤読だった**  
   以前 handoff の「tip-cv は T0.15 だが Public は T0.5」は、SUB-14 採点前の暫定。**覆された**。

3. **同一 kernel の二重提出で 6.419 vs 6.530**  
   55001828 と 55001822 は同じ tip+T0.5。差 **0.111** は大きい。  
   → tip 系は **非決定性 / 再実行ゆれ**あり得る。Final は **良い方の ref を明示選択**。重複提出は枠浪費（教訓再確認）。

4. **Final 方針（ユーザー確定 · 不変）**  
   - 枠1 = **CV 1位** · 枠2 = **Public 1位**  
   - Public 1位が入れ替わったら **枠2をそれに差し替える**  
   - 現時点は両枠とも **SUB-14**（CV1=Public1 一致）  
   - 多様性のための別候補探しはしない · Agent は UI 自動差替しない（記録+通知のみ）

5. **SUB-15 twostage** は diagnostic **COMPLETE** · Public **6.494**/6.564 · Best外 · 詳細 [`ops-lb-sub15`](ops-lb-sub15-twostage-public-2026-07-27.md)。

## Explicit Stop

- T≤0.10 への乱打（223/227 NO-GO）  
- spr12 tip 採用（214 NO-GO）  
- Final UI の Agent 自動差替

## 記録先

- SUBMIT: [`tip-gated-lik-temp-0p15`](../my-submitted-notebook/tip-gated-lik-temp-0p15/SUBMIT.md)  
- forecast / Final2: 本結果を反映して更新
