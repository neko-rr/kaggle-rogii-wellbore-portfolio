# L 改善法則 — dual 梯子 最終版（コンペ終了）

> date: 2026-08-06 · **COMP CLOSED** · live dual 確定  
> 数値: 761/782/804/802 · **781** · **784** · faces **041247** · α **0.35**  
> 提出禁止・新規 train なし

---

## 0. 一行（終了結論）

**sample_weight も residual-path soft L\* も Huber loss も、tip-cv 再学習 L では residual Trust（mid+α0.35）を抜かなかった。**  
最終提出は **学習 dual 外の既知面** **666（Trust）+ farvol（Public）** のみ。

---

## 1. Live dual 梯子（hard Δpool · 正=悪化 · 最終）

| rank | CHK | 機構 | hard Δ | hybrid Δ | d\|L−mid\| | 病理 |
|---:|---|---|---:|---:|---:|---|
| 1 最良失敗 | **781** | residual-path soft L\* | **+0.44** | +0.19 | **−0.97** | mild · **F046** |
| 2 | **688** | baseline retrain | **+0.52** | +0.23 | （軽） | residual 微悪化 |
| 3 | **804** | known×Q4 weight | **+0.74** | +0.33 | **−1.43** | mild collapse · **F044** |
| 4 | **802** | MD-Q4 行 weight | **+1.79** | +0.79 | **−4.24** | moderate · **F044 · E2E ABORT** |
| 5 | **782** | resid-drag weight | **+3.81** | +1.71 | **−7.93** | severe · **F044** |
| 6 | **761** | fold-driver weight | **+4.01** | +1.81 | **−7.93** | severe · **F044** |
| 7 最悪 | **784** | Huber loss | **+6.27** | +2.86 | **−4.06** | L 崩壊 · **F045** |

**未 dual:** 777 reg↑（body のみ · 締切）。

---

## 2. 採用法則

| # | 法則 | 根拠 | 終了時 |
|---|---|---|---|
| **L1** | residual RMSE（α0.35）必須 · TVT-OOF 単独 GO 禁止 | 全 dual | 維持 |
| **L2** | \|L−mid\| 下落 = mid-collapse シグナル | 761–802 · 784 | 維持 |
| **L3** | hard/Q4/MD-Q4 **sample_weight** は residual に伝わらない | F044 | **閉** |
| **L4** | offline oracle ≠ live dual 符号 | Pack D −3.03 vs 781 **+0.44** | **確定** |
| **L5** | hurt 井の単純 upweight 禁止 | 688hurt | 維持 |
| **L6** | hard + Q4 SSE 尾 dual 必須 | 813 | 維持 |
| **L7** | residual-path offline 天井は live で未再現 | 781 NOGO · **F046** | **閉** |
| **L8** | GR 本命禁止 · 特徴は dual 後 | — | 未検証のまま終了 |
| **L9** | mid 先改修で L 救済しない | F015 | 維持 |
| **L10** | α 触らない | F043 Public 梯子 | 維持 |
| **L11** | Huber/MAE 等 **loss 形 1 機構** は residual で壊滅しうる | 784 hard+6.3 | **F045 閉** |

---

## 3. Final との関係

| 面 | 役割 |
|---|---|
| **666** residual α0.35（旧 L） | Trust 枠1 · Public NO-GO のまま採用 |
| **farvol** | Public 枠2 · **6.190** Best |
| 新 L residual E2E | dual GO 無しのため **0 本** |

---

## 4. 禁止まとめ

- F044 weight 言い換え / dual NOGO 後 E2E  
- F045 Huber/Fair/MAE loss 形言い換え再学習  
- F043 α 梯子 / F015 生 Soft·L·mid FINAL  
- residual-path 言い換え（781 · **F046**）  
- failures: F043 / F044 / **F045** / **F046**

---

## 参照

| 用途 | パス |
|---|---|
| exp-index（現在地） | [`../exp-index.md`](../exp-index.md) |
| 781 dual | [`../work/out-t3-cpu-harvest/l-dual-CHK-781-kaggle-v1/report.md`](../work/out-t3-cpu-harvest/l-dual-CHK-781-kaggle-v1/report.md) |
| 784 ops | [ops-784](ops-chk784-dual-nogo-2026-08-05.md) |
| failures | F043 / F044 / **F045** / **F046** · [`../improvement-loop-failures.json`](../improvement-loop-failures.json) |
| archive | [`../checklist-archive.md`](../checklist-archive.md) |
