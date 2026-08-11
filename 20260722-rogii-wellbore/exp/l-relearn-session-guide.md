# L 再学習セッションガイド — 別セッション SSOT

> **用途:** 別チャットの AI Agent が **L（learned / S1）品質改善** を自律実行するときの **唯一の手順書**  
> **親 Active（要約のみ）:** [`experiment-checklist.md`](experiment-checklist.md)  
> **関連:** [`t2-candgen-learn-checklist-2026-08-04.md`](t2-candgen-learn-checklist-2026-08-04.md) §C · 定規 [`experiment-checklist.md`](experiment-checklist.md) §T3-B  
> **faces SSOT:** [`work/colab-final-t2/CURRENT-T2-FACES.md`](work/colab-final-t2/CURRENT-T2-FACES.md)（現行 `20260804-041247`）  
> **metric:** Trust CV = residual `mid + α(L−mid)` の **pool + mean_worst + max_band**（747）· α 既定 **0.35**（666）  
> **updated:** 2026-08-05（**804 NOGO · F044 · 法則 · next 802/781**）  
> **L 法則:** [`latest/l-improvement-laws-2026-08-05.md`](latest/l-improvement-laws-2026-08-05.md)  

> **グラフ:** [`within-stage-comparisons.md`](within-stage-comparisons.md)（整理同期）  
> **親 Active:** [`experiment-checklist.md`](experiment-checklist.md)  
> **CV 仮説ハンドオフ:** [`l-cv-hypothesis-handoff-2026-08-05.md`](l-cv-hypothesis-handoff-2026-08-05.md)  
> **GPU 橋渡し（必読）:** [`latest/session-bridge-cpu-to-gpu-2026-08-05.md`](latest/session-bridge-cpu-to-gpu-2026-08-05.md)  
> **GR ドメイン:** [`docs-ja/discussion/gr-instrument-limits-cv.md`](../docs-ja/discussion/gr-instrument-limits-cv.md)

---

## 0. このレーンでやること / やらないこと

### やる（B 本体）

- tip-cv 上で **FORCE retrain** し **learned face CSV のみ**を取る  
- 新 L を **同一 mid** 上 residual `α=0.35` で旧 L と比較（ローカル dual）  
- 通過後のみ E2E tipdist dual（762）· 昇格 residual は 756（**新 L 後**）

### やらない（言い換え再実行禁止）

| 禁止 | 理由 |
|---|---|
| 現 L の **residual-α 連打**（井α / confα / MD α） | **F043** |
| L / mid / soft **生 FINAL** | **F015** |
| residual **Public 提出** | **679** · 641 |
| soft→mid 注入 | **620** |
| 下流 agree/row 微スイープ本命 | 上流 L/mid へ |
| 1ジョブに mid 改修 + L 学習 + Public | **681** |
| **GR 本命特徴 / 高周波 GR 合わせ / 欠損充填だけで dual GO** | **機器制限** · 811 ρ≈0 · [gr-inst](../docs-ja/discussion/gr-instrument-limits-cv.md) · Host wiggle 低周波 |
| **hard/Q4/drag sample_weight L retrain 言い換え**（761/782/804） | **F044** · mid-collapse · offline oracle ≠ dual |
| **TVT-OOF 改善だけで L1 GO** | 804 OOF 9.13 でも dual NOGO |

### GPU / 実行承認

- Kaggle/Colab **起動はユーザー許可 + 対象ジョブ指示**が必要（Rule `kaggle-private-assets`）  
- 本ガイド内の **L0/L1/L2 ジョブ**は checklist 上「L セッション起動」指示があれば実行可  
- **同時 GPU:** フル 688 と L1 を取り合いしない。688 RUNNING 中は **L0 静的 / ローカル dual 準備** のみ推奨

---

## 1. 別セッション開始チェックリスト（毎回）

Agent は **ターン開始時に必ず**:

