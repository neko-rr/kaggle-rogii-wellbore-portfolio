# CHK-212 結果 — Best tip + LIK_TEMP=0.5 E2E smoke

> date: 2026-07-26 · GPU · **提出なし**  
> kernel: [tip-gated-lik-temp-0p5](https://www.kaggle.com/code/kazeneko77/tip-gated-lik-temp-0p5) Ver1 COMPLETE  
> 数値: [`chk212-score.json`](../../exp/work/wave20-upstream/chk212-score.json)  
> tip-cv 根拠: [`chk205`](chk205-lik-temp-result.md)

## 1 行

**本番 Best tip に T=0.5 を載せた E2E は COMPLETE（smoke GO）。**  
`submission.csv` は Best SUB-9 と **別物**（約 30% 行が変化 · mean|Δ|≈1.22）。**提出は未実施**。

## 確認

| 項目 | 結果 |
|---|---|
| LIK_TEMP ログ | `LIK_TEMP= 0.5` 出力あり |
| 行数 | 14151 · 列 `id,tvt` |
| vs Best SUB-9 | maxabs 4.0 · frac_diff **0.304** |
| gated soft | `00bbac68` / `00e12e8b` applied · `000d7d20` skip |
| Error/Traceback | なし |

## 判定

| 仮説 | 判定 |
|---|---|
| Best tip+T0.5 が E2E 完走 | **GO（smoke）** |
| Public 提出 | **済 SUB-13** · ref **55001828** PENDING · 重複 55001822 |

## 次

- Public 確定待ち（数時間のことあり）  
- 上流命中の tip 面検証は [`chk214`](chk214) / spr12 tip-cv
