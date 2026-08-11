# Private Test Update and Rescore

> Topic ID: **707695**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/707695  
> 投稿者: **Ryan Holbrook**（Kaggle Staff）  
> 投稿日時: **2026/06/11** UTC  
> 最新コメント: **2026/06/13** UTC  
> 票: 18  
> 原文: `docs-en/discussion/Kaggle-Staff_707695-Private-Test-Update-and-Rescore.md`

## 要約

Private test に **outlier well** があり、採点から **除外**。Rescore 実施。

- Public LB は変化なし（Private のみ）
- データ自体は test に残るため **実行時間はほぼ変わらない**
- 既存提出が一時 pending になることがある

副作用報告（2026/06/11–12）: 一部ベスト提出が Error 表示 → 再提出で成功。Staff 対応。

## タイムライン影響

- Private 採点定義の変更あり（outlier 除外）— 最終順位に影響しうるが Public では見えない
- `comp-timeline` の評価補足に反映済み想定 → 必要なら追記

## スコア向上への示唆

- Public 最適化だけでは Private outlier 周りを見誤る可能性（Working Note の CV 規律と整合）
