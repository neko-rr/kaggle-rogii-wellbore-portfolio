# Submission Validation — CHK-458 diagnostic

- status: **PASS（提出時）→ Public COMPLETE · 判定 NO-GO**
- profile: csv
- submit_mode: **notebook-linked**
- artifact: `exp/work/wave31-selector-replace/out-458-e2e/submission.csv`
- kernel: `kazeneko77/chk458-keep-self-verified-e2e-gpu` Ver1
- refs: **55161873**（主）· **55161881**（再送重複）

## Public harvest（2026-08-02）

| ref | Public | 判定 |
|---|---:|---|
| 55161873 | **7.781** | **NO-GO** |
| 55161881 | **7.760** | **NO-GO**（同帯） |

vs SUB-14 **6.269** ≈ **+1.51** · vs farvol Best **6.190** ≈ **+1.59** · SUB-18 learned 同帯（~7.7）。  
分析: [`exp/latest/ops-lb-chk458-public-2026-08-02.md`](../../exp/latest/ops-lb-chk458-public-2026-08-02.md) · **F042**

## L0-L1 Checks（提出時）
- [x] artifact exists
- [x] csv extension ok
- [x] basic secret scan passed
- [x] timeline found (final-submit not marked closed)
- [x] csv rows=14151
- [x] required column check executed
- [x] id has no duplicates
- [x] `check-codecomp-submit-kernel.py` PASS

## L2
- [x] E2E self kernel（固定CSVコピーではない）
- [x] Internet OFF · Private
- [x] 診断1枠意図（Final差替ではない）
- [!] CLI 再実行で **2件**（同一内容）
- [x] Final 枠に載せない · 460/461 提出禁止強化
