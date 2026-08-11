# CHK-283 結果 — 現行 lik 逆転の観測項分解（2026-07-29）

> action: **T4** · ローカル CPU（Kaggle CPU Ver1 も COMPLETE）· **提出なし**  
> 作業: [`exp/work/wave24-generator-redesign/run_chk283_lik_term_decomp.py`](../../exp/work/wave24-generator-redesign/run_chk283_lik_term_decomp.py)  
> JSON: [`chk283-report.json`](../../exp/work/wave24-generator-redesign/chk283-report.json) · 井表: [`chk283-per-well.csv`](../../exp/work/wave24-generator-redesign/chk283-per-well.csv)  
> kernel: [`kazeneko77/chk283-lik-term-decomp-cpu`](https://www.kaggle.com/code/kazeneko77/chk283-lik-term-decomp-cpu)

## 1行方針

**誤順位の主因観測項は `md_late` と `anchor`（各 63.6% 方向一貫）。** 次は CHK-284 で遠MD/外れ値に頑健な尤度、CHK-285 で MD帯・距離の heteroscedastic 分散を優先する。

## 集計（hard20 · tip PF 128@4.5 · soft s5@T0.15）

| 項目 | 値 |
|---|---:|
| ranking_fail 井 | **11 / 20** |
| pooled tip soft | **17.24** |
| pooled oracle | **12.88** |
| pooled argmax_ll | **18.40** |

## 項別（ranking_fail 上の wrong_dir 率）

| 項 | wrong_dir | mean Δ(oracle−argmax) | seed corr(−RMSE) | culprit |
|---|---:|---:|---:|---|
| level | 36.4% | +0.005 | +0.137 | no |
| gradient | 27.3% | **+0.083** | +0.012 | no（むしろ正しい側） |
| multiscale_corr | 45.5% | −0.006 | −0.012 | no |
| **anchor** | **63.6%** | −0.0005 | +0.054 | **yes** |
| md_early | 27.3% | +0.014 | +0.032 | no |
| md_mid | 54.5% | +0.002 | +0.023 | no（閾値未満） |
| **md_late** | **63.6%** | −0.0009 | +0.156 | **yes** |

## 解釈

- 現行 PF の **全体 level ガウス** は主犯ではない（wrong 36%）。問題は **遠MD帯の level 過信** と、**heel 近傍への寄り過ぎ（anchor）**。
- **gradient** は oracle を正しく優遇しやすい → 284 の多尺度に残差勾配を入れる根拠。
- multiscale_corr 単体は 60% 未達 → 284 の主ノブにはしないが補助可。

## 判定

| 項目 | 値 |
|---|---|
| verdict | **PASS** |
| culprits | `md_late` · `anchor` |
| next | **CHK-284**（robust / 遠MD）· **CHK-285**（heteroscedastic MD/距離）並行 screen |

## Explicit Stop

- 本診断を tip-cv PASS としない（T4）
- F028（offset 再初期化）に逃げない — anchor 問題は観測重みで扱う
- F026 粒子増量には戻らない
