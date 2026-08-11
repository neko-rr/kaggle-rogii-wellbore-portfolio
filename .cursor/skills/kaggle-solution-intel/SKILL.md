---
name: kaggle-solution-intel
description: >-
  コンペ中・終了後の上位解法 intel を半自動収集。LB top-N、Solution 系 Discussion、
  任意で formal writeup URL。fetch-solution-intel、solution writeup、上位解法、
  exp-intel 更新、NVIDIA writeups 相当と言ったときに使う。
  深い分析は solution-analysis / discussion-summary に任せる。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| fetch-solution-intel.ps1 · kaggle-cli.ps1 | Kaggle HTTPS | 読取のみ。KAGGLE_API_TOKEN 任意（post-comp）— ログ禁止 | comp-root · exp/ | intel/solution-writeups/ · docs-en/solution-intel/ |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle Solution Intel

**収集専用** — LB + Solution 系 Discussion を manifest にまとめる。要約・勝因分析は別 Skill。

参考: [NVIDIA/nvidia-kaggle writeups workflow](https://github.com/NVIDIA/nvidia-kaggle/blob/main/skills/nvidia-kaggle-skill/writeups.md)  
自チームは **OAuth（.venv KaggleApi）** を主路線。`KAGGLE_API_TOKEN` は formal writeup URL 用の **任意** 経路。

## 役割分担

| Skill | 担当 |
|---|---|
| **本 Skill** | 収集 · manifest · summary · 原文保存 |
| `kaggle-cli-fetch` | 個別 Discussion CLI 取得（任意） |
| `discussion-summary` | 1 トピックの日本語要約 |
| `solution-analysis` | **終了後** 深い解法分析 · 実験案 |
| `leaderboard-analysis` | **終了後** LB 総括 |
| `experiment-result-management` | `exp/exp-intel.md` 更新 |
| `kaggle-simulation-tracker` | 公開 notebook catalog（別系統） |

## コンペ中 vs 終了後

| フェーズ | 何が取れる？ | 本 Skill の設定 |
|---|---|---|
| **コンペ中** | LB 順位 · Solution **Discussion**（"Top 100 solution" 等） | `--Phase during-comp`（default） |
| **終了後** | 上記 + 正式 **/writeups/** URL（コンペによる） | `--Phase post-comp` + 任意 `KAGGLE_API_TOKEN` |

**simulation コンペ**（Orbit Wars 等）では、上位解法の多くが **Discussion スレッド** として出る。tabular ほど formal writeup が並ばない。

## 前提

- `.\scripts\setup-kaggle-venv.ps1`（**cli** profile で可 — 収集は KaggleApi のみ）
- `.\scripts\check-kaggle-cli.ps1` OK
- `<comp-root>/intel/solution-writeups/`（bootstrap で作成）

## 実行

```powershell
cd <repo-root>
.\scripts\fetch-solution-intel.ps1 -Competition <slug> -TopN 10
# 本文も保存（docs-en/solution-intel/）
.\scripts\fetch-solution-intel.ps1 -Competition <slug> -FetchBodies
# 終了後 — formal writeup URL も試す（KAGGLE_API_TOKEN 設定時）
.\scripts\fetch-solution-intel.ps1 -Competition <slug> -Phase post-comp -TopN 5
```

Python 直実行:

```powershell
.\.venv\Scripts\python.exe .\scripts\fetch-solution-intel.py orbit-wars --fetch-bodies
```

## 出力

`<comp-root>/intel/solution-writeups/`:

| ファイル | 内容 |
|---|---|
| `manifest.json` | LB top-N · solution_topics · formal_writeups |
| `summary.md` | 人間向け索引（リンク付き） |

`--fetch-bodies` 時:

| ファイル | 内容 |
|---|---|
| `<comp-root>/docs-en/solution-intel/topic-*.md` | Discussion 原文 |

## 収集後（Agent）

1. `exp/exp-intel.md` に **事実のみ** 追記（解釈は別段落）
2. 重要トピック → Skill `discussion-summary`
3. コンペ終了後 → Skill `solution-analysis` / `leaderboard-analysis`
4. simulation: `sim-track/` の catalog と **混同しない**（notebook peak ≠ writeup）

## トラブルシュート

| 症状 | 対処 |
|---|---|
| OAuth 401 | `.\.venv\Scripts\kaggle.exe auth login` |
| solution_topics が 0 | キーワード未該当 — Host スレッドを手動で `kaggle-cli-fetch` |
| formal_writeups 空 | 正常（sim / 進行中）— Discussion 側を使う |
| formal_writeups 空（終了後） | 任意: `KAGGLE_API_TOKEN` 設定して `-Phase post-comp` |

## 関連

- 公式 CLI: https://pypi.org/project/kaggle/#description
- `kaggle-cli-ops` — venv · preflight
