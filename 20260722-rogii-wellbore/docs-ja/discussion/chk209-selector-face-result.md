# CHK-209 結果 — selector 面強制 × init_spr9×seeds256

> Kernel: [tip-cv-sel-face-combo-h20](https://www.kaggle.com/code/kazeneko77/tip-cv-sel-face-combo-h20) Ver1 · COMPLETE · **提出なし**  
> harvest: `exp/work/wave20-upstream/chk209-kaggle-out/`

## 1 行

**selector 面は tip-cv phys 面と別物（全行差異）。**  
combo の hard20 RMSE は **33.54**（phys-blend tip-cv 14.87 より大幅悪化）。  
ただし 14.87 は **TVTリーク phys** なので「combo が悪い」判定には使えない → **selector 面 baseline（4.5×128）との比較が次**。

## 数値

| 面 | hard20 RMSE | vs tip-cv phys-blend |
|---|---:|---|
| tip-cv phys-blend（従来） | **14.870** | — |
| **209 selector-face combo** | **33.541** | maxabs 60.4 · 全行差異 · 0/20 井で phys より良 |

ログ: `selector_face True` · `PF 256-seed` · `STOP_AFTER_SELECTOR` · Physical model 計算は20井（rows は selector 使用）

## 読み

1. **USE_SELECTOR_FACE は効いた**（MD5 ≠ tip-cv · 本番 PF 経路の tip-cv 化に成功）。  
2. phys 14.87 への勝ち負けは **物差し不正**（[`rootcause`](wave20-tipcv-phys-leak-rootcause.md)）。  
3. combo が lik-ensemble 面を良くするかは **CHK-211**（selector-face · init_spr4.5×seeds128）との差分で判定。

## 公平比較（CHK-211 後）

| 面 | hard20 RMSE |
|---|---:|
| 211 baseline 4.5×128 | **33.178** |
| 209 combo 9×256 | **33.541**（Δ **−0.36** · 悪化） |

**combo は tip lik-ensemble 面 NO-GO。** 詳細: [`chk211-selector-baseline-result.md`](chk211-selector-baseline-result.md)

## 判定（更新）

| 仮説 | 判定 |
|---|---|
| tip-cv に selector を載せられる | **GO** |
| combo が phys 14.87 を超える | **無効比較** |
| combo が PF tip 面を改善 | **NO-GO** |