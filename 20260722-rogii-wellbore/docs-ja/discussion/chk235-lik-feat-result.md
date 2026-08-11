# CHK-235 結果 — weight以外の尤度特徴

> date: 2026-07-28 · local mid-bank · **提出なし** · ≠F022 · F023遵守（GPU未実施）

## 判定

**NO-GO**

| face | Δ vs T0.15 |
|---|---:|
| contact_ramp α1（最良） | **−0.242** |
| contact_hold α1 | −0.288 |
| egfdl_gr α1 | −0.392 |
| early_gr / smooth / 複合 | −0.5〜−1.36 |

接触連続・先頭GR・EGFDL近傍GR・平滑の後段 lik 加算はいずれも tip soft を悪化。

## 含意

- 現行 PF lik（全区間 GR）への **後段特徴加算**は閉じる。
- tip-cv GPU は mid 全敗のため起動しない（F023）。

出典: `chk235-lik-feat-report.json`
