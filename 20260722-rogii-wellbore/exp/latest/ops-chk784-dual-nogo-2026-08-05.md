# CHK-784 dual · NOGO（2026-08-05 / 08-06 JST）

## 結論

| 項目 | 値 |
|---|---|
| tag | `CHK-784-huber-fast2` |
| mechanism | LightGBM `objective=huber` · α=0.9 · **no sample_weight** · FAST2 hard20 |
| dual L1_pass | **False** |
| next | **NOGO_L1** · Huber 言い換え禁止 · 損失帯（MAE/Fair）即再実行 **避ける** |
| ban-gate post | **NO-GO**（T3）· streak T3=2 |
| submit | **FORBIDDEN** |

## 主数値（α=0.35 · faces `20260804-041247`）

| 尺 | Δ（new−old · 悪化+） |
|---|---|
| hard residual pool | **+6.2657** |
| hard mean_worst3 | **+6.8752** |
| hybrid80 residual | **+2.8588** |
| 812 Q4 | **+3.7869**（ok=False） |
| 813 SSE top50 | **+3.5967**（ok=False） |
| 815 d\|L−mid\| | **−4.0613**（mid に潰れ方向 · collapse） |

raw F015 hard new L RMSE **26.94** vs old L **9.54** — L 自体が崩壊。

## face / dual パス（Drive）

| 役割 | path |
|---|---|
| run | `colab-final-t2/runs/20260805-143010-chk784-huber-hard20-fast2/` |
| face harvest | `out-t3-cpu-harvest/chk784-colab-face-huber/learned_trajectory_submission.csv` (3 524 941 · sha `a635d3f2…`) |
| dual out | `out-t3-cpu-harvest/l-dual-CHK-784-huber-fast2/` |

（後段セル `FACES` NameError は face コピー後のノイズ · face は有効）

## 解釈

Huber は尾部を「守る」想定だったが、residual 載荷どころか **hard/hybrid 全尺で大幅悪化** + mid-collapse。  
802 weight 帯より hard Δ が重い（+6.3 ≫ +1.8）。**loss 形状いじりの 1 機構は閉鎖扱い**。

## 次（本セッション · 781 と直交）

- **しない:** Huber α 変える · MAE/Fair · weight 再実行 · 781 触る · submit  
- **候補:** **CHK-777** reg↑（L2 / min_data · 1 機構）or **CHK-770** early-stop 強化（別機構）
