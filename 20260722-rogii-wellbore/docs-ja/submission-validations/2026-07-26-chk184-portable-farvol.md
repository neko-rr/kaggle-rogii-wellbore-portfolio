# Submission Validation — tip-chk184-portable-farvol（SUB-10）

> date: 2026-07-26  
> profile: csv  
> status: **PASS**  
> submit_mode: `notebook-linked`

## Artifact

- kernel: `kazeneko77/tip-chk184-portable-farvol` Ver1
- rows: 14151 · `id,tvt`
- sha256: `b192d3f348ae00680dc4df942b95cef5fd708c636a741f77dfb6b6e89b9ded4a`
- vs tip BH: **0 rows changed**（可視 test 3井で apply=0）
- vs SUB-9: 3405 rows differ（SUB-9 の適用分）

## Gate report（可視 3井）

| well | reason |
|---|---|
| 000d7d20 | skipped_portable_gate（self_dev≈2.07） |
| 00bbac68 | **excluded_farvol**（farvol≈2.22） |
| 00e12e8b | skipped_portable_gate（self_dev≈9.65 or heel≥0.85） |

→ 可視出力は tip FINAL と同値。Public は tip 帯（≈6.569）想定。隠し井で効くかは PENDING で確認。

## Submit

- ref: **54983914**
- status: **PENDING**
- message: `CHK-184 portable farvol exclude f33-s05 (T2 screen +0.072)`
