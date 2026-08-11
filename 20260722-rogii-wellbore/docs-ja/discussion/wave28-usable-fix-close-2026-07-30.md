# Wave-28 クローズ — 提出可能な直し方ハント（2026-07-30）

## 1行

**外部NB/文献由来の6仮説を T4 screen → 全 NO-GO（F040）。次は OPS-FINAL2 のみ。**

## 初学者向け

「提出で使える直し方」を他者コードと文献から6つ試しました。

| 仮説 | 結果（一言） |
|---|---|
| heelでラグを測って曲線をずらす | ほぼ効かない |
| 評価開始だけつなぐ | tipは既につながっている |
| 整合特徴で残差を学ぶ | tipと同じ面（相関≈1） |
| 別の系列ベースライン | tipより大幅に悪い |
| 傾きで変化速度を抑える | 全体は少し良く見えるが多くの井で悪化 |
| 粒子をGRで再重み | 良くならない |

→ 実験レーンは閉じ、**Final枠の確定（OPS-FINAL2）** に戻ります。

## 結果表

| CHK | 仮説 | 主要数値 | 判定 |
|---|---|---|---|
| 363 | H-A1 heel自己相関→MD位相 | soft 17.236 · 最良ゲート Δ**0.0** | **NO-GO** |
| 364 | H-A4 PS連続 | median \|gap0\|≈**0.07** · 最良 Δ≈**−3e−5** | **NO-GO**（実質Δ0） |
| 365 | H-A2 整合特徴 LOO residual | pearson≈**0.9999** · Δ**+2.55** | **NO-GO** |
| 366 | H-A3 last-anchor / 局所NCC | 最良代替 23.82（tip+6.6） | **NO-GO** |
| 367 | H-B2 dZ rate prior | pooled Δ**−0.26** だが mean井Δ**+0.88** · 15/20悪化 | **NO-GO**（非悪化FAIL） |
| 368 | H-B1 GR窓再重み | 最良 mix≡0 · Δ**0** | **NO-GO** |

work: [`exp/work/wave28-usable-fix/`](../../exp/work/wave28-usable-fix/)  
hunt: [`usable-fix-hypothesis-hunt-2026-07-30.md`](usable-fix-hypothesis-hunt-2026-07-30.md)

## Kaggle CPU/GPU

ローカル pack screen で完結。Kaggle 起動は不要だった（許可は受領済み）。

## 次

**OPS-FINAL2**（枠1=SUB-14 · 枠2=Public1 · UIユーザー）
