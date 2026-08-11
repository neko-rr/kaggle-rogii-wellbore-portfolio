# 公開 NB の `gs`（GR noise scale）×1.3 観察

> Topic ID: **728712**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/728712  
> 投稿者: **suzu10**  
> 投稿日時: **2026/07/24** UTC  
> 最新コメント: **Nicolai Karcher · 2026/07/27** UTC  
> 原文: `docs-en/discussion/728712-gs-noise-scale-public-nb.md` · refresh: `728712-refresh-20260729-raw.md`

## 要約

公開ノート `hjyact/ultimate-pf-config-strategy-a-reproducible-score` で、  
**GR ノイズ推定 `gs` を約 1.3 倍**にする1行変更が、未変更版より明らかに良いスコアになった、という共有。

- SNS だけでなく Forum に載せたのは **公平性**のため（他参加者の指摘）

## コメント

| 誰 | 日時 (UTC) | 要点 |
|---|---|---|
| **Nicolai Karcher** | 2026/07/27 07:36 | 票が付いているが、**この種の変更が Private によく伝わると期待すべきでない** · 良い ML 実践ではない |

## 自チームへの示唆

| 判断 | 内容 |
|---|---|
| **F001 とは別物** | F001 は Typewell 無し heel affine の `gs`。本スレは **PF 系の GR noise scale** |
| 枠1 | tip 公開コードに **`* 1.3` が既にある**（2026-07-25 確認 · ultimate-pf / gs130 / luck は同一コード）。追加移植は不要 |
| 枠2 | **使わない**（同家系 · 多様性にならない） |
| 採択 | 「未実装の1行」ではない。LB 一言での再チューニングも不要 · Nicolai 指摘と整合 |

## 効果が薄い／注意

- 「公開 NB の1パラメータ追い」は Public 密集帯の典型。Private 耐性の根拠にしない
- tip への盲目な再乗算（1.3×1.3 等）は禁止- 詳細コード突合: [public-useful-refresh-20260725.md](../others-notebook/public-useful-refresh-20260725.md)