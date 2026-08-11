# OPS-SUBMIT C/D — Public結果（2026-07-30）

> kernels Ver1 **COMPLETE** · validator **PASS** · Public確定

## 候補

| 案 | kernel | Ver | 比率 | SHA vs SUB-14 | vs SUB-14 RMSE | 提出 |
|---|---|---|---|---|---|---|
| **C** | `kazeneko77/tip-blend-sub14-sub9-090-010` | 1 | **0.90 / 0.10** | **≠** | 0.110 | **55094041 · 6.237** |
| **D** | `kazeneko77/tip-blend-sub14-sub9-075-025` | 1 | **0.75 / 0.25** | **≠** | 0.276 | **55094043 · 6.276** |

比較基準: `exp/work/wave22-candidates/harvest-tip-t015-final/submission.csv`（SUB-14）  
C↔D RMSE ≈ 0.165（相互にも異なる）

## ログ確認

- secondary: `/kaggle/input/notebooks/kazeneko77/tip-gated-selfline-selfdev8/submission.csv`
- n_common=14151 · E2E tip T0.15 後に末尾ブレンド（F005 回避）

## 判定

- **C:** 表示Public1。ただし旧Best差−0.004はノイズ帯。改善GOではなく、Public1運用として枠2暫定。
- **D:** Cより+0.039。NO-GO。
- 追加の比率スイープは行わない。詳細: [`OPS-LB-ABCD`](../exp/latest/ops-lb-abcd-public-2026-07-30.md)

## 注意

- Final2: 枠1=SUB-14 · 枠2=C（B7門番PASS時は別面へ差替）
- SUB-19（14×13）とは別面（SUB-9 gated）
