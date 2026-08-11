# residual T2 井効果（help/hurt）— 2026-08-04

> 出典: [`hard20_vs_t2_residual_dual.csv`](../work/colab-final-t2/out-cv-gaps-cpu-20260804/hard20_vs_t2_residual_dual.csv)  
> T2 wells=**80** · hard20=**20** · mid 悪化3井は sample（`70925e23` · `ab3ced07` · `19871e7f`）  
> **行レベル residual ヒートは faces 再計算待ち**（RMSE は線形合成不可）· ここは **count と順序**のみ厳密

## T2≈80（vs tip · help = residual が tip より良い）

| id | pooled T2 | help | hurt | 読み |
|---|---:|---:|---:|---|
| mid 基準 | 12.279 | 77 | 3 | 勝ち分本体 |
| **641 α0.30** | **10.309** | **77** | **3** | mid と同 win 集合 · 深さ改善 |
| **666 α0.35** | **9.998** | **77** | **3** | 同上 · 全井で mid+α 方向 |
| 668 α0.30+β0.05 | 10.206 | **71** | **9** | soft 足しで hurt 増 |
| 668 α0.30+β0.10 | 10.124 | **66** | **14** | β↑で hurt 増 |
| 660 tip+α0.5 | 11.165 | 77 | 3 | tip 土台 residual |

## hard20 サブセット

| id | pooled h20 | help | hurt |
|---|---:|---:|---:|
| 641/666/668 系ほぼ | 表 dual | **20** | **0** |
| mid | 20.390 | 0 | 0（基準） |

T2 面の hard20 では residual が **全20井 help**（517 旧面の mid 悪化パターンと不一致）。

## Public との関係（埋め）

| id | T2 | Public | 井効果→Public は |
|---|---:|---:|---|
| 641 α0.30 | 10.309 · help77 | **6.472 NO-GO** | Trust 井勝ち ≠ Public |
| 666 α0.35 | 9.998 · help77 | 未提出 | Public 危険推定（641 より td 大） |
| 541/558b tip⊕ | — | 6.256/6.238 | tip 近く · 枠2NO |

## 次（埋められない）

- residual **well_id 別 RMSE 表** → row faces 要 · 643 完了後でも残差再計算スクリプト可  
- **S3–S6 井別** → 643 ladder 後
