# CHK-197 結果 — portable + tip_std two-stage E2E（2026-07-26）

> kernel: `kazeneko77/tip-portable-twostage-s05` Ver1 · **GPU COMPLETE** · **提出なし**  
> 作業: [`my-ran-notebook/tip-portable-twostage-s05/`](../../my-ran-notebook/tip-portable-twostage-s05/)  
> 前提: Wave-17 CHK-193（T2 +0.063 / +0.0005）

## 1 行

**tip E2E で two-stage が動作確認できた。** 可視 test では portable 通過 1 井（`00bbac68`）のみ → 必然的に halve（s=0.025）。SUB-12（s=0.05）との差分は同井の遠MDのみ（max_abs≈1.03 ≈ SUB-12 移動量の半分）。

---

## 可視 test 適用

| well | reason | tip_std | strength | two_stage_halve |
|---|---|---:|---:|---|
| 000d7d20 | skipped_portable_gate | 0.17 | — | — |
| **00bbac68** | **applied** | **2.22** | **0.025** | **True** |
| 00e12e8b | skipped_portable_gate | 0.42 | — | — |

## vs SUB-12（portable s05）

| 比較 | max_abs | n_diff rows |
|---|---:|---:|
| twostage vs portable | **1.030** | 1985（`00bbac68` のみ） |
| portable vs pre-graft | 2.060 | 1985 |
| twostage vs pre-graft | 1.030 | 1985 |

→ strength 半減の幾何が正しい。

## 並行探索

| ID | 結果 |
|---|---|
| **CHK-197b** gated>8 + twostage | **NO-GO** · sample −0.014〜−0.024 |
| **CHK-198** tip_std 連続 strength | **NO-GO** · two-stage 硬閾値を超えず（最良≈同等） |

## 次

- **提出はしない**（日次枠消化済 · SUB-10/11/12 Public 待ち）
- Public 後: SUB-12 が弱い / farvol（SUB-10）が弱いとき、**本 kernel を提出候補**に
