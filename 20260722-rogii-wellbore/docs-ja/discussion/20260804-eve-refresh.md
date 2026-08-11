# Discussion · 公開NB · LB refresh — 2026-08-04 eve

> CLI: `kaggle competitions topics list/show` · `kernels list` · `leaderboard -d` · `submissions`  
> 前回: [20260804-refresh](20260804-refresh.md)（日中）  
> 原文: `docs-en/discussion/*-refresh-20260804-eve-raw.md` · kernels: `docs-en/others-notebook/kernels-list-*-20260804-*.txt`  
> pull: `others-notebook/public-useful-refresh-20260804-eve/`  
> LB: `docs-en/leaderboard/publicleaderboard-2026-08-04.csv` · [`docs-ja/leaderboard.md`](../leaderboard.md)

## 1 行結論

**戦略変更なし。** Discussion の新規トピックは無し。差分は (1) **732455** に Tucker の「スケールアップで一貫した改善」コメント、(2) 公開 NB は **Q0522/Contact 同家系の改題・再送**、(3) Public LB は密集帯が **6.0–6.5 に移動**し、自チーム farvol **6.190 = Rank #122**。

---

## Discussion 差分（vs 08-04 日中）

| topicId | 票 / コメ | 変化 | 示唆 |
|---|---|---|---|
| **732455** | 17 / 9（←11/7） | **Tucker** 2026/08/04 01:38: 計算コスト高でも **モデル拡大で一貫した gains** · Michael が追随意志 | 自チームの **L 再学習 / 質改善レーン**と外部で整合 · **Public 密集帯クローンは依然危険** · [追記](732455-leaderboard-thoughts.md) |
| **731550** | 23 / 24 | 新規コメントなし | Final2=Trust CV+Public1 維持 |
| 732296 / 732422 / 732432 / 732443 | — | 変化なし | 運用メモ維持 |
| **新規トピック** | — | **なし** | 終盤は Forum 静穏 + 再掲スレ中心 |

---

## 公開 Notebook スキャン

| 判定 | slug · 票 | 要点 |
|---|---|---|
| **捨て（同家系）** | `yaroslav…/reproduce-strongest-reference-aeroridge-v34`（43·本日 run） | タイトル AeroRidge でも本文は **Contact/U Restore · Q2522 Consensus Gate** · residual w=0.12 · row cap 0.50 · DS は koolbox/nina/pilkwang/fleongg · **Final不可** · [分析](../others-notebook/yaroslav-aeroridge-v34-Ver.md) |
| **捨て（同家系）** | `brianbovell/akiirolabs-tvt-prediction-model`（1·本日 run） | koolbox + fleongg + ravaghi artifacts · PF/接触系 stack · 新規経路なし · [分析](../others-notebook/akiirolabs-tvt-Ver.md) |
| 監視票増 | Contact+U **55→78** · daniil 6.390 **145→171** · physics 7.872 v48 **再 run** | 看板人気のみ |
| 既監視 | Final Hierarch · Georgy noise-floor · Frontier II · robust-ensemble-v3 | 変更なし |

---

## Public LB 差分（要点 · 詳細は leaderboard.md）

| 項目 | 07-23 / 07-25 旧 | **08-04** |
|---|---|---|
| チーム数 | ~5.5k | **6,118** |
| 1位 | 4.859 | **4.608**（shu01） |
| Top10 閾値 | ≈5.51 | **5.205** |
| 密集帯 | 6.5–7.0 | **6.0–6.5（1,391 チーム）** へ移動 |
| **Kazeneko** | 旧 6.644 #444 級 | **6.190 · Rank #122**（遠 vol Best） |
| Silver 概算（上位5%） | — | Rank ≤305 · Score ≤ **6.356** |
| Bronze 概算（上位10%） | — | Rank ≤611 · Score ≤ **6.408** |

※ Public のみ。Private は未公開。密集帯移動は **公開フォーク追随 + 上位の改善** が主因で、自戦略変更の根拠にはしない。

---

## 自チーム行動

| する | しない |
|---|---|
| 732455 Tucker=「重いモデル拡大に信号」を **688 L 質改善**の外部補強としてリンク | Public 6.1–6.3 帯の公開フォークを Active/Final に載せる |
| LB 現在地を SSOT に同期（Best 6.190 / #122） | rank 上昇だけを Final2 差替理由にする |
| sample assert 禁止・9h=全 test を提出運用で維持 | AeroRidge / Contact+U / Akiiro を新経路と誤認 |
| Final2 · farvol 枠2 · Trust=666 tipdist · residual 政策閉 | tip 同家系の言い換え提出 |

**戦略変更:** なし（Trust=CV · 枠2=Public1/farvol · tip Final 不可 · σ≈0.03 · 本命=688）
