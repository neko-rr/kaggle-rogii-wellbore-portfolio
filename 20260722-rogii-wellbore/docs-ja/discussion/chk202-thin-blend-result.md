# CHK-202 結果 — tip FINAL × mid 薄混ぜ（Type A · 2026-07-26）

> 作業: [`exp/work/wave19-thin-blend/`](../../exp/work/wave19-thin-blend/) · `chk202-report.json`  
> action: **T4** · 提出: **なし** · F015 厳守（中間面を submission にしない）

## 1 行結論

**NO-GO。** Type A だけに α≤0.05 で SP45 面を薄混ぜしても、hard20 は **すべて tip より悪化**。  
最良でも α=0.02 · Type A 7井で **Δpool = −0.093**。α を上げるほど悪化が拡大。

---

## 何を測ったか

| 項目 | 内容 |
|---|---|
| tip FINAL | `tip-cv-out/tip_train_preds.csv`（hard20） |
| mid 代理 | `chk091-sp45-h20/tip_train_preds.csv`（SP45 0.5 面 · mean_abs≈**8.71**） |
| ゲート | Type A = portable ∧ `tip_std_far/prox < 0.842`（farvol keep と同型） |
| α | 0.02 / 0.05 |
| 比較ゲート | Type A · portable · all hard20 |
| 採点 | tip-cv hard20（sample 部分集合なし） |

**注:** tip-cv 既定ランは train に raw `sp45`/`learned` 差分 dump が無い（test 側 mean_abs は sp45≈2.08 · learned≈4.37）。  
ラベル付き評価のため CHK-091 面を mid 代理とした（F013 の「プロファイル全置換スイープ」ではない）。

---

## 数値（hard20 · tip 14.870 基準）

| 設定 | n_apply | Δpool | 判定 |
|---|---:|---:|---|
| α=0.02 · Type A | 7 | **−0.093** | 最良だが悪化 |
| α=0.02 · portable | 9 | −0.115 | 悪化 |
| α=0.02 · all h20 | 20 | −0.198 | 悪化 |
| α=0.05 · Type A | 7 | −0.234 | 悪化 |
| α=0.05 · portable | 9 | −0.289 | 悪化 |
| α=0.05 · all h20 | 20 | −0.496 | 悪化 |

参照（既知 T2）: farvol **+0.072** · portable **+0.053** — 薄混ぜはこれらに遠く及ばない。

---

## 読み

1. SP45/learned 方向への寄せは、**薄い α でも tip FINAL を壊す**（CHK-091 / F013 と同方向）。  
2. Type A に狭めても符号は変わらない → **ゲートでは救えない失敗型**。  
3. 中間層の残ノブとしては **閉じる**。提出レバーは引き続き portable / farvol / twostage のみ。

---

## 次

- 本 CHK を昇格・提出しない  
- **SUB-10/11/12 Public** 待ち → 必要なら `tip-portable-twostage-s05`  
- 188/189 · F015 中間面昇格は触らない
