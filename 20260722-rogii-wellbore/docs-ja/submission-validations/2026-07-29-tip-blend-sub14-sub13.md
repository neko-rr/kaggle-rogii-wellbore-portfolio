# Submission Validation — tip-blend-sub14-sub13-e2e

> date: 2026-07-29  
> profile: csv  
> result: **PASS → submitted**  
> submit_mode: notebook-linked

## Artifact

| 項目 | 値 |
|---|---|
| kernel | `kazeneko77/tip-blend-sub14-sub13-e2e` **Ver3** |
| ref | **55066793** |
| SUB | **SUB-19** |
| status | COMPLETE · Public **6.277** |
| purpose | diagnostic · SUB-14×SUB-13 **0.85/0.15** · Final自動採用なし |
| vs Best | 再構成 RMSE **0.165**（≠SHA · F025回避）· Public Best+0.008 · **枠外** |

## L0

- [x] rows=14151 · `id,tvt` · unique · finite
- [x] tip E2E @T0.15 後に T0.5 face と合成（ログ: `n_common 14151`）
- [x] secondary path: `/kaggle/input/notebooks/kazeneko77/tip-gated-lik-temp-0p5/submission.csv`

## L0.5

- [x] `check-codecomp-submit-kernel.py` PASS

## 併記

- **T=0.10 E2E** は最終≡Best のため **未提出**（[`nosubmit`](2026-07-29-tip-gated-lik-temp-0p1-nosubmit.md)）
