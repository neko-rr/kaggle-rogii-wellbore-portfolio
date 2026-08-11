# CHK-206 結果 — tip init_spr=9 hard20

> 作業: [`exp/work/wave20-upstream/`](../../exp/work/wave20-upstream/)  
> Kernel: [tip-cv-init-spr9-h20](https://www.kaggle.com/code/kazeneko77/tip-cv-init-spr9-h20) · **提出なし**

## 1 行

**Ver1/Ver2 とも tip-cv hard20 出力 ≡ baseline（RMSE 14.8695 · MD5 一致）。**  
これは init_spr 無効ではなく、**Physical model 成功時に `rows` が PF/selector を使わない**ため。  
Ver2 は literal 9.0 + selector-stop で完走（learned Blend ERROR 回避）。

## 事実

| 項目 | Ver1 | Ver2 |
|---|---|---|
| init_spr | `globals().get(..., 9.0)` | **literal 9.0**（ログ確認） |
| stop | なし → Blend ERROR | **STOP_AFTER_SELECTOR** 完走 |
| tip_train_preds vs baseline | MD5 一致 | MD5 一致 `4ed07e7a…` |
| hard20 RMSE | 14.8695 | 14.8695 |

## 根因（Ver2 で確定）

```python
if tvt_phys is not None:
    tvt_val = float(tvt_phys.iloc[ridx])   # ← 全 hard20 で Physical model OK
else:
    tvt_val = float(tvt_selector[ridx])    # PF はここにしか乗らない
```

ログは全井 `Physical model OK` + `PF 128-seed OK`。PF は計算されるが tip-cv 提出面（rows）に入らない。  
ローカル tip 型 PF では init_spr 4.5 vs 9 で ensemble が動く → ノブ自体は生きている。

## 読み

1. tip-cv early-exit / selector-stop の物差しでは **init_spr を評価できない**（phys 面）。  
2. generator 命中（207/208）の tip screen は **selector 面強制**か train-id 対応 full E2E FINAL。  
3. 本番 tip も同分岐なら、init_spr は phys 失敗井と後段にしか効かない。

## 補足（深掘り）

tip-cv 出力は **`0.3·CF + 0.7·phys` と数値一致**。phys の offset は train 真値 `TVT` 依存（リーク）。  
詳細: [`wave20-tipcv-phys-leak-rootcause.md`](wave20-tipcv-phys-leak-rootcause.md)

## 次

- combo を tip CFG に載せない（公平比較 NO-GO）  
- **CHK-210** · **CHK-205**（承認後）  
- 詳細: [`chk211-selector-baseline-result.md`](chk211-selector-baseline-result.md)
