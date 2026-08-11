# Colab 成果物転送 · Private Kaggle Dataset 優先（教訓メモ）

> type: ops-lesson · status: **post-comp Skill 修正待ち**  
> evidence: 2026-08-05 CHK-802 dual 前後（final day）  
> **コンペ中はこの方針で運用** · **Skill 本体は終了後に直す**（ユーザー明示 2026-08-05）

---

## 結論（1行）

**Desktop ↔ Colab で必要な小さな deps / 中程度の face を Agent が運ぶとき、既定は Private Kaggle Dataset（zip 1 本）または Drive 実体同期。MCP 経由の hex / b64 分割ペーストは禁止級。**

---

## なぜ（理由）

### 1. コストの内訳が「転送」であって「計算」ではない

| 作業 | 体感 |
|---|---|
| dual deps zip | **~13 KB**（allowlist / hard-wells / catalog / weight maps + dual script） |
| dual 本体 | 面があり deps が揃えば **数十秒〜数分** |
| MCP hex / gzip-b64 分割（5〜数十セル） | **何十分〜数時間** · 破損修正込みで更に伸びる |

CHK-802 では **学習済み face は既にあった**のに、deps 転送だけがボトルネックだった。最終日にこれが致命。

### 2. MCP 分割転送の失敗モードが再現した

- 長い hex / b64 は **途中欠損・文字化け・SHA 不一致**が起きる（shard 再貼りで悪化することがある）
- Agent が「壊れたから再分割」を繰り返し、**ユーザー知覚 = 何も進まない**
- `run_code_cell` の待ちは **完了後もタイムアウトで切断**され、完了報告が遅れる（実は dual 完了済みのケースあり）

### 3. 「正しい経路」が既に存在する

| 経路 | 向き | 向き先 | 備考 |
|---|---|---|---|
| **Private Kaggle Dataset** | Desktop → Colab / Kaggle | `datasets create/version` → Colab `kaggle datasets download` | **自作は isPrivate=true** · Rule `kaggle-private-assets` |
| Drive 正本 | Colab train の face / logs | Desktop は同期 or harvest のみ読む | train 中は Drive に書く · MCP で面をバイト転送しない |
| MCP zip-less pack | 極小 JSON 数個のみ | 緊急のみ | 合計 **≲数 KB・1 セル**のときだけ |
| MCP hex multipack | **禁止** | — | face（MB）や dual pack 全体に使わない |

過去成功例（同一リポ）: faces を  
`kazeneko77/rogii-final-t2-faces-20260804-041247` 等の **Private Dataset** にした履歴あり  
（`exp/work/colab-final-t2/_finalize_t2_local_20260804.py` · cat `private_dataset`）。

### 4. なぜ「zip をそのまま Drive に置けば」では足りないことがある

- Windows **Drive Desktop が `exp/work/...` を同期しない**ケースがある（chk802 face が Desktop に MISSING）
- Agent から見えるパスと Colab の `/content/drive/...` が一致しないと **ローカル zip が Colab に即見えない**
- そのときの代替として「MCP 分割」は魅力的に見え、実際は最悪 — **Dataset 経由の方が API 一本・再現可能**

---

## 運用ルール（コンペ中 · Agent）

1. Colab / 他環境へ運ぶ成果物は先に **役割別 zip** を作る  
   - 例: `dual_deps_*.zip`（deps only） · `*-face.zip` · `dual_result_*.zip`  
2. **Private Dataset** を create / version（必ず Private assert）  
3. Colab は 1 セルで download → extract → 本処理  
4. 監視は Drive `runs/`・harvest path のみ · 長時間 train 中にセル割り込みしない  
5. Dataset 化をスキップしてよいのは:  
   - ユーザーが Drive に手置きした · または  
   - 既に Drive 上に deps が存在することが probe で確定したとき

禁止（Agent）:
- face / dual script / multi-JSON を **hex 再構築ループ**で運ぶ  
- 学習中セルに deps 上書きを割り込む  
- Public Dataset（自作資産）

---

## 実装スケッチ（終了後 Skill に書く用）

```text
A. Desktop
   dual_deps.zip | face.csv|zip を staging にまとめる
B. Private Dataset
   dataset-metadata.json isPrivate: true
   assert-kaggle-private.ps1
   kaggle-cli.ps1 datasets create|version ...
C. Colab 1 cell
   kaggle datasets download -d <user>/<slug> -p /tmp/pack --unzip
   unpack to expected ROOT relative paths
   assert sha / size
   run dual | train | harvest
```

CLI は常に:
`scripts/check-kaggle-cli.ps1` → `assert-kaggle-private.ps1` → `scripts/kaggle-cli.ps1`

---

## 終了後 · 修正する Skill / Rule 候補

> **今は触らない。** コンペ終了後にユーザーが改修する。

| 対象 | 追加する内容 |
|---|---|
| `kaggle-kernels-runbook` | 「Colab 入力の持ち込み経路」節 · Dataset 既定 · MCP hex 禁止 |
| `cursor-colab-runtime` / Colab MCP 運用メモ | 長時間監視=Drive · 成果物輸送≠MCP ボディ |
| `kaggle-cli-ops` / `kaggle-cli-fetch` | **自作 Private Dataset で transfer pack** の短い runbook（作成・version・download） |
| `kaggle-private-assets` | transfer pack も Private 必須の明記（既定どおり） |
| `kaggle-notebook-folders` / experiment 周辺 | harvest 後 dataset slug を ops に残す |
| `knowledge/` harvest | concept: `artifact_transfer_via_private_dataset` · evidence L0/L1 = rogii 802 |

既存メモとの関係:
- MCP 長時間実行: `cursor.md` § Colab MCP · 本メモは **「データ持ち込み」** 層
- 802 dual 実測: `exp/latest/ops-chk802-dual-nogo-2026-08-05.md`

---

## 根拠イベント（rogii · 802）

| 時点 | 事実 |
|---|---|
| face | harvest 済 · 3.5 MB · Drive 上 OK · Desktop Drive 未同期 |
| dual_deps.zip | Desktop に **13 KB** 済み |
| 失敗した道 | MCP hex / b64 multipack · 時間浪費・破損 |
| 成功した道 | gzip+b64 5-part で all-in-one を Colab に載せ dual 完走 · が **手順として標準化すべきでない** |
| dual 結果 | L1 NOGO · 転送コストが検証コストを上回った |

---

## 変更禁止（本メモ）

- 提出経路（Notebook 紐づけ）を変えない  
- Dataset Public 化禁止  
- 終了前に templates / skills を勝手に一括書き換えしない
