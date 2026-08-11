---
name: kaggle-cli-ops
description: >-
  Kaggle CLI の venv セットアップ・preflight・認証・トラブルシュート。
  setup-kaggle-venv、check-kaggle-cli、kaggle-cli ラッパー、venv、pip install kaggle、
  OAuth、kaggle auth login、CLI が見つからない、401/403 と言ったときに使う。
  読み取り fetch は kaggle-cli-fetch に任せる。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| setup-kaggle-venv.ps1 · setup-comp-venv.ps1 · check-kaggle-cli.ps1 · kaggle-cli.ps1 | Kaggle HTTPS · PyPI（setup 時） | 読取のみ。token/.env をログ·Git 禁止 | repo · requirements-*.txt · requirements-local.txt | .venv/（setup 経由のみ） |

**要ユーザー明示 OK:** Kaggle 書込操作（`kernels push` · Dataset/Model create/version）。許可に加えて対象ジョブの実行指示が必要

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle CLI Ops

**venv 内 CLI の作成・確認・修復。** Discussion 取得は Skill `kaggle-cli-fetch`。

## 役割分担

| Skill | 担当 |
|---|---|
| **本 Skill** | `.venv` bootstrap、preflight、認証案内、障害切り分け · **DL 前チェック表** |
| `kaggle-comp-deps` | **コンペ計算依存**（`requirements-local.txt` · `setup-comp-venv`） |
| `kaggle-cli-fetch` | 読み取り CLI（topics / submissions / replay） |
| `kaggle-submission-validator` | 提出前 L0–L2 |
| `discussion-summary` | Discussion 要約 |

## 前提（SSOT）

| 項目 | 値 |
|---|---|
| Python | **3.11+**（kaggle PyPI 要件） |
| venv | リポジトリ `.venv/` |
| 依存 | `requirements-kaggle-cli.txt` · `requirements-local-sim.txt`（sim）· **`<comp>/requirements-local.txt`**（計算） |
| Profile | **cli**（default）= CLI のみ · **sim** = CLI + `kaggle-environments` |
| 実行 | **`.\scripts\kaggle-cli.ps1`** のみ |
| ルール | `.cursor/rules/kaggle-cli-venv.mdc` · `kaggle-comp-dependencies` |

**初回 install（cli）** は軽量（数十秒）。**sim** は数分。**numpy/pandas は cli に含まれない** — ローカル計算は `setup-comp-venv`。

## 初回 / 新 PC / 新コンペ clone 後

```powershell
cd <repo-root>
# CLI のみ（Discussion / 提出履歴）
.\scripts\setup-kaggle-venv.ps1
# ローカル計算（numpy 等）— 内で CLI も揃う
.\scripts\setup-comp-venv.ps1 -CompRoot ".\YYYYMMDD-slug"
# simulation コンペ — ローカル sim も使うとき（先に CLI）
.\scripts\setup-kaggle-venv.ps1 -Profile sim
.\scripts\check-kaggle-cli.ps1
.\.venv\Scripts\kaggle.exe auth login    # 初回のみ（対話）
.\scripts\kaggle-cli.ps1 --version
```

**新コンペごとに venv 再作成は不要。** clone 先で setup 1 回 + コンペごとの `setup-comp-venv`。

## セッション開始（毎回）

```powershell
.\scripts\check-kaggle-cli.ps1
```

venv 欠如時は Agent が bootstrap 可:

```powershell
.\scripts\check-kaggle-cli.ps1 -Bootstrap
```

## Agent 許可される pip

| 操作 | コマンド |
|---|---|
| CLI のみ（default） | `.\scripts\setup-kaggle-venv.ps1` |
| simulation ローカル sim | `.\scripts\setup-kaggle-venv.ps1 -Profile sim` |
| コンペ計算依存 | `.\scripts\setup-comp-venv.ps1 -CompRoot ".\YYYYMMDD-slug"` |
| リスト更新後のみ | `.\.venv\Scripts\pip.exe install -r ".\YYYYMMDD-slug\requirements-local.txt"` |
| 版更新 | setup に `-Upgrade` |

