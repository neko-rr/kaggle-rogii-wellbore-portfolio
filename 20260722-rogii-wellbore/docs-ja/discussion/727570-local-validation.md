# How are you validating locally?

> Topic ID: **727570**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/727570  
> 投稿者: **IamDiganta.7**  
> 投稿日時: **2026/07/19** UTC  
> 最新コメント: **2026/07/23** UTC（**souldrive**）  
> 原文: `docs-en/discussion/727570-how-are-you-validating-locally.md`  
> 更新: 2026/07/24（souldrive コメント追記）

## 要約

ローカル CV と LB の相関が取れない、という質問への回答スレ。

### CV / LB 共有値

| 誰 | 日時 UTC | CV | LB | 備考 |
|---|---|---|---|---|
| **Tucker Arrants** [+3] | 2026/07/19 | **4.98**（5fold × 5seed） | **5.7** | well-group。**per-well データのみ**。近傍/空間特徴なら分割を変える。LB はノイジー |
| OpPrime | 2026/07/21 | 6–8 | 8–10 | モデル依存。GRU 例: CV6 → LB7.35。memorization しやすい骨格あり |
| **souldrive** [+1] | **2026/07/23** | 下表 | — | **well-CV と field-CV を常に併記** |

追加: 同一モデル・同一 seed でも **GPU 差でノイズ**（Tucker, 2026/07/21）。  
OpPrime: ソース無し ensemble（Fleongg 系等）は fold/seed 不一致で CV–LB 関係が崩れる。

### souldrive — two-level CV（2026/07/23）★新規

| 分割 | 意味 |
|---|---|
| **By well** | 最低ライン。行単位 CV はほぼ補間測定 → リーク |
| **By field** | 井の median X/Y で k-means（k=5）し、グループごと hold-out。hidden の「未見地域」に近い |

単純ベースライン（773 wells）:

| 手法 | well-CV | field-CV | worst field |
|---|---|---|---|
| flat anchor | 15.799 | 16.085 | 19.208 |
| anchor + 0.02×local slope | 15.497 | 15.884 | 19.137 |

- field−well ギャップ ≈ **0.3 ft** = 「近傍を既に見た分」→ hidden では貰えない
- **worst field** も見る（平均だけ良いモデルが危険）。ただし k-means seed で動くので pooled と併記
- 他人の CV–LB ギャップ（+0.32〜+1.35）を自分の校正に借りるのは危険
- **`test/` は検証に使えない**: 3 wells は train の完全コピー（prefix RMSE 0）。提出時に差し替わるプレースホルダ

Notebook: https://www.kaggle.com/code/souldrive/rogii-tvt-identity-and-honest-cv-design

## スコア向上への示唆

- 目標目安: well-group pooled CV **~5** 前後が上位帯の一例（Tucker）
- 近傍特徴を入れるなら **空間リーク防止の分割**を別設計
- **well-CV と field-CV の差**を監視（Trust CV の補強）
- LB ±0.5〜1 程度の揺れを織り込む
- 手元 `test/` スコアは無意味（identity）

## 効果が薄かった取り組み

- CV と LB を無理に一致させようとして分割を歪める
- 他人の CV–LB オフセットを自分の校正に流用する
- `test/` 3 wells での「検証」
