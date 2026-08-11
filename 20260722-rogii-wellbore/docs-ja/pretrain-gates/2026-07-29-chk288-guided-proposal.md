# pretrain-gate — CHK-288 innovation-guided proposal

> date: 2026-07-29  
> chk: **CHK-288** · action: T3 · lane: Kaggle GPU  
> hypothesis-ban: **PASS**（`-Force` + allowlist escalation bypass）

## Tier 0 / 1

| 項目 | 結果 |
|---|---|
| train path | OK（local + competition_sources） |
| numba PF guided | OK（warmup + 2井 smoke） |
| 出力 | `chk288-per-well.csv` / `chk288-report.json` 生成 |
| 提出 | **禁止**（hard20 screen のみ） |

## Tier 2（煙）

- 2井 smoke 完走（約7min）· crash/OOM なし
- 2井だけでは採否しない（hard20 が本判定）
- baseline tip soft 生成可能 · variant 格子実行可能

## 判定

**PASS** → Kaggle GPU `chk288-guided-proposal-gpu` 起動可

## Stop

- F026 spr 拡大なし（init_spr=4.5 固定）
- oracle-only 改善は採択しない
