# CHK-239 結果 — 216型 / 1b1eba53

> date: 2026-07-28 · **提出なし**

## T4 診断

heel GR は健全（corr≈0.83）。**候補不足**（oracle≈41.7）と遠区間悪化が主因。  
「heel 観測モデル直し」単独は期待薄。

## 井内 screen（239b）

| spec | oracle | s5@T0.15 |
|---|---:|---:|
| baseline | 41.70 | 45.20 |
| **stretch 1.15** | **10.69** | **15.33** |
| ls_offset +30/+45 | ≈14.8 | ≈23–25 |

## hard20 展開

| 方式 | Δ tip soft | Δ oracle | 判定 |
|---|---:|---:|---|
| 混在 1.0+1.15 | **−5.13** | +2.81 | tip悪化（P2） |
| maxlik で stretch 選択 | **−4.79** | −0.85 | NO-GO · A井を巻き込み |

## 判定

**NO-GO（tip-cv 採択不可）** · 知見は残す。

- 1b1eba53 単体では TW stretch が効く
- 自己教師（maxlik）ゲートは誤発火が多く、全体 tip を壊す
- 安全な井ゲートが見つかるまで tip CFG に載せない

出典: `chk239-obs-break-report.json` · `chk239b-1b1eba53-report.json` · `chk239c/d-*.json`
