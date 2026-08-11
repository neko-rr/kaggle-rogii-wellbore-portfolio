# pretrain-gate — CHK-FINAL-T2 Colab Trust face dump

> PASS（条件付き）· Colab GPU · Drive 永続 · **提出禁止**

## job

- notebook: `my-local-eval-notebook/tip-cv-final-t2-colab/tip-cv-final-t2-colab.ipynb`
- lane: **Google Colab GPU**（Kaggle 9h 外 · Drive 必須）
- phase1: `hard20_balanced`（≈80井 · 見積 1.5–3h）
- phase2（勝者のみ）: `all773`（見積 14–18h · Drive checkpoint）

## Tier 0/1

- [x] 目的は Final 枠1の A/B/C 頭突き（採用判定）。提出しない
- [x] 面は同一ラン: tip_selector / before_hedge(mid) / learned
- [x] F015: learned は agree ゲートのみ · inject は mid
- [x] 採点は `score_final_trust_abc.py`（hard20 smoke で 26.655/26.768 再現済）
- [x] Drive: `MyDrive/Kaggle/rogii-wellbore/.../exp/work/colab-final-t2/runs/<run_id>/`
- [x] MCP 切断後も Drive に残る前提

## 見積

| phase | wells | tip-cv wall（外挿） |
|---|---:|---|
| T2 balanced | 80 | ~1.5–3h |
| all773 | 773 | ~14–18h |

## Verdict

**PASS** — ユーザー明示の Colab GPU 許可後に T2 から起動してよい。773 は T2 勝者確定後のみ。
