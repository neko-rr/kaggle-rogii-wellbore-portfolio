# OPS-SUBMIT A/B — harvest（2026-07-30）

> kernels Ver1 COMPLETE · 当初見送り後、ユーザー明示指示で **Notebook 紐づけ提出**

## 結果

| 案 | kernel | Ver | LIK_TEMP / BH | final SHA vs SUB-14 | 提出 |
|---|---|---|---|---|---|
| **A** | `kazeneko77/tip-gated-lik-temp-0p08` | 1 | 0.08 / 0.60 | **≡** | **55093490 · 6.323** |
| **B** | `kazeneko77/tip-gated-bh-strength-0` | 1 | 0.15 / **0.0** | **≡** | **55093492 · 6.274** |

比較基準: `exp/work/wave22-candidates/harvest-tip-t015-final/submission.csv`（SUB-14）

## 読み

1. **A:** T=0.08 も最終面は T0.15 と同一（F025 が 0.08 にも波及）。残枠を使う指示で診断再提出。
2. **B:** `_BH_STRENGTH=0` は意図どおり動作（ログ確認）。ただし PF seed-branch hedge は本 run で **applied 0**（1井 `skip_minor_mass`）。最終 CSV は SUB-14 と同一。
3. **before_gated_selfline → final** の RMSE≈0.97 が主差分。いわゆる「hedge 前後」差の多くは **gated selfline 以降**側。
4. A/B/SUB-14/SUB-20の同一ローカル面はPublic range 0.082 · σ≈0.034。設定差ではなく実行ノイズとして扱う。

## 次

- A/B Public harvest 後も、同一 CSV の微差はモデル改善と解釈しない。
- A/BともNO-GO。Final2は枠1=SUB-14 · 枠2=Public1 C。

## 成果物

- `exp/work/kernels-output-tip-gated-lik-temp-0p08/`
- `exp/work/kernels-output-tip-gated-bh-strength-0/`