1. `exp/exp-index.md`「現在地」  
2. 本ファイル §2（ピラミッド）と §5 Active L 表  
3. `exp/work/colab-final-t2/CURRENT-T2-FACES.md`  
4. `improvement-loop-failures.json`（F015 / F043）  
5. 688 系 kernel status（RUNNING なら **第二 GPU フルを勝手に載せない**）

```powershell
# リポジトリルートで
.\scripts\kaggle-cli.ps1 kernels status kazeneko77/tip-cv-chk688-learned-retrain-h20
```

### ban-gate（重い学習前）

```powershell
.\scripts\run-hypothesis-ban-gate.ps1 `
  -ChkId CHK-xxx -ActionType T3 `
  -Hypothesis "..." `
  -Mechanism "concrete: FAST/LGB-only/weights/..." `
  -Phase pre `
  -ExpDir ".\20260722-rogii-wellbore\exp"
```

- T3 streak FAIL 時: `exp/improvement-loop-allowlist.json` に該当 CHK の `bypass: ["escalation"]`（failures 照合は継続）  
- 完了後: `-Phase post -Verdict GO|NOGO`

### 記録（毎 CHK 必須）

| ファイル | 何を書く |
|---|---|
| **本 MD** §5 status | `pending / in-progress / GO_* / NOGO / blocked` |
| `hyperparameter-table.md` | exp 1 行 |
| `exp-train.md` 先頭メモ | 1–3 行 |
| `experiment-checklist.md` Active | **要約 1 行のみ**（詳細は本 MD） |
| `exp-index.md` | Best/次アクション変化時のみ |

提出は **ユーザー明示指示があるまでしない**（最終残り≈5 回 · 自律提出禁止 · 永久凍結ではない）。

---

## 2. 実験ピラミッド（必須）

| 段 | 目的 | 設定 | 目安 | 採否物差し |
|---|---|---|---|---|
| **L0 スモーク** | 即死排除 | `FAST=1` · LGB **1本** · fold **2–3** · hard20 · stop after learned | 15–40 min | learned.csv 非空 · 形 OK |
| **L1 スクリーン** | 仮説方向 | `FAST=1` または木 1/5–1/3 · **1機構のみ** · hard20 | 1–2 h | **ローカル residual dual** vs 旧 L（§3） |
| **L2 本番** | 採否 | FAST=0 · フル stack · hard20（通れば balanced80） | 数 h | §3 dual + **762 E2E tipdist** |

**規則:**

- L0 FAIL → 設定/コード修正。仮説変更ではない。  
- L1 で **residual pool と mean_worst が両方 旧 L より悪化** → **L2 に上げない** · status=NOGO  
- L1 3 連続 NOGO 同ファミリー → 仮説帯を変える（weights → loss → 特徴）  
- L2 GO のみ 756 residual 再格子（固定 α 格子 · **≠ 井α**）

---

## 3. 最短採点（新 L が出たら必ず）

### 3.1 ローカル residual dual（数十秒）

```powershell
.\.venv\Scripts\python.exe `
  .\20260722-rogii-wellbore\exp\work\out-t3-scratch\run_l_residual_local_dual.py `
  --learned <path\to\learned_trajectory_submission.csv> `
  --tag CHK-xxx
```

比較対象（固定）:

- **旧 L:** `runs/20260804-041247/faces/learned.csv`  
- **mid:** `.../mid_before_hedge.csv`  
- **residual:** `mid + 0.35 * (L − mid)`  
- wells: tip-cv allowlist balanced 80  
- 出力: `exp/work/out-t3-cpu-harvest/l-dual-<tag>/`

### 3.2 GO 判定（L1）

| 条件 | L1 通過 |
|---|---|
| **平面** | **hard_plane**（new L が載った井）で判定。hybrid80 は併記マップ（CHK-790） |
| pool(new) ≤ pool(old) − **0.05** | 必須側 · hard_plane |
| mean_worst3(new) ≤ mean_worst3(old) − **0.05** | 必須側 |
| max_band が old + **0.5** 以内 | 必須 |
| mean_worst_8 ≤ old_8 + **0.10** | **WATCH** · 超えなら L2 しない（CHK-791） |
| hard20 数値単体 GO 禁止 · 751 · **16 vs 10 誤読禁止** | 補助 |

