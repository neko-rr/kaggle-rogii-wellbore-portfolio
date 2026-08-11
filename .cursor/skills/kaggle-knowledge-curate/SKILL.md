---
name: kaggle-knowledge-curate
description: Kaggle知見の類似候補を確認し、ユーザー承認付きalias統合とactive・conditional・disputed・deprecated・supersededの寿命管理を行う。重複整理、反証、廃止時に使う。
---

# Kaggle Knowledge Curate

重複候補を提示し、根拠確認後だけcanonical cardへalias化する。カードは削除しない。

## 重複候補

```powershell
./scripts/run-kaggle-knowledge.ps1 -Action duplicates -Threshold 0.82
```

`knowledge/duplicate-candidates.json` のconcept key、類似度、根拠、成立条件を人が確認する。類似度だけで統合しない。

## alias

ユーザー承認後だけ実行する。

```powershell
./scripts/run-kaggle-knowledge.ps1 -Action alias `
  -SourceCardId "KGL-source" `
  -TargetCardId "KGL-canonical" `
  -Reason "同じ抽象機構を別コンペで確認" `
  -Approve
```

- source_refsとevidenceをtargetへ追加
- sourceは削除せず`superseded`
- sourceの`superseded_by`と双方の`related_cards`を記録

## 寿命変更

```powershell
./scripts/run-kaggle-knowledge.ps1 -Action lifecycle `
  -CardId "KGL-..." -LifecycleStatus deprecated `
  -Reason "評価条件変更で再利用不可" `
  -SourceRef "<competition>/exp/result.md#CHK-..." -Approve
```

`superseded`はalias専用。`active`はL2以上が必要。NO-GOは削除せずcontraindicationsへ追加し、activeカードは自動で`disputed`になる。
