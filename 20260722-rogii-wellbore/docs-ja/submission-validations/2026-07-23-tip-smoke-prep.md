# Submission Validation (auto)

- status: PASS
- profile: csv
- artifact: 20260722-rogii-wellbore/my-ran-notebook/rogii-luck-is-all-you-need-private-tip-fork/submission.csv
- checked_utc: 2026-07-23
- method: Python quick check（validate-submission.ps1 の Import-Csv が 14k 行でタイムアウトしうるため）

## Checks

- [x] artifact exists · non-empty
- [x] columns = id,tvt
- [x] rows = 14151
- [x] tvt NaN/Inf = 0
- [x] id duplicates = 0
- [x] submit_mode: notebook-linked（予定）

## Notes

- tip smoke CHK-014 · kernel `kazeneko77/rogii-luck-is-all-you-need-private-tip-fork` Version 1
- L2: Notebook 紐づけ · Internet OFF · Private tip
- submit ref **54920651** · COMPLETE · Public **6.569**（2026-07-24 確認）
- 作者公開 6.478 との差 +0.091 · 自 Best 6.524 未更新 → 戦略 tip だが LB 主提出は top-reproducible 継続
- 採点待ちは長時間（7h+）だったが完了済み
