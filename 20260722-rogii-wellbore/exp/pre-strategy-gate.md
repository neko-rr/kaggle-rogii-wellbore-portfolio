# 戦略前機械チェックゲート — rogii-wellbore

> comp-type: **tabular**（+ code-competition · 9h · internet-off → **R** 併用）· 更新: 2026-07-23  
> カタログ SSOT: `knowledge/mechanical-improvements.md`  
> 判定: `.\scripts\check-pre-strategy-gate.ps1 -CompRoot .\20260722-rogii-wellbore`

## 使い方

- 記法: `- [ ]` 未完了 / `- [x]` PASS / `- [-]` N/A（行末に `N/A: 理由`）
- **「## 必須」節の `[ ]` が 0 になるまで戦略CHKを作らない**

## 必須 — C: 共通・土台

- [x] C1 評価指標のローカル再現 — 証拠: `docs-ja/metric-repro.md`（RMSE · rules-only）
- [x] C2 提出形式の機械検証スクリプト — 証拠: `scripts/validate-submission.ps1` · `docs-ja/submission-rules.md`
- [x] C3 最弱ベースラインの提出 — 証拠: `exp/exp-infer.md`（LB スコア付き提出複数 · パイプライン疎通済）
- [x] C4 sample_submission との整合確認 — 証拠: `docs-ja/submission-rules.md` · `docs-ja/dataset.md`（`id,tvt`）· 提出 COMPLETE 済み
- [x] C5 seed・決定性の固定 — 証拠: `docs-ja/others-notebook/rogii-det-mha-family-Ver2.md`（決定論バリアント方針）· 自前本流は CHK-010 で再固定
- [x] C6 SSOT の初期化 — 証拠: `exp/exp-index.md` · `exp/experiment-checklist.md` · 本ファイル
- [x] C7 締切・提出回数・フェーズの記録 — 証拠: `docs-ja/comp-timeline.md`
- [x] C8 ルール由来の禁止事項の列挙 — 証拠: `docs-ja/submission-rules.md` · `docs-ja/conditions.md` · `docs-ja/comp-strategy.md` Stop

## 必須 — A: 精度向上型

- [x] A1 欠損・重複・型の機械検査 — 証拠: `docs-ja/dataset.md` · `docs-ja/others-notebook/public-validation-education-Ver.md`（公開 EDA）。**ローカル全列再集計は Z1（dataset DL 後）**
- [x] A2 ターゲット分布・不均衡の確認 — 証拠: 同上 · TVT 連続値 RMSE（分類不均衡なし）
- [x] A3 リーク候補の列挙と判定 — 証拠: `docs-ja/dataset.md` · `docs-ja/comp-strategy.md` Stop（train tops / 例示 test）
- [x] A4 CV 設計の根拠記録 — 証拠: `docs-ja/comp-strategy.md` · Discussion 719389/727149（well-group · leave-field）
- [x] A5 CV-LB 相関の初期確認 — 証拠: `exp/exp-infer.md`（det-mha α スイープで LB 単調寄り）· 自前 CV は CHK-010
- [x] A6 単純後処理の網羅 — 証拠: `exp/exp-infer.md` · Discussion 711878（bimodal midpoint）· FOYSAL 悪化ログ
- [-] A7 定型特徴量の一括試行 — N/A: 行単位定型 FE は本命にしない方針確定（`comp-strategy` Stop · Discussion 726751）
- [x] A8 アンサンブル前の単独検証 — 証拠: Ver2 単系統スコア表 · `docs-ja/others-notebook/README-kazeneko-v2.md`

## N/A — O: 最適化・コスト最小化型

- [-] O1 — N/A: 本コンペは精度（RMSE）主目的
- [-] O2 — N/A: 同上
- [-] O3 — N/A: 同上
- [-] O4 — N/A: 同上
- [-] O5 — N/A: 同上
- [-] O6 — N/A: 同上
- [-] O7 — N/A: 同上
- [-] O8 — N/A: 同上

## N/A — S: シミュレーション・対戦型

- [-] S1 — N/A: simulation ではない
- [-] S2 — N/A: 同上
- [-] S3 — N/A: 同上
- [-] S4 — N/A: 同上
- [-] S5 — N/A: 同上
- [-] S6 — N/A: 同上

## N/A — G: 生成・LLM型

- [-] G1 — N/A: LLM 生成提出ではない
- [-] G2 — N/A: 同上
- [-] G3 — N/A: 同上
- [-] G4 — N/A: 同上
- [-] G5 — N/A: 同上
- [-] G6 — N/A: 同上

## 必須 — R: 実行制約・効率型

- [x] R1 実行時間の実測 — 証拠: `docs-ja/discussion/error/728152-scoring-stuck-timeout.md`（×200 wells 注意）· 自前ベンチは CHK-011
- [x] R2 メモリの実測 — 証拠: 同上方針 · 自前は CHK-011
- [x] R3 依存の事前パッケージ化 — 証拠: Ver2/公開 NB は koolbox wheel · Internet OFF（`kernels-runbook` · notebook 要約）
- [-] R4 バッチ化・ベクトル化 — N/A: 現状制限内の公開パイプラインを維持。ボトルネック時に再オープン
- [x] R5 モデル・アセットサイズの確認 — 証拠: 提出 COMPLETE 複数 · `submission-rules.md`
- [x] R6 制約超過の自動検知 — 証拠: `scripts/validate-submission.ps1`

## 必須 — X: 外部成果物・運用

- [x] X1 外部成果物の実体確認 — 証拠: `exp/exp-intel.md` · `docs-ja/others-notebook/README-public-useful.md` · `README-kazeneko-v2.md`
- [x] X2 license 台帳の記録 — 証拠: `docs-ja/license-ledger.md`（T010–T021）
- [-] X3 prior-knowledge の確認記録 — N/A: knowledge ストア空（カード無し）。新規 harvest 時に再オープン
- [x] X4 Private・実行レーンの遵守確認 — 証拠: Rule `kaggle-private-assets` · `scripts/assert-kaggle-private.ps1` · checklist 実行制約
- [x] X5 作業ゴミ掃除の配線 — 証拠: `exp/work-protect.json` · `exp/artifact-routing.json`
- [x] X6 禁止台帳ゲートの配線 — 証拠: `exp/improvement-loop-failures.json` · `scripts/run-hypothesis-ban-gate.ps1`（空台帳でも PASS）

## コンペ固有の機械項目（任意）

- [x] Z1 公式 `dataset/` DL 後に A1/A2 をローカル再集計（欠損率・dtype·TVT 分布）— 証拠: `exp/work/dataset-eda-20260723.json` · `docs-ja/dataset.md`
- [x] Z2 Georgy ruler / well-GroupKFold OOF スクリプト配置 — 証拠: `my-local-eval-notebook/wave0-ruler/run_wave0_ruler.py` · `exp/work/wave0-ruler/`（CHK-010）
