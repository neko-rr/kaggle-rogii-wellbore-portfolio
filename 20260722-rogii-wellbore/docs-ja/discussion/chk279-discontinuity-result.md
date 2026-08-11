# CHK-279 結果 — oracle≪tip 断絶タイプ診断（2026-07-29）

> action: **T4** · ローカル突合（再学習なし）· **提出なし**  
> 作業: [`exp/work/wave23-ceiling-bridge/run_chk279_discontinuity_diag.py`](../../exp/work/wave23-ceiling-bridge/run_chk279_discontinuity_diag.py)  
> JSON: [`chk279-report.json`](../../exp/work/wave23-ceiling-bridge/chk279-report.json) · 井表: [`chk279-per-well.csv`](../../exp/work/wave23-ceiling-bridge/chk279-per-well.csv)  
> 入力: CHK-186 · CHK-205b · CHK-241

## 1行方針

**主因は『順位付け失敗』。** 次は **CHK-271→272/275**（選び方変更）。後工程破壊は副次（CHK-276 は後段）。

## 集計（hard20 · gap≥0.5 を断絶）

| 項目 | 値 |
|---|---:|
| 断絶井 | **18 / 20** |
| ranking_fail（±post） | **10** |
| soft_dilution（±post） | **3** |
| ranking-like 合計 | **13** |
| post_destroy 単独 | **5** |
| cascade でも soft gap≥0.5 | **15** |

## 典型井

| 型 | 例 | 所見 |
|---|---|---|
| ranking_fail | `4c2208f5` · `91db7070` | oracle シードの ll_rank 122/116 · soft≪oracle |
| soft≈oracle → FINAL悪化 | `5f4d2a52` · `86454a6f` | 選ぶ人は当たるが清書で潰す（副次） |
| soft_dilution | `7e721392` | rank 良好でも soft 平均が希釈 |

## 含意

- Wave-23 の入口分岐は **『順位付け失敗』側** → **271 を厚く**。
- tip-cv の主戦場は soft 面。FINAL だけの post 破壊は F025/276 系で別扱い。
- F027（同じ選ぶ人）は再確認: cascade でも soft gap が残る。

## Explicit Stop

- 本診断を tip-cv PASS としない（T4）
- mid-bank 代理採択禁止（F023）
- 現行 soft T0.15 を天井バンクにそのまま掛けない（F027）
