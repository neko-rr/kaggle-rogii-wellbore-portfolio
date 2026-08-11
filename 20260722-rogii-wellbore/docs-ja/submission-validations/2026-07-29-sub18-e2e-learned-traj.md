# Submission Validation — SUB-18 E2E learned_trajectory

> date: 2026-07-28 22:29 UTC  
> profile: csv  
> artifact: `exp/work/kernels-output-tip-e2e-learned-traj/submission.csv`  
> execution: kaggle GPU · COMPLETE  
> result: **PASS**  
> submit_mode: notebook-linked

## Artifact

- kernel: `kazeneko77/tip-e2e-learned-traj` **Ver1**
- promote: `learned_trajectory_submission.csv` → `submission.csv`
- sha256: `61797DE06526048340BAD29768519DBA485E6E8754FDB12DC84D9CC49DD073F9`
- submit_ref: **55066050**（正）· 誤重複 **55066056**（同一メッセージ再 submit）
- purpose: **diagnostic** · F005 remake · Final 枠候補にしない

## L0

- [x] rows=14151 · cols=`id,tvt` · unique id · finite tvt
- [x] `validate-submission.ps1` PASS

## L0.5（Code Comp kernel）

- [x] `check-codecomp-submit-kernel.py` PASS（固定 CSV コピーではない）

## L1 / L2

- [x] Private · Internet OFF · E2E 同一 NB 末尾昇格
- [x] Notebook 紐づけ `-k kazeneko77/tip-e2e-learned-traj -v 1`
- [x] SUB-17 は SHA≡promote-pre-bh（6.653）+ F015 のため **見送り**（ユーザー承認）

## 提出枠

- UTC 2026-07-28: 本提出で **2 枠消費**（意図1 + 誤重複1）
- 残り: 日次5 − 2 = **3**（同 UTC 日）