### 3.3 GO 判定（L2 · Trust 候補）

- 上記 3 点 **かつ** strict8  
- E2E tipdist: `run_chk762_dual_new_L.py --learned ...` · 666 帯を大きく超えない（地図）  
- **生 L FINAL 禁止**  
- 参考: hybrid80 Δ は deploy 地図 · hard_plane と混ぜない

---

## 4. 成果物・NB 置き場

| 役割 | パス |
|---|---|
| L2 ベース（フル） | `my-notebook/tip-cv-chk688-learned-retrain-h20/` |
| L1 FAST 雛形 | `my-notebook/tip-cv-l-fast-h20/` · 生成: §6 |
| 761 重み付き | `my-notebook/tip-cv-chk761-weighted-h20/` · weights: `exp/work/out-t3-cpu-harvest/chk748-751-diag/chk761_well_weights.json`（**v2 fold-driver**） |
| run-log 凍結 | `my-ran-notebook/tip-cv-*/run-log.md` |
| harvest | `exp/work/out-688-harvest/` · `exp/work/out-l-*/` |
| dual | `exp/work/out-t3-scratch/run_chk762_dual_new_L.py` · `run_l_residual_local_dual.py` |

### kernel-metadata 規律

- `"is_private": true` · `"enable_gpu": true`（L0/L1/L2） · internet OFF  
- competition: `rogii-wellbore-geology-prediction`  
- push 前: `assert-kaggle-private`  
- 提出経路・`CHK*_ALLOW_SUBMISSION=False`

---

## 5. Active L 仮説キュー（Agent が status を更新）

> 1 CHK = 1 仮説。status をここだけ詳細更新。  
> P: 0=今 · 1=次 · 2=後 · 3=低

### 5.1 運用・物差し（process）

| ID | P | status | hypothesis | acceptance | type |
|---|---|---|---|---|---|
| **L-OPS-01** | 0 | **applied** | L 実験は **L0→L1→L2 ピラミッド**で回し、L1 NOGO を L2 に上げない | 本 MD §2 | T4 |
| **L-OPS-02** | 0 | **applied** | 新 L の最初の判定は **ローカル residual dual（α0.35·三点）** · tipdist は L2 | dual script §3 | T4 |
| **L-OPS-03** | 0 | **applied** | 1 セッション 1 機構（重み **or** loss **or** 特徴 **or** 木/モデル数） | 681 と同旨 | T4 |
| **CHK-767** | 0 | **nb_ready** | L0 FAST スモーク NB を標準入口にし、フル前の即死を 30 分以内に潰せる | FAST learned dump 成功 1 回 · NB [`tip-cv-l-fast-h20`](../my-notebook/tip-cv-l-fast-h20/) | T3 ops |
| **CHK-768** | 0 | **pending** | L1 連続 3 NOGO 同帯で帯を変えるルールを運用すると GPU 浪費が減る | ログに帯切替 | T4 |

### 5.2 ベースライン（進行中）

| ID | P | status | hypothesis | acceptance | type |
|---|---|---|---|---|---|
| **688** | 0 | **COMPLETE dual NOGO** | フル retrain residual 天井が動く | dual vs 666 · F015 なし · **hard20 Δpool+0.52 NOGO** | T3 |
| **692** | 1 | **pending after 688** | 新 L の TRAIN/T2/TEST face dump だけで 676 入口を更新できる | 面整合 · tipdist 記録 | T3 |
| **693** | 1 | **pending after 692** | 新 L + **旧 mid** residual で **L単独寄与**を分離できる | residual T2 dual | T2 |
| **762** | 0 | **script ready** | 新 L 直後 T2+T3-B+tipdist 一発 dual | three_point vs 041247 666 | T3 ops |
| **756** | 1 | **pending after L GO** | **新 L 後のみ** 固定α residual 再格子 · 三点昇格 | pool∧worst∧tipdist | T3 |

