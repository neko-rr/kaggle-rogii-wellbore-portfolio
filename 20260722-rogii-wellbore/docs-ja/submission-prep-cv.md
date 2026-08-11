# 提出準備 CV — 手順 SSOT（初学者向け）

> updated: 2026-07-23  
> checklist: **CHK-014**  
> tip: `kazeneko77/rogii-luck-is-all-you-need-private-tip-fork`  
> CV NB: `kazeneko77/tip-train-cv-allowlist`

## なにを判定するか

| チェック | 意味 |
|---|---|
| **Smoke 提出（1回）** | tip が自分の Kaggle で動くか・Public が作者帯に近いか |
| **tip CV** | train の評価区間で tip 予測を測り、**同じ井の CF より良いか**・難井が壊れていないか |

**追加の LB 提出は tip-cv-report が PASS のときだけ。** FAIL でも改善実験（CHK-020）は可。

**Public / CV / Private の読み方:** [`cv-lb-private-relation.md`](cv-lb-private-relation.md)  
— tip smoke と Best の **~0.05 差は seed バンド扱い**。採択は tip CV（相対）優先で、Public 順位最適化はしない。

**用途別 Tier:** [`cv-tiers.md`](cv-tiers.md) — hard20 は T0/T1。graft 本採用は **T2（方位層化≈80井）**、Final は **T3（3 seed）**。  
**T3 注意:** 表の T3＝フル tip×3 seed（重い）。固定 faces 上の残差 multi-seed は **T3-B（秒〜分）** で fold 安定監査向き。**T2 上位互換・井増加ではない** — 詳細は [`cv-tiers.md`](cv-tiers.md) §「T3 の2種」。

## ファイル地図

| パス | 役割 |
|---|---|
| `my-local-eval-notebook/wave0-ruler/score_tip_cv.py` | 採点器（CPU） |
| `my-local-eval-notebook/wave0-ruler/build_tip_cv_allowlist.py` | 難井20±サンプル allowlist |
| `my-notebook/tip-train-cv-allowlist/` | tip を train allowlist で回す Private GPU NB（**主レーン**） |
| `my-local-eval-notebook/tip-train-cv-colab/` | 同上の **Colab バックアップ**（再失敗／9h 超時） |
| `exp/work/wave0-ruler/tip-train-preds.csv` | tip の train 予測（harvest） |
| `exp/work/wave0-ruler/tip-cv-report.json` | PASS/FAIL 判定 |

レーン判断: [`tip-cv-kaggle-vs-colab.md`](tip-cv-kaggle-vs-colab.md)

## 手順 A — tip CV（GPU → ローカル採点）

```powershell
# 1) allowlist（hard20 疎通 → 必要なら hard20_sample）
python .\20260722-rogii-wellbore\my-local-eval-notebook\wave0-ruler\build_tip_cv_allowlist.py --phase hard20
# NB 再生成が必要なら:
python .\20260722-rogii-wellbore\exp\work\build_tip_train_cv_nb.py
.\scripts\assert-kaggle-private.ps1 -KernelDir .\20260722-rogii-wellbore\my-notebook\tip-train-cv-allowlist
.\scripts\kaggle-cli.ps1 kernels push -p .\20260722-rogii-wellbore\my-notebook\tip-train-cv-allowlist

# 2) 完走後 harvest
.\scripts\kaggle-cli.ps1 kernels output kazeneko77/tip-train-cv-allowlist -p .\20260722-rogii-wellbore\exp\work\wave0-ruler\tip-cv-out
Copy-Item .\20260722-rogii-wellbore\exp\work\wave0-ruler\tip-cv-out\tip_train_preds.csv `
  .\20260722-rogii-wellbore\exp\work\wave0-ruler\tip-train-preds.csv

# 3) 採点
python .\20260722-rogii-wellbore\my-local-eval-notebook\wave0-ruler\score_tip_cv.py `
  --preds .\20260722-rogii-wellbore\exp\work\wave0-ruler\tip-train-preds.csv `
  --out .\20260722-rogii-wellbore\exp\work\wave0-ruler\tip-cv-report.json
```

### 手順 A′ — Colab バックアップ（Kaggle 再失敗／9h 超時）

1. Cursor で `my-local-eval-notebook/tip-train-cv-colab/tip-train-cv-colab.ipynb` を開く  
2. Select Kernel → **Colab** → GPU（Skill `cursor-colab-runtime`）  
3. Bootstrap セル（`kaggle.json` 要）→ 続けて Run All → `tip_train_preds.csv`  
4. ローカルへコピー後、上記手順 A の採点（`score_tip_cv.py`）と同じ  

詳細: [`tip-cv-kaggle-vs-colab.md`](tip-cv-kaggle-vs-colab.md)

### PASS 条件

1. tip pooled RMSE **&lt; 同じ井集合の CF pooled**
2. hard-set 平均の悪化 **≤ 0.1**（tip − CF）
3. 予測カバー率 **≥ 99%**

## 手順 B — Smoke 提出（Notebook 紐づけ・今回1回）

1. ローカル `submission.csv` を validator PASS  
2. UI「Submit to Competition」または CLI `-k` / `-v`（**自 tip fork のみ**）  
3. `docs-ja/submission-validations/` と `exp-infer.md` に記録  
4. Public LB は参考。**次提出の可否は tip-cv-report のみ**
5. **採点待ち:** 提出後の Public 確定は **7 時間以上**かかることがある（2026-07-23 観測 · SSOT [`submission-rules.md`](submission-rules.md) §提出後の採点待ち）。PENDING 中も tip-cv は進めてよい

## 既知の落とし穴（Ver2 失敗）

`test_wells = ...` と `for wid in test_wells` は **同一セル**。セルの後ろにパッチを置くとループ後になり無効。  
`build_tip_train_cv_nb.py` は **セル内の test_wells= 直後に inject**し、セル末尾で `tip_train_preds.csv` を書いて `SystemExit(0)` する（Ver3+）。
