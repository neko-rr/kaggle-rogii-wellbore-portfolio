# 別面門番の注意 — 生Pearsonだけでは切らない（CHK-395）

> updated: 2026-07-30  
> source: [`chk395-gate-audit.md`](../exp/work/wave30-soft-preserve/chk395-gate-audit.md)  
> 適用: Final2候補・別面門番・「tipと高相関だからNO-GO」判定全般

---

## 1行

**tip FINAL との行単位生Pearson ≈ 0.999 は、共通の大きな TVT トレンドでも起きうる。単独の別面NO-GO根拠にしない。**

---

## なぜ起きるか（初学者向け）

TVT予測は坑井に沿って大きく上下する。2つの予測が同じ大局トレンドを持つと、局所の補正が大きくても生Pearsonはほぼ1になる。

```text
tip      1000 → 1100 → 1200
新予測   1015 → 1118 → 1320   ← 補正ありでも Pearson は高く出やすい
```

CHK-395 実測（Soft-Preserve vs tip FINAL）:

| 指標 | 値 |
|---|---:|
| 生Pearson | 0.9995 |
| 誤差Pearson | **0.689** |
| 井中心化Pearson | **0.895** |
| tip→new RMSE | 29.88 → 17.35（20/20井改善） |

---

## 必須チェック（別面 / Final2 門番）

生Pearson ≥ 0.99 で切り捨てる前に、**同じ予測ペア**で次を記録する:

| # | 指標 | 目安 |
|---|---|---|
| 1 | **誤差Pearson** `(pred−y)` vs tip | ≪ 生Pearson（例: ≤ 生−0.05）なら「失敗同型」ではない疑い |
| 2 | **井中心化Pearson** | 井平均除去後も見る |
| 3 | **RMSE vs tip / CF** | tipより良いのに生Pearsonだけで切らない |
| 4 | **井別 mean(pred−tip)** | 一律平行か、井ごとに符号が違うか |
| 5 | **tip×新面ブレンド**（診断のみ） | tip単体より改善するか |

**禁止:** 生Pearson閾値を緩めて Soft-Preserve 再学習を自動再開する（F041）。本注意は **判定指標の監査** であり、禁止仮説の言い換え許可ではない。

---

## 過去実験で疑うべきパターン

次に当てはまる NO-GO / Final2不可は、**再計算候補**（再学習ではなく、既存predsの監査）:

1. 根拠がほぼ「tip pearson ≈ 0.999」だけ
2. なのに CF超え or tip RMSE より良い／近い
3. 誤差相関・井中心化が未記録

代表例: CHK-392（監査済=395）· CHK-070/040/Sunny（監査済=**CHK-396**）。  
※ tip RMSE に大敗しているものは「別面失敗」より「弱いモデル」の可能性が高く、優先度は下げる。

**CHK-396 実測（再学習なし · tip-cv selector RMSE≈29.88 基準）:**

| case | raw | error | centered | vs tip | 解釈 |
|---|---:|---:|---:|---|---|
| CHK-070 | 0.9994 | 0.727 | 0.525 | −1.9 | 生Pearson過強 · ただし tip非改善 · **F010維持** |
| CHK-040 | 0.9991 | 0.841 | 0.107 | −16.1 | 同上 · **F011維持** |
| Sunny | 0.9996 | 0.821 | 0.751 | −0.4 | 同上 · Sunny Final不可維持 |
| CHK-392 | 0.9995 | 0.689 | 0.895 | +12.5 | tip改善だが F015/F041 · 提出不可 |

詳細: [`chk396-tip-corr-catalog.md`](../exp/work/wave30-soft-preserve/chk396-tip-corr-catalog.md)

---

## Agent / checklist 運用

- `exp/experiment-checklist.md` の pearson系 acceptance で本ファイルを参照する
- 新規 CHK の acceptance に「生Pearsonのみ」を書かない。最低でも誤差Pearson or 井中心化を併記
- Soft-Preserve 再学習・soft提出は別問題（F041 / F015）
- **追記 2026-07-31:** CHK-403/404で「閉鎖は正しい（tip負け+F015）」「caveatは現状維持」を確定 · [`403`](discussion/chk403-gate-reconcile-2026-07-31.md) · [`404`](discussion/chk404-pearson-caveat-decision-2026-07-31.md)
- **追記 2026-07-31:** CHK-396で過去 tip-corr NO-GO をカタログ化。**ban自動解除なし**