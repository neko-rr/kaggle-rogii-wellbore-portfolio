# CHK-204 結果 — 上流ギャップ × portable ゲート

> date: 2026-07-26 · ローカル CPU · **提出なし**  
> 数値: [`chk204-report.json`](../../exp/work/wave20-upstream/chk204-report.json)  
> 入力: CHK-203 partial `chk203-tip_train_preds_selector.csv` ≡ `chk203-sp45_preds.csv`（T2 80井）

## 1 行

**NO-GO。** tip-cv 経路では `sp45_projection_submission` が selector 保存物と **同一**（pooled 8.330 ≡）で、回収できる上流ギャップが無い。learned は test-id で tip-cv 計測不能（203/203b）。

## 数値

| 面 | pooled RMSE |
|---|---:|
| selector | **8.330** |
| sp45 | **8.330**（≡） |
| stage-oracle | **8.330**（≡） |
| frac wells sp45 better | **0** |

どの portable ゲート（tip_std / n_eval / md_span）も Δpool = 0。acceptance（Δpool≥+0.05）未達。

## 判定

| 仮説 | 判定 |
|---|---|
| 上流ギャップをゲート特徴のみで ≥+0.05 | **NO-GO** |
| 薄混ぜ再発明 | **禁止継続**（CHK-202 と同型） |

## Explicit Stop

- selector≡sp45 のまま「上流ブレンド」を繰り返さない
- learned を tip-cv で無理に混ぜない（F015）
