# Georgy — Measure your noise floor before believing a lever

> analyzed: 2026-07-29  
> source: [`georgymamarin/measure-your-noise-floor-before-believing-a-lever`](https://www.kaggle.com/code/georgymamarin/measure-your-noise-floor-before-believing-a-lever)  
> 原文: `others-notebook/public-useful-refresh-20260729/georgy-noise-floor-lever/`  
> 祖先: [fork-the-ruler](../discussion/712037-fork-the-ruler.md) · 議論: [728477](../discussion/728477-public-lb-precise-but-biased.md)  
> license: **T033**

## 1 行結論

**提出コードではない診断 NB。** 同一カーネルを無編集で複数回提出し、公開 LB の **個人ノイズ床（seed band）** を測れ、という主張。Georgy 実測は **σ≈0.03 ft**（fork A sd=0.037 · B=0.027）。これ未満の「レバー改善」は信じない。自チームの Trust CV ≫ Public 微差、と強く整合。

## 使用するデータ

コンペ公式 + GWC2021 expert interpretations（人間ノイズ床 §5d）。GPU OFF · Internet OFF。

## 前処理 / パイプライン

提出パイプラインなし。oracle ladder · GR shift scan · leave-field-out · 二峰 datum の既存「ruler」論に、**冒頭の再提出実験**を追加した改訂版。

## モデルの定義

なし（診断・可視化・ハーネス）。

## 学習の設定

なし。

## 測定結果（2026-07-26 スナップショット基準）

| kernel（無編集再提出） | n | Public scores | spread | sd |
|---|---|---|---|---|
| A ayodeji v599 系 | 4 | 6.700 / 6.726 / 6.641 / 6.671 | 0.085 | **0.037** |
| B baidalin 7.201 系 | 4 | 7.219–7.282 | 0.063 | **0.027** |
| C/D/E | 2 each | — | 0.03–0.11 | 推定不安定 |

- F検定上、5本は **共通 σ≈0.03** と矛盾しない  
- 2回だけでは σ が読めない（→ 4–5 回推奨）  
- 自レバー比較: 差 **≲0.08–0.10 ft**（2単発同士の 2SE）は多くが **nothing**  
- Bronze 付近は **±0.037 に約570チーム**が密集 → 順位微動≠技能

## フォーラムとの関係

- souldrive 728477（精密な物差し）の機構は認めるが、**相手パイプラインの rerun 帯が無いと決着しない**  
- radiant-allomancer の CV改善↔LB悪化（0.249）は Georgy の σ では説明しきれない可能性 → 相手の floor 測定が必要

## 自チームへの示唆

| する | しない |
|---|---|
| Public 微差（≤~0.05–0.08）を CHK GO 根拠にしない | この NB を提出フォーク |
| tip-cv / Trust CV で採用を決める（既存方針） | seed 再提出レースで枠を溶かす（締切近） |
| ruler / GWC / 二峰は既存 S 枠のまま | Active に「noise-floor 測定 CHK」を増やす必要は薄い（既に方針化済） |
