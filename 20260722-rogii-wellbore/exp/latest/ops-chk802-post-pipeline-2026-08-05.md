# CHK-802 結果分析 · 後工程 CV ロック · 提出方針（2026-08-05）

> dual 生レポート: [`../work/out-t3-cpu-harvest/l-dual-CHK-802-colab-fast2/report.md`](../work/out-t3-cpu-harvest/l-dual-CHK-802-colab-fast2/report.md)  
> dual 概要: [`ops-chk802-dual-nogo-2026-08-05.md`](ops-chk802-dual-nogo-2026-08-05.md)  
> FAST2: [`ops-chk802-fast2-final-day-2026-08-05.md`](ops-chk802-fast2-final-day-2026-08-05.md)  
> 法則: [`l-improvement-laws-2026-08-05.md`](l-improvement-laws-2026-08-05.md) · 台帳 **F044**

---

## 結論（1行）

**802 residual `mid + 0.35·(L802−mid)` は Trust dual で明確 NOGO。α 再格子・E2E Submit・weight 言い換えはすべて禁止。後工程は 808→781(+805·807) のみ。Final2 は 666 × farvol 維持。**

---

## 実験定義（実施済み）

| 項目 | 値 |
|---|---|
| 機構 | MD-Q4 **行** sample_weight L retrain（weight 帯最終 1 本） |
| train | Colab FAST2 · 2fold · LGB×1 n200 · CatBoost skip · OOF **9.3765** |
| residual 尺 | faces **`20260804-041247`** · α **0.35** 固定（F043） |
| dual | `CHK-802-colab-fast2` · 810/812/813/815 済み |
| L1_pass | **False** · ban-gate post **NO-GO** |

計画時メモ「faces+推論 → 即 E2E Submit（dual 並列可）」は、**dual が完了した今、Submit は実行しない**。

---

## live dual 数値（CV 正）

| 尺 | 旧 resid | 新 resid | **Δ（新−旧 · +悪化）** | 判定 |
|---|---:|---:|---:|---|
| hard20 | 16.304 | 18.090 | **+1.785** | **NOGO** |
| hybrid80 | 10.094 | 10.886 | **+0.792** | **NOGO** |
| B_Q4_rows（802 本命帯） | 12.828 | 13.850 | **+1.022** | **本命帯も悪化** |
| SSE top50 | 12.358 | 13.356 | **+0.998** | 813 fail |
| D_688_hurt | 17.218 | 19.250 | **+2.032** | protect 必要帯が最悪 |
| non_hard | 6.411 | 6.411 | **0** | L 変化は hard 系に集中 |
| mid-hurt3 / Q4e / Q1e | — | — | **0** | 差分なし |
| 815 d\|L−mid\| hard | — | — | **−4.241** | **mid-collapse 中等度** |

---

## Kaggler 読み（なぜ落ちたか）

1. **目的関数のズレ**  
   TVT OOF（9.38）や MD-Q4 重み付けは「L を y に近づける」方向。提出 Trust の主尺は **`mid+α(L−mid)` residual RMSE**。L が mid に寄るほど `(L−mid)` が潰れ residual が死ぬ（815）。

2. **本命帯逆行**  
   MD-Q4 を攻めたのに **B_Q4 residual が +1.02**。重みは「どこに寄せたか」ではなく「residual 幾何を壊したか」で判定すべき、という F044 確認。

3. **崩壊強度は梯子の中位**  
   d\|L−mid\| **−4.24** は 804（−1.43）と 761/782（≈−7.9）の間。hard Δ **+1.79** も同じ帯。weight 族は **軽→中→重すべて NOGO** で閉じた。

4. **non_hard 不動**  
   非 hard は residual 完全一致 → 余計に mid 全体を良くする余地は無し。攻撃は hard / Q4 / hurt で失敗。

5. **α・POST・E2E への外挿は不可**  
   - α を触ると F043（Public residual 梯子でも既に全滅系）。  
   - residual E2E は 641/666/710/702 が Public NO-GO。L が悪いと Trust も 666 より悪化確定寄り。  
   - 残り提出 ≈5、Final2 枠は多様ペア済み → **802 で枠を燃やす価値なし**。

---

## 後工程 CV ロック（802 確定後）

| 後工程 | 802 前の計画 | **802 後の CV 最適** |
|---|---|---|
| dual residual α | α=0.35 screen | **α 固定 0.35 · 再格子禁止（F043）** |
| mid / tip⊕ / soft | 材料 | **触らない** · tip⊕ NOGO · F015 |
| weight 言い換え・v1d·814 live | 低優先 map | **禁止（F044 + 802 確定）** |
| 809 midhurt protect train | optional | **low · 781 優先**（map only 可） |
| **781 residual-path** | 本命候補 | **唯一 live L1** · Pack D d_pool sim **−3.03** |
| 805 / 807 | 781 内包 | **残** · resid stop 優先 |
| POST-L 779/756/764 | L1 GO 後 | **blocked**（L1 未 GO） |
| E2E Submit 802 resid | faces 即提出 | **ABORT** · notebook を立てない |
| Final2 | 666×farvol | **LOCK 維持** · 自動差替なし |

```text
DONE weight: 688 / 761 / 782 / 804 / **802** = F044 closed
NOW:         CHK-781 residual-path（Kaggle GPU RUNNING）
GO only if:  dual hard Δ ≤ −0.05 相当の L1 基準 + 813SSE + 815 no collapse
THEN:        POST-L → （GO のみ）E2E 提出準備 · 明示時だけ submit
ELSE NOGO:   Final2 現状維持 · 新規 L1 禁止帯に入らない
```

---

## 提出準備ステータス

| 候補 | Trust dual | E2E NB | 提出 |
|---|---|---|---|
| **802 mid+α0.35(L802−mid)** | **NOGO** hard+1.79 | **作成しない** | **禁止** |
| **666 residual（現枠1）** | SSOT head | 提出済 · 再提出禁止 | Final2 ★ |
| **farvol（枠2）** | N/A Public | 提出済 · 再提出禁止 | Final2 ★ |
| **781 residual-path** | **pending**（train RUNNING） | dual GO 後のみ雛形 | 明示 + GO のみ |

### 781 が COMPLETE したときの提出前シーケンス

**移動先 SSOT:** [`ops-chk781-post-pipeline-2026-08-05.md`](ops-chk781-post-pipeline-2026-08-05.md)  
（本節は互換のための短縮）

1. harvest learned face  
2. dual `run_l_residual_local_dual.py` · **813 + 815** · OOF 単独 GO 禁止  
3. L1 GO 時のみ E2E · α0.35 · **明示時だけ Submit**  
4. NOGO → STOP · 本ファイルの weight 再走なし  

---

## 禁止（この判定後）

- 802 residual の E2E / Public / Final 差替  
- MD-Q4 / 行 weight の言い換え再学習  
- α・well-α 再スイープ（F043）  
- POST-L without L1 GO  
- residual Public 本命（既提出帯と同型）

---

## 参照

| 用途 | パス |
|---|---|
| dual report | [`l-dual-CHK-802-colab-fast2`](../work/out-t3-cpu-harvest/l-dual-CHK-802-colab-fast2/report.md) |
| 781 run-log | [`tip-cv-chk781-resid-path-h20/run-log.md`](../../my-notebook/tip-cv-chk781-resid-path-h20/run-log.md) |
| Pack D | [`ops-cpu-pack-d-residual-path`](ops-cpu-pack-d-residual-path-2026-08-05.md) |
| Final2 | [`final2-ops-20260805`](final2-ops-20260805.md) |
