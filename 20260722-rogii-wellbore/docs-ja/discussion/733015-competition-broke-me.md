# このコンペに潰された（〜8 ft OOF 天井）— 733015

> Topic ID: **733015**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733015  
> 投稿者: **Nicolai Karcher**  
> 投稿日時: **2026/08/05 15:17** UTC  
> 最新コメント: **Cody_Null · 2026/08/05 20:12** UTC  
> 票/コメ（08-06）: **6 / 13**  
> 原文: `docs-en/discussion/733015-refresh-20260806-raw.md`  
> refresh: [`20260806-refresh.md`](20260806-refresh.md)

## 要約

締切当日の感情+技術スレ。著者は **pooled OOF RMSE 〜8 ft** を抜けられず、**cycle skip（跳躍）** の見分けに詰まった、と吐露。終了後の writeup 待ちが主旨。

## コメント（重要）

| 誰 | 日時 (UTC) | 要点 |
|---|---|---|
| **GG Ayo** | 2026/08/05 15:22 | GPU 学習なしでの **DP/PF の理論的天井**への興味 |
| **symmys** | 2026/08/05 15:23 | 同じく 8 ft 帯 · 上位の 5 ft Public の「現実」を知りたい |
| **Andrey** | 2026/08/05 16:13〜 | 冗談寄り: LLM が Private を嗅ぐ、等（**本番根拠にしない**） |
| **Rob Boyd** | 2026/08/05 16:06 | Milankovitch 説は意図的ミスリードでは、との冗談 |
| **Cody_Null** | 2026/08/05 20:12（+1） | **CV 5.x なのに LB 8.3** · train 側 **リーク事故**で 6.5 LB が出て以降その線も超えられない · 上位 5.x 到達過程が謎 |
| **AK** | 2026/08/05 19:25 | このコンペは実際に hard |

## スコア向上にとって

| 判断 | 内容 |
|---|---|
| **高（追認）** | **hard/jump 井**と **cycle skip** が多数の天井 · 自 L dual 全滅（F044–046）と整合 |
| **高（警告）** | Cody: **CV 良でも Public/隠れで壊れる** · リークで得た 6.5 を本命にしない |
| **中** | 上位 5.x の機構は **まだ非公開** · Private 後 writeup 待ち |
| Active CHK | **不要**（締切済 · 実験停止） |

## 効果が薄い／注意

- LLM が Private を抜く類のジョークに依存しない  
- 「〜8 で全員同じ」ではない（Public 上位は 4–5 帯）。**自 Trust レーンは別物差し**
