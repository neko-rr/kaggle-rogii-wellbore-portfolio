---
name: kaggle-static-check
description: >-
  Agent が書いた Python/Notebook を本実験前に静的検査する。
  run-static-checks.ps1（構文・ipynb・private・ruff）。
  エディタ Ruff 拡張では代替不可。静的テスト、syntax、lint ゲート、実行前チェックで使う。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| `run-static-checks.ps1` · `check-static.py` · setup-kaggle-venv（ruff 欠時） | — | — | my-notebook/ · scripts/ · exp/work/ | exp/work/static-check-last.json |

**禁止:** FAIL のまま train · kernels push · 長 GPU · submit

# Kaggle Static Check（Agent 必須ゲート）

**詳細 SSOT:** [`_shared/STATIC-CHECKS.md`](../_shared/STATIC-CHECKS.md)

## なぜエディタ Ruff では足りないか

- Cursor の **Ruff 拡張**（Kaggle-Light プロファイルにあり）は **人が UI で見る用**
- ユーザーがコードを書かない運用では **誰も波線を見ない**
- Agent はターミナルで **`run-static-checks.ps1` が exit 0** するまで実験に進まない

## 必須手順（Agent）

1. `.py` / `.ipynb` / `kernel-metadata.json` を **書いた・直した**
2. すぐに:
   ```powershell
   # 推奨: 触ったファイルだけ
   .\scripts\run-static-checks.ps1 -Path ".\path\to\file.py" -Path ".\path\to\nb.ipynb"
   ```
3. **verdict PASS** のみ次へ（ban-gate → smoke → pretrain → 本実験）
4. **FAIL** → 修正 → 再実行。ユーザーに「回しました」と報告しない

## ruff が WARN missing のとき

```powershell
.\scripts\setup-kaggle-venv.ps1
```

`requirements-kaggle-cli.txt` に **ruff** が入っている。拡張とは別パッケージ。

## 他 Skill

| 前 | 後 |
|---|---|
| （コード編集） | **本 Skill** |
| 本 Skill PASS | `kaggle-hypothesis-ban-ledger` · shape smoke · `kaggle-pretrain-gate` |
| pretrain PASS | runbook · eval |

Subagent: **SA-8** `/kaggle-static-check`（範囲広いとき）