### 5.3 L 改善仮説（高速優先順）

| ID | P | status | hypothesis（手法 × 期待効果） | acceptance | type | L 段 |
|---|---|---|---|---|---|---|
| **761** | 0 | **COMPLETE NOGO_L1** | fold-driver hard Δ**+4.01** · mid-collapse · 再禁止 | [ops](latest/ops-l1-chk761-782-harvest-dual-2026-08-05.md) | T3 | L1 |
| **782** | 0 | **COMPLETE NOGO_L1** | resid-drag hard Δ**+3.81** · 同 collapse · 再禁止 | 同上 · ∩688+4.18 | T3 | L1 |
| **769** | 0 | **nb_ready · GPU待ち** | **LGB 1–2 本のみ**（CB 省略）FAST で方向が見え、フル stack と同じ方向なら L2 でも再現する | indent 修正済 · 782 後 | T3 | L1 |
| **770** | 1 | **pending** | 早期停止強化 + 木本数 1/3 でも residual dual がほぼ維持される（過学習削減） | dual Δ < 0.1 で維持 or 改善 | T3 | L1 |
| **771** | 0 | **elevated by 794·804** | **既知帯行のみ**強重み（未知帯を弱める）· map は 804 併記 | residual dual · F015 なし | T3 | L1 |
| **689** | 1 | **pending** | well-group / pad を GroupKFold 単位に明示（現状 well 単位を維持しつつ meta-group）で偶然記憶が減る | known-zone CV + dual | T3 | L1–L2 |
| **690** | 1 | **pending** | loss を **MAE** または **ΔTVT(rate)** 主体にすると横断・高 RMSE 井の L 方向が residual に乗りやすい | residual help↑ / worst↓ | T3 | L1 |
| **772** | 1 | **pending** | 目的を TVT 絶対値ではなく **残差ターゲット (y−mid)** にすると residual 載荷と整合し dual が動く | dual vs 直接 TVT 学習 | T3 | L1 |
| **691** | 2 | **pending** | multi-scale NCC · tortuosity · signed az · landing state を **1 群だけ**足すと tipdist/residual が動く | dual · tipdist map | T3 | L1–L2 |
| **773** | 1 | **pending** | hard20 で L1 GO 後、**balanced80 再学習**すると T2 一般化が上がる（hard 過適合検知） | dual on 80 · flip 監視 | T3 | L2 |
| **774** | 2 | **pending** | 2-seed OOF 平均 L（seed 差分を平滑）で max_band が下がる | band↓ · pool 非悪化 | T3 | L2 |
| **775** | 2 | **pending** | 既知帯 MD 近傍のみ sample_weight↑（heel/遠 MD 差）で遠方 L 破綻が減る | quartile RMSE + dual | T3 | L1 |
| **776** | 2 | **pending** | CatBoost のみ / LGB のみ の勝者を最終 1 系統にすると過学習が減り dual が安定する | abl LGB vs CB dual | T3 | L1 |
| **777** | 2 | **pending** | 正則化↑（L2 / min_data）で mean_worst が pool と同方向に改善する | dual | T3 | L1 |
| **778** | 3 | **pending low** | soft_diag を **特徴として**入れる（注入ではない）と L が mid を追従し residual 余地が減る | dual · soft注入禁止維持 | T3 | L1 |
| **779** | 1 | **pending after L1 GO** | L1 GO なら **L2 フル stack** を 1 本（761 は NOGO のため候補外） | L2 dual + tipdist | T3 | L2 |
| **780** | 2 | **pending** | 768 帯切替後の第 2 帯として **特徴（691）を post-761** に限定すると探索順序が最短になる | 順序メモ遵守 | T4 | — |

### 5.3b L1 追加仮説（2026-08-05 整理後 · 証拠由来）

