# run-ledger — rogii-wellbore

> type: run-economics  
> skill: experiment-management（`kaggle-comp-timeline` と連動）  
> updated: 2026-08-04（CHK-FINAL-T2 T2追記）  
> purpose: **1 run = 環境 + GPU 時間 + 概算コスト + 評価指標への効果** を追跡する

**SSOT:** 実行の時間・コスト・metric の詳細は本ファイル。  
**今日の意思決定**（提出枠・優先 run）は `docs-ja/comp-timeline.md` の「提出・実行戦略」節。

---

## 使い方

| タイミング | 動作 |
|---|---|
| 学習 / 重い推論 **開始前** | 見積行を `pending` で追加（env, gpu, 見積時間, 期待 delta） |
| pretrain-gate **PASS 後** | `verdict` を `go` に更新してから長時間実行 |
| run **完了後** | `wall_hours`・`est_cost_usd`・`metric`・`delta` を実測で埋める |
| LB / holdout **確定後** | `metric_source` を更新。効かなければ `exp-train.md` の「効かなかった」へリンク |
| 作業開始時（日次） | `comp-timeline` の戦略節と突き合わせ、今日の GPU 予算を確認 |

### 記録ルール

1. **1 行 = 1 run**（学習完走、Kaggle kernel 完走、Tinker job、提出 1 回に紐づく検証 run）
2. `exp_id` / `chk_id` は `hyperparameter-table.md` または `experiment-checklist.md` と一致させる
3. `metric` はコンペの **公式評価指標** に合わせる（例: Accuracy, AUC, Public LB score）
4. コスト不明は `est_cost_usd` を `—`、notes に根拠（例: Colab Pro+ 込み・Kaggle 無料）
5. narrative は `exp-train.md` / `exp-infer.md` に書き、本ファイルは **表のみ**

### 見積の目安（notes 用・コンペごとに上書き可）

| env | gpu | 典型 wall_hours | est_cost_usd の考え方 |
|---|---|---|---|
| kaggle | T4 x2 | 〜9h（上限） | 0（無料枠） |
| kaggle | P100 | 〜9h | 0 |
| colab | T4 | 〜12h/日 | Pro+ 月額按分 or `—` |
| colab | A100 | 数時間 | セッション単価の概算 |
| tinker | — | job 依存 | Discussion / 公式料金を notes へ |
| local | RTX 等 | 実測 | 電気代は通常 `—` |

---

## Run ログ

