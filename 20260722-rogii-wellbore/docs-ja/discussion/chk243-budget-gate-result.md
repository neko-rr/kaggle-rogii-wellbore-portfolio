# CHK-243 結果 — tip_std 難易度ゲートで提案予算配分

> date: 2026-07-28 · local hard20 PF · **提出なし** · ≠SOFT後処理

## 判定

**NO-GO**（GPU tip-cv へ進めない）

| spec | pooled s5@T0.15 | Δ vs baseline | pooled oracle | Δ oracle |
|---|---:|---:|---:|---:|
| baseline 128 | 17.236 | 0 | 12.881 | 0 |
| tipstd_gate（probe32→192/64） | 19.552 | **−2.317** | 14.150 | −1.268 |

平均 seeds はともに 128（予算総量同じ）。配分だけ変えて tip・oracle 両方悪化。

## 含意

- tip_std 上位＝難井、の代理が粗い／追加シードがノイズ増。
- 難井予算↑は本実装では閉じる。CHK-242（多ラン結合）へ。

出典: `chk243-partial-summaries.json`
