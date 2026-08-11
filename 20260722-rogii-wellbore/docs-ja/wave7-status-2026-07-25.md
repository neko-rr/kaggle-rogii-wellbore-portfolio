# Wave-7 終了スナップショット（2026-07-25）

> purpose: B1 梯子の最終結果と提出枠消化の記録  
> 数値の正: [`exp/exp-index.md`](../exp/exp-index.md)  
> SUB-4–7 LB: [`sub-4-7-lb-analysis.md`](sub-4-7-lb-analysis.md)

---

## フェーズ結果

| Phase | 結果 |
|---|---|
| 0–1 書類・設計 | **完了** |
| 2 CHK-100 | **NO-GO** · early-ridge hard20 対照比悪化 · [`chk100-early-gate-memo.md`](../exp/work/chk100-b1/chk100-early-gate-memo.md) |
| 2 CHK-101 | Best T2 graft · **tip と preds 一致（8.330）** · Best固有CV未測 · [`chk101-best-t2-memo.md`](../exp/work/chk100-b1/chk101-best-t2-memo.md) |
| 2 CHK-103 | **NO-GO** · 特徴版は対照≈同値（改善なし） |
| 2 CHK-102 | **未実施**（100 PASS 条件未達） |
| F014 | **追記** · 学習内方位閉鎖 |
| F015 | **追記** · tip 中間面 / mpkg 単独の最終化禁止 |

### CHK-100 / 103（early ridge hard20）

| | pooled | well_mean |
|---|---|---|
| 対照 ridge-sub1 | 31.280 | 26.662 |
| B1 split | 31.822（+0.54） | 27.306（+0.64） |
| az-feat | 31.283（+0.003） | 26.664（+0.002） |

---

## 提出（枠消化 · Public 確定）

| ID | ref | kernel | Public | tip比 | 判断 |
|---|---|---|---|---|---|
| SUB-4 | 54958356 | promote gated_010 | **6.718** | +0.149 | **F015** |
| SUB-5 | 54958359 | promote pre-BH | **6.653** | +0.084 | **F015** |
| SUB-6 | 54958970 | promote gated_020 | **6.621** | +0.052 | **F015** |
| SUB-7 | 54958971 | promote mpkg-only | **20.067** | +13.5 | **F015** 壊滅 |
| （参考）VISUALS | 54958520 | Frontier Lab Ver2 | **6.581** | +0.012 | Best未満 |

tip smoke **6.569** · Best **6.524** はいずれも未更新。

---

## Final 仮

| 枠 | 仮 |
|---|---|
| 枠1 | tip Trust CV（T2 **8.33**） |
| 枠2 | Public Best **6.524** |
| B1 | **閉鎖（F014）** |
| 中間面昇格 | **閉鎖（F015）** |