> 根拠: 766 resid 拖 · 757 L 17/20 win · 765 residual 天井 · Trust 最終形=`mid+α0.35(L−m)` · F043 αいじり禁止。  
> **≠** 761（fold-driver 重み）· **≠** 772（y−mid 回帰のみ）· **≠** 771（既知帯 soft 重み）

| ID | P | status | hypothesis（手法 × 期待効果） | source | acceptance | type | L 段 |
|---|---|---|---|---|---|---|---|
| **781** | 0 | **pending design** | **Trust 残差目的**で学習: OOF/`y` に対し loss=`RMSE(mid+0.35·(pred−mid))`（固定α）。純 L RMSE 最小化より residual dual が直接動く | 666 FINAL 定義 · 765 | L1 dual vs 688/TVT学習 | T3 | L1 |
| **782** | 0 | **COMPLETE NOGO_L1** | resid-drag n41 hard Δ**+3.81** · mid-collapse · 再禁止 | [ops](latest/ops-l1-chk761-782-harvest-dual-2026-08-05.md) | dual done | T3 | L1 |
| **783** | 1 | **CANCEL · queue after 782** | **hard20∩749 top wells** に重み（fold-driver と集合差がある時だけ）で hard 帯が下がる | I5 · 749 · 751 補助 | dual · set≠v2 時のみ実行 | T3 | L1 |
| **784** | 1 | **pending** | loss を **Huber/Fair**（RMSE 置換・1機構）にすると最悪井尾部の mean_worst が先に下がる | mean_worst 定規 · ≠690 MAE 同帯 | dual vs RMSE baseline | T3 | L1 |
| **785** | 1 | **pending · 793 ready** | CV 分割を **field/leave-field Group** にすると T3 worst 畑の偶然記憶が減り dual が安定する · field 表 [793](work/out-t3-cpu-harvest/cv-improve-pack-20260805/chk793_field_prefix_resid.csv) | 763 flip0 · 689 隣接≠ · 793 | dual band · known CV | T3 | L1 |
| **786** | 1 | **pending** | **未知帯行を学習から完全除外**（771 の soft 重みより厳しい）と既知帯 L が residual に乗りやすい | 687 quartile · 771 隣接 | dual · F015 なし | T3 | L1 |
| **787** | 2 | **pending** | multi-task: 主=TVT · 副=`y−mid` を同一 LGB で同時学習すると 772 単体より residual 整合する | 772 拡張 | dual vs 772/688 | T3 | L1 |
| **788** | 2 | **pending low** | 教師を **soft-label blend** `(1−λ)y+λ·mid`（λ小）にすると tipdist 爆発しない L になり dual 帯が残る | I4 tipdist↔α | dual·tipdist map · ≠F043 deployα | T3 | L1 |

**L1 追加地図（pack2 · L-CPU-EDA · LB後 · 2026-08-05）**

| ID | status | hypothesis |
|---|---|---|
| **802** | map · queue#2 | MD **Q4 heavy** sample_weight（796） |
| **803** | map · queue · **792≡** | max(789∪782∪792) · **792 GPU skip** |
| **804** | **DONE NOGO_L1 · F044** | known×Q4 v1c · hard Δ**+0.74** · d\|L−mid\| **−1.43** · [ops](latest/ops-l1-chk804-colab-dual-2026-08-05.md) · 言い換え禁止 |
| **805** | **GO_ops · 781内包** | Q3–Q4 **L\*** ≫ y · [C6](work/out-t3-cpu-harvest/cpu-expert-pack-c-20260805/c6_805_q34_path_oracle.csv) |
| **806** | map · queue#3 · **∩688 72%** | attack+protect · dual 監査 · [json](work/out-t3-cpu-harvest/l-cpu-eda-20260805/chk806_attack_protect_weights.json) |
| **781** | design_ready · **本命次** | **residual RMSE loss** · L\* path · [CPU-C](work/out-t3-cpu-harvest/cpu-expert-pack-c-20260805/) |
| **807** | design WATCH | 停止選抜=residual · OOF 単独禁止 · [C9](work/out-t3-cpu-harvest/cpu-expert-pack-c-20260805/c9_807_stop_metric_proxy.json) |
| **808** | **ops · JUMP 待機** | weight 帯済 → **即 781** |
| **809** | **nb_ready** | mid-hurt3 除外 · [nb](../my-notebook/tip-cv-chk809-midhurt-excl-h20/) |
| **810** | **ops harvest PASS** | dual type slices · Kaggle COMPLETE |
| **811** | proxy done · after 781 | \|L−mid\| 1群 · soft 禁止 |
| **812** | ops WATCH | Q4 · midhurt 非悪化 |

