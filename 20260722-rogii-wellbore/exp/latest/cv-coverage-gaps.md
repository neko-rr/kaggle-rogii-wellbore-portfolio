# CV カバレッジ穴 — 別セッション実行用メモ

> **created:** 2026-08-04 · **updated:** 2026-08-05（**all773 COMPLETE · tip フル尺固定**）  
> **目的:** full≈773井 CV の **未計測** を一覧  
> **SSOT:** [`within-stage-comparisons.md`](../within-stage-comparisons.md) · [`experiment-checklist.md`](../experiment-checklist.md)  
> **all773 tip 尺:** **CLOSED 2026-08-05** · [cv](chk-final-t2-all773-cv-2026-08-05.md) · faces `20260804-115307` · tip pool 10.84 / hard 26.83 · tip⊕ NOGO  
> **残本命は L dual**（761/804…）· residual T3 は **041247** 維持

---

## 今セッションで閉じた穴（再実行不要）

| 穴 | 結果 | 参照 |
|---|---|---|
| **all773 Trust A/B/C** | tip **10.839** · hard **26.829** · tip⊕ Δ−0.008 · mid≈tip · **GO_baseline / tip⊕ NOGO** | [all773-cv](chk-final-t2-all773-cv-2026-08-05.md) |
| 643 ladder (v2 local) | tip_collapse=false · S3 blend 主因 | ladder v2 |
| 697 mid w0.50 | GO_t2 + E2E map tipdist 3.30 | e2e analysis |
| 702/710 residual on **新 mid** | tipdist **≥3.4 NOGO** · FIXED3∩test=0 | [cascade](../work/wave31-neural-proposal/out-710-downstream-cascade/report.md) |
| blend dual T2×tipdist | T2 Best w0.50 · tipdist Best mid w0.60 | [blend dual](../work/colab-final-t2/out-blend-weight-dual-cascade/report.md) |
| w050 residual/α/s3/soft/tip⊕ **local T2×hard20** | fill report · α↑=T2↓ · tip⊕弱 | [fill](../work/colab-final-t2/out-cv-gaps-fill-20260804/report.md) |
| hard20 residual dual (旧 faces) | order flip なし | out-cv-gaps-cpu-20260804 |
| faces 114917 vs 041247 residual α0.35 | mid meanΔ0.15 · residual 9.998→**10.094** | local compare |
| soft_diag T2 80 · 620 | GO dump · inject NOGO | 既知 |
| geo 650–655 | NOGO | 既知 |

---

## 残りの CV 穴（all773 以外）

| 優先 | 穴 | 規模 | 環境 | メモ |
|---|---|---|---|---|
| **P1** | **soft β tipdist**（695） | E2E faces 要 soft 面 | GPU 短 or faces+soft | local T2 9.307 のみ · soft を pipeline に載せた E2E |
| **P2** | ~~farvol train face → T2 副作用（635）~~ | local | **done** | T2 farvol **8.26 ≪ mid 12.28** · 枠2は触らず · [635](../work/colab-final-t2/out-cv-gaps-fill-20260804/chk635-farvol-t2-side.md) |
| **P2** | tip⊕g0.10 **T2+hard20** | CPU fill に含む | ローカル済 | tip_g* T2 弱確認済 |
| **P3** | mid468 full tip-cv dump | hard20 | GPU 長 | 643 経路と重複注意 · 低優先 |
| **P3** | all773 FINAL-T2 tip ABC | ~773 | **CLOSED 08-05** | [all773-cv](chk-final-t2-all773-cv-2026-08-05.md) · tip⊕ NOGO · residual は 041247 |
| **P1 戦略** | **L 再学習 761/804…** | pretrain 後 | GPU | residual 天井 · **Trust 本命** |

---

## 主物差し（再掲）

| 物差し | 使い方 |
|---|---|
| **T2≈80 pooled / T3 residual 041247** | residual Trust 本命 · 666 頭 |
| **all773 tip pool / hard_mean** | フル train 人口 tip 床 · tip⊕ 評価 |
| hard20 | 補助 · order flip 監視 |
| tipdist E2E | residual dual 必須 · all773 mid tipdist **≠** residual tipdist |
| Public | residual **禁止帯** · farvol 枠2 |

---

## 別セッション コピースタート

```
1. 読む: cv-coverage-gaps.md · exp-index · cascade report
2. GPU status: 697b / 711 → harvest tipdist
3. CPU harvest: residual-t2-hard20-dual · sample3-watch
4. 次 Trust: L 688 pretrain-gate → 再 dump residual dual
5. 禁止: all773無断 · residual Public · farvol · soft→mid 620 · 生 L FINAL
```

---

## 提出禁止

全 dump / dual / map は **診断**。Final2 はユーザー OPS。