**禁止:** グローバル `pip install` · リスト未更新のワンショット · 生の `kaggle ...`

## 書込 CLI の固定手順（ミス防止）

`kernels push`、Dataset / Model の create・version は、次を **順番どおり**実施する。1つでも FAIL なら書き込まない。

1. チャットに **ユーザー許可 + 対象ジョブの実行指示**がある
2. `.\scripts\check-kaggle-cli.ps1` が PASS
3. 対象フォルダを明示し、metadata の `id` / `title` / `code_file`（該当時）と実ファイルを確認
4. `.\scripts\assert-kaggle-private.ps1 -KernelDir <dir>`（または `-DatasetDir` / `-ModelDir`）が PASS
5. 実行直前に **操作・slug・ローカルパス・CPU/GPU・Private** を1行で再確認
6. **`.\scripts\kaggle-cli.ps1 ...` のみ**を実行（生の `kaggle` 禁止）
7. push 後は `kernels status` で対象 slug と Version を確認。COMPLETE 後に `kernels output` で実体を検証

**並列起動:** Kaggle は CPU 最大5枠・GPU 最大2枠。指示済みジョブだけを上限内で並列化する。CLI push は対象取り違え防止のため **1件ずつ preflight → push → slug/version確認**し、その後の実行待ちは並列でよい。

**禁止:** パス省略 push · metadata 未確認 · private assert 省略 · 他者 slug への書込 · 未指示ジョブの起動 · `competitions submit`（Agent は実行しない）

## 認証

Kaggle CLI は **`.env` を自動読まない。**

| 方式 | 手順 |
|---|---|
| **OAuth（推奨）** | `.\.venv\Scripts\kaggle.exe auth login` |
| `kaggle.json` | `%USERPROFILE%\.kaggle\kaggle.json` |
| 環境変数 | `KAGGLE_USERNAME` / `KAGGLE_KEY`（CI 向け） |

詳細: [kaggle-cli-fetch/setup.md](../kaggle-cli-fetch/setup.md)

## トラブルシュート

| 症状 | 原因 | 対処 |
|---|---|---|
| kaggle が見つからない | `.venv` 未作成 | `setup-kaggle-venv.ps1` |
| ImportError numpy 等 | 計算依存未入 | `setup-comp-venv.ps1 -CompRoot …`（リスト先） |
| preflight FAIL | venv 破損 | `.venv` 削除 → `setup-kaggle-venv.ps1` |
| 401 / 403 | 未認証・期限切れ | `kaggle auth login`（venv 内） |
| topics 403 | CLI < 2.2 | `setup-kaggle-venv.ps1 -Upgrade` |
| 並列 replay で path キャッシュ競合 | `.cache/kaggle-cli-path.txt` 同時書込 | replay DL は直列化 |
| exit `4294967295` | PS ラッパー異常 | コマンド再実行 · 直列化 |
| グローバル kaggle と venv の混在 | PATH 優先順 | ラッパー経由のみ（venv 優先） |

### 提出（`kernels push` / `competitions submit`）でよく詰まる（必読）

| 症状 | 原因 | 対処 |
|---|---|---|
| `'cp932' codec can't ...` で push クラッシュ | 日本語 Windows の Python 既定 cp932 | 修正版ラッパーが `PYTHONUTF8=1` を自動設定。旧環境は手動で `$env:PYTHONUTF8="1"; $env:PYTHONIOENCODING="utf-8"` |
| `-p`/`-v` が「無効なパラメータ」/ `Metadata file not found` | PowerShell が `-p`/`-v` を共通パラメータに部分マッチ | 修正版ラッパーは `$args` 素通しで解消（`--%` 不要）。旧版は `kaggle-cli.ps1 --% kernels push -p <dir>` |
| `kernel title does not resolve to the specified id` → 別 slug が生成 | metadata `id` と title 不一致（初回は title から slug 決定） | 既存 kernel 更新は **id/title を変えない**。SSOT「push 前チェック 1」 |
| `Notebook not found` | `code_file` と実 ipynb 名不一致 | push フォルダに `code_file` と**同名**の ipynb を置く。SSOT「push 前チェック 2」 |
| 新規 slug push で `403 Forbidden` | 他者 slug / 新規作成の権限 | **既存の自 fork を更新**して Version を作る（新規 slug を避ける） |
| 提出 zip が 871B 等で 0 点 | `kernels files` の size 表示クセを鵜呑み | **`kernels output -p <dir>`** で実体 DL → `Length`/`sha256` 検証してから提出 |

