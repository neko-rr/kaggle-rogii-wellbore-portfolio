# CHK-781 dual 後工程 — 最適化（2026-08-05）

> **SSOT:** 本ファイルが **781 COMPLETE 以降**の唯一手順。  
> 802 確定後: [`ops-chk802-post-pipeline-2026-08-05.md`](ops-chk802-post-pipeline-2026-08-05.md) · **F044 weight 全閉**  
> dual コード: [`../work/out-t3-scratch/run_l_residual_local_dual.py`](../work/out-t3-scratch/run_l_residual_local_dual.py)  
> E2E 雛形: [`../../my-notebook/tip-e2e-chk781-mid-a035-l-resid/`](../../my-notebook/tip-e2e-chk781-mid-a035-l-resid/)  
> train: [`../../my-notebook/tip-cv-chk781-resid-path-h20/`](../../my-notebook/tip-cv-chk781-resid-path-h20/)  
> 提出禁止 until dual **GO** + ユーザー明示

**最適化の前提（802 後）**

| 閉じたこと | 後工程での扱い |
|---|---|
| F044 weight 5 本 NOGO | **再学習・言い換え 0** |
| 802 residual E2E | **作らない・触らない** |
| F043 α | dual / E2E とも **α=0.35 固定** · regrid 禁止 |
| tip⊕ / 生 mid · Soft FINAL | **禁止**（F015） |
| POST-L フル梯子 | **締切モードでは GO 時も圧縮**（下 §3） |

---

## 0. 分岐図（dual 直後）

```text
781 tip-cv COMPLETE
  │
  ├─① harvest learned face（必須）
  ├─② dual 810/812/813/815（必須 · 1 コマンド）
  │
  ├─ GO_L1 ──► ③ E2E 雛形 unlock → validator →【明示時のみ】Submit 1 回
  │            └─ 時間あり: tip-dist / 面多様性メモのみ · α・weight・mid 先禁止
  │
  └─ NOGO_L1 ─► STOP · Final2 不変 · ban post NO-GO · 新規 L1 なし
```

**原則:** dual 結果が出るまで E2E/Submit/POST-L **一切やらない**。  
**原則:** GO でも **1 面だけ**（`mid+α0.35(L781−mid)`）。枝刈りしない 779/762/756 フルは締切では捨てる。

---

## 1. COMPLETE → harvest（最短）

| 順 | 作業 | 完了条件 |
|---:|---|---|
| 1 | `kernels status` → **COMPLETE**（ERROR ならログ harvest → 修正 Ver2 · 本表は COMPLETE 用） | status COMPLETE |
| 2 | `kernels output` → `exp/work/out-t3-cpu-harvest/chk781-kaggle-face/` | `learned.csv` or tip-cv 同等 learned face |
| 3 | id カバー確認（allowlist または dual が n_wells 報告） | dual が落ちない |
| 4 | （任意）Private DS `rogii-chk781-l-face` は **E2E が DS 読みのときだけ**。local dual には不要 | — |

学習 mid は residual 尺 **faces `20260804-041247`** を dual/E2E で使う（train 中の soft L\* とは別）。

```powershell
# 例（パスは harvest 先に合わせる）
$root = "."  # repo root
$out  = "$root\20260722-rogii-wellbore\exp\work\out-t3-cpu-harvest\chk781-kaggle-face"
New-Item -ItemType Directory -Force -Path $out | Out-Null
& "$root\scripts\kaggle-cli.ps1" kernels output kazeneko77/tip-cv-chk781-resid-path-h20 -p $out -o
```

---

## 2. dual（必須・コマンド固定）

```powershell
$root = "."  # repo root
$comp = "$root\20260722-rogii-wellbore"
# LEARNED は harvest の learned CSV の絶対パス
& "$root\.venv\Scripts\python.exe" `
  "$comp\exp\work\out-t3-scratch\run_l_residual_local_dual.py" `
  --learned "<LEARNED.csv>" `
  --tag "CHK-781-kaggle-v1" `
  --alpha 0.35
```

出力: `exp/work/out-t3-cpu-harvest/l-dual-CHK-781-kaggle-v1/` · `summary.json` · `report.md`

### GO / NOGO（802 梯子込み · 締切用）

| 条件 | GO に必要 | 802 参照（失敗型） |
|---|---|---|
| L1 機械 | `l1_pass=True`（pool∧worst∧band） | 802 = False |
| 813 SSE | top50 / top100 residual **悪化させない**（watch ok） | 802 top50 **+1.00** |
| 812 Q4 | Q4 residual 悪化 WATCH · path 本命なら ideally ≤0 | 802 B_Q4 **+1.02** |
| 815 | **mid-collapse 禁止**: d\|L−mid\| 大幅↓ かつ resid↑ | 802 **−4.24** |
| OOF 単独 | **使わない**（804/802 教訓） | — |

**追加解釈（path 専用）**

