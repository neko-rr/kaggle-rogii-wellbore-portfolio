# 公開コード在庫 — top 解法（2026-08-08 取得）

> Skill: `kaggle-kernel-repro`（pull）· `solution-code-summary`（要約）  
> **weights / competition data は未DL**（コードのみ）

## 保管場所（終了後であることが分かるパス）

```text
retro/archive/others-notebook/post-comp-top-20260808/   ← 終了後公開 kernel
retro/archive/solutions/code/                           ← 学習リポ clone
```

コンペ中の `others-notebook/workspaces/` には **置かない**（pointer 用 README のみ）。

## 取得成功

| Place | Team | Artifact | ローカルパス |
|---:|---|---|---|
| **1** | Ruby | Infer NB `w5833946/submit-reproduce` | `retro/archive/others-notebook/post-comp-top-20260808/rank01-ruby-w5833946-submit-reproduce/` |
| **6** | k256.dev | Infer NB `k256net/public20th-private6th-…` | `…/rank06-k256net-public20th-private6th-pf-bagging/` |
| **14** | keithtyser | GitHub train + submit script | `retro/archive/solutions/code/keithtyser-…/` · `…/rank14-keithtyser-private-14th-…/` |
| **23** | Kaggle Agent (Jiwei) | Full infer script | `…/rank23-jiweiliu-rogii-v5-run4-sr-dual-t4/` |

## 公開なし / 未取得（調査時点）

| Place | Team | 状態 |
|---:|---|---|
| 2 | Bilzard | writeup のみ · code リンクなし |
| 3 | tereka | writeup のみ · notebook 内学習記述 |
| 4 | L&J&A&A | writeup のみ |
| 5 | daimaru | writeup のみ |
| 7 | roglike | writeup のみ |
| 9 | tremors | writeup のみ |
| 6 | GitHub | 著者「later」· 当面は Kaggle NB のみ |

## 要約ファイル

| 対象 | パス |
|---|---|
| #1 Ruby | [`code-rank01-ruby.md`](code-rank01-ruby.md) |
| #6 k256 | [`code-rank06-k256.md`](code-rank06-k256.md) |
| #14 keith | [`code-rank14-keith.md`](code-rank14-keith.md) |
| #23 jiwei | [`code-rank23-jiwei.md`](code-rank23-jiwei.md) |
| 横断統合 | [`../retro/retro-solutions.md`](../../retro/retro-solutions.md) §コード公開分 |

## CLI（再取得）

```powershell
$base = "20260722-rogii-wellbore/retro/archive/others-notebook/post-comp-top-YYYYMMDD"
.\scripts\kaggle-cli.ps1 kernels pull w5833946/submit-reproduce -p "$base/rank01-ruby-w5833946-submit-reproduce" -m
.\scripts\kaggle-cli.ps1 kernels pull k256net/public20th-private6th-pf-pf-pf-pf-and-bagging -p "$base/rank06-k256net-…" -m
.\scripts\kaggle-cli.ps1 kernels pull keithtyser/private-14th-rogii-construction-a-v1-submit -p "$base/rank14-…" -m
.\scripts\kaggle-cli.ps1 kernels pull jiweiliu/rogii-v5-run4-sr-dual-t4 -p "$base/rank23-…" -m
# 学習リポは solutions/code へ
git clone --depth 1 https://github.com/keithtyser/rogii-wellbore-geology-solution
```
