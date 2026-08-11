# Phase 1: チェックリスト作成プロンプト（Agent 用断片）

以下を Phase 1 で実行する。実験はまだ開始しない。

## 入力

- `exp/exp-intel.md`
- `exp/hyperparameter-table.md`
- `exp/exp-train.md`, `exp/exp-infer.md`
- `docs-ja/discussion/`（あれば）
- `docs-ja/others-notebook/`（あれば）

## 手順

1. **既試行の抽出** — hyperparameter-table と exp-train/infer から、設定・notebook・手法の一覧を作る（重複防止用）
2. **他者候補の抽象化** — intel / discussion / notebook 要約から、**写経ではない** 1仮説1行を抽出
3. **dedupe** — 既試行・checklist done/rejected と意味が同じ候補は除外または rejected へ
4. **prioritize** — 弱点（metric / カテゴリ / LB gap）に直結するものを high
5. **書き込み** — `exp/experiment-checklist.md` の Pending に `CHK-xxx` 形式で追加。各項目に `acceptance` を必須記載
6. **index 更新** — `exp/exp-index.md` の次アクションを「Phase 2: CHK-001 から実行」に更新

## 禁止

- 同一仮説を pending に二重登録
- rejected 項目を pending に戻す（仮説変更なし）
- Phase 1 で LB 提出や大容量学習を開始
- チェックリスト無しで Phase 2 に入る
- **`fork {author}/{notebook}` だけ** · **`〇〇を提出` だけ**を CHK 仮説の主語にする（fork 先は intel / `my-notebook/` · 提出は exp-infer）
- **提出履歴・fork 優先度リストを checklist に複製する**

**許可:** fork は `kaggle-kernels-runbook` / `my-notebook/` で実施。CHK では **材料として** `source: notebook/...` や acceptance に Run All を書いてよい。

## 完了報告

Phase 1 完了時のみ、pending 件数・high priority 上位3件・除外した重複数を短く報告してよい。  
Phase 2 中は **完了報告でターンを終えない**。
