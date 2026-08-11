# Pretrain Gate — {{CHK_OR_EXP_ID}}

> skill: kaggle-pretrain-gate  
> date: yyyy/mm/dd HH:MM UTC  
> profile: （tabular | lora | simulation | ensemble）  
> tier: 0+1 / 0+1+2  
> chk: CHK-xxx  
> result: PASS | FAIL | DEFER  
> execution: local-smoke | kaggle-short | colab-short

---

## 仮説・acceptance（CHK から）

- hypothesis: 
- acceptance: 

---

## Tier 0（静的）

- [ ] データ path・件数
- [ ] 提出形式整合
- [ ] import / 設定

**Tier 0 結果:** PASS | FAIL

---

## Tier 1（スモーク）

- [ ] 1 step / 1 episode / 10行 infer
- [ ] 即エラーなし

**Tier 1 結果:** PASS | FAIL

---

## Tier 2（ミニ検証）

- [ ] CV / holdout ≥ baseline または acceptance
- [ ] ensemble 整合（該当時）

**Tier 2 結果:** PASS | FAIL | SKIP

---

## 判定

| 結果 | 次アクション |
|---|---|
| **PASS** | `kaggle-kernels-runbook` で本番実行可 |
| **FAIL** | 長時間学習禁止。`run-log.md` 参照して修正 |
| **DEFER** | Tier 2 未実施。ユーザー判断 |

### ブロッカー（FAIL 時）

- 

### デバッグログ

- `my-ran-notebook/.../run-log.md`（あれば）

