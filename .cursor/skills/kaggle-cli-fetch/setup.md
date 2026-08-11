# Kaggle CLI セットアップ（venv 前提）

> **Ops SSOT:** Skill `kaggle-cli-ops` · スクリプト `scripts/setup-kaggle-venv.ps1`

## 公式

| 項目 | URL / 内容 |
|---|---|
| **PyPI（公式パッケージ）** | https://pypi.org/project/kaggle/ |
| 依存ファイル | `requirements-kaggle-cli.txt` · `requirements-local-sim.txt`（repo ルート） |
| Profile | default **cli** · simulation は **sim** |
| Python 要件 | **3.11 以上**（PyPI 記載） |
| コマンド一覧 | `.\scripts\kaggle-cli.ps1 --help` |

Kaggle CLI は **`.env` を自動では読みません**。認証は OAuth または `kaggle.json`。

---

## 1. venv セットアップ（初回 / clone 後）

```powershell
cd <repo-root>
# CLI only (fast)
.\scripts\setup-kaggle-venv.ps1
# simulation local sim
.\scripts\setup-kaggle-venv.ps1 -Profile sim
.\scripts\check-kaggle-cli.ps1
```

中身: `python -m venv .venv` → `pip install -r requirements-kaggle-cli.txt` または `requirements-local-sim.txt`

版更新:

```powershell
.\scripts\setup-kaggle-venv.ps1 -Profile sim -Upgrade
```

**Agent は上記スクリプト経由の pip を許可。** グローバル `pip install kaggle` は禁止。

---

## 2. 認証方法（推奨順）

### A. OAuth（推奨・v2.1.1+）

```powershell
.\.venv\Scripts\kaggle.exe auth login
```

ブラウザが開くので Kaggle アカウントでログイン。API キーの手動ダウンロードは不要。

### B. `kaggle.json`（従来方式）

1. Kaggle → Settings → API → **Create New Token**
2. ダウンロードした `kaggle.json` を配置:

| OS | パス |
|---|---|
| Windows | `%USERPROFILE%\.kaggle\kaggle.json` |
| macOS/Linux | `~/.kaggle/kaggle.json` |

### C. 環境変数（CI / スクリプト向け）

CLI 認証は **`kaggle auth login`** または **`%USERPROFILE%\.kaggle\kaggle.json`** を優先。  
環境変数を使う場合は OS / Colab **Secrets** 側で設定する（値をファイルや Git に書かない）。  
Secrets 名の例: `KAGGLE_USERNAME` · `KAGGLE_KEY`（このドキュメントに値は載せない）。

---

## 3. `.env` ファイルについて

**Kaggle CLI 標準機能では `.env` は読み込まれません。**

OAuth を使えば `.env` も `kaggle.json` も不要。

任意: `KAGGLE_CLI_PATH` で exe を上書き（通常は不要 — ラッパーが `.venv` を優先）。

---

## 4. Git 除外（必須）

`.gitignore` 済み: `.venv/`, `.kaggle/`, `kaggle.json`, `.env`

**絶対にコミットしない:** API key、`kaggle.json`、`.env`

---

## 5. 動作確認

```powershell
.\scripts\check-kaggle-cli.ps1
.\scripts\kaggle-cli.ps1 competitions list -s orbit
.\scripts\kaggle-cli.ps1 competitions topics list orbit-wars
```

---

## 6. トラブルシュート

Skill `kaggle-cli-ops` · `docs-ja/cli-troubleshooting.md`

| 症状 | 対処 |
|---|---|
| kaggle がない | `setup-kaggle-venv.ps1` |
| 401 / 403 | `.\.venv\Scripts\kaggle.exe auth login` |
| topics 403 | `setup-kaggle-venv.ps1 -Upgrade` |

---

## 7. Cursor Agent

- **bootstrap 可:** `setup-kaggle-venv.ps1` · `check-kaggle-cli.ps1 -Bootstrap`
- **実行:** `.\scripts\kaggle-cli.ps1 <args>` のみ
- **禁止:** グローバル pip · 生 `kaggle`
- ルール: `.cursor/rules/kaggle-cli-venv.mdc`
