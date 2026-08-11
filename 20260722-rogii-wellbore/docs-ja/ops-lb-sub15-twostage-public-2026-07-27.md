# OPS-LB SUB-15 — twostage 診断 Public（2026-07-27）

> refs: **55012195** · 重複 **55012192**（同 kernel · 同メッセージ）  
> kernel: `kazeneko77/tip-portable-twostage-s05` Ver1 · CHK-197  
> SSOT Best: [`exp/exp-index.md`](../exp/exp-index.md)（**SUB-14 = 6.269** · 本提出は Best 外）

## 1 行

**twostage Public は 6.494 / 6.564。Best（6.269）・T0.5（6.419）・旧gated（6.484）いずれも超えず。**  
portable / two-stage / s05 系は **Public 戦場外で確定**（診断として閉じる）。

## 数値

| SUB | CFG | ref | Public | vs Best(6.269) | vs SUB-9(6.484) |
|---|---|---|---:|---:|---:|
| **14** | Best tip + T=0.15 | 55006677 | **6.269** | 0 | −0.215 |
| **13** | Best tip + T=0.5 | 55001828 | 6.419 | +0.150 | −0.065 |
| **9** | gated self_dev>8 | 54972467 | 6.484 | +0.215 | 0 |
| **15a** | portable twostage s05 | **55012195** | **6.494** | +0.225 | +0.010 |
| **15b** | （同一・二重提出） | **55012192** | **6.564** | +0.295 | +0.080 |
| 12 | portable compound s05 | 54986214 | 6.556 | +0.287 | +0.072 |
| 11 | gated s05 | 54986210 | 6.530 | +0.261 | +0.046 |

## Kaggler 解釈

1. **仮説の検証結果 = NO（枠候補にしない）**  
   「portable + tip_std two-stage が Public で Best tip+T 帯に近づく」→ **否定**。  
   最良の二重提出でも **6.494** で SUB-9 よりわずかに悪い（+0.010）。T0.15 Best からは遠い。

2. **Wave-17 / OPS-LB-101112 結論の追認**  
   s05 · portable · farvol 系は Public で枠に入らない、という打ち切り判断を **E2E Public で再確認**。  
   → checklist で twostage を Active スコア仮説に戻さない。

3. **同一提出の 6.494 vs 6.564（Δ0.070）**  
   SUB-13 の 6.419 vs 6.530（Δ0.111）に続く **非決定性の実測**。  
   tip 系は再実行ゆれが大きい。Final は **良い ref を明示選択** · 診断の二重提出は枠浪費（再発防止）。

4. **Final2 への影響**  
   なし。枠1/枠2は引き続き **Public1位 = SUB-14（6.269）**。  
   twostage は枠候補に上げない。

5. **次に効く軸**  
   Best 更新の主戦場は **上流/中間（Wave-21）** と温度梯子の残り（T=0.3 E2E 完走済・未提出なら診断候補）。  
   後処理 portable/twostage の再提出は **Stop**。

## Explicit Stop（本結果で強化）

- tip-portable-twostage / compound / s05 の **Public 再提出**  
- 同一 kernel の連続二重提出（枠消費）

## 記録

- SUBMIT: [`tip-portable-twostage-s05`](../my-submitted-notebook/tip-portable-twostage-s05/SUBMIT.md)  
- CHK-197: [`chk197-result`](discussion/chk197-twostage-e2e-result.md)
