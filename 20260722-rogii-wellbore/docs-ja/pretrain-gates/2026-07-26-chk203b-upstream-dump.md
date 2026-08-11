# Pretrain gate — CHK-203b tip-cv-upstream-dump-t2b

> date: 2026-07-26  
> job: `kazeneko77/tip-cv-upstream-dump-t2b` · Kaggle GPU · **提出なし**  
> profile: tabular · tip TIP_CV full E2E + learned-skip

## Tier 0

- [x] tip 既知パイプライン + TIP_CV inject · dataset_sources tip 同型
- [x] 評価区間 = `TVT_input` NaN
- [x] 出力 `id,tvt` · **提出禁止**
- [x] F015: 中間面昇格なし
- [x] learned blend id mismatch を TIP_CV 下でスキップ（203 ERROR 修復）

## Tier 1

- [x] tip-cv / 203 系完走実績あり · 差分は blend skip + dump status
- [ ] 完走後 `chk203_stage_dump_report.json` で selector + ≥1 upstream `ok` を確認

## Tier 2

- [-] N/A（診断 T4）

## 判定

**PASS** — 見込み ~2–3h · 9h 以内 · 提出なし

## 停止条件

- OOM / 9h → hard20 に縮小
- dump 前落ち → ログ残して報告
