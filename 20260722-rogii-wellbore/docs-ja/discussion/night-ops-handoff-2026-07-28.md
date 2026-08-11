# night-ops handoff — 2026-07-28

> 睡眠中 ~3h 自律ランの起床用まとめ

## 提出（3/3 使用）

| SUB | 内容 | ref | 期待 |
|---|---|---|---|
| 16 | T=0.3 E2E | 55037034 | **≡Best CSV** → Public≈**6.269**（F025）· まだ PENDING のまま長い |
| 17 | before_branch_hedge | 55037385 | Best差 rmse0.97 · COMPLETE・Public欄空（採点待ち/要確認） |
| 18 | learned_trajectory | 55037386 | Best差 rmse5.74 · 同上 |

詳細: [`ops-lb-sub161718-night-2026-07-28.md`](../ops-lb-sub161718-night-2026-07-28.md)

## 実験クローズ

| CHK | 結果 |
|---|---|
| 251 dip state | **rejected**（mid壊滅） |
| 252 ESS heel | **rejected** tip-cv **29.921 (−0.02)** · mid+0.225は偽（F023） |
| 253 fault jump | **rejected**（先） |
| Wave-21 Active | **実質空**（OPS-FINAL2 のみ） |

## 重要発見 **F025**

E2E で `LIK_TEMP∈{0.15,0.2,0.3}` の**最終 submission.csv は同一**。  
`learned_trajectory` だけ差が出る → 後段（branch_hedge〜）が温度差を消す。  
**T0.2/0.3 最終の再提出は禁止。**

## 起床後の優先

1. `competitions submissions` で SUB-16/17/18 Public 記入  
2. SUB-17/18 が Scoring Error なら再提出判断  
3. **OPS-FINAL2**（枠は当面 SUB-14）  
4. 新 Wave は「後段を薄くした tip 面」か全く別軸（T3 連続 NO-GO 34+）