| run_id | date_utc | exp_id | chk_id | env | gpu | wall_hours | est_cost_usd | metric | delta | metric_source | verdict | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R-FINAL-T2 | 2026-08-03 | colab-final-t2 | CHK-FINAL-T2 | colab | CPU主体 | **~1.5–3（80井 dump）** | — | agree-only pooled **12.279** · hard_mean **18.521** | tip 17.030 → Δ−4.75 | local-cv | **done** | run `20260803-114917` · facesローカル済 · 提出禁止 · `t2-catalog-report.md` |
| R-FINAL-T2-773 | 2026-08-03 | colab-final-t2 | CHK-FINAL-T2 | colab | CPU high-mem | **~14–18（見積）** | — | all773 agree-only | — | local-cv | **pending** | restart `20260803-160035` · 切断後要再開 · 提出禁止 |
| R-OPS-A | 2026-07-29 | OPS-SUBMIT-A | OPS-A | kaggle | GPU | **0.213（≈765s）** | 0 | Public **6.323** | +0.054 vs SUB-14 | public-lb | **reject** | T0.08 · SHA≡14 · F025追認 |
| R-OPS-B | 2026-07-29 | OPS-SUBMIT-B | OPS-B | kaggle | GPU | **0.211（≈759s）** | 0 | Public **6.274** | +0.005 vs SUB-14 | public-lb | **reject** | BH=0 · applied=0 |
| R-OPS-C | 2026-07-29 | OPS-SUBMIT-C | OPS-C | kaggle | GPU | **0.214（≈770s）** | 0 | Public **6.237** | −0.032 vs SUB-14 | public-lb | **done** | Public1運用 · 改善GOではない |
| R-OPS-D | 2026-07-29 | OPS-SUBMIT-D | OPS-D | kaggle | GPU | **0.230（≈829s）** | 0 | Public **6.276** | +0.007 vs SUB-14 | public-lb | **reject** | 25% gated · C未満 |
| R-W0-001 | 2026-07-23 | W0-ruler | CHK-010/012/024 | local | none | 0.056（200s/773wells） | 0 | CF pooled RMSE 15.91 | — | local-cv | done | CPU 物差し。200well換算≈52s |
| R-TIP-001 | 2026-07-23 | tip-luck-fork | CHK-013/011 | kaggle | GPU | **~0.22（≈13min · 3wells）** | 0 | submission.csv 14,151 rows | — | local-output | done | COMPLETE · scoring×200 は **9h超リスク** → PF削減/分割が縮小案 |
| R-TIPCV-001 | 2026-07-23 | tip-train-cv | CHK-014 | kaggle | GPU | hard20 見積 ~1–2h | 0 | tip_train_preds | — | — | done | hard20 初回 · 後続 T2/T3 へ |
| R-TIPCV-FILL | 2026-07-24 | tip-train-cv-allowlist | filler | kaggle | GPU | **~1.64（≈5906s · 80井）** | 0 | tip pooled **8.330** | vs CF同井 27.77 | local-cv | **done** | Ver5 filler · PASS再確認 · `tip-cv-report-allowlist-filler.json` |
| R-SMOKE-001 | 2026-07-23 | tip-smoke | CHK-014 | kaggle | GPU | — | 0 | Public PENDING | — | public-lb | go | submit ref 54920651 · Notebook 紐づけ Ver1 |
| R-CF-MS-001 | 2026-07-24 | W0-cf-multiseed | CHK-060 | local | none | **0.0096（≈34s）** | 0 | CF pooled **15.91** · worst_fold band **0.51** | — | local-cv | **done** | `--cf-only` · `cf-multiseed-report.json` |
| R-TIPCV-T2 | 2026-07-24 | tip-train-cv-t2 | CHK-061 | kaggle | GPU | **1.50（≈5385s · 80井）** | 0 | tip T2 pooled **8.33** | vs CF同井 27.77 | local-cv | **done** | Ver4 COMPLETE · PASS · `tip-cv-report-t2.json` |
| R-TIPCV-051b | 2026-07-24 | tip-train-cv-hard20-seed2 | CHK-051 | kaggle | GPU | **0.55（≈33min）** | 0 | tip pooled 14.87 · spread0 | 0 vs seed42 | local-cv | **done** | Ver1 COMPLETE · preds identical · `tip-nondet-report.json` |
| R-TIPCV-T3a | 2026-07-24 | tip-train-cv-t3 | CHK-062 | kaggle | GPU | ~6h ×2 seed | 0 | tip multi-seed band | — | local-cv | **done** | band0 · pooled 8.330 |
| R-TIP-E2E-002 | 2026-07-24 | tip-luck-fork | filler | kaggle | GPU | **~0.22（≈13min）** | 0 | submission.csv | — | local-output | **done** | Ver2 wall-clock remasure · filler |
| R-CHK040-001 | 2026-07-24 | chk040-heel-window-train | CHK-040 | kaggle | GPU | **~1.66（≈5983s）** | 0 | OOF **45.96** · tip corr **0.999** | CF 49.56 · unconst 72.24 | local-cv | **reject** | Ver1 · **F011 NO-GO** · `tip-cv-report-chk040.json` |
| R-CHK040-W40 | 2026-07-24 | chk040-heel-window-train | filler | kaggle | GPU | **~0.17（≈605s）** | 0 | OOF **44.58** · tip corr **0.999** | unconst 52.90 | local-cv | **reject** | Ver2 ±40 ablate · F011再確認 · 採択根拠にしない |
| R-CHK080 | 2026-07-24 | chk080-screen | CHK-080 | local | none | — | 0 | 層別表 | — | local-cv | **done** | `chk080-report.json` |
| R-CHK081 | 2026-07-24 | chk081 via chk071 | CHK-081 | kaggle | GPU | **~0.005（≈17s）** | 0 | OOF **49.59** · tip corr **0.999** | 適用3/20 | local-cv | **reject** | Ver5 soft · **F012** · `chk081-final2-memo.md` |
| R-TIPCV-FILL2 | 2026-07-24 | tip-train-cv-allowlist | filler | kaggle | GPU | **~1.84（≈6608s · 80井）** | 0 | tip pooled **8.330** | ≡T2 | local-cv | **done** | Ver6 · preds identical · `tip-cv-report-allowlist-filler2.json` |
| R-TIPCV-SEED2F | 2026-07-24 | tip-train-cv-hard20-seed2 | filler | kaggle | GPU | **~0.46（≈1652s · 20井）** | 0 | tip pooled **14.870** | ≡hard20基準 | local-cv | **done** | Ver4 · preds identical · `tip-cv-report-seed2-filler.json` |
| R-CHK090 | 2026-07-24 | tip-cv-vp-cons-h20 / E2E | CHK-090 | kaggle | GPU | hard20≈0.5h + E2E比較 | 0 | E2E≡default | tip14.87 | local-cv | **reject** | tip-cvはVP非到達 · E2E同一 · F013 |
| R-CHK091 | 2026-07-24 | tip-cv-sp45-h20 | CHK-091 | kaggle | GPU | hard20≈0.5h | 0 | pooled **24.78** | tip14.87 | local-cv | **reject** | F013 · `tip-cv-report-chk091.json` |
| R-CHK093 | 2026-07-24 | tip-bimodal E2E screen | CHK-093 | — | — | — | 0 | E2E≡default | — | local-cv | **reject** | F013 · 提出0 |

**verdict:** `pending` / `go` / `done` / `defer` / `reject`  
**metric_source:** `local-cv` / `holdout` / `public-lb` / `private-lb` / `sim-episode` / `—`

---

## 集計（任意・月次 or コンペ終了時）

| 期間 | 総 wall_hours | 総 est_cost_usd | 最良 delta | 採用 run_id |
|---|---|---|---|---|
| （コンペ通算） | — | — | — | — |

---

## 関連ファイル

| ファイル | 役割 |
|---|---|
| `docs-ja/comp-timeline.md` | 締切・提出上限・**提出・実行戦略（今日）** |
| `exp/exp-train.md` | 学習の narrative・CV 設計 |
| `exp/exp-infer.md` | 提出・LB の narrative |
| `exp/hyperparameter-table.md` | exp_id 別ハイパラ |
| `docs-ja/pretrain-gates/gate-log.md` | pretrain-gate の PASS/FAIL |