詳細手順: **`_shared/NOTEBOOK-LINKED-SUBMIT.md`**「push 前チェックリスト」「push 後チェック」  
詳細表: `<comp-root>/docs-ja/cli-troubleshooting.md`

## ダウンロード前チェック（Agent 必須）

> **前提:** `competitions download` · `datasets download` · `kernels pull -DownloadInputs` は **ユーザー明示 OK 後のみ**（`.cursor/rules/kaggle-cli-venv.mdc` · Skill `kaggle-cli-fetch`）。  
> 以下は **OK を得たあと・コマンド実行前** に必ず行う。FAIL なら **DL しない**。

| # | チェック | 手順 | FAIL 時（止める） |
|---|---|---|---|
| 1 | **ユーザー OK** | チャットで dataset / kernel input / 一括 DL の指示あり | OK なし → **実行禁止** |
| 2 | **容量見積もり** | Web で comp data / dataset のおおよそのサイズを確認。不明なら **≥5 GB 余裕** を仮定 | 空き < 見積 × 1.5 → ユーザーに報告し **中止** |
| 3 | **書込先** | `<comp-root>/dataset/` または `others-notebook/workspaces/`。**repo ルート・`.venv/` へ DL 禁止** | パス誤り → 修正するまで **中止** |
| 4 | **部分 workspace** | kernel 再現: 同名 `workspaces/<owner>-<slug>/` が既にある → `kernel-metadata.json` · `src/` の有無を確認 | 前回 pull 途中・壊れ → **削除または別 slug へ移してから** 再 DL（上書き混在禁止） |
| 5 | **archive / 展開** | tar/zip 後: サイズ 0 · 展開エラー · 必須ファイル欠落 | **部分ファイルを残さない**（壊れた tree を削除）→ ユーザーに報告。**自動 retry 禁止** |
| 6 | **disk 空き（任意・推奨）** | `Get-PSDrive -PSProvider FileSystem` で書込ドライブの Free を確認 | Free GB < 見積 → **中止** |

**容量見積もり早見（Orbit Wars / simulation）**

| 操作 | 典型サイズ | 備考 |
|---|---|---|
| Discussion / submissions / replay JSON | MB 級 | `kaggle-cli-fetch` — 通常 OK |
| `competitions download`（tabular） | 100 MB〜数 GB | comp による。Starter kit 手動 DL が SSOT のコンペも多い |
| `setup-kernel-workspace -DownloadInputs` | kernel + input 合算 | Skill `kaggle-kernel-repro` Phase 2 のみ |

**Agent 規則（DL）**

1. チェック表で **1 行でも FAIL** → `kaggle-cli.ps1` で download 系を **実行しない**
2. archive 失敗・ネット中断 → 壊れた出力を消して止まる。**ユーザーに「再 DL しますか？」と聞く**（独断 retry 禁止）
3. simulation コンペで **comp data 不要**なら `competitions download` 自体を提案しない

## 再現性

- 依存は **`requirements-kaggle-cli.txt`** / **`requirements-local-sim.txt`** / **`<comp>/requirements-local.txt`**
- 完全 pin: `pip freeze > requirements-local-sim.lock.txt`（Git 任意 · sim profile 後）
- LB 提出スコアの再現性は venv ではなく **提出コード + Kaggle 評価環境**

## 関連

- コンペ計算依存: Skill **`kaggle-comp-deps`** · `_shared/COMP-DEPENDENCIES.md`
- チートシート: `<comp-root>/docs-ja/cli-cheatsheet.md`
- 公式: https://pypi.org/project/kaggle/
