# CHK-404 — 生Pearson門番見直しの文書判定

> verdict: **caveat更新 = NO（現状維持）** · Soft-Preserve再開 = **NO（F041維持）**  
> date: 2026-07-31

## 問い

| 問い | 判定 | 理由 |
|---|---|---|
| 誤差Pearsonを門番に採用するか | **記録必須・閾値自動PASSはしない** | 395で有用だが、単独PASS条件にすると別面を誤採択しやすい |
| 生Pearson単独NO-GOは是か | **否**（caveatどおり） | 共通トレンドで ≈1 になりうる |
| CHK-392を自動PASSにするか | **NO** | 402Aで tip負け + F015 が後続確定 |
| Soft-Preserve再学習を再開するか | **NO** | F041 · 402Aで提出価値なし |
| `gate-pearson-caveat.md` を大きく書き換えるか | **NO** | 現行で十分 · 402A/403を参照追記のみ可 |

## 推奨運用（確定）

1. 生Pearson ≥ 0.99 のとき **切捨て前に** 誤差Pearson・井中心化・RMSE・井別を記録（caveat）
2. Soft-Preserve / soft提出は別問題（F041 / F015）— 門番見直し ≠ 再開許可
3. 402A以降の別面候補は **tip RMSE を主物差し**、相関は補助

## 参照

- [`gate-pearson-caveat.md`](../gate-pearson-caveat.md)
- [`chk403-gate-reconcile-2026-07-31.md`](chk403-gate-reconcile-2026-07-31.md)
- [`chk402a-compare.md`](../../exp/work/wave30-soft-preserve/chk402a-compare.md)
