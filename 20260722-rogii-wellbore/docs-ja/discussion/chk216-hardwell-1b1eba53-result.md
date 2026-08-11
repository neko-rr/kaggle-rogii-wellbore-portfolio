# CHK-216 結果 — 難井 `1b1eba53` 診断

> date: 2026-07-26 · ローカル CPU · **提出なし**  
> 数値: [`chk216-report.json`](../../exp/work/wave20-upstream/chk216-report.json)

## 1 行

**1b1eba53 は spr 拡大でも oracle≈30+ のまま、かつ尤度が最良シードを拾えないため観測/尤度側の破綻が主因（散布ノブでは閉じない）。**

## 根拠

| 設定 | oracle | 備考 |
|---|---:|---|
| spr4.5 | 41.7 | baseline 帯 |
| spr12 | 31.5 | 213 最良でも難 |
| spr20 / 30 | ≈40 | 広げても悪化 |
| spr12 × gs=1.0 | **25.1** | 局所は効くが p50 は悪化 · 面には乗らない |
| seeds256 | ≡31.5 | シード増は無効 |

spr12 詳細: 最良シードの尤度順位 **120/128** · lik-best RMSE 42.0 vs oracle 31.5（Δ+10.5）· tip-cv 面 RMSE≈60.8（205）。

## 次ノブ（1つ）

**閉じる:** generator **散布軸は打ち切り**。井専用モデルは別仮説（低優先・承認後）。  
（gs=1.0 の局所効きは CHK-207 pool 既試と整合し、Wave-20 tip 採用にはしない）

## 判定

| 項目 | 値 |
|---|---|
| verdict | **GO_CLOSE** |
| close_generator_axis | true |
