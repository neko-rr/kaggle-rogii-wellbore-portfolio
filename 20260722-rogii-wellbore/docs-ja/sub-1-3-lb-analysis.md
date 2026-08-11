# SUB-1 / SUB-3 提出結果分析（Private 上位狙い）

> date: 2026-07-24  
> goal: **Private LB 上位**（Public は壊れ検知 · 採用は Trust CV）  
> SSOT 数値: [`exp/exp-index.md`](../exp/exp-index.md) · 関係論: [`cv-lb-private-relation.md`](cv-lb-private-relation.md)

---

## 実測（2026-07-24）

| ID | ref | 内容 | Public | 状態 |
|---|---|---|---|---|
| **SUB-1** | 54935410 | Sunny physical（Final2 予備狙い） | **9.150** | COMPLETE |
| **SUB-3** | 54937788 | tip-mpkg020-as-submission Ver1 | **なし** | **Submission Scoring Error** |
| （参考）Best | 54914222 | top-reproducible conservative | **6.524** | COMPLETE |
| （参考）tip smoke | 54920651 | tip vp_balanced_modelpkg_005 | **6.569** | COMPLETE |
| SUB-2 | 54937708 | tip BH hedge OFF | **6.599** | COMPLETE · 枠2不採用（詳細は予測台帳） |

---

## CV · Public · Private 予測表

**生きた SSOT（今後の提出もここに追記）:** [`cv-public-private-forecast.md`](cv-public-private-forecast.md)

本ファイルは SUB-1/3 の深掘り。要約表の最新版は上記 SSOT を見ること。

---

## SUB-1（Sunny）深掘り

**事実:** Public **9.150** ≫ Best **6.524**。CHK-053 で相関 0.999 でも hard20 RMSE Sunny≈24≫tip≈14.5。

**教訓:** 高相関≠多様性。RMSE 絶対値必須。

**行動:** Sunny を Final/予備から **完全除外（F004）**。Final 選抜は [`comp-strategy`](comp-strategy.md)（枠1 CV / 枠2 Public最良）。

---

## SUB-3（mpkg020）深掘り — Scoring Error

**UI:** `Submission Scoring Error` · tip-mpkg020-as-submission Version 1  
**メッセージ:** SUB-3 tip model-package gated max_w=0.020 as submission

**何をした提出か**

- tip-bh-strength-off の中間成果物 `submission_model_package_gated_020.csv` を  
  **別 kernel（`kernel_sources`）からコピーして `submission.csv` にする**だけの Script
- Version 出力・ローカルでは 14151 行 · id 集合一致 · finite · validator PASS

**想定原因（Code Competition）**

採点時は Script が **hidden test 上で再実行**される。  
他 kernel 出力に依存する「固定 CSV コピー」は、採点環境で入力欠落・パス不一致・再実行失敗になりやすく **Scoring Error** になる。  
CSV 形式より **提出経路（copy-kernel）** が主因と考える。

**含意**

| 項目 | 内容 |
|---|---|
| Public / Private | **スコア無し** → LB 判断材料にならない |
| 枠 | 1 日提出枠を **無効に消費** |
| 手法評価 | mpkg0.020 の良し悪しは **未検証のまま** |
| 再提出 | 同じ copy-kernel 方式は **禁止** |

**運用ルール追加**

- Code Comp 提出は **自 kernel がコンペデータから `submission.csv` を生成する Version** のみ
- 他 kernel 出力のコピー Script での `-k/-v` 提出はしない
- 中間成果物を試すなら tip 本体 NB の最終セルで `submission.csv` に書く（E2E GPU ラン）

---

## Private 上位への戦略更新

方針の正は [`comp-strategy.md`](comp-strategy.md)（枠1=Trust CV · 枠2=Public最良）。  
候補数値は [`cv-public-private-forecast.md`](cv-public-private-forecast.md)。

本提出からの固定教訓: Sunny 禁止（F004）· コピー提出禁止（F005）· α/seed 乱獲禁止。

---

## 更新履歴

| date | 内容 |
|---|---|
| 2026-07-24 | SUB-3 を **Submission Scoring Error** に確定 · コピー提出禁止 · 予測表は `cv-public-private-forecast.md` へ移管 |
| 2026-07-24 | 初版（SUB-1=9.150） |
