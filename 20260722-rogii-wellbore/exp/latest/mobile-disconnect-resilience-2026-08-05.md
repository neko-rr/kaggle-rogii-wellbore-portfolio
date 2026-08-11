# 移動・切断レジリエント — 実験継続ノート（2026-08-05 17:4x）

> **目的:** PC移動で Cursor/MCP が切れても、**成果物は Drive / ローカル Desk に残る**ようにする  
> **提出禁止** · **Kaggle GPU 新規 push 禁止** · 実験 GPU = **Colab L4**

---

## LIVE → DONE（2026-08-05 夜）

| 項目 | 値 |
|---|---|
| **804 run_id** | **`20260805-073247-chk804-l1-hard20`** · **COMPLETE** |
| Drive face | `…/runs/20260805-073247-chk804-l1-hard20/faces/learned_trajectory_submission.csv` |
| **Desktop face** | `exp/work/out-t3-cpu-harvest/chk804-colab-face-20260805/learned_trajectory_submission.csv`（sha256 一致） |
| dual | **NOGO_L1** · hard Δ**+0.74** · d\|L−mid\| **−1.43** · [ops](ops-l1-chk804-colab-dual-2026-08-05.md) |
| 次 | **Colab 802**（Desktop SSOT + Drive body パターン再使用） |
| 切断 | Cursor 落ちて可 · **成果は Desktop dual + face に既存** |

---

## いまどこに何があるか（永続）

| 役割 | 永続場所 | 状態 |
|---|---|---|
| 現在地 SSOT | Desktop `…/exp/exp-index.md` | Best / 次アクション |
| 作業キュー | Desktop `…/exp/experiment-checklist.md` | Active |
| セッション橋 | Desktop `…/exp/latest/session-bridge-cpu-to-gpu-2026-08-05.md` | Colab 本線 |
| **本ファイル** | Desktop `…/exp/latest/mobile-disconnect-resilience-2026-08-05.md` | 移動時必読 |
| **761 dual** | Desktop `…/exp/work/out-t3-cpu-harvest/l-dual-CHK-761-harvest/` | **NOGO** · hard Δ+4.01 · mid-collapse |
| **782 dual** | Desktop `…/exp/work/out-t3-cpu-harvest/l-dual-CHK-782-harvest/` | **NOGO** |
| 761/782 harvest faces | Desktop `…/watch-v2-20260805/harvest-761|782/` | learned CSV あり |
| ops 統合 | Desktop `…/exp/latest/ops-l1-chk761-782-harvest-dual-2026-08-05.md` | |
| **Colab driver body** | **Drive + Desktop** `…/colab-final-t2/_colab_main_body.py` | WORK_DIR=Drive `RUN_DIR/work` |
| **Colab 804 run**（学習出力） | **Drive only** `…/runs/20260805-073247-chk804-l1-hard20/` | `logs/` · `checkpoints/status.json` · `faces/` · **`work/`** |
| residual faces SSOT | Desktop `…/runs/20260804-041247/faces/` | dual 尺 |
| dual 脚本 | Desktop `…/out-t3-scratch/run_l_residual_local_dual.py` | 813/815 込 |
| 814/816 map | Desktop `…/chk814-816-maps-20260805/` | after-804 |

**揮発（使わない）:** `/content/*` のみ · `/tmp/*` · Colab セッション RAM だけの変数

---

## Colab で実行するとき（切断後の再開含む）

1. Runtime → **GPU L4** 接続（**既存 073247 が走っていれば Runtime 再起動しない**）  
2. セル順: **koolbox READY** → **main**（Drive の `_colab_main_body.py` を exec）  
3. 進捗確認（カーネルが空いているとき別セル可）:
   - `runs/20260805-073247-chk804-l1-hard20/checkpoints/status.json`
   - `…/logs/chk804-l1.log`
   - face: `…/faces/learned_trajectory_submission.csv` または `work/learned_trajectory_submission.csv`
4. **メイン学習中は同一カーネルで status セルがブロック**される → タブ左出力 or 再接続後 status  
5. **MCP/Cursor 切断してもタブを残せば学習継続**（`status.json` / log は cell 境界で Drive へ）  
6. 完走後: Colab で `faces/learned*.csv` を確認 → Desktop へコピー →  
   ```powershell
   cd 20260722-rogii-wellbore\exp\work\out-t3-scratch
   python run_l_residual_local_dual.py --learned <path\to\learned.csv> --tag CHK-804-colab
   ```

### 必須ポリシー

- **WORK_DIR = `RUN_DIR/work`（Drive 下）** · `/content/chk804_work` は禁止  
- Kaggle GPU auto-push **禁止**（watcher kill 済 · `ALLOW_KAGGLE_GPU_PUSH=False`）

---

## 実験キュー（再開用）

```text
DONE: 761 · 782 · 804 = L1 NOGO（いずれも mid-collapse 系）
NOW:  Colab 802 MD-Q4 hard20 → Drive faces → Desktop dual
NEXT: 809 → 806 · weight3 → 808→781(+805)
STOP: 提出 · tip⊕ · residual α · Kaggle 新規 L1 · GR · 804 再言い換え
```

---

## 別 Agent 起動時の手順（コピー用）

1. 本ファイルと `session-bridge` を読む  
2. Drive `runs/*chk804*` の status/log を確認  
3. face あれば dual · なければ Colab 再 run（body は Drive から）  
4. 結果は Desktop `exp/work/out-t3-cpu-harvest/` + exp-index/checklist 更新  

updated: 2026-08-05 夜 · **804 dual NOGO 永続済 · next 802**
