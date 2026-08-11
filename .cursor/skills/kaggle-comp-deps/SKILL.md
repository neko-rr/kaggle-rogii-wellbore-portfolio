---
name: kaggle-comp-deps
description: >-
  コンペごとの requirements-local.txt と setup-comp-venv。
  ImportError・numpy が無い・ローカル依存・pip で入れる手順。
  setup-comp-venv、コンペ依存、ModuleNotFoundError と言ったときに使う。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| setup-comp-venv.ps1 · setup-kaggle-venv.ps1 · `.venv\Scripts\pip.exe install -r` | PyPI HTTPS | — | requirements-local.txt | requirements-local.txt · .venv/ |

**禁止:** グローバル pip · リスト無しのワンショット install · submit

# Competition Dependencies

**SSOT:** [`_shared/COMP-DEPENDENCIES.md`](../_shared/COMP-DEPENDENCIES.md)  
**Rule:** `kaggle-comp-dependencies` · `kaggle-cli-venv`

## いつ使う

| 状況 | 操作 |
|---|---|
| Day0 · 新 PC · clone 後 | `setup-comp-venv.ps1 -CompRoot <inner>` |
| ImportError | リスト追記 → setup-comp-venv 再実行 |
| CLI だけ | `setup-kaggle-venv.ps1`（計算依存は入らない） |

## コマンド

```powershell
# 推奨（CLI + コンペ依存 + import smoke）
.\scripts\setup-comp-venv.ps1 -CompRoot ".\20260101-my-comp"

# smoke だけ
.\.venv\Scripts\python.exe .\scripts\check-comp-imports.py `
  --requirements ".\20260101-my-comp\requirements-local.txt"
```

## Agent の ImportError ループ

1. エラーのモジュール名 → PyPI 名を `requirements-local.txt` に 1 行追加  
2. `setup-comp-venv.ps1 -CompRoot …`  
3. 失敗したセル / 脚本を再実行  
4. 実験記録に「依存追加: …」を 1 行（任意）

## 関連

- `kaggle-cli-ops` · `kaggle-static-check` · `kaggle-pretrain-gate`