| 観測 | 読み | 次 |
|---|---|---|
| hard Δ≪0 · d\|L−mid\|↑ · 815 ok | path 当たり · GO 有望 | E2E 1 |
| hard Δ>0 · d\|L−mid\|↓ | weight 同型 collapse · **NOGO** | STOP（言い換え禁止） |
| hard 良 · Q4 悪 | 帯ずれ · 締切では **NOGO 扱い**（β 再スイープしない） | STOP |
| cover wells ≪80 | face 不完全 · dual 無効 | harvest やり直し · 提出不可 |

ban-gate post:

```powershell
.\scripts\run-hypothesis-ban-gate.ps1 -ChkId CHK-781 -ActionType T3 `
  -Hypothesis "residual-path soft Lstar L1 dual" `
  -Mechanism "train_stack soft path PackD" -Phase post `
  -Verdict GO   # or NOGO
  -ExpDir ".\20260722-rogii-wellbore\exp"
```

---

## 3. GO 後工程（**圧縮版** · 締切最適）

優先は **残秒で Trust 枠に載せられる 1 本** だけ。

| 優先 | ID / 作業 | やる / 捨てる |
|---|---|---|
| **P0** | E2E `tip-e2e-chk781-mid-a035-l-resid` · α**0.35** · L=781 face · mid=041247 系 | **必須** · validator → 明示 Submit **最大 1** |
| **P1** | Final UI: 枠1 を 781 residual に差替検討（着弾後） | ユーザー · 自動差替なし |
| **P2** | tipdist / pair diversity メモ | 時間が許せば |
| — | **779** tip dual 全面 | **締切スキップ**（残差本命で足りる） |
| — | **756** α regrid | **禁止 F043** |
| — | **762 / 764 / 757** mid ノブ | **禁止** until 余裕·L2 |
| — | **809 / 814 / 816 / weight** | **禁止 F044** |
| — | **784 Huber · multi-task** | **捨てる** |
| — | POST-L フル `779→762→756→764` | **ブロック解除は名目のみ** · 実行は P0 完了後かつ時間があれば 1 ノブまで |

### E2E チェックリスト（GO 時のみ）

1. `SUBMIT_FORBIDDEN=False`（雛形 README どおり）  
2. L face = 781 harvest · **not** 802/804 weight face  
3. residual = `mid + 0.35*(L−mid)` only  
4. `check-codecomp-submit-kernel.py` + `validate-submission.ps1`  
5. competitions submit は **ユーザー明示** · Notebook 紐づけ  
6. 再提出禁止リスト（666/farvol 等）を踏まない · **新規 1 面**

---

## 4. NOGO 後工程（最短 stop）

| やること | やらないこと |
|---|---|
| report を checklist / laws に 1 行追記 | Ver2 weight・β 総スイープ |
| Final2 **不変** | residual E2E |
| 監視ログを閉じる | POST-L |
| ban post **NO-GO** | 802 型・F044 再起動 |

オフライン Pack D の −3.03 は **GO 根拠にしない**（oracle ≠ live · 804/802 済み）。

---

## 5. 資源（781 専用）

| 枠 | 用途 |
|---|---|
| Kaggle GPU | train 中は 781 占有 · COMPLETE 後は **空ける**（E2E が GPU なら 1 回のみ） |
| Kaggle / local CPU | **dual / harvest** 最優先 |
| Colab | weight 禁止 · 781 再学習に使わない（Kaggle と二重化しない） |

---

## 6. 記録更新（dual 直後・必須薄）

| ファイル | 更新 |
|---|---|
| `experiment-checklist.md` | 781 行 = dual GO/NOGO · next リンク本ファイル |
| `exp-index.md` | 次アクション 1 行 |
| `hyperparameter-table.md` | dual 数値 1 行 |
| `l-improvement-laws-2026-08-05.md` | 梯子に 781 を 6 本目として追記 |
| ban-gate post | GO / NO-GO |
| run-log 781 | harvest path · dual path |

**グラフ / Canvas** は dual 確定後の整理時のみ（毎 CHK 不要）。

---

## 7. 禁止ショートリスト

- dual 前 E2E / Submit  
- OOF だけで GO  
- α 変更 · well-α · tip⊕  
- weight L1 · 802 面 · F044 言い換え  
- GO 後に複数 residual バリアントの量産  
- NOGO 後の「β だけ変えて」同一 path の無制限再 push  

---

## 8. 現在地（確定）

| 項目 | 値 |
|---|---|
| train | **COMPLETE** Ver1 |
| dual | **NOGO_L1** · hard Δ**+0.44** · hybrid **+0.19** · d\|L−mid\| **−0.97** |
| cover | hard20 only（n=20 · 107478 rows） |
| E2E | **禁止** |
| report | [`../work/out-t3-cpu-harvest/l-dual-CHK-781-kaggle-v1/`](../work/out-t3-cpu-harvest/l-dual-CHK-781-kaggle-v1/) |

**読み:** weight 族より mild（802 +1.79 · 804 +0.74）だが residual は悪化 · mid 寄りの soft path は live で効かず。offline Pack D −3.03 天井 ≠ live。

updated: 2026-08-06 · dual 確定 NOGO · STOP
