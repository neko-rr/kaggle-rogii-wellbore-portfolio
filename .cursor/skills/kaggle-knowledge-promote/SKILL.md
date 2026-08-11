---
name: kaggle-knowledge-promote
description: Kaggle知見候補を根拠レベルで審査し、承認済みカードへ昇格する。知見の一般化、再現性評価、候補昇格、複数コンペでの再現確認に使う。
---

# Kaggle Knowledge Promote

`knowledge/candidates/` の候補を審査し、ユーザー承認後だけ `knowledge/cards/` へ昇格する。

## 証拠レベル

- `L0`: 1回の観測。条件付き仮説
- `L1`: 同一コンペ内で複数回再現
- `L2`: 複数コンペで再現
- `L3`: 複数コンペの自チーム実測と上位解法が一致

`L0/L1` は `conditional`、`L2/L3` だけが標準方針候補になる。スコア値そのものはコンペ間比較しない。
昇格上限は `knowledge/evidence/` から機械計算する。指定だけでL1以上へ上げることはできない。

## 必須確認

1. `source_refs` が存在し、リポジトリ相対パスである
2. 「条件 → 作用 → 結果」が説明できる
3. コンペ固有trickと汎用機構を分けている
4. 反証・適用禁止条件を確認した
5. Skill `kaggle-knowledge-feedback` で必要な再現証拠が記録されている
6. **昇格についてユーザーの明示承認がある**
7. （推奨）L2+ や標準方針候補の前に **SA-7 `pre-harvest`** で over-generalize を1パス

## 実行

```powershell
./scripts/run-kaggle-knowledge.ps1 -Action promote `
  -CardId "KGL-..." -EvidenceLevel L1 -Approve
./scripts/run-kaggle-knowledge.ps1 -Action validate
```

承認後は **Private knowledge-store へ push**（他コンペの `git pull` で `cards/` が取れる）:

```powershell
cd knowledge
git pull origin main
git add cards/ candidates/ evidence/
git commit -m "promote: KGL-..."
git push origin main
```

承認がない場合は `-Approve` を付けず、昇格しない。Rule化は別判断とし、カード昇格だけで alwaysApply にしない。
