# CHK-259 結果 — F025 attractor-hedge × lik_temp

> 2026-07-28 · Kaggle CPU `chk259-hedge-temp-cpu` Ver1 · **提出なし**  
> 物差し: hard20 soft×seed-median attractor（≠E2E branch_hedge）

## 要約

**rejected（NO-GO）** · 温度差を残しつつ RMSE を落とさない設計は **h=0（現状）のみ**。attractor 寄せは divers↓かつ tip 悪化。

| design | h | pooled RMSE T0.15 | divers(0.15↔0.30) | Δ vs tip |
|---|---|---|---|---|
| post/pre | **0.0** | 17.588 | **2.39** | 0.00 |
| post/pre | 0.25 | 18.669 | 1.79 | −1.08 |
| post/pre | 0.50 | 20.989 | 1.20 | −3.40 |
| post/pre | 0.75 | 24.196 | 0.60 | −6.61 |
| post/pre | 1.0 | 27.985 | ≈0 | −10.4 |

raw divers（hedge前）pooled ≈ **2.39**。h↑で divers と RMSE が同時に悪化。

## 解釈

- F025 の「後段が温度差を消す」現象の局所 proxy: attractor へ寄せると差が消える。
- 差を残す＝hedge しない（h=0）であり、**新設計の PASS ではない**。
- tip-cv / E2E 再凍結の材料なし · T0.2/0.3 再提出禁止（F025）維持。

## 成果物

`exp/work/wave22-candidates/chk259-hedge-temp-cpu-harvest/`
