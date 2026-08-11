# 全実験マップ — 工程別（CHK 〜675）

> **Canvas:** [`full-pipeline-experiment-map.canvas.tsx`](<cursor-workspace>/canvases/full-pipeline-experiment-map.canvas.tsx)  
> **updated:** 2026-08-04 午後（**Final Push · 519–675 · residual/Public**）  
> 井ヒート本命: [`pipeline-stage-well-map-2026-08-03.md`](pipeline-stage-well-map-2026-08-03.md)  
> 件数は archive / checklist からの **概算**（厳密一意割当ではない）

---

## なぜ図が「薄く」見えるか

| 見え方 | 実態 |
|---|---|
| 井ヒートが 1 本 | 採用候補の説明用（S9 mid/H-D 年代）|
| 500 番台が薄く見えた | 400 までで別レーン閉鎖後にゲートに絞った |
| **600 番台が増えた** | Final Push: residual dual · soft dump · Public 診断 · 上流 dump |

---

## 量の事実（概算）

| 指標 | 値 |
|---|---|
| unique CHK 言及 | **~350+**（0〜675 帯） |
| hyperparameter 行 | **~420+**（2026-08-04） |
| 失敗型 | **F001–F042** |
| 厚い帯 | 200 · 300 · 400 · **600 Final Push** |
| Active 主線 | 643 → 673 · residual 666 · 枠2 farvol |

---

## 工程別（要約 · 工程順）

| 順 | 工程 | だいたいの量 | 残ったもの / 直近 |
|---|---|---:|---|
| 0 | **S0** selector / tip 温度 | 多 | T0.15 tip · 456/490b 信号 |
| 1 | **S0′** E2E 診断 | 中 | cascade §0 · FINAL≡tip は失敗ではない |
| 2 | **S1–S2** 生 L/soft | 中 | **生 FINAL 禁止** · 工程改善は 519–570 / residual で再開 |
| 3 | **S3–S8** 後段スタック | 中 | mid 親 · **643 dump 中（個別面）** |
| 4 | **S9 ゲート** | 中〜多 | agree/row/HD · T2 では絞り損 · hard20 旧 H-D は 514 Public NO-GO |
| 5 | **S9 residual / tip⊕gate** | **Final Push 厚** | **666 GO_e2e** · 668 map · 641/660 · 541/558b/618c Public |
| 6 | **B0** Public ブレンド | 中 | **farvol 6.190 枠2** · SE 無効 |
| 7 | **Gen\*** 上流代替 | 多 | ほぼ NO-GO · F022– |
| 8 | **Bridge\*** Soft/橋 | 多 | F041 · soft 注入 **620 NOGO** |
| 9 | **Geom\*** 幾何 | 最大 | Wave-25–29 閉鎖 |
| 10 | **Upstream final** | 進行中 | **670–675 規律** · **643→673** · 626 待ち |

「同じ実験ばかり」ではなく、**別レーンを潰してから residual / Public / 上流 dump に絞った**。

---

## Wave 年表（追記）

| Wave | CHK | 主題 | 結果 |
|---|---|---|---|
| W0–11 | 〜162 | ruler / tip 門番 | tip・gated 基盤 |
| W12–19 | 160–202 | gated · farvol · mid soft | portable 微改善 |
| W20 | 203–231 | lik_temp · selector | T0.15 Best |
| W21–24 | 232–296 | 上流/橋/生成器 | 全滅 F027–F035 |
| W25–29 | 297–382 | 難井 · ねじれ | F036–F041 |
| W30 | 390–410 | Soft-Preserve | F041 |
| W31a–c | 411–470 | cascade · 親差し替え | P-461/468 |
| W31d–e | 471–518 | 勝ち分ゲート · 提出 | H-D / 514–515 |
| **W31f Final Push** | **519–675** | soft dump · residual · Public 診断 · 上流 dump | **下記** |

### Final Push（519–675）ハイライト

| 帯 | 結果 |
|---|---|
| 541 / 558b / 579 | Public **6.256 / 6.238 / 6.277** · 枠2NO · row STOP |
| 618c | Public **6.231** · tipdist 11.9 · Soft FINAL 禁止 |
| 620 | soft→mid T2 **12.907 NOGO** · 閉鎖 |
| 641 / 644 / 660 | residual 梯子 · 641 診断提出 · 644 train-only |
| **641 residual** | Public **6.472** NO-GO · T2 10.309 | Trust のみ · 再提出禁止 |
| **666 / 668** | GO_e2e / map · 提出禁止 | help 77/3 · 71/9 |
| 650–657 · 651–654 | match / heel / lateral · 層別 NOGO 寄り |
| **643** | stage dump Ver2 **RUNNING** → 673 |
| 670–675 | 上流規律 applied |

---

## 本命に残っている「細い束」（全体のごく一部）

```
枠2 Public:  farvol B0
枠1 Trust:   residual 666 候補  または  上流 643→新面（未完）
土台:        tip S0 + mid 材料（生 FINAL 禁止）
診断閉鎖:    薄 mid gate · soft 注入 · tip|mid 切替 · HD 連打
```

---

## 関連

| 目的 | パス |
|---|---|
| checklist | [`../experiment-checklist.md`](../experiment-checklist.md) |
| 工程内 | [`../within-stage-comparisons.md`](../within-stage-comparisons.md) |
| 工程×井 | [`pipeline-stage-well-map-2026-08-03.md`](pipeline-stage-well-map-2026-08-03.md) |
| hyperparameter | [`../hyperparameter-table.md`](../hyperparameter-table.md) |
