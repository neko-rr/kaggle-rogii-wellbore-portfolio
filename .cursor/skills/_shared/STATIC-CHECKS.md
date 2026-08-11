# Static Checks — Agent 執筆コードの実行前検査（Kaggle 汎用 SSOT）

> **目的:** 人がコードを書かない運用で、Agent が **テストせず実験**するのを止める。  
> **正本スクリプト:** `scripts/run-static-checks.ps1` · `scripts/check-static.py`  
> Skill: **`kaggle-static-check`** · Subagent: **SA-8** `/kaggle-static-check`

---

## 1. エディタ Ruff との違い（必読）

| | Cursor / VS Code **Ruff 拡張** | **本ゲート（必須）** |
|---|---|---|
| 誰のため | **人**がファイルを開いて見るとき | **Agent** が train/eval する前 |
| いつ動く | 編集中・保存時 | **明示実行** `run-static-checks.ps1` |
| Agent | **無視できる**（UI 専用） | **exit 0 必須** |
| インストール | Kaggle-Light プロファイルに含まれる | `.venv` に **ruff パッケージ**（setup-kaggle-venv） |

**拡張が入っていても、Agent ゲートは満たさない。**  
人間が波線を見ない前提の運用では、機械ゲートだけが防波堤。

---

## 2. いつ必須か

| タイミング | 必須？ |
|---|---|
| Agent が `.py` / `.ipynb` を**書いた・直した直後**、本実験の前 | **必須** |
| ローカル train / 長 eval / 多 seed | **必須** |
| kernels push / 提出前（validator の前でも可） | **必須** |
| Markdown・exp 表だけの編集 | 不要 |
| T4 調査でコード変更なし | 不要 |

**FAIL のまま** pretrain・kernels・長時間 Colab に進まない。

---

## 3. 検査内容（L0）

| 検査 | 重大度 |
|---|---|
| `.py` 構文（`py_compile` + `ast`） | **FAIL** |
| `.ipynb` JSON + code cell 構文（magic 行は静的では剥がす） | **FAIL** |
| `kernel-metadata.json` の `is_private: false` | **FAIL** |
| `code_file` 欠落 | **FAIL** |
| ruff（`E9,F63,F7,F82` 等・クラッシュ寄り） | **FAIL**（ruff あり時） |
| ruff 未導入 | **WARN**（構文は見る · `setup-kaggle-venv` 推奨） |

対象ディレクトリ（コンペ内・日付フォルダ可）:

- `my-notebook/` · `my-local-eval-notebook/` · `scripts/` · `sim-track/`  
- **既定では** `my-ran-notebook/` · `my-submitted-notebook/` は見ない（過去成果）。再編集時は `-Path` で指定

除外: `.venv` · `dataset/` · `knowledge/` · `others-notebook/` 等

---

## 4. コマンド

```powershell
# 変更ファイルだけ（Agent 標準 · 推奨）
.\scripts\run-static-checks.ps1 -Path ".\my-notebook\foo\train.py" -Path ".\my-notebook\foo\run.ipynb"

# 広いスキャン（新コンペや棚卸し）
.\scripts\run-static-checks.ps1 -CompRoot ".\20260101-my-comp"
```

PASS → 続行。FAIL → 修正して再実行。  
レポート: `exp/work/static-check-last.json`（見つかれば）

初回・venv 再作成後:

```powershell
.\scripts\setup-kaggle-venv.ps1   # ruff が入る（requirements-kaggle-cli）
```

---

## 5. 他ゲートとの順序

```text
code 編集
  → run-static-checks.ps1   ← 今ここ（最速で落ちる）
  → ban-gate pre
  → shape smoke / pretrain-gate
  → 本実験 / kernels
  → submission-validator
```

static は **形 smoke や pretrain の代替ではない**（データ・提出形は別）。  
pretrain は static **PASS 後**に進む。

---

## 6. Subagent SA-8

重い範囲の列挙や一括確認は `/kaggle-static-check` に委譲可。  
**GO 権限は親。** サブはスクリプトを回してサマリのみ返す。

---

## 7. 禁止

- ❌ 拡張 Ruff の波線確認だけで「テストした」と書く  
- ❌ FAIL を無視して GPU / kernels を開始する  
- ❌ dataset/ や others-notebook をゲート対象に含めて時間を溶かす  
