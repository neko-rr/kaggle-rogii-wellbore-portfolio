# Final Push Campaign — 上流・中間面優先（ブレンド凍結）

> updated: 2026-08-03 · owner: Agent  
> **ユーザー指示:** ブレンドは最終日までやらない。根本改善=上流→中間→後工程の順。  
> **目標:** **Private 向上のみ**（代理=Trust tip-cv）。tip に似せない。  
> **後段:** mid **全面残しではない** · **現行より良い部分だけ**通し、後段をスコア最適化。  
> Final: **2026-08-05** · 全面 mid≠tip FINAL **F042禁止** · soft生提出 **F015/F041禁止**  
> SSOT（誤読防止）: [`pipeline-cascade-retest.md`](../work/wave31-selector-replace/pipeline-cascade-retest.md) **§0**

---

## 0. ボトルネック（3日分の結論）

| 段 | tip-cv RMSE | 意味 |
|---|---:|---|
| soft（中間） | **17.236** | 品質の天井に近い |
| tip selector / FINAL | **29.899** | Trust 現状 |
| soft→selector | **+12.663** | **破壊段 · 本命** |
| 451/456 gated pack | **≈23.45–23.76** | 崖の半分を回収済 |
| soft との残差 | **≈+6** | **まだ埋めていない根本ギャップ** |
| mid **全面**を FINAL に残す | Public ~7.8 | **F042** · 全面残し提出のみ禁止 |
| 勝ち分だけ残す＋後段最適化 | （未完） | **これからやる本命の後段作業** |

ブレンドは tip×partner で Trust を 29.2 帯まで寄せるだけ。**根本ではない。最終日まで HOLD。**

---

## 1. 工程順（これ以外の順番で実験しない）

```
S0   上流・selector / 粒子・提案・ゲート     ← いまここ
     勝ち分マップ（井/区間で mid が現行より良いか）
S0′  E2E 段差分の診断のみ（消えた=失敗、ではない）
S3–S8 後工程を新親＋勝ち分に合わせてスコア最適化（tip類似度は見ない）
S9   Trust tip-cv（主判定）
── 最終日のみ ──
B0   tip×partner 薄ブレンド
```

---

## 2. Agent 所有レーン

```
Lane U — Upstream / Mid（本線）
  U0 [DONE] 破壊段特定: soft→selector +12.7（CHK-380）
  U1 [DONE] 条件付き selector: 450→451（23.76）· 448全面 NO-GO
  U2 [DONE] anti-clone 提案: 455→456（23.45 · 非clone）
  U3 [DONE] CHK-489: 残差解剖（bank_gap≈11 · soft_diag vs mass_mid）
  U4 [DONE] CHK-490 push弱GO(23.35) → **490b aggregator GO: topk5_soft pack 20.44**
            （主因は粒子pushではなく集約 · ≠F041 Soft-Preserve）
  U5 [DONE] CHK-491: P-490b E2E 診断（overlap前まで差・FINAL≡tipは診断）
  U5b[DONE] CHK-490c/d · 495/497/499 易井併用
  U5c[NOW]  CHK-496: 297-dual E2E + 勝ち分マップ
  U6 [NEXT] 勝ち分だけ通す後段最適化 → Trust tip-cv（S9）· tip一致は成功指標にしない

Lane P — Post（中間GO後）
  目的: tip に戻すことではなく **Trust/Private 代理の改善**
  親が変わったら cascade 不足分だけ · 済工程の親またぎ再実行禁止
  全面 mid preserve 提出は禁止（F042）· 勝ち分マップ必須

Lane B — Blend（最終日まで凍結）
  CHK-485 se040/se060: 戦略ABORT（実行中なら UI で Cancel 可 · 成果は Final 判断に使わない）
  473/479–484/486–488: **HOLD until final day**

Lane D — 禁止
  mid FINAL · Soft-Preserve再学習 · tipノブ · 448全面 · 454同型 · F025–F041言い換え · ブレンド連打
```

---

## 3. 分岐（諦め禁止 · ブレンドに逃げない）

| U4/U5 結果 | 次 |
|---|---|
| pack 改善 · 勝ち分あり | 勝ち分マップ → 後段をスコア最適化 → Trust |
| FINAL≡tip（診断） | **失敗扱いしない** · 後段最適化で勝ち分を通せ |
| pack 改善だが easy 悪化 | 易井門番（297/298）強化 · 全面置換禁止 |
| tip-clone（中間自体が tip） | 損失/提案を変更して U4 再試（454/434 同型は禁止） |
| 改善ゼロ | soft−selector 残差の別特徴で再解剖（ブレンドへ逃げない） |

---

## 4. いまの数値

| ID | Trust / pack | 役割 |
|---|---:|---|
| soft | 17.236 | 上流天井の参照（提出不可） |
| tip / SUB-14 | 29.899 / Public 6.269 | 枠1防衛 |
| 456 gated | 23.450 | 旧 S0 |
| 490b topk5 gated | 20.44 | S0′ E2E GO（491） |
| **495/490d ess↓** | **17.14** | **現行最良 pack · E2E待ち** |
| soft ungated | 17.24 | ほぼ天井到達（pack） |
| farvol | Public 6.190 | 枠2（触らない） |

---

## 5. セッション再開

1. 本ファイル  
2. checklist Active（U3–U6 のみ）  
3. ブレンド CHK を再開しない（最終日まで）  
4. 「次どうする？」を聞かない — U3→U4→U5→U6
