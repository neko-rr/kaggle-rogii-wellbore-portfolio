# CHK-237 結果 — 尤度ランクの seed-oracle 向け校正（非リーク）

> date: 2026-07-28 · local mid-bank · **提出なし** · ≠F022 weight

## 判定

**NO-GO**（GPU tip-cv へ進めない）

| face | Δ vs T0.15 | 備考 |
|---|---:|---|
| leak α=2（上限・y混入） | **+1.66** | 採択不可 · ポテンシャルのみ |
| LOWO linear lik | +0.07 | 非リーク |
| LOWO ridge（lik+軌跡特徴） | **+0.016** | 非リーク最良 |

## 含意

- **選択誤りは実在**（リーク上限が大きい）が、井横断で移せる代理特徴が弱い。
- スカラー weight（F022）以外の単純校正では tip 面 +0.15 に届かない → 本波閉じる。
- 将来: 井内オンライン校正や接触モデル（239）側へ。

出典: `chk237-lik-calib-report.json` · `chk237b-lik-calib-report.json`
