# OPS-LB — CHK-641 Public 着弾分析

> date: 2026-08-04 · CLI COMPLETE · ref **55223002**  
> kernel: `tip-e2e-chk641-mid-alpha-l-resid` Ver1  
> Final2 自動差替 **なし** · **再提出禁止**

---

## スコア

| 項目 | 値 |
|---|---:|
| Public | **6.472** |
| vs tip 6.269 | **+0.203** |
| vs farvol 6.190 | **+0.282** |
| tipdist E2E | **1.743** |
| T2 residual α0.30 | **10.309**（Trust 良） |

σ≈0.03 帯を **明確に超える** 悪化。

---

## 優秀 Kaggler 読み

1. **T2 良 · Public 悪化** — residual α0.30 は Trust レーン専用と確定。  
2. tipdist 1.74 は 541/558b より遠いが 618c(11.9) より近い **中距離でも Public 失敗**。  
3. **666 α0.35 は更に tip から離れる**（td 1.99）→ Public 無診断提出は更に危険。  
4. **枠1 residual 候補は T2 dual で選ぶ** · Public で residual を本命にしない。  
5. **枠2 farvol 固定** · 641 は診断クローズ · 再提出禁止。

## 対比（同セッション Public）

| ID | Public | レーン |
|---|---:|---|
| farvol | 6.190 | 枠2 |
| 618c soft | 6.231 | 枠2NO · 危険帯 |
| 558b | 6.238 | 枠2NO 薄い |
| 541 | 6.256 | 枠2NO 薄い |
| tip | 6.269 | 基準 |
| 579 | 6.277 | row STOP |
| **641 residual** | **6.472** | **Public NO-GO** · Trust のみ |

## 禁止

- 641 再提出  
- residual を Public 本命に  
- 641 悪化で Trust residual 全停止（レーン分離）
