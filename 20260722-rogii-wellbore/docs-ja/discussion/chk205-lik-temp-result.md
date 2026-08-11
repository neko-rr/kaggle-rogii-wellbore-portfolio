# CHK-205 結果 — tip selector 面 · 尤度温度 T

> date: 2026-07-26 · GPU · **提出なし**  
> kernels: [T=0.5](https://www.kaggle.com/code/kazeneko77/tip-cv-sel-face-temp0p5-h20) · [T=2.0](https://www.kaggle.com/code/kazeneko77/tip-cv-sel-face-temp2p0-h20)  
> 物差し: CHK-211 baseline **33.178** · [`chk211`](chk211-selector-baseline-result.md)  
> 数値: [`chk205-score.json`](../../exp/work/wave20-upstream/chk205-score.json) · 井別 [`chk205-per-well.csv`](../../exp/work/wave20-upstream/chk205-per-well.csv)  
> 事前: [`chk205b`](chk205b-wait-screen-result.md)

## 1 行

**T=0.5 は tip selector 面 hard20 を +0.90 改善（PASS）。T=2.0 は −0.52 悪化（NO-GO）。**  
局所 205b の方向予測は当たった（tipΔ ↔ 局所 s5Δ 相関 **0.92**）。

## 数値（hard20 · USE_SELECTOR_FACE · tip 既定 4.5×128）

| 面 | RMSE | vs 211 |
|---|---:|---:|
| **211 baseline** T=1 | **33.178** | 0 |
| **205 T=0.5** | **32.276** | **+0.902** |
| **205 T=2.0** | **33.696** | **−0.518** |
| 209 combo（参考） | 33.541 | −0.363 |
| tip-cv phys-blend（禁止） | 14.870 | — |

| 判定 | 結果 |
|---|---|
| T=0.5 ≥+0.30 vs 211 | **PASS** |
| T=2.0 ≥+0.30 vs 211 | **NO-GO** |

- 行の差: T0.5 で **97%** 行が変化（maxabs 8.76）→ ノブは面を動かしている  
- 井単位: T0.5 良化 **15/20** · T2.0 良化 **5/20**  
- `tip_train_preds` ≡ selector（STOP_AFTER_SELECTOR 正常）

## 井別ハイライト（T=0.5）

| well | 211 | T0.5 | Δ | 読み |
|---|---:|---:|---:|---|
| **86454a6f** | 60.22 | **54.19** | **+6.02** | 209 最悪悪化井が最大改善 |
| ba48188d | 21.72 | 20.10 | +1.62 | |
| 2fd68f7b | 26.36 | 25.29 | +1.07 | |
| 91db7070 | 38.91 | 39.42 | −0.51 | 少数悪化側 |

→ 尖った重み（T↓）は「尤度が良いシードに寄せる」。難井で尤度が有用なとき効く。平坦化（T↑）は平均に寄り悪化。

## Kaggler 解釈

1. **209（combo）NO-GO と矛盾しない**  
   combo は *候補集合* を広げつつ *重み付け* は旧のまま → 面が悪化。  
   205 は *同じ候補* で *重み付けだけ* を尖らせる → 面が改善。  
   「命中↑」と「面↑」は別レバー。今回は後者に効いた。

2. **205b 局所が正しい事前フィルタだった**  
   局所 pf_scale T0.5 +1.68 / T2 −2.5 → tip 面も同符号。相関 0.92。  
   今後の温度系は **局所 reweight → GPU tip-cv** の二段が安い。

3. **採用は tip CFG の微小ノブ**  
   `weights = exp(lik / (scale·T))` の T=0.5。F013 の「プロファイル大切替」ではないが、**本番 tip への反映は別 CHK（承認・pretrain・提出ゲート）**。本 CHK は tip-cv 面のみ。

4. **Public 乱獲禁止**  
   hard20 +0.90 は selector 面。LB は後段（BH/gold/learned）込み。即提出しない。

## 次アクション（提案）

| 優先 | 内容 |
|---|---|
| 1 | **CHK-205 を done（T0.5 PASS / T2 NO-GO）** として閉じる |
| 2 | 本番 tip に T=0.5 を載せるか **ユーザー承認の新 CHK**（例: tip CFG 1行 · GPU smoke · 提出は別判断） |
| 3 | T の細かい探索（0.3 / 0.7）は EV 次第 · まず 0.5 固定の tip 面採用可否を決める |
| 4 | combo（init_spr9×256）は **載せない**（209 確定） |

## Explicit Stop

- T=2.0 を再実行・採用しない  
- tip-cv 32.28 を Public 予想と混同しない  
- F015 mid-face promote · F013 薄混ぜと混ぜない
