# OPS-LB-PEND — Public harvest（blend / T0.10 / SUB-18）

> updated: 2026-07-29 · CLI `competitions submissions` · COMPLETE  
> SSOT Best: [`exp/exp-index.md`](../exp/exp-index.md) · 関係論: [`cv-lb-private-relation.md`](cv-lb-private-relation.md)

## 提出（直近4件）

| 順 | SUB / 名 | CFG | ref | kernel | Public | vs SUB-14 |
|---|---|---|---|---|---|---|
| 1 | **SUB-20** | tip E2E **T=0.10** | **55066862** | tip-gated-lik-temp-0p1 Ver1 | **6.241** | **−0.028**（表示上 Best） |
| 2 | **SUB-19** | blend SUB-14×13 **0.85/0.15** | **55066793** | tip-blend-sub14-sub13-e2e Ver3 | **6.277** | +0.008 |
| 3 | **SUB-18** 誤重複 | learned_trajectory E2E | **55066056** | tip-e2e-learned-traj Ver1 | **7.768** | +1.499 |
| 4 | **SUB-18** 正 | learned_trajectory E2E | **55066050** | tip-e2e-learned-traj Ver1 | **7.705** | +1.436 |

比較基準: SUB-14 `55006677` Public **6.269**。

---

## 1 行判定

| 提出 | 判定 |
|---|---|
| **T=0.10** | 表示 Best **6.241**。ただし収穫 CSV は **SHA≡SUB-14**（F025 が T=0.10 にも波及）→ Δ0.028 は **Georgy σ≈0.03 ノイズ帯**。モデル差として採用しない |
| **blend** | **6.277** · Best+0.008 · ノイズ以下の悪化 · **枠外** |
| **SUB-18** | **7.705 / 7.768** · 中間面 final 化は壊滅 · **F015 系追認** · 枠禁止 |

---

## 深掘り — T=0.10（SUB-20）

### 事実

- tip-cv（CHK-223）: T=0.10 **29.848** · T=0.15 **29.899** · 改善 **+0.051**（閾値 ≥0.30 未達 · 既定は T0.15 凍結）
- ローカル収穫 `exp/work/kernels-output-tip-gated-lik-temp-0p1/submission.csv` と SUB-14 CSV: **SHA256 一致** · RMSE 差分 **0**
- Public: **6.241** ≠ SUB-14 **6.269**（同一予測なのに表示差）

### 解釈

1. **F025 拡張:** `LIK_TEMP∈{0.10,0.15,0.2,0.3}` は learned 面では差が出ても、**branch_hedge 以降の最終 CSV は T0.15 と同一**になり得る（今回 T0.10 で実測）。
2. **Public Δ0.028:** 同一 CSV 前提なら「温度冷却の勝ち」ではない。σ≈0.03 と整合する **表示/採点ゆらぎ**、または提出物とローカル収穫の不一致疑い。いずれにせよ **CHK GO / 温度梯子採用の根拠にしない**（[`cv-lb-private-relation`](cv-lb-private-relation.md)）。
3. **温度梯子（予想 vs 実測）:** [`temp-ladder`](discussion/temp-ladder-public-forecast-2026-07-28.md) の「T0.10≈6.20–6.30」は数字は当たったが、**最終≡T0.15** なら梯子形状の検証にはならない。SUB-16 T0.3=**6.385** は最終≠Best 側の悪化として有効。

### Final2 への含意

| 枠 | 割当 | 理由 |
|---|---|---|
| **枠1 CV1** | **SUB-14** 維持 | tip-cv 既定は T0.15 凍結（223 は閾値 NO-GO）· 最終面も同一 |
| **枠2 Public1** | 表示上は **55066862（6.241）** | ルール上 Public 最良。**中身≡SUB-14** なら UI でどちらを選んでも実質同じ · 推奨は **SUB-14 を明示維持**（説明容易）か、Public1 ラベルで 55066862 |

---

## 深掘り — blend（SUB-19）

- 再構成 RMSE **0.165**（≠SHA · F025 回避）· Public **6.277**
- Best よりわずかに悪い · Δ≪0.08 → **診断閉 · 再提出・Final 昇格なし**
- T0.15×T0.5 の線形寄せは Public で効かない（同族内）

---

## 深掘り — SUB-18 E2E

- 正 **7.705** · 誤重複 **7.768**（Δ0.063 · 非決定性帯）
- `learned_trajectory` を最終面にした E2E は tip 最終（6.27 帯）から **+1.4 以上**悪化
- F005 remake は採点は通ったが、**面として不採用**（F015「中間面を final にすると悪化」の強化証拠）
- **再提出禁止** · Final 枠禁止

---

## 次アクション

- [x] OPS-LB-PEND harvest
- [ ] OPS-FINAL2: 枠1=SUB-14 · 枠2=Public1（表示 6.241 なら 55066862、中身同一なら SUB-14 でも可）· **ユーザー UI**
- [ ] Wave-23 残（276/277 弱）または **実験打ち切り → Best 防衛**
- [ ] T∈{0.10,0.15,0.2,0.3} の **最終 CSV 再提出禁止**（F025 維持·拡張）

## 関連

- validator: [`2026-07-29-tip-gated-lik-temp-0p1`](submission-validations/2026-07-29-tip-gated-lik-temp-0p1.md) · [`blend`](submission-validations/2026-07-29-tip-blend-sub14-sub13.md)
- 夜メモ: [`ops-lb-sub161718`](ops-lb-sub161718-night-2026-07-28.md)
- CHK-223: [`chk223-lik-temp-0p1-result`](discussion/chk223-lik-temp-0p1-result.md)
