# 提出ルール — 20260722-rogii-wellbore（csv）

> skill: kaggle-submission-validator  
> submission-profile: **csv**（Code Competition · Notebook 紐づけ）  
> last-updated: 2026-08-03（9h=全 test · [732422](discussion/error/732422-private-lb-9h-runtime.md)）

LB 提出直前の検証ルール **SSOT**。提出方式: `.cursor/skills/_shared/NOTEBOOK-LINKED-SUBMIT.md`

---

## 提出形式（変更禁止）

| 項目 | 内容 |
|---|---|
| 成果物 | **`submission.csv`**（ヘッダ必須 · 列 **`id,tvt`**） |
| `id` | `{WELLNAME}_{row_index}`（例: `000d7d20_1442`） |
| `tvt` | 予測 True Vertical Thickness (ft) · NaN/Inf 禁止 |
| **Agent** | Overview / 本表の形式を **変えない**（列追加・リネーム・独自 ID 禁止） |
| **標準提出** | **Notebook 紐づけ**（UI「Submit to Competition」または CLI `-k` / `-v`） |
| Code Comp 制約 | CPU/GPU ≤ **9h（Public+Private 全 test）** · **Internet OFF** · 出力ファイル名は `submission.csv` · [732422](discussion/error/732422-private-lb-9h-runtime.md) |
| 日次上限 | **5 Submissions / day**（Rules · **UTC 日付**） |
| Final 選択 | **最大 2** Final Submissions |
| **Public / Private** | Public ≈ テストの **26%** · 最終順位は残り **74%**（Private）。公式文は [`conditions.md`](conditions.md) §Public/Private |
| 非推奨 | ローカル csv の **`-f` のみ**（採点は通っても Notebook が提出履歴に残らない） |

---

## L0-L1（自動）

```powershell
# Code Comp: 固定CSVコピー NB を先に弾く（F005 · SUB-17/18）
.\.venv\Scripts\python.exe .\scripts\check-codecomp-submit-kernel.py -p ".\20260722-rogii-wellbore\my-notebook\<slug>"

.\scripts\validate-submission.ps1 -ArtifactPath .\submission.csv -Profile csv `
  -ExpectedColumns "id,tvt" -ExpectedRows <N> -CompInner .\20260722-rogii-wellbore
```

`<N>` は `sample_submission.csv` の行数（ヘッダ除く）に合わせる。データ DL 後に確定。  
**L0 PASS だけでは提出不可** — 下の L2（E2E）も必須。

---

## L2（手動 · コンペ固有）

- [ ] sample_submission と列名・順序が一致（`id,tvt`）— **形式を変更していない**
- [ ] **sample 行数（例: 14151）の assert / 固定比較は禁止**（Submit の hidden で落ちる · [732296](discussion/error/732296-notebook-threw-exception.md)）
- [ ] 行数・ID 集合が一致（hidden test では Notebook **再実行**側で保証）
- [ ] NaN / Inf が無い · `tvt` が数値
- [ ] **Notebook 紐づけ**で提出する（zip/csv 直 `-f` のみは避ける）
- [ ] **`check-codecomp-submit-kernel.py` PASS**
- [ ] **自 kernel がコンペデータから `submission.csv` を E2E 生成**する Version（固定 Dataset CSV コピー / kernel_sources コピー Script は **Scoring Error · F005** · SUB-3/17/18）
- [ ] 中間面を出すなら **同一 E2E 実行の末尾で昇格**（別の短 NB で載せ替えない）
- [ ] Internet OFF · 実行時間 ≤ 9h で完走する想定
- [ ] 日次上限（5 · UTC）を超えていない · ユーザーの「今日は提出しない」指示を優先
- [ ] Final 2 候補の意図が記録されている
- [ ] **Public スコアを最終順位と誤解していない**（Public≈26% · Private≈74% · [`conditions.md`](conditions.md)）
- [ ] 外部依存があれば `license-ledger.md` Tier R 更新済み（メダル/賞金前は A+）

---

## 提出手順（標準）

SSOT: `.cursor/skills/_shared/NOTEBOOK-LINKED-SUBMIT.md`

1. `check-codecomp-submit-kernel.py` PASS
2. validator PASS
3. 自 kernel を Save Version / `kernels push`（**Private** · **E2E**）
4. UI Submit **または** CLI `-k <YOUR_USER>/<SLUG> -v N -f submission.csv`
5. 403 時は **zip/csv-only に逃げない** — 自 fork 更新を先に

---

## 提出後の採点待ち（観測メモ · 2026-07-23）

| 項目 | 内容 |
|---|---|
| 現象 | Submit 後 `SubmissionStatus.PENDING` が長時間続く |
| **目安** | **Public スコア確定まで 7 時間以上**かかることがある（短時間で完了しない前提で待つ） |
| 実測例 | `54914222`（2026-07-22 23:48 UTC）と tip smoke `54920651`（2026-07-23 06:07 UTC）が、提出から **約 7h+** 経過してもなお PENDING（ローカル確認 2026-07-23 15:59 JST 頃） |
| 運用 | PENDING 中に追加提出しない · LB 未着でも tip-cv などローカル／Kaggle 実行は進めてよい · Discussion [728152](discussion/error/728152-scoring-stuck-timeout.md) の 9h+ timeout とも別件で併記 |
| Scoring Error | CSV L0 通過でもコピー専用 NB なら Error（F005）— 形式問題ではなく **再実行不能** |