**L1 探索帯（1機構1 session · 2026-08-05 · CPU-C 後）**

```text
NOW:    Colab **802**（任意）or **781** · Kaggle GPU **空** · F044
DONE:   688/761/782/**804** dual NOGO · [laws](latest/l-improvement-laws-2026-08-05.md)
NEXT:   dual 813/815 · 802 NOGO → **808→781(+805·807)**
JUMP:   weight 言い換え禁止 · path-loss へ
THEN:   769 / 770 / 785 → 811
GO:     779 L2 → 762 tipdist → 756 α regrid → 764/795 · dual に 810
STOP:   fold-driver / resid-drag 言い換え · Kaggle 新規 L1
```
### 5.3c CV ops（2026-08-05 pack · 提出禁止）

| ID | status | 要点 |
|---|---|---|
| **789** | GO_map | 688 hurt n=15 · weights ready · after 782 |
| **790** | GO_ops | dual hard_plane + hybrid80 · script適用 |
| **791** | GO_ops | worst8 WATCH · span≈+0.63 |
| **792** | GO_map | continuous drag · after 782 |
| **793** | GO_design | field residual table → 785 |
| **794** | GO_map | known/unknown +6.27 → elev 771 |
| **795** | GO_defer | mid-hurt SSE 87% · after L |

### 5.3d 工程×井タイプ（session 共有 · 詳細は handoff）

| タイプ | 学習 | 主 CHK |
|---|---|---|
| A Attack hard resid | weight↑ **失敗** | **781**（~~761/804~~ F044） |
| C resid>L 拖 | drag 重み | **782 閉鎖** · 地図のみ |
| D 688 hurt | protect 低 weight | 789 |
| E mid-hurt3 | **attack 除外** | **809** |
| F L 強 / known | weight≤1 | 804 protect |
| G known gap | known 寄 | 771/804/786 |
| H field | Group 分割 | 785 |

工程: S1 L 本命 · S9 residual は α固定 · mid-hurt= L後 · tip resid 660 は Trust 外  
Public: 666=6.509 Trust only · 詳細 [`handoff`](l-cv-hypothesis-handoff-2026-08-05.md)

### 5.4 診断済み（再学習しない）

| ID | status | 要点 |
|---|---|---|
| **765** | GO_ceiling | oracle α で pool 6.57 vs 10.09 · meanα*0.91 · **deploy 井α禁止** |
| **766** | GO_map | resid>L 41/80 · mid が L を薄めている |
| **715** | NOGO | soft residual 置換不可 |
| **749** | GO | top wells 済 · 761 入力は **v2 fold-driver 優先** |

---

## 6. NB / スクリプト（Agent が使うコマンド）

### 6.1 L1 FAST 雛形を生成

```powershell
.\.venv\Scripts\python.exe `
  .\20260722-rogii-wellbore\exp\work\out-t3-scratch\build_l_fast_nb.py
```

生成物: `my-notebook/tip-cv-l-fast-h20/`  
既定: `FAST=1` · LGB-only スイッチ · fold 3 · stop after learned · 提出禁止

### 6.2 ローカル residual dual

```powershell
.\.venv\Scripts\python.exe `
  .\20260722-rogii-wellbore\exp\work\out-t3-scratch\run_l_residual_local_dual.py `
  --learned <csv> --tag CHK-761-L1
