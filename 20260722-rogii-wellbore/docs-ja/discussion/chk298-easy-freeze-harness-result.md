# CHK-298 結果 — easy tip 非回帰 harness（2026-07-30）

> action: **T4** · CI契約 · **提出なし**  
> 作業: [`run_chk298_easy_freeze_harness.py`](../../exp/work/wave25-hardwell-lane/run_chk298_easy_freeze_harness.py)  
> 契約: [`chk298-contract.json`](../../exp/work/wave25-hardwell-lane/chk298-contract.json)

## 1行方針

**以後の Wave-25 本実験は、この harness を必須ゲートにする。**

## 契約

| 閾値 | 値 |
|---|---|
| `MAX_ABS_STRICT` | 1e-6（厳密同一） |
| `MAX_ABS_SOFT` | 0.02（近同一） |
| `MAX_DELTA_RMSE` | 0.02（近同一時のみ） |
| 規則 | `max_abs≤STRICT` **または** (`max_abs≤SOFT` ∧ `ΔRMSE≤0.02`) |
| easy 定義 | CHK-297 panel `y==0`（45井） |

大きな改変が RMSE 改善しても **PASSにしない**（初期実装の逃げ道を塞いだ）。

## self-test

| ケース | 結果 |
|---|---|
| tip ≡ tip | PASS（45/45） |
| easy 1井を +5 破壊 | FAIL（検知） |
| hard だけ +5 | easy PASS（難井改変は契約外） |

## CI

```text
python exp/work/wave25-hardwell-lane/run_chk298_easy_freeze_harness.py --tip TIP.csv --cand CAND.csv
```

exit 0 = easy 凍結契約 PASS。
