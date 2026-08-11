# コンペ開始チェックリスト — rogii-wellbore

> comp-slug: **rogii-wellbore** · Kaggle slug: **rogii-wellbore-geology-prediction** · 締切: **2026-08-05**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction  
> 完了したら `[x]` にする。Agent は未完了項目をユーザーに報告する。

---

## Day 0 — リポジトリ生成

- [x] `new-kaggle-comp.ps1` 実行（`-Name` 衝突なし · **Cursor infra 自動インストール**）
- [x] **`init-comp-layout.ps1`** 実行（本チェックリスト · folder-map · exp 4 層 · lifecycle）
- [x] **`install-cursor-infra.ps1`** → `test-cursor-hooks.ps1` **PASS**（`new-kaggle-comp` 未実行時の手動）
- [ ] **Cursor: Developer → Reload Window**（hooks 反映）
- [ ] `Kaggle-Light` Profile で `open-kaggle-light.ps1` 起動
- [ ] `-InitGit` または `git init` + `install-git-hooks.ps1`

## Day 0 — コンペ理解（SSOT 初版）

- [ ] `AGENTS.md` — comp-type · submission-profile · 締切
- [ ] Skill **`kaggle-comp-router`** → `docs-ja/comp-profile.md` 確定
- [ ] `docs-ja/comp-timeline.md`（Skill `kaggle-comp-timeline`）
- [ ] `docs-ja/conditions.md`（Skill `competition-conditions`）
- [ ] `docs-ja/comp-strategy.md` — Goal / Stop 骨格
- [ ] **戦略前ゲート:** `exp/pre-strategy-gate.md` の型節を確定し、`check-pre-strategy-gate.ps1` **PASS まで戦略CHK禁止**（Skill `kaggle-pre-strategy-gate`）
- [ ] 3 段ゲート初版: `pretrain-acceptance.md` · `kernels-runbook.md` · `submission-rules.md`（`scripts/templates/submission-rules.md.template` · **Notebook 紐づけ:** `_shared/NOTEBOOK-LINKED-SUBMIT.md`）
- [ ] `license-ledger.md` 空 BOM（Tier R）
- [x] **Private 必須:** Rule `.cursor/rules/kaggle-private-assets.mdc` · `scripts/assert-kaggle-private.ps1` · 自作資産は常に Private · `datasets create --public` 禁止
- [ ] **実行レーン方針:** ユーザー許可 + 対象ジョブ指示の両方が必要 · Kaggle CPU最大5枠 / GPU最大2枠 · 未指示ジョブで空きを埋めない
- [ ] **CLI 書込手順:** preflight → metadata/path → Private assert → wrapper。`kernels push` は `-p` 明示

## Day 0 — データ

- [x] `dataset/README.md` に DL 手順を記載
- [x] データを `dataset/` に配置済み（ROGII 復旧移行 · train 773 / test 3 · zip 同梱）
- [ ] `docs-ja/dataset.md`（Skill `dataset-summary`）

## Day 0 — comp-type 別

### simulation（`comp-type: simulation`）

- [ ] `sim-track/` 初期化済み（`init-comp-layout.ps1 -CompType simulation`）
- [ ] `setup-kaggle-venv.ps1 -Profile sim`
- [ ] Colab 接続確認: Skill **`cursor-colab-runtime`**（Select Kernel → Colab）
- [ ] サンプル bot を `my-notebook/starter-baseline/` に配置 · **`lifecycle-manifest.md` を wip で登録**
- [ ] `docs-ja/agent-debug.md` が active なら Error 解析手順を確認

### tabular / notebook-output

- [ ] `sim-track/` **作らない**
- [ ] Colab 長時間: Skill **`cursor-colab-runtime`** · `docs-ja/colab-cursor-runbook.md`
- [ ] ローカル eval 方針: `exp/protocol/` または `metric-repro.md`
- [ ] 他者 NB 方針: `notebook-analysis` · 必要時 `kaggle-kernel-repro`

---

## 運用中 — 毎回 Agent が守ること

| イベント | 必須 |
|---|---|
| 自作 Kernel / Dataset / Model push | **Private assert PASS** · `is_private` / `isPrivate: true` |
| Kaggle CPU / GPU / Colab | **ユーザー許可 + 対象ジョブ指示後のみ** · CPU最大5枠 / GPU最大2枠 · 未指示ジョブで空きを埋めない |
| bot / ipynb 編集開始 | `my-notebook/` · manifest `wip` |
| Kaggle/Colab 実行後 | → `my-ran-notebook/` · manifest `ran` · run-log |
| local-eval fork | → **`my-local-eval-notebook/` のみ** · manifest `local-eval` |
| 他者 NB fork（材料） | → **`my-notebook/`** · intel 索引 · manifest `wip`（**checklist には仮説のみ**） |
| 提出 PASS | → `my-submitted-notebook/` · manifest `submitted` · **Notebook 紐づけ提出**（UI または CLI `-k` / `-v`） |
| LB / 公開 NB 記録 | `sim-track/` append（simulation） |
| replay 取得 | `exp/replay/{用途}/` |
| 分析確定 | `exp/latest/` + `exp/latest/manifest.md` |

---

## 参照

| ドキュメント | 用途 |
|---|---|
| [`folder-map.md`](folder-map.md) | 置き場所 SSOT |
| [`../lifecycle-manifest.md`](../lifecycle-manifest.md) | コード成果物索引 |
| [`../exp/README.md`](../exp/README.md) | 分析 MD レイアウト |
| `.cursor/skills/_shared/ARTIFACT-LIFECYCLE.md` | 状態遷移 |

---

## 完了確認（Agent）

開始セットアップ完了時、以下が存在すること:

- [ ] `lifecycle-manifest.md`
- [ ] `docs-ja/folder-map.md`
- [ ] 本ファイル（comp-start-checklist.md）
- [ ] `exp/README.md` · `exp/latest/manifest.md`
- [ ] 各 `my-*-notebook/README.md`
- [ ] simulation なら `sim-track/sim-track-index.md`
