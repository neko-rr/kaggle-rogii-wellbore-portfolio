# CHK-284 結果 — robust 多尺度尤度 screen（2026-07-29）

> action: **T4** · ローカル CPU（パック再利用）· Kaggle Ver2 push 済 · **提出なし**  
> 作業: [`run_chk284_robust_lik_screen.py`](../../exp/work/wave24-generator-redesign/run_chk284_robust_lik_screen.py)  
> JSON: [`chk284-report.json`](../../exp/work/wave24-generator-redesign/chk284-report.json)  
> 前提: CHK-283 culprits=`md_late`·`anchor`

## 1行方針

**後段で PF lik を Huber/Student-t/遠MD スコアに差し替えるだけでは採択不可。** RF井の oracle 順位は上がるが、易井の順位と pooled soft が壊滅する。次は CHK-285（井条件付き heteroscedastic / pf_ll 混合）または CHK-287。

## 主結果

| 項目 | 値 |
|---|---:|
| LOO 最頻 | **pf_ll**（20/20） |
| LOO 中央値順位改善 | **0%** |
| LOO pooled Δ | **0.00** |
| acceptance | **FAIL** |

### 代表 variant（ranking_fail 上）

| variant | RF median rank_imp | median rank drop | pooled Δ vs tip |
|---|---:|---:|---:|
| student_t3 | **+0.64** | −0.38 | **−13.3** |
| huber_1p345 | +0.64 | −0.31 | −13.3 |
| late_het_grad | +0.30 | −0.77 | −13.9 |
| pf_ll | 0 | 0 | 0 |

## 解釈

- 283 の culprit 方向（遠MD・頑健化）は **RF井だけでは正しい**。
- しかし tip 面の soft 置換は易井（pf_rank≈1）を壊し、pooled が 17→30 帯へ悪化。
- **生成時の観測モデル組込み（286）の前に、井条件付き適用（285）か proposal 側（287）が必要。**

## 判定

| 項目 | 値 |
|---|---|
| verdict | **NO-GO** |
| next | **CHK-285**（texture/欠測/距離の heteroscedastic · pf_ll 混合）· 並行で **CHK-287** 可 |

## Explicit Stop

- 本 screen の「全井一括 robust soft 置換」を言い換えて再スイープしない
- F029（バンク専用 soft 再校正）へ戻らない
