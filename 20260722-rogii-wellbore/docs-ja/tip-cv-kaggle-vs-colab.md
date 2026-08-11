# tip-train-cv — 実行レーン判断（Kaggle vs Colab）

> CHK-014 · updated: 2026-07-23

## 結論（今回）

| レーン | 役割 |
|---|---|
| **Kaggle GPU（主）** | tip と同依存 DS が既にマウント済み。`tip-train-cv-allowlist` **Ver3**（セル内 inject 修正）を完走させる |
| **Google Colab（副）** | Ver3 が再失敗、または hard20+sample が 9h 超のときのバックアップ |

**理由:** tip は koolbox / ravaghi / fleongg / model-package 等に依存。Kaggle なら metadata の dataset_sources でそのまま使える。Colab は同じ DS を API DL か手動配置する必要があり、初回セットアップが重い。

## Colab を使うとき（ユーザー操作）

Skill: `cursor-colab-runtime`（Agent は UI 接続不可）

1. Cursor で [`my-local-eval-notebook/tip-train-cv-colab/tip-train-cv-colab.ipynb`](../my-local-eval-notebook/tip-train-cv-colab/tip-train-cv-colab.ipynb) を開く
2. Select Kernel → **Colab** → GPU
3. セル0の案内に従い、**competition `train/`** をランタイムから読めるようにする（Mount Server → `sample_data/`、または Drive）
4. 依存 DS が無い場合はセルの `kaggle datasets download`（要 `kaggle.json`）を実行
5. 完走後 `tip_train_preds.csv` をローカル `exp/work/wave0-ruler/` へコピー
6. `score_tip_cv.py` で採点（CPU・ローカル）

## Kaggle 継続手順

```powershell
.\scripts\kaggle-cli.ps1 kernels status kazeneko77/tip-train-cv-allowlist
# COMPLETE 後:
.\scripts\kaggle-cli.ps1 kernels output kazeneko77/tip-train-cv-allowlist -p .\20260722-rogii-wellbore\exp\work\wave0-ruler\tip-cv-out
```

ログに **`TIP_CV inject OK test_wells 20`** が **Processing 1/20** より前に出ること。  
（Ver2 失敗原因: inject がループ後だった）
