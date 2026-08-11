# Submission fails with "Notebook Threw Exception"（提出エラー）

> Topic ID: **729554**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/729554  
> 投稿者: **Angel R, Gadea L.**（当時 ~5761st）  
> 投稿日時: **2026/07/26** UTC  
> 最新コメント: **PC Jimmmy · 2026/07/26 ~22:31** UTC  
> 原文: `docs-en/discussion/729554-notebook-threw-exception.md` · refresh: `729554-refresh-20260727-raw.md`

## 要約

Save & Run All では `submission.csv`（**14151×2** · sample 順）が正しく出るが、**Submit** すると `Notebook Threw Exception`。ログ末尾は NbConvert のみで Python traceback が無い。最小の「submission だけ作る」NB は受理された。

## コメント時系列

| 誰 | 日時 (UTC) | 要点 |
|---|---|---|
| **PC Jimmmy**（~2870th） | 2026/07/26 02:06 | 見えるログは **3偽井**のみ · 多くは hidden≈**200井**の shape/mem · 対策: エディタで **train を予測**して潰す · 難しければ Public 化してリンク共有 |
| **OP** | 2026/07/26 18:10 | 多井再現で原因特定: **`offset_inicio` を sample_submission（3井）から生成**していた → 実 test_horizontal から動的生成に変更 · 200井シミュレーションでは通るが **Submit はなお Exception** |
| **PC Jimmmy** | 2026/07/26 22:31 | 例年は sample_submission が頼りだったが **今年は危険**（別コンペでは private 環境にファイル自体が無く大量失敗）· **mental note: never use it** · 公開リンク共有を再勧奨 |

## 自チームへの示唆

| 判断 | 内容 |
|---|---|
| 既知リスク | 手元 `test/`（3井）成功 ≠ hidden 完走（EDA #4 · CHK-011） |
| **運用強化** | 行数・offset・井リストを **`sample_submission` にハード依存させない**（hidden / train-規模で組み立て） |
| **確定罠（2026-08-03）** | [732296](732296-notebook-threw-exception.md): **`assert len(sample_sub)==14151` は Submit で Exception**（sample 行数） |
| 新規 CHK | **不要**（エラー系の再確認） |

## 効果が薄い／注意

- 「14151 行で検証OK」は **sample 規模の検証**に過ぎない（Q0522 系の sample 固定パッチと同系統の罠）
- OP は修正後も Submit 失敗 → 別の hidden 固有要因の可能性。公開デバッグを待つ
