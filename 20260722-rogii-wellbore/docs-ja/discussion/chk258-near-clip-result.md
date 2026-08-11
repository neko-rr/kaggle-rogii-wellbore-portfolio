# CHK-258 結果 — (B) tip近傍クリップ enrichment

> 2026-07-28 · Kaggle CPU `chk258-b-near-clip-cpu` Ver2 · **提出なし**

## 要約

**rejected（NO-GO）** · 最良 k=0.5 でも hard20 pooled Δ **−0.47**（全 k で悪化）。

| k | pooled tip | pooled enr | Δ | Δ_B | frac_B↑ |
|---|---|---|---|---|---|
| 0.5 | 17.588 | 18.060 | **−0.47** | −0.56 | 0.29 |
| 1.0 | 17.588 | 18.568 | −0.98 | −1.16 | 0.21 |
| 1.5 | 17.588 | 19.076 | −1.49 | −1.76 | 0.21 |
| 2.0 | 17.588 | 19.427 | −1.84 | −2.18 | 0.21 |

## 解釈

- bank を tip±k·std に投影しても tip soft より悪い（k を広げるとさらに悪化）。
- 261/268（棄却ゲート）と同様、近傍制約 enrichment は局所でも効かない。
- tip-cv へ進めない。

## 成果物

`exp/work/wave22-candidates/chk258-b-near-clip-cpu-harvest/`
