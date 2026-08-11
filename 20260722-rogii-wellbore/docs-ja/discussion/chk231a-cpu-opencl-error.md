# CHK-231a ERROR — tip-cv on CPU without LGBM device patch

> date: 2026-07-27 · slug `kazeneko77/tip-cv-cpu-w055-h20-chk-231a`

**ERROR:** `LightGBMError: No OpenCL device found`（In[14] LGBM `device`/`device_type=gpu`）

tip パイプラインは LGBM/CatBoost が **GPU 前提**。Kaggle CPU 枠（`enable_gpu:false`）では OpenCL が無く即死。

## 対応

- tip-cv ノブは **GPU×2** で再実行: `tip-cv-gpu-w055-h20` · `tip-cv-gpu-var-s5-h20`
- CPU 用 builder に `device_type/device/task_type → cpu` 強制パッチを追加（`build_tip_cv_cpu_knob.py`）
- 旧 CPU×4（未パッチ）は同様に ERROR 見込み → 枠解放後に `tip-cv-cpu2-*` を投入

## 判定

提出・tip-cv 採点には使わない（完走せず）。
