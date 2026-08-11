# 17th place solution — Falcon

**Topic ID:** 733860  
**URL:** https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733860  
**投稿日:** 2026/08/08 · **取得:** 2026/08/10 UTC  
**作者:** Falcon · **順位:** Private **17th**（Priv **6.376** / Pub **5.853**）  
**票:** 8 · **コメント:** 0  
**原文:** [`docs-en/solution/topic-733860.txt`](../../docs-en/solution/topic-733860.txt)

---

## 要約

- 最終は **3 モデルの加重**: (1) last_known からの **GBDT 相対 TVT** · (2) **CNN で局所 slope→積分** · (3) **600ft セグメント系統誤差の補正**。
- 単独 GR-likelihood PF は CV 11 台。 Model1→1+2→1+2+3 で CV **7.09→6.66→6.32**、Priv **6.376**。
- 上位の UNet/ PF bank 本命とは別筋だが、**「非学習 estimator の工場 + ドリフト/段補正」**は silver 圏まで届く。
- 開発の核は **AI agent 大量実験**と、人間による方向判定・早期クローズ阻止。

---

## スコア向上にとって重要だったこと

1. **難易度帯別の採用基準**  
   井ごとの naive PF RMSE で normal / mid / high / catastrophic の4帯に分割。総合 RMSE のみだと **catastrophic 6% が支配**し、「hard を直して normal を悪化」でも CV がよく見えて Pub が落ちた。成功条件を **「全帯改善・とくに normal 大改善」**に固定。
2. **Model2=slope 積分**で Model1 の **定数ドリフト**を分散。  
3. **Model3=600ft セグメント誤差**で残る長尺シフトを LightGBM で減算。  
4. 特徴の中心は **非学習 estimator 群**（PF · beam · multi-scale NCC · 近傍 pseudo typewell 等）264 → slope 74ch · error 160 など。

## 効果が弱かった / 危険

- 総合 RMSE だけで agent に GO を出すと **hard 偏重仮説**が増える。  
- agent が「方向は尽きた」と閉じたがる（定数シフト方向を一度閉じて Model3 到達が遅れた）。  
- 後半は agent が cheap method ばかり提案する傾向。

## 運用メモ（agent 共同）

| 役 | 担当 |
|---|---|
| 実装・計測・台帳 | Agent |
| 問題設定・方向・最終採用 | Human |
| 量 | 実験 script 136 · 分析 750+ · memory 232 |

---

## 自チームとの関係

- 難易度帯 / hard pack の思想は自チーム L dual と近いが、自チームは **tip residual 主戦場**、本解法は **estimator+補正スタック**。  
- 「RMSE 1本採択禁止」は trust CV 設計の好例。

**最新コメント:** なし（2026/08/10）。
