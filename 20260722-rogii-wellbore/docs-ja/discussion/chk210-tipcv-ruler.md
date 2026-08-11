# tip-cv 物差し（CHK-210）— 本番同型で測る

> SSOT · updated: 2026-07-26 · CHK-210  
> 関連: [`wave20-tipcv-phys-leak-rootcause`](wave20-tipcv-phys-leak-rootcause.md) · selector baseline [`chk211`](chk211-selector-baseline-result.md)

## 初学者向け要約

- **旧 tip-cv** は「リーク付き物理モデル＋CF」を測っていた（14.87）。本番の多くの test 井とは別物。  
- **新 tip-cv（本物差し）** は本番と同じく **PF/selector 面**を測る。hard20 基準値は **33.178**（CHK-211）。  
- 14.87 を PF 改善の指標に使わない。

## 既定フラグ（TIP_CV_MODE 時）

| フラグ | 既定 | 意味 |
|---|---|---|
| `TIP_CV_DISABLE_PHYS` | **True** | train 井でも `tvt_from_contacts`（TVTリーク）を使わない |
| `TIP_CV_USE_SELECTOR_FACE` | **True**（推奨） | rows に selector を明示使用 |
| `TIP_CV_STOP_AFTER_SELECTOR` | 診断時 True | learned/test-id 経路で落とさない |

## ビルダー

| 用途 | スクリプト |
|---|---|
| 標準 tip-cv | `exp/work/build_tip_train_cv_nb.py` |
| Wave-20 診断 | `exp/work/wave20-upstream/build_tip_cv_*.py` |

## 受け入れ（CHK-210）

- [x] tip-train-cv / wave20 ビルダーに phys 無効既定を反映  
- [x] 本ファイルを SSOT として checklist からリンク  
- [x] 「14.87 = tip PF」誤解を Explicit Stop に明記済み
