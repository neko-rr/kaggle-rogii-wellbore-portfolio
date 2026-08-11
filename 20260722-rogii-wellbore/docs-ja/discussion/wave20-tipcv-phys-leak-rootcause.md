# Wave-20 根因 — tip-cv は PF を測っていない（phys + ラベルリーク）

> date: 2026-07-26 · 作業: [`exp/work/wave20-upstream/`](../../exp/work/wave20-upstream/)  
> 関連: [`chk206`](chk206-init-spr9-result.md) · [`chk208`](chk208-combo-oracle-result.md)

## 1 行

**tip-cv hard20 の tip_train_preds（RMSE 14.87）は PF/selector 面ではない。**  
`0.3·CF + 0.7·tvt_from_contacts(train)` と数値一致し、`tvt_from_contacts` は **train の真値 `TVT` で offset を合わせている**。

## コード経路（本番 tip NB）

```python
if wid in train_wells:
    hw_tr, tw_tr = load_well(wid, 'train')
    tvt_phys = tvt_from_contacts(hw_tr, tw_tr)  # offset に hw_tr['TVT'] 使用
...
if tvt_phys is not None:
    tvt_val = tvt_phys[ridx]      # ← tip-cv では常にこちら
else:
    tvt_val = tvt_selector[ridx]  # ← 真の test 井（train に無い）はこちら = PF
```

`tvt_from_contacts`:

```python
offset = (hw_tr['TVT'] - (ref_tvt - (hw_tr['Z'] - hw_tr[ref_col]))).mean()
return ref_tvt - (hw_tr['Z'] - hw_tr[ref_col]) + offset
```

## ローカル実証（hard20）

| 比較 | 値 |
|---|---|
| tip_train_preds vs `0.3·CF+0.7·phys` | max abs **≈0**（一致） |
| phys 単独 vs 真値 RMSE | **≈0.0055**（ラベルリークでほぼ復元） |
| tip / blend RMSE | **14.8695**（CF 0.3 が悪化要因） |
| train∩local test | 3井（sample_submission も train 内） |
| test CSV の `TVT` / formation tops | **無し**（本番の純 test 井では phys 不可） |

## 含意

| 場面 | 実際に効く面 | init_spr / PF ノブ |
|---|---|---|
| tip-cv / TIP_CV allowlist | **phys（リーク）+ CF** | **見えない**（206 の「不変」の正体） |
| Kaggle 本番の純 test 井 | **PF/selector** | **効く**（ここが本番） |
| train∩test の少数井 | phys（リーク） | 本番でも PF をスキップ |

## 正しい screen

1. **CHK-209:** `TIP_CV_USE_SELECTOR_FACE=True` で tip-cv に PF/selector を強制し、combo（init_spr9×seeds256）を測る  
2. tip-cv の 14.87 を「tip FINAL の PF 性能」と読まない  
3. 上流（sp45/learned）診断も、selector-stop 面が phys なら解釈を誤る

## 禁止（この根因を踏まえて）

- tip-cv phys 面の改善を PF ノブ成功と誤認する  
- tip-cv 14.87 を PF generator の天井と混同する（天井は seed-oracle / selector 面で測る）
