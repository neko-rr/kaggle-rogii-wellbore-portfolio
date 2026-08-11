# Competition dependencies — local Agent vs Kaggle vs Colab

> **目的:** 「numpy が入っていない」を手動ワンショット pip で塞がない。  
> **コンペごとに買い物リストを持ち、同じ `.venv` に再現インストールする。**

| ファイル | 役割 |
|---|---|
| リポ `requirements-kaggle-cli.txt` | 全コンペ CLI（kaggle · ruff） |
| リポ `requirements-local-sim.txt` | simulation 汎用 |
| **`<comp>/requirements-local.txt`** | **当該コンペのローカル計算依存**（numpy 等） |
| 雛形 | `comp/requirements-local.txt.template` |

スクリプト:

| 命令 | 内容 |
|---|---|
| `setup-kaggle-venv.ps1` | CLI（± sim）のみ |
| **`setup-comp-venv.ps1 -CompRoot …`** | CLI + **requirements-local.txt** + import smoke |
| `check-comp-imports.py` | リストの import 確認 |

---

## 1. 3 つの箱（混ぜない）

| 環境 | 依存の入れ方 |
|---|---|
| **PC · Agent** | `.venv` + `setup-comp-venv.ps1` |
| **Colab** | ノート先頭 `%pip install -q -r requirements-local.txt`（Drive 上のパス） |
| **Kaggle Notebook** | プリインが多い。足りない分だけ `%pip` し **リストにも書く** |

CLI 用 venv に巨大な torch を常時載せない。重いスタックは **requirements-local で必要なときだけ** uncomment。

---

## 2. Agent 規則（ImportError 時）

1. 失敗したパッケージを **`<comp>/requirements-local.txt` に追記**（先にリスト）  
2. インストール:
   ```powershell
   .\scripts\setup-comp-venv.ps1 -CompRoot ".\20260101-slug"
   # またはリスト更新後のみ:
   .\.venv\Scripts\pip.exe install -r ".\20260101-slug\requirements-local.txt"
   ```
3. `check-comp-imports` または setup の smoke が PASS してから再実行  
4. **禁止:**
   - グローバル `pip install`
   - リスト未更新のワンショット `pip install numpy`
   - `.venv` を Git にコミット

---

## 3. Day0

1. テンプレから `requirements-local.txt` を配置（`new-kaggle-comp` で自動）  
2. `comp-type` に合わせて不要行を消し、必要なスタックを uncomment  
3. **ファイルは ASCII または UTF-8 BOM**（Windows の pip は BOM 無し UTF-8 日本語を cp932 で落ちることがある）  
4. `.\scripts\setup-comp-venv.ps1 -CompRoot <inner>`  
5. 本実験前は static-check と併用  

---

## 4. フロー

```text
setup-kaggle-venv (cli)     # 初回 PC
  → setup-comp-venv         # コンペごと / ImportError 後
  → run-static-checks -Path …
  → ban / smoke / pretrain
  → 本実験
```

---

## 5. 関連

- Rule `kaggle-cli-venv` · `kaggle-comp-dependencies`
- Skill `kaggle-comp-deps` · `kaggle-cli-ops` · `kaggle-static-check`
- 地図 `_shared/DECISION-FLOW.md`
