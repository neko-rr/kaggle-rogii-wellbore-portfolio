# OPS-LB — CHK-514 / 515 Public（tip⊕468 gate）

> date: 2026-08-03 · diagnostic only · **Final 2 差替なし**  
> σ≈**0.03**（Georgy noise-floor）· tip SUB-14 **6.269** · 表示Best farvol0.95 **6.190**

---

## 着弾

| ID | ref | Public | tipdist（local） | Trust hard20 | 判断 |
|---|---|---:|---:|---:|---|
| **514 H-D** | **55195968** | **6.335** | ≈0.727 | **28.283**（本命だった） | **NO-GO** · tip+0.066 |
| 514 誤再送 | 55195975 | **6.346** | 同上 | 同上 | 同系 · Δ再送 +0.011（ノイズ） |
| **515 row** | **55195981** | **6.249** | ≈2.121 | 28.901 | **≈tip**（−0.020）· Best未達 · 枠外 |
| tip SUB-14 | 55006677 | 6.269 | 0 | 29.899 | 枠1防衛 |
| farvol 0.95 | 55148128 | 6.190 | — | — | 表示Best · 枠2 |

---

## 判定（Kaggler）

| 仮説 | Public 結果 | 結論 |
|---|---|---|
| H-D（井 frac≥0.7∧row）が tip を抜く | 6.335 ≫ 6.269 | **反証 · NO-GO** |
| 行ゲートだけなら安全に tip 近傍 | 6.249 ≈ 6.269（σ内） | **部分成立** · 改善主張なし |
| Trust 順（H-D≪row≪tip）が Public でも保たれる | **逆転**（H-D 最悪） | **Trust≠Public**（485と同型） |
| Final を 514/515 に差替 | Best/tip 未達 | **禁止** |

---

## 読み

1. **井ゲート H-D は hard20 過学習**  
   LOO でも thr=0.7 だったが、Public 26% 切片では tip を明確に悪化。井 LF 特徴は Trust 用に閉じる。

2. **行ゲートは「壊さない」が「勝たない」**  
   515 は tip −0.020 でノイズ帯。farvol（6.190）や OPS-C（6.237）には届かない。

3. **tipdist は Public の代理にならない**  
   514 tipdist≈0.73（薄い）なのに Public 悪化 · 515 tipdist≈2.12（厚い）の方が Public はマシ。残差の量ではなく **どの行を載せるか** が Public で失敗した。

4. **468 mid 面のゲート提出は診断終了**  
   再提出・αスイープ・H-D 閾値いじりは枠浪費。次は **P-495 載荷**（571/578 Trust ~26.76）の tip-cv → Public 診断。

5. **Final 2 維持**  
   枠1=SUB-14 · 枠2=farvol 0.95/0.05。

---

## 禁止（追記）

- 468-H-D / 同系井ゲートの Final 差替・再提出
- Trust-best だけで枠1を動かす（579 tip-cv + Public 後にユーザー判断）

## SSOT

- [`exp-index.md`](../exp-index.md) · [`exp-infer.md`](../exp-infer.md) · [`experiment-checklist.md`](../experiment-checklist.md) · [`cv-public-private-forecast.md`](../../docs-ja/cv-public-private-forecast.md)
