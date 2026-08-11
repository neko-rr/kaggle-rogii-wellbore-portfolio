# CHK-403 — 402A vs 392/395/398 門番突合

> verdict: **門番どおり棄却**  
> Soft-Preserve再学習なし（F041）· 提出なし

## 固定観点表

| # | 観点 | CHK-392 (hard20) | CHK-395 (監査) | CHK-398 (外井) | **CHK-402A (同一20井+tip)** |
|---|---|---|---|---|---|
| 1 | CF / pooled | final 17.35 ≪ CF 49.56 | 同左 | final 14.81 < CF 15.44 | tip **10.66** ≪ ranker **14.73** < CF 15.60 |
| 2 | vs soft | soft≈final | — | final **>** soft · soft≡final | final **>** soft · soft≡ranker ρ≈1.0 · **F015** |
| 3 | 生Pearson tip | 0.9995 | 同左 | tip CSV無し | tip↔ranker raw ≈0.9998 |
| 4 | 誤差/中心化 | 未記録→395で補完 | err 0.689 · centered 0.895 | — | err 0.659 · centered 0.864 |
| 5 | 井別 | 20/20 tip改善（hard20） | 同左 | tip不可 | tip勝ち10/20 · **poolは tip大勝** |

## 判定

| 問い | 答え |
|---|---|
| 門番どおりの正しい棄却か | **YES** |
| 門番定義の見直し候補か | **部分のみ**（生Pearson単独切捨は caveat 継続 · ただし 402A は tip負け+F015で別根拠） |
| 398同型再発か | **YES**（soft≡final · final>soft） |
| Soft-Preserve再開か | **NO**（F041） |

## 一文

392の「生Pearsonだけで切った」点は395で弱いが、**402Aで tip FINALに大敗かつ F015** が確定したので Soft-Preserve 提出ルート閉鎖は正しい。

## 参照

- [`chk402a-compare.md`](../../exp/work/wave30-soft-preserve/chk402a-compare.md)
- [`gate-pearson-caveat.md`](../gate-pearson-caveat.md)
- [`chk398-exhard-cv.md`](../../exp/work/wave30-soft-preserve/chk398-exhard-cv.md)
