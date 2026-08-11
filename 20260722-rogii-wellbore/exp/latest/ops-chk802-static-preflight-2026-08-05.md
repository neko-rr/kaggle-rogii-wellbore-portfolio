# CHK-802 静的検査結果（2026-08-05）

> 実行前ゲート · **GPU 未起動** · 提出禁止

## 結果

| 検査 | コマンド / 成果物 | 結果 |
|---|---|---|
| body 生成 | `build_chk802_from_804.py` → `_colab_main_body_chk802.py` · `colab-chk802-l1-hard20-driver.py` | OK |
| **CHK-802 preflight** | `run_chk802_preflight.py` | **PASS** |
| **CHK-802 extra** | `run_chk802_extra_static.py`（weight 帯 10/10/60 · markers） | **PASS** |
| CHK-804 回帰 | `run_chk804_preflight.py` | PASS（互換維持） |
| dual 静的 | `run_dual_static_preflight.py` | PASS |
| hypothesis-ban pre | `run-hypothesis-ban-gate.ps1 -ChkId CHK-802 -ActionType T3 … -ExpDir .\20260722-rogii-wellbore\exp` | **PASS** |

## 静的で確認した点

- `g = globals()` 禁止 / `exec` を g に固定しない  
- STOP/FORCE: BEFORE_HEDGE=False · STOP_AFTER_LEARNED=True · FORCE_RETRAIN=True  
- **WORK_DIR = Drive `RUN_DIR/work`** · `/content/chk*_work` なし  
- tip-cv patch 対象（train_stack / GroupKFold / FORCE raise / fit）残存  
- `ensure_koolbox_real` + fallback shim 検知  
- weight map **80 井** · n(2.0)=**10** · n(1.5)=**10** · n(1.0)=**60** · SSOT JSON と一致  
- AST compile（`google.colab` スタブ）  

## 生成物

- `exp/work/colab-final-t2/_colab_main_body_chk802.py`  
- `exp/work/colab-final-t2/colab-chk802-l1-hard20-driver.py`  
- 検査: `run_chk802_preflight.py` · `run_chk802_extra_static.py`

**Colab 本実行は上記 PASS 後のみ。** 指示があれば起動します。
