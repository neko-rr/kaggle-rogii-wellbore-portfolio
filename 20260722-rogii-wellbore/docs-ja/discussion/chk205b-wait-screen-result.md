# CHK-205b — 待ち時間 screen（lik_temp 局所面 + 209×208 井別）

> date: 2026-07-26 · **ローカル CPU** · **提出なし**  
> 作業: [`exp/work/wave20-upstream/run_chk205b_liktemp_oracle_and_join.py`](../../exp/work/wave20-upstream/run_chk205b_liktemp_oracle_and_join.py)  
> 数値: [`chk205b-report.json`](../../exp/work/wave20-upstream/chk205b-report.json)  
> 関連: GPU 本体 [`CHK-205`](chk211-selector-baseline-result.md)（tip selector 面 · 実行中）

## 1 行

**A:** tip 同型 PF の **尤度重み付け面**は T=0.5 で pooled **+1.68**（T=2.0 は悪化）。  
**B:** tip面Δ と oracleΔ の相関 **≈0.04** · **7/20 井が oracle↑・tip↓**（209 の構造を再確認）。

## Part A — lik_temp（hard20 · 128×500 · init_spr=4.5）

| 面 | pooled RMSE | vs T=1 |
|---|---:|---:|
| seed-oracle（T無関係） | **12.881** | — |
| argmax_ll（尤度最良シード） | 18.396 | — |
| **pf scale=5 · T=0.5** | **18.405** | **+1.280** |
| pf scale=5 · T=1.0 | 19.685 | 0 |
| pf scale=5 · T=2.0 | 22.513 | −2.827 |
| **4-scale mean · T=0.5** | **18.642** | **+1.676** |
| 4-scale mean · T=1.0 | 20.318 | 0 |
| 4-scale mean · T=2.0 | 22.842 | −2.523 |

- 判定（局所 pf_scale 面 · 閾値 ≥0.30）: **PASS（T=0.5）**  
- **注意:** これは tip-cv selector 面（211=33.178）ではない。205 GPU の PASS を保証しないが、**T=0.5 を優先・T=2.0 は見込み薄**の事前情報。

特記: 井 `86454a6f` で s5 **21.45→7.99**（T=0.5）。209 で tip 面最悪悪化井と一致。

## Part B — 209 tip × 208 oracle 象限

| 象限 | 井数 |
|---|---:|
| oracle↑ · tip↑ | 8 |
| **oracle↑ · tip↓** | **7** |
| oracle↓ · tip↑ | 3 |
| oracle↓ · tip↓ | 2 |

- corr(tipΔ, oracleΔ) = **0.041**  
- tip 最悪: `86454a6f`（tip Δ−2.70 · oracle はむしろ +0.48）

→ **「命中が上がっても lik-ensemble 面は別物」**は井単位でも確認。CHK-205 は温度で「面」を寄せる挑戦であり、oracle 改善の延長ではない。

## 205 GPU への含意

| Kernel | 期待 |
|---|---|
| `tip-cv-sel-face-temp0p5-h20` | **本命**（局所 +1.68） |
| `tip-cv-sel-face-temp2p0-h20` | **NO-GO 見込み**（局所 −2.5） |

受け入れはあくまで tip selector 面 vs **33.178**（Δ≥+0.30）。

## Explicit Stop

- 局所 pf_scale 18.x を tip-cv 33 や LB と混同しない  
- A PASS だけで tip CFG に T を載せない（205 harvest 必須）
