# exp/ — 実験記録レイアウト

> Skill: `experiment-management` · `experiment-result-management`  
> **Agent は `exp-index.md` → `latest/manifest.md` の順で読む。**  
> コード成果物の索引は [`../lifecycle-manifest.md`](../lifecycle-manifest.md)（別系統）。

## 必須 SSOT（root のみ）

| ファイル | 役割 |
|---|---|
| `exp-index.md` | 現在地 · Best · 次アクション |
| `exp-train.md` | 学習 · CV |
| `exp-infer.md` | 提出 · LB · Validation |
| `exp-intel.md` | 他者 · Discussion |
| `hyperparameter-table.md` | 実験 ID 表 |
| `experiment-checklist.md` | CHK ループ |
| `run-ledger.md` | GPU / コスト 1 run 1 行 |
| `artifact-routing.json` | root に散乱する固有生成物の pattern → `work/` 移動先 |
| `work-protect.json` | cleanup から守る Best / 保険成果物 |

**root に分析 MD を増やさない。** 日次分析は `work/` · 確定版は `latest/`。

## サブフォルダ

| パス | 用途 |
|---|---|
| `protocol/` | ローカル検証 SSOT |
| `latest/` | **最新・有効**な分析 + `manifest.md` |
| `work/YYYY-MM-DD/` | 当日 WIP |
| `work/profiles/<tool>/<date>/` | profiler の一時 raw 出力 |
| `archive/history/` | 置き換え済み過去分析 |
| `archive/superseded/` | reject 確定（再提出判断に使わない） |
| `replay/` | episode JSON のみ |
| `local-eval/` | protocol 実行 JSON · スクリプト出力 |

## 昇格ルール

1. 日次メモ → `work/YYYY-MM-DD/`
2. 判断確定 → `latest/` · `latest/manifest.md` 更新 · 旧版 → `archive/history/`
3. 方法論 reject → `archive/superseded/`

## 再レイアウト（既存 comp の移行時のみ）

```powershell
.\scripts\reorganize-exp-layout.ps1 -WhatIf
.\scripts\update-exp-path-references.ps1 -WhatIf
```
