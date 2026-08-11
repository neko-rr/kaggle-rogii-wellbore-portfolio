# OPS-LB — CHK-618c Public 着弾分析

> date: 2026-08-04 · CLI COMPLETE · ref **55222561**  
> kernel: `tip-e2e-chk618c-soft-diag-agree` Ver1  
> Final2 自動差替 **なし** · **再提出禁止**  
> E2E 機構: [`../work/wave31-neural-proposal/out-618c-e2e-analysis/report.md`](../work/wave31-neural-proposal/out-618c-e2e-analysis/report.md)  
> Public 梯子統合: [`ops-lb-chk664-public-branch-2026-08-04.md`](ops-lb-chk664-public-branch-2026-08-04.md)

---

## スコア

| ID | ref | Public | Δ tip(6.269) | Δ farvol(6.190) | tipdist E2E | 備考 |
|---|---|---:|---:|---:|---:|---|
| **farvol 0.95** | 55148128 | **6.190** | −0.079 | 0 | — | **枠2** |
| **618c soft_diag agree** | **55222561** | **6.231** | **−0.038** | **+0.041** | **11.933** | Trust診断 · 枠2NO |
| 558b agree-only mid | 55221471 | 6.238 | −0.031 | +0.048 | 0.382 | 枠2NO |
| 515 | 55195981 | 6.249 | −0.020 | +0.059 | — | — |
| 541 | 55221459 | 6.256 | −0.013 | +0.066 | 0.278 | 枠2NO |
| tip SUB-14 | 55006677 | 6.269 | 0 | +0.079 | 0 | — |
| 579 row only | 55206184 | 6.277 | +0.008 | +0.087 | 0.907 | 枠2NO-GO |

σ≈0.03 · |Δ|≲0.08 は確定勝ち主張禁止帯。

---

## 機構

- FINAL = **tip ⊕ soft_diag** on **agree**(mid495×learned) · frac≈0.127  
- Soft **FINAL ではない**（¬agree は tip）  
- anti-promote PASS · 618c E2E GO  
- 対比: **620** は T2 上で tip⊕soft → mid に全面負け（NOGO）· **618c** は Public 上で tip より良い

---

## 優秀 Kaggler 読み

### 1. Public では farvol に次ぐ（自診断内）

```
farvol 6.190  <  618c 6.231  ≲  558b 6.238  <  541 6.256  <  tip 6.269
```

- 618c は **自提出診断のうち farvol を除けば最良 Public**  
- それでも **farvol に +0.041** → **枠2差し替え禁止**

### 2. tipdist 大 × Public 良 = 危険な良

| 面 | tipdist | Public | 読み |
|---|---:|---:|---|
| 541 | 0.28 | 6.256 | 安全・薄い |
| 558b | 0.38 | 6.238 | 薄い改善 |
| **618c** | **11.9** | **6.231** | Public 良でも **Private 振れ幅大** |
| farvol | （薄 blend） | 6.190 | 枠2 既定 |

「Public が良いから Trust/Private も」は **禁止**（tipdist 11.9 が反証）。  
**620 NOGO と矛盾しない:** 評価軸（T2 mid 土台 vs Public tip 土台）が違う。

### 3. Soft 方針への含意

| 可 | 不可 |
|---|---|
| tip⊕soft_diag agree の **診断価値は確認済** | Soft 生 FINAL |
| Trust レーンで soft 面を **dual-score** 材料として保持 | 620 型 **soft≻mid 注入** 再開 |
| | 618c **再提出** · 枠2 自動差替 |

### 4. Final2

| 枠 | 判定 |
|---|---|
| **枠2** | **farvol 固定**（618c 未達） |
| **枠1** | residual **666** が T2 主候補 · 618c は Trust 補助情報 · 自動差替なし |
| レーン | Trust≠Public で実験停止 **しない** · 枠2を 618c に移すこともしない |

---

## 禁止

- 618c 再提出  
- Soft / soft_diag 生 FINAL  
- 620 soft→mid 注入再開  
- Public 6.231 だけで Final2 差替  

## 次

1. **641 Public** 着弾待ち（残差 α0.30 の Public 座標）  
2. **643** harvest → 673  
3. residual **666** 提出はユーザー明示時のみ
