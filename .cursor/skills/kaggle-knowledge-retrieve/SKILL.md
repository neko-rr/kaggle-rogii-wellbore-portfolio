---
name: kaggle-knowledge-retrieve
description: 新しいKaggleコンペの型と制約に合う過去知見を検索し、実験前のprior-knowledgeを生成する。コンペ開始、初期戦略、類似コンペ知見、実験候補作成時に使う。
---

# Kaggle Knowledge Retrieve

作業ツリーの `knowledge/`（**Private knowledge-store の clone**）からカードを読み、`exp/prior-knowledge.md` を生成する。

SSOT: `_shared/PRIVATE-KNOWLEDGE-AND-INFRA.md`

## 前提（開始時）

1. `knowledge/store.json` がある（無ければ clone）:
   ```powershell
   git clone https://github.com/neko-rr/kaggle-knowledge-store.git knowledge
   # $env:KAGGLE_KNOWLEDGE_GIT_URL で上書き可
   ```
2. 最新を取り込む: `cd knowledge; git pull origin main`
3. `docs-ja/comp-profile.md` の comp-type / 副タグが確定している

## 手順

1. 通常は承認済み `cards/` のみ:

```powershell
./scripts/run-kaggle-knowledge.ps1 -Action retrieve `
  -CompRoot "./<competition>" -Limit 10
```

2. **カードが少ない／開始直後**は候補も見る（現状の運用はこちらが主）:

```powershell
./scripts/run-kaggle-knowledge.ps1 -Action retrieve `
  -CompRoot "./<competition>" -Limit 20 -IncludeCandidates
```

3. `exp/prior-knowledge.md` を読む。  
   **順序:**  
   1. `domain` フィルタ（Kaggle なら `domain-kaggle` + `domain-shared`。AHC なら ahc+shared）  
   2. axis: **A 物差し（CV 含む）→ C 運用 → B 手法**  
   3. **CV 設計フェーズでは A を優先抽出**（tag `knowledge-axis-cv-validation` · body に split/group/OOF/leak）。Skill **`kaggle-cv-design`** で `docs-ja/cv-design.md` の参照表へ落とす  
   4. 各カードの **`conditions` / `contraindications`（apply/avoid）** — 不一致は捨てる  
   5. `transferability=conditional` · `evidence_level=L0` を「一般則」にしない  
4. 採用項目だけ、ユーザー確認後に `experiment-checklist` 仮説へ（**CV unit と矛盾するものは載さない**）  
5. pre-strategy-gate **X3** に prior 確認を記録 · **A4** に `cv-design.md` を証拠リンク

## 禁止

- 自動 CHK 化 · L0 を一般則扱い  
- 類似コンペというだけで評価指標・CV・提出制約を無視  
- 絶対パスを Skill / カードに書く  
- 外側 public repo に knowledge を載せる前提で「十分」とする

## メモ

- コンペ本体が GitHub に無くても、**knowledge clone だけで prior は生成できる**  
- カードの `source_refs` 先（旧コンペ retro）は本体が無いと開けない — **apply/body が本文として十分**なのが目標  
- ベクトル検索: [vector-search-roadmap.md](vector-search-roadmap.md)（任意 · 条件付き）
