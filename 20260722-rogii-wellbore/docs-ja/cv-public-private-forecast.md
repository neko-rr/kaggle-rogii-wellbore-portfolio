# CV · Public · Private 予測台帳（生きた SSOT）

> updated: 2026-08-05（**Final2 Ops · 666/farvol/660/641 最新化**）  
> purpose: **提出ごと**に CV / Public / Private 予測帯を更新し、Final 2 判断の材料にする  
> 数値の正（Best）: [`exp/exp-index.md`](../exp/exp-index.md)  
> **Final2 Ops（scoreboard + pair）:** [`../exp/latest/final2-ops-20260805.md`](../exp/latest/final2-ops-20260805.md)  
> 選抜方針: [`comp-strategy.md`](comp-strategy.md) §Final2 · Discussion 731550  
> 関係論: [`cv-lb-private-relation.md`](cv-lb-private-relation.md)

---

## 前提（短）

Private 揺れ大 · tip CV と Public は別物差し。  
**枠1 = Trust residual dual · 枠2 = Public 最良 · 2 本 diversify。**  
**Public 差 ≲0.08 はノイズ**（σ≈0.03）。Public だけで枠1を落とさない。

### Public 確定後の1行コメント用（コピペ）

```
差 Δ=___ ft · 閾値: ≲0.08=ノイズ / 0.08–0.15=CV確認 / ≳0.15=方向議論可 · 採用はレーン別
```

---

## Agent 更新ルール

| タイミング | 書くこと |
|---|---|
| **提出前** | 候補行: レーン · Trust三点 · tipdist · Public予測 · Final仮 |
| **Public 確定後** | Public 実測 · Final判断更新 · pair diversity 任意 |
| **Scoring Error** | Public=`Error` · Final 禁止 |
| **方針転換時** | 本要約表 + `exp-index` · `final-board` |

checklist / AGENTS に本表をコピーしない。

---

## 要約表（2026-08-05 最新 · Final2 主候補）

| 候補 | レーン | Trust pool / worst3 | tipdist E2E | Public | Private 予測（帯） | Final 仮 |
|---|---|---|---:|---:|---|---|
| **666 mid+α0.35** | Trust | **10.094 / 11.905** | 1.985 | **6.509** | shake 大 · Trust耐性狙い | **★枠1** |
| **farvol 0.95/0.05** | Public | N/A | 0.078 vs tip | **6.190** | Public良 · tip 薄家系 | **★枠2** |
| **660 tip+α0.5** | Public-diag | 11.17（T2 tip residual） | 1.923 | **6.239** | tip⊕ 密集帯 | 枠外 · farvol未超え |
| **641 mid+α0.30** | Trust | 10.40 / 12.28 | 1.743 | **6.472** | residual 毒帯 | 枠外 · Trust 2nd |
| tip SUB-14 T0.15 | base | — | 0 | **6.269** | tip 同族 | 土台参照 |
| 711 tip⊕g0.10 | Public-diag | — | 0.327 | **6.359** | tip 近傍悪化 | 枠外 NO |
| 710ssot residual | Trust-diag | ≈666 尺 | ≈2.02 | **6.613** | residual 毒 | 枠外 NO |
| 702 w050+r | — | — | 4.22 | **7.394** | 壊滅 | 枠外 NO |

**pair:** 666×farvol tipdist_AB **1.950** · same_family **False** · **OK_diverse**  
（[`final2-ops`](../exp/latest/final2-ops-20260805.md) · Kaggle `cpu-final2-ops-diversity`）

### 列の意味

| 列 | 意味 |
|---|---|
| **レーン** | Trust / Public · 横断 1 指標で勝敗を付けない |
| **Trust** | residual dual · 枠1 採否の主 |
| **Public** | LB 実測 · 枠2 採否の主 |
| **Private 予測** | 帯のみ（点推定しない） |
| **Final 仮** | 枠1/2 扱い · 確定はユーザー UI |

---

## 履歴要約（08-03 以前 · 抜粋）

| 候補 | Public | メモ |
|---|---:|---|
| OPS-C 14×9 | 6.237 | 旧枠2候補 · farvol に逆転 |
| 579 / 541 / 558b / 618c | 6.23–6.28 | tip⊕ 診断 · 枠2NO · 再提出禁止 |
| 458 mid 残存 | 7.76+ | F042 |
| Sunny SUB-1 | 9.150 | F004 |

---

## 提出ログ（追記）

| 日付 | ID | Public | メモ |
|---|---|---:|---|
| 2026-08-05 | Final2 Ops | — | scoreboard+pair · LOCK 維持 |
| 2026-08-05 | 711/710/702 | 6.359/6.613/7.394 | residual Public 毒 |
| 2026-08-05 | 660/666 | 6.239/6.509 | [ops-660-666](../exp/latest/ops-lb-chk660-666-public-2026-08-05.md) |
| 2026-08-04 | 641 | 6.472 | residual Public NO |
