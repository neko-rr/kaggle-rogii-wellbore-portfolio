# CHK-214 plan — tip-cv selector · init_spr=12 ± T

> date: 2026-07-26 · GPU · **提出なし**  
> kernels: [T=1.0](https://www.kaggle.com/code/kazeneko77/tip-cv-sel-face-spr12-t1p0-h20) · [T=0.5](https://www.kaggle.com/code/kazeneko77/tip-cv-sel-face-spr12-t0p5-h20)  
> 根拠: [`chk213`](chk213-generator-diversity-result.md) oracle +2.50 · 物差し [`chk211`](chk211-selector-baseline-result.md)=33.178

## 受け入れ

| 面 | PASS |
|---|---|
| spr12 · T=1.0 | RMSE ≤ 33.178 − 0.30 |
| spr12 · T=0.5 | 同上（複合） |

**Explicit Stop:** PASS 前に tip CFG へ spr12 を載せない（209 教訓）。

## 状態

**RUNNING** Ver1×2
