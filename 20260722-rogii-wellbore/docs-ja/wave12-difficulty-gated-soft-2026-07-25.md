# Wave-12 — 難易度ゲート付き tip_self_line（CHK-160/161/162 · 2026-07-25）

> CHK-160/161: ローカル CPU · CHK-162: **GPU E2E COMPLETE · SUB-9 PENDING**  
> 作業: [`exp/work/chk160-difficulty-gate/`](../exp/work/chk160-difficulty-gate/) · [`exp/work/chk161-gated-soft/`](../exp/work/chk161-gated-soft/)  
> NB: [`my-submitted-notebook/tip-gated-selfline-selfdev8/`](../my-submitted-notebook/tip-gated-selfline-selfdev8/) · [SUBMIT](../my-submitted-notebook/tip-gated-selfline-selfdev8/SUBMIT.md)

## 1 行

**良い所取りは成立。** tip が自分の遠MD自己線から大きく外れている井だけ SOFT（`f33-s08`）を掛けると、T2 厳格ゲート（pool≥+0.05 · sample≥−0.05）を **PASS**。全井 SOFT より sample 悪化が小さい。

## CHK-160（分類）

| 項目 | 結果 |
|---|---|
| SOFT 改善井（Δ>+0.05） | あり · 悪化井も混在 |
| Δ と相関が強いメタ | **`tip_far_self_dev` +0.45** · tip_rmse +0.39 · heel_corr −0.15（弱い） |
| 提出不可の oracle | hard20 だけ SOFT は参考上限 |
| 提出可能ゲート候補 | `self_dev>8/12` · `heel_corr<0.85` が近似で厳格帯に入る |

## CHK-161（正確 T2）

| ゲート | n_apply | Δpool | Δhard | Δsamp | 厳格 |
|---|---:|---:|---:|---:|---|
| **self_dev>8** | 32 | **+0.084** | **+0.203** | **−0.043** | **PASS** |
| heel_corr&lt;0.85 | 64 | +0.079 | +0.195 | −0.046 | **PASS** |
| **self_dev>12** | 12 | +0.073 | +0.166 | **−0.021** | **PASS**（sample 最安全） |
| self_dev>5 | 54 | +0.074 | +0.203 | −0.075 | FAIL（sample） |
| heel_corr&lt;0.70 | 12 | +0.027 | +0.060 | −0.004 | FAIL（pool） |
| 全井 SOFT（対照） | 80 | +0.069 | +0.194 | −0.076 | FAIL（sample） |

**推奨既定:** `self_dev>8`（改善最大）  
**保守:** `self_dev>12`（sample ほぼ維持）

## 禁止帯との関係

| ID | 関係 |
|---|---|
| F018 | CF フォールバックではない（tip 上の strength だけ） |
| F020 | 全井攻撃的 self-line ではない · sample ゲート付き |
| hard20 ID | **未使用**（リーク回避） |

## CHK-162（GPU E2E smoke → SUB-9）

| 項目 | 結果 |
|---|---|
| Kernel | `kazeneko77/tip-gated-selfline-selfdev8` Ver1 **COMPLETE** |
| ゲート | `tip_far_self_dev > 8` · f33-s08 |
| test wells | 3 · **applied 2**（00bbac68 · 00e12e8b）· **skip 1**（000d7d20 · self_dev≈2.07） |
| vs tip BH | 3405 rows · max_abs≈3.30 |
| vs ungated SOFT | **1266 rows**（skip 井の far のみ · 期待どおり） |
| 提出 | **SUB-9** ref **54972467** · **PENDING** · 診断のみ · 枠1自動差し替えなし |

## 次

1. **OPS-LB-89 DONE** · SUB-9 Public **6.484**（新Best）· SUB-8 **6.582** 打ち切り · [`ops-lb-89`](ops-lb-89-sub89-public-2026-07-26.md)  
2. **Wave-13 B:** CHK-184 → 172/178（承認後）· [`wave13-plan`](wave13-plan-2026-07-25.md)  
3. Final仮: 枠1 gated · 枠2 旧Best保険 · **OPS-FINAL2**
