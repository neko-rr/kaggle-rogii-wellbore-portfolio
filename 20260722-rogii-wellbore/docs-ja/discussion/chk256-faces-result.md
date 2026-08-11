# CHK-256 結果 — tip 内部面 tip-cv hard20（2026-07-28）

> kernel: `tip-cv-chk256-faces-h20` Ver1/Ver2（audit UnboundLocal で score セル未達）  
> 採点: ローカル train TVT × Ver2 成果物 · **提出なし** · F015  
> 数値: [`chk256_face_report.json`](../../exp/work/wave22-candidates/chk256_face_report.json)

## 1 行

**案Cの「内部面天井」は tip-cv 上で見つからない。**  
selector≡sp45≡gold≡before_hedge（pool **30.089**）。learned は計測不能。  
FINAL（hedge 後）は 1井だけ微改善（pool **30.072** · Δ+0.017）→ **昇格候補にならない**。

## tip-cv（eq-well RMSE · hard20 · T0.15）

| 面 | pool | Δ vs selector | beat wells |
|---|---:|---:|---:|
| selector | **30.089** | 0 | 0 |
| sp45 / gold_* / before_hedge | 30.089 | 0 | 0 |
| learned | — | — | unmeasurable（test-id） |
| mpkg_* | — | — | tip-cv 下 disable（Ver2） |
| **final**（hedge 後 submission） | **30.072** | **+0.017** | **1/20**（`2fd68f7b` +0.42） |

凍結 tip-cv 29.899 との差は集約差帯。**面間差ゼロ（hedge 除く）**が主結論。

## test 多様性（参考 · ラベル無し）

before_hedge↔FINAL RMSE **0.968**（Public pre-BH 6.653 / F015 と整合）。  
tip-cv では before_hedge≡selector のため、test 差分は本番後段の挙動差。

## 判定

| 項目 | 結果 |
|---|---|
| acceptance（面×井表） | **PASS** |
| 案C「FINAL を超える内部面」 | **NO** |
| 次分岐 | **C 薄く** · **A（CHK-261→）厚く** · 257/263 は低優先 |

## Explicit

- 内部面の E2E 昇格（257/263）は **根拠なし**（F015 再確認）
- Ver3（audit 修正のみ）は **不要**（採点済み）
