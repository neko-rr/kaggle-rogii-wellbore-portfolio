# OPS-LB — CHK-541 / CHK-558b Public 着弾分析

> date: 2026-08-04 · CLI `competitions submissions` · status=**COMPLETE**  
> Final2 自動差替 **なし** · **再提出禁止**  
> 分岐統合: [`ops-lb-chk664-public-branch-2026-08-04.md`](ops-lb-chk664-public-branch-2026-08-04.md)

---

## スコア（公式 Public）

| ID | ref | kernel | Public | Δ vs tip(6.269) | Δ vs farvol(6.190) | tipdist E2E | Trust hard20 | frac_gate |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **farvol 0.95** | 55148128 | — | **6.190** | −0.079 | 0 | — | — | — |
| **558b agree-only** | **55221471** | tip-e2e-chk558b-agree-only-p495 | **6.238** | **−0.031** | **+0.048** | **0.382** | **26.629** | 0.127 |
| 515 tip⊕row468 | 55195981 | — | 6.249 | −0.020 | +0.059 | ≈2.12 | 28.901 | — |
| **541 agree∧row** | **55221459** | tip-e2e-chk541-agree-p495 | **6.256** | **−0.013** | **+0.066** | **0.278** | **26.655** | 0.100 |
| tip SUB-14 | 55006677 | — | **6.269** | 0 | +0.079 | 0 | 29.899 | — |
| 579 tip⊕row495 | 55206184 | — | 6.277 | +0.008 | +0.087 | 0.907 | 26.768 | row only |

σ≈**0.03** · |Δ|≲**0.08** は単独で「確定勝ち」を主張しない帯。

---

## 機構（思い出し）

| ID | FINAL | 面 |
|---|---|---|
| **541** | tip ⊕ **agree∧row**(mid495) | tip 土台 · より狭いゲート（frac≈0.100） |
| **558b** | tip ⊕ **agree-only**(mid495) | tip 土台 · やや広いゲート（frac≈0.127） |
| 579 | tip ⊕ **row only** | tip 土台 · agree なし |

どちらも Soft / mid / L の **生 FINAL ではない**（F015 外 · tip⊕gate）。

---

## 優秀 Kaggler 読み

### 1. Public 梯子（薄い中流注入）

```
farvol 6.190  ≪  558b 6.238  <  515 6.249  <  541 6.256  <  tip 6.269  <  579 6.277
```

- **agree フィルタ付き mid 注入**は tip より **わずかに良い Public**（両方）。
- **row only（579）**は tip より **わずかに悪い** → Public では agree が最低条件に近い。
- ゲートが広い **558b の方が 541 より Public も Trust も良い**（同系内で整合）。

### 2. tipdist ↔ Public 相関（この帯では）

| tipdist | Public | 読み |
|---:|---:|---|
| 0.278 (541) | 6.256 | tip 最近傍 · 改善も最小 |
| 0.382 (558b) | 6.238 | 中距離・薄い · **同系最良 Public** |
| 0.907 (579) | 6.277 | tip から離れると Public 逆 |
| 11.9 (618c) | PENDING | Public 本命にしない（既定） |

「tip 近すぎ＝安全」でも「少し離すと Public 微増」がありうる。ただし **farvol は別家系**（薄 blend）で、この mid495 系は **全員 farvol に −0.05 前後負け**。

### 3. 枠判断（強制）

| 項目 | 判定 |
|---|---|
| **枠2（Public）** | **farvol 固定** · 558b/541 は枠2候補に **しない**（Δ vs farvol +0.048 / +0.066） |
| **枠1（Trust）** | 558b/541 は hard20 **26.6 帯**。より強い Trust は residual/soft 系（別レーン） |
| **再提出** | **禁止**（両 ref 1 回のみ） |
| **|Δ|≲0.08 で Final2 差替** | **禁止** |
| **row495 再連打** | **STOP**（579 が裏付け） |

### 4. CV↔Public 乖離で止めない

- Trust では 558b≺541≺579（低いほど良）。Public でも同じ順序で良い。
- 乖離を理由に Trust 実験を止めない（Rule `kaggle-public-lb-bias-stop`）。
- 同時に **Public が良くても farvol 以下なら枠2は動かない**。

### 5. 次に効く含意

| 含意 | 行動 |
|---|---|
| thin mid495 tip⊕gate は Public 微プラス | **枠2差し替え理由にはならない** · 診断は閉じる |
| さらに Public を詰めるなら | farvol 家系 or **tip 近い薄 residual**（ユーザー明示のみ） |
| Trust を詰めるなら | **上流面 / residual dual**（666 等）· 541/558b 再提出はしない |

---

## 禁止

- 541 / 558b / 579 再提出  
- 枠2 を 558b や 541 に無断差替  
- Public σ 帯だけで Trust CHK 停止  

## 次

1. **618c / 641** Public 着弾 → 664 表を完成（いま PENDING）  
2. **643** harvest → 673  
3. 新 Public 診断は **ユーザー明示時のみ**
