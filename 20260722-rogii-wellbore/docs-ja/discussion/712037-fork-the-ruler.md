# Fork the ruler, not the model — where the error actually lives

> Topic ID: **712037**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/712037  
> 投稿者: **Georgy Mamarin** · **2026/06/22** UTC · 票 24  
> 更新コメント: **2026/07/20** など  
> 原文: `docs-en/discussion/712037-fork-the-ruler-not-the-model.md`

## 要約

公開 NB は ~7.2 に群れる。モデル fork より **誤差の回収可能性**を測れ、というノート。

- per-well 目標はほぼ **1 数値 = drift slope**（曲面は ~99% 線形）
- その slope は **未見 field の合法特徴から学習不能**（field-group OOF R²&lt;0）
- GR は粗い信号（PF で ~16→~10 ft）だが、合法校正では **細かい per-well slope をピン留めできない**（退化）
- 罠: CV↔LB 幻影 · seed/refork 分散
- harness: `oracle_ceiling` + `wall_test`（leave-one-group-out + shuffle-null）
- 人間ノイズ床（ROGII Geosteering World Cup）: 専門家中央値で真値から **20.5 ft**、専門家間 pointwise median **9.5 ft**

## Tucker（2026/06/22）[+12]

- 公開 NB の CV は高く LB に seed 過適合気味  
- 単一モデル CV **~5 ft**、ensemble で **4 未満**も視野  
- **per-well データのみ**（クロス well / 空間 / 外部 tops なし）· **pooled** per-row RMSE  

## その他

- wharekawa: oracle ladder 再現（773 wells: const/line/smooth **9.04 / 6.70 / 3.05**, carry-last **15.91**）
- BirdCLEF 類比: 終盤 blend は seed 運で順位入れ替え

## スコア向上への示唆

1. 公開 fork 量産より **回収可能な誤差**を測る  
2. slope 学習を無理に追わない（727149 と整合）  
3. seed ブレンドで Public を追わない  

## 効果が薄かった取り組み

- 公開強パイプラインの再 fork のみ  
- 「公開 LB が学習セット」と誤認した時期の議論（のち訂正: hidden ~200）
