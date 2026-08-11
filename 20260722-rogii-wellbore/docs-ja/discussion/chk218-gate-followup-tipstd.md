# tip_std ゲート追試（CHK-218 後 · tip-cv 実測）

日付: 2026-07-26（風呂セッション）
データ: `chk205-per-well.csv`（T1 vs T0.5 tip-cv）+ train tip_std

## 結果（hard20 pool RMSE）

| 戦略 | RMSE | vs T0.5 global |
|---|---:|---:|
| T1 global（CHK-211） | 33.178 | — |
| **T0.5 global（CHK-205）** | **32.276** | 0 |
| tip_std < med → T0.5 else T1 | 32.322 | −0.046 |
| tip_std ≥ med → T0.5 else T1 | 33.133 | −0.857 |
| lowest tercile only T0.5 | 32.334 | −0.058 |
| oracle per-well best(T1,T0.5) | 32.239 | +0.037 |

## 判定

- **tip_std ゲートは global T0.5 を超えられない**（corr tip_std↔d05 = −0.71 でも）
- T1/T0.5 間の oracle 余裕は **+0.037 のみ** → 温度の井別切替の余地はほぼ尽きた
- **次の中間改善は「温度の井別」ではなく「温度の値」（0.3 vs 0.5）または別 generator** に振る

## 含意（CHK-219）

- tip-cv で T=0.3 が T=0.5（32.276）を上回れば採用
- 負けたら T=0.5 を tip 面の既定温度として固定し、上流（seed/spr/init）に戻る
