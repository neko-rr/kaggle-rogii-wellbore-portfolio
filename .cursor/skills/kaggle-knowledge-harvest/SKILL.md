---
name: kaggle-knowledge-harvest
description: Kaggleコンペ終了時に失敗台帳とretroの汎用教訓を候補カードへ収穫し、Private knowledge-store へ反映する。post-comp、振り返り、知見集約、次コンペへ教訓を残す依頼で使う。
---

# Kaggle Knowledge Harvest

コンペ中の記録から、横断利用できる知見候補を **`knowledge/candidates/`** へ保存する。  
作業ツリーの `knowledge/` は **Private GitHub `kaggle-knowledge-store` の clone** であることが標準。

SSOT: `_shared/PRIVATE-KNOWLEDGE-AND-INFRA.md` · Rule `kaggle-knowledge-isolation`  
ID: 台帳 **Fnnn**＝コンペ内禁止 · harvest 後のカードは常に **KGL-…**（F の番号をカード ID にしない）。学びメモは **LES-** 可。  
`_shared/EXPERIMENT-ID-NAMESPACES.md`

## 境界

- Kaggle プロジェクト内だけで使う
- Skill・コマンド・根拠参照には相対パスだけを書く
- 外側コンペ Git では `/knowledge/` 除外。**nested git で Private push**
- 候補は未検証。自動で Rule や実験 CHK へ昇格しない

## 手順

0. **（推奨）SA-7 mode=`pre-harvest`** — 横断に持ち上げる教訓が over-generalize / apply-avoid 空でないか  
   Skill `kaggle-adversarial-review` · `_shared/ADVERSARIAL-REVIEW.md`  
1. `exp/exp-index.md`、`exp/improvement-loop-failures.json`、`retro/retro-lessons.md` を確認する
2. 汎用教訓が空なら、根拠付きで最低3件を `retro/retro-lessons.md` に記入する。  
   **必須フォーマット（各項目）:**
   ```markdown
   1. **太字タイトル**
      - body: 何を・なぜ
      - apply: 成立条件（このとき有効）
      - avoid: 禁忌（このとき使うな）
      - origin: own|topsolution|ops|mixed
      - domain: kaggle|ahc|shared
      - evidence: 根拠
   ```
   見出しは `### A. CV…` / `### B. 解法…` / `### C. 運用…`。空の apply/avoid は禁止。
3. 実行:

```powershell
./scripts/run-kaggle-knowledge.ps1 -Action harvest -CompRoot "./<competition>"
./scripts/run-kaggle-knowledge.ps1 -Action validate
./scripts/run-kaggle-knowledge.ps1 -Action audit
```

4. 作成件数・`conditions` / `contraindications`・コンペ固有語を確認する
5. L0 / conditional のままにする（勝手に promote しない）
6. 外部由来は provenance + audit
7. **Private knowledge-store へ反映（必須）:**
   ```powershell
   cd knowledge
   git pull origin main   # 先に取り込み
   git add -A
   git status
   git commit -m "harvest: <comp-slug> lessons/failures"
   git push origin main
   ```
   push しないと **他コンペの Agent は古い candidates のまま**になる。

## 収穫対象

- failures（**Fnnn 禁止台帳**）→ card **KGL-…** · kind `anti-pattern`（ID 文字は KGL。F 番号は provenance に残す）
- `retro-lessons` 構造化項目（**LES 可**）→ kind `lesson`（axis / origin / domain / apply / avoid）
- AHC は `personal/domain-policy.md`（shared のみ）

**F ≠ KGL。** コンペ内禁止 ID と横断カード ID を同一記号にしない。

タイトル変更の再 harvest は旧 `*-lesson-*.json` を消してから。

人間向け振り返り SSOT: 各コンペ `retro/retro-lessons.md`。