```

### 6.3 フル 688 harvest（COMPLETE 後）

```powershell
.\scripts\kaggle-cli.ps1 kernels output kazeneko77/tip-cv-chk688-learned-retrain-h20 `
  -p .\20260722-rogii-wellbore\exp\work\out-688-harvest
# その後 dual
.\.venv\Scripts\python.exe `
  .\20260722-rogii-wellbore\exp\work\out-t3-scratch\run_l_residual_local_dual.py `
  --learned (Get-ChildItem ...learned*.csv | sort LastWriteTime -Descending | select -First 1).FullName `
  --tag CHK-688
.\.venv\Scripts\python.exe `
  .\20260722-rogii-wellbore\exp\work\out-t3-scratch\run_chk762_dual_new_L.py `
  --learned <same>
```

### 6.4 推奨実行順（別セッションが迷ったらこれ）

```text
詳細 SSOT: l-cv-hypothesis-handoff-2026-08-05.md

1) 761 dual / 782 dual（RUNNING なら待つ · 第二 GPU 取り合い注意）
2) GO → 779 L2 1本 → 762 → 756（固定α）→ 764 mid 1ノブ
3) 両方 NOGO → 804 dual
4) weight 連鎖 NOGO → 802|803/792 → 806 → 789 → 809
5) weight 系 3 NOGO → 【808】即 781（±805 residual-path 行 · ±807 residual stop）
6) なお NOGO → 769/770/785 → 811
7) 各 L1 後: local residual dual · 810 タイプ表 · 812 Q4/mid-hurt WATCH
8) 提出はユーザー明示のみ
```

---

## 7. 気付き→設計（セッション共有）

| 気付き | 設計への接続 |
|---|---|
| residual help≈mid help(77/3) | L で深度のみ · mid 集合を壊さない |
| mid-hurt3 で L も弱い | **809** attack 除外 · weight↑ 毒 |
| Q4 gap 最大 · 688 Q4 悪化 | **802 確認 or 781/805** 主戦場 · weight 804 閉 |
| 688 L良 resid悪 | **781/807** 採点関数整合 |
| 666 Public 6.509 | Trust only · α 触らない · L 継続 |
| pure L が top20 で最多 win | L 再学習が本命 · mid 1 点は後 |
| residual が L を薄める井が半数超 | 固定α0.35 でも L 質↑が効く · **782 重み** |
| oracle α≈0.91 | 井α deploy ではなく **L 改善**· **781 residual-path 目的** |
| 761 v1 と fold driver ズレ | weights は **v2** を使う |
| フル stack が時間を食い尽くす | **FAST / モデル削減**を L1 既定に |
| Trust FINAL=`mid+αL` | 学習目的を pure L だけにしない · **781 / 772** |

詳細: `exp/work/out-t3-cpu-harvest/session-1h-cv-20260805/report.md` · `chk754-757-763-insights/report.md` · [`l-cv-hypothesis-handoff-2026-08-05.md`](l-cv-hypothesis-handoff-2026-08-05.md)

---

## 8. ハンドオフ文（次の Agent にコピペ）

```text
L / Trust residual CV。GPU セッション担当のとき:
  1) exp/latest/session-bridge-cpu-to-gpu-2026-08-05.md を先に読む
  2) exp/experiment-checklist.md Active · exp/exp-index.md 現在地
  3) exp/l-cv-hypothesis-handoff-2026-08-05.md · exp/l-relearn-session-guide.md
規則: L0→L1→L2 · 1機構/session · F043/F015/Public residual 禁止 · 提出=ユーザー明示のみ
今すぐ: (1) 761/782 COMPLETE→harvest→dual (810/812 · 782は∩688 49% WATCH)
        (2) 両方 NOGO → 804 **v1c**（map 済 · NB焼き）
        (3) weight 3 NOGO → 808→781（+805 L* Q3-4 · 807 residual stop）
CPU 済: GAP-b · P0P1 · expert-C → 繰り返さない
記録: checklist · hyperparameter-table · exp-index 次アクション · bridge 必要なら更新
```
