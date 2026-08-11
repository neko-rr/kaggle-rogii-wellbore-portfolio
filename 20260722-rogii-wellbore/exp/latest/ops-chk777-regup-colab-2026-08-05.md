# OPS · CHK-777 reg↑ · Colab Trust CV · after 784 NOGO

> orthogonal: ≠781 residual-path · ≠784 Huber/MAE · ≠F044 weight · **submit forbidden**

| 項目 | 内容 |
|---|---|
| ID | **CHK-777** |
| T3 hyp | reg↑ で mean_worst を残差 dual と同方向に改善 |
| params | `reg_lambda=30` · `reg_alpha=1.0` · `min_child_samples=60` · **objective=regression** · FAST2 hard20 |
| ban-gate pre | **PASS** 2026-08-05 |
| prior | 784 NOGO dual hard **+6.27** — loss 帯閉鎖 |

## 実行

1. body: `_colab_main_body_chk777.py` · catbox `g9wbeg.py`
2. Colab train → faces
3. dual 813/815 · faces SSOT 041247 · α0.35
4. post ban-gate

## 状態（終了）

| 項目 | 値 |
|---|---|
| dual | **未実施** |
| verdict | **incomplete · 締切停止** |
| train | body 準備のみ · Colab フル train **未完** |
| submit | **FORBIDDEN** |
| archive | [`checklist-archive.md`](../checklist-archive.md) 2026-08-06 節 |

- **784 DONE dual NOGO** · hard Δ**+6.27** · mid-collapse · F045  
- **777 body ready:** local `exp/work/colab-final-t2/_colab_main_body_chk777.py` · catbox `g9wbeg.py` (32066)  
- コンペ終了のため **再起動・dual は行わない**
