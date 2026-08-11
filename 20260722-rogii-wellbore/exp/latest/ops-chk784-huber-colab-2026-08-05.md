# OPS · CHK-784 Huber loss · Colab Trust CV screen · 2026-08-05

> **lane:** Colab GPU · Trust residual dual のみ  
> **orthogonal / no-overlap:** 781 residual-path（Kaggle）· 802 weight（閉）· F044 · Submit 全部外  
> **session owner:** this Colab CV session only

---

## 仮説（1機構）

| 項目 | 内容 |
|---|---|
| ID | **CHK-784** |
| type | T3 |
| 機構 | LightGBM `objective=huber` · `alpha=0.9` · **sample_weight なし** |
| screen | FAST2 = 2-fold · LGB×1 · n_est200 · CB skip · hard20 · FORCE retrain · STOP_AFTER_LEARNED |
| 期待 | mean_worst / hard 帯が RMSE objective より先に下り、residual dual（813/815）が動く |
| ban-gate pre | **PASS** 2026-08-05 |

## NOT this session

| 仕事 | owner |
|---|---|
| 781 train / dual / E2E | **他セッション（Kaggle GPU）** |
| 802 residual E2E / weight 再実行 | **禁止** |
| Public residual ladder / Final2 swap | **禁止** |
| sample_weight L1 live | **F044 閉** |

## 実行順

1. Drive へ body 書込: `_colab_main_body_chk784.py`
2. Colab: body exec → face を `runs/*chk784-huber*/faces/`
3. Desktop harvest face（Drive sync 後）
4. `run_l_residual_local_dual.py` · faces SSOT **20260804-041247** · α0.35 · 813/815
5. ban-gate **post** GO/NOGO · OOF 単独 GO 禁止

## acceptance（Trust dual only）

| 定規 | 厳 | 緩め WATCH |
|---|---|---|
| hard_plane pool | Δ ≤ 0 vs faces 基準 dual | ≤ +0.15 |
| mean_worst | ≤ 0 | WATCH |
| max_band | 非悪化 | |
| 815 mid-collapse | **FAIL if collapse** | d\|L−mid\| 激減 |

## 成果物パス

| 役割 | path |
|---|---|
| body | `exp/work/colab-final-t2/_colab_main_body_chk784.py` |
| upload oneshot | `exp/work/colab-final-t2/_b64p/chk784_hex_shards/one_shot_upload.py` |
| runs | Drive `.../colab-final-t2/runs/*chk784-huber*/` |
| dual report | 後続 `latest/ops-chk784-colab-dual-*.md` |

## 状態

- **body on Drive:** `.../colab-final-t2/_colab_main_body_chk784.py` (**31622** · catbox `lmrbtm.py` · syntax OK)
- **train 途中:** run `20260805-135927-chk784-huber-hard20-fast2` · tip-cv cells 通過 · **train_stack start で MCP 切断**（DONE/FACE 未確認）
- **2026-08-06 00:30JST:** Colab kernel がセル実行を受け付けず（execution_count=null · 出力空）— **Runtime > Interrupt / Restart が必要な可能性**
- **次:** kernel 復帰 → EXEC body 再実行（FORCE retrain）→ face → dual 813/815
- submit: **FORBIDDEN**
- **overlap ban:** 781 Kaggle · 802 weight/E2E · not this session
