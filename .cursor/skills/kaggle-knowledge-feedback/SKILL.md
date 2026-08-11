---
name: kaggle-knowledge-feedback
description: 過去のKaggle知見を別コンペで試した結果を再現証拠として記録し、L1/L2/L3昇格上限を算出する。知見のGO・NO-GO、再現確認、反証、転用評価時に使う。
---

# Kaggle Knowledge Feedback

実験後の結果を `knowledge/evidence/<card-id>/` に追加する。カード本文を直接書き換えず、コンペ別証拠を積み上げる。

## 手順

1. 対象カード、実験ID、GO/NO-GO、根拠ファイルを確認する
2. 根拠はリポジトリ相対パスで指定する
3. 次を実行する

```powershell
./scripts/run-kaggle-knowledge.ps1 -Action feedback `
  -CompRoot "./<competition>" `
  -CardId "KGL-..." `
  -ExperimentId "CHK-..." `
  -Verdict GO `
  -SourceRef "<competition>/exp/hyperparameter-table.md#CHK-..."
```

4. 出力された昇格上限を確認する
5. 昇格は別途 `kaggle-knowledge-promote` でユーザー承認後に行う

## 昇格上限

- `L0`: 証拠不足または1回だけ
- `L1`: 同一コンペでGOが2回以上
- `L2`: 異なる2コンペ以上で自チームGO
- `L3`: L2に加え、公開上位解法の独立証拠がある

`MIXED`と`NO-GO`も削除せず残す。都合の良いGOだけを選ばない。
NO-GO/MIXEDはカードの`contraindications`へコンペ・実験・根拠を追記する。`active`カードの場合は`disputed`へ下げ、再審査する。
