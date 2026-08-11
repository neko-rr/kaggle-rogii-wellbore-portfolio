# Pretrain gate — CHK-203 tip-cv-upstream-dump-t2

> date: 2026-07-26  
> job: `kazeneko77/tip-cv-upstream-dump-t2` · Kaggle GPU · **提出なし**  
> profile: tabular · tip TIP_CV full E2E（early exit 撤去）

## Tier 0

- [x] tip 既知パイプライン（`rogii-luck-is-all-you-need` + TIP_CV inject）· dataset_sources 既存 tip と同型
- [x] 評価区間 = `TVT_input` NaN（inject で sample 構築）
- [x] 出力形式 `id,tvt`（`tip_train_preds.csv` = FINAL）· **提出禁止**を VARIANT / dump セルで明示
- [x] F015: 中間面を submission 昇格しない（診断 dump のみ）

## Tier 1

- [x] tip-train-cv-allowlist 完走実績（selector early-exit · T2 ~1.5–2h）あり → inject/依存は既知
- [x] 本ジョブ差分は early exit 撤去 + 末尾 dump のみ（新モデルなし）
- [ ] 本ラン完走後に `chk203_stage_dump_report.json` で段階 mean_abs を確認（Tier1 事後）

## Tier 2

- [-] N/A: スコア改善実験ではない（診断 T4）。採点はローカル harvest 後

## 判定

**PASS（長時間 GPU 起動可）** — tip 家系の再実行 · 提出なし · 見込み ~2–3h（9h 以内）

## 停止条件

- OOM / 9h 接近 → hard20 に縮小して再 push
- dump セル前に落ちた場合は selector のみで CHK-203 不完全 → ログ残して報告
