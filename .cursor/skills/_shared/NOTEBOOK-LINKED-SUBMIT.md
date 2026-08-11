# Notebook 紐づけ提出 — SSOT

> 参照: 各 Skill の Permissions · `docs-ja/submission-rules.md`  
> 対象: **`submission-profile: notebook-output`** · tabular / notebook 提出が主のコンペ · simulation でも Kernel 紐づけ可能な場合  
> **既定方針: できるだけ Notebook 紐づけで提出する。** zip/csv 直 `-f` のみだと Kaggle 上で提出コードが見れなくなる。  
> **Kaggle 公式 CLI:** [tutorials.md — Submit to a Competition](https://github.com/Kaggle/kaggle-cli/blob/main/docs/tutorials.md) · [kernels_metadata.md](https://github.com/Kaggle/kaggle-cli/blob/main/docs/kernels_metadata.md) · [competition commands](https://github.com/Kaggle/kaggle-api/blob/main/docs/README.md#documentation-for-api-endpoints)  
> **本リポジトリ実行:** 常に `.\scripts\kaggle-cli.ps1`（venv ラッパー）。生の `kaggle ...` は禁止（`.cursor/rules/kaggle-cli-venv.mdc`）

---

## 方針（Kaggler）

| 優先 | 方式 | 提出履歴の表示 | Kaggle 上で NB 参照 |
|:---:|---|---|---|
| **1（推奨）** | Kaggle UI「Submit to Competition」 | `Notebook <title> \| Version N` | **可** |
| **2** | CLI `-k` / `-v`（下記） | 同上 | **可** |
| 3（例外のみ） | CLI `-f` ローカル zip のみ | メッセージ文字列のみ | **不可** |

**Agent / ユーザー共通:** LB 採点だけが目的でも、**方式 1 または 2（Notebook 紐づけ）を既定**とする。  
理由: 提出履歴からコードを辿れ、再現・監査・後追い改善ができる。zip 直アップロード（方式 3）は「NB 不要・緊急」とユーザーが**明示**したときだけ。

## 提出形式・Code Competition（必読）

- **提出形式（列・ファイル名・ID）はコンペ Overview / `docs-ja/submission-rules.md` の指定どおり。変更禁止。**
- Code Competition は採点時に Notebook を **hidden test で再実行**する。
- **禁止:** Dataset やローカルに置いた固定提出物を読むだけの短 Notebook · 他 kernel 出力の丸コピー Script（L0 通過でも Scoring Error になりうる）。
- **正しい中間面・別レイヤ診断:** 本番と同じ E2E パイプラインを走らせ、**同一実行の末尾**で目的の成果物を提出ファイル名へ昇格する。
- 提出前: `.\.venv\Scripts\python.exe .\scripts\check-codecomp-submit-kernel.py -p <kernel-dir>` が **PASS**（Skill `kaggle-submission-validator`）。
- コンペ固有の過去失敗は `docs-ja/submission-rules.md` 等に書く（本ファイルには書かない）。

---

## Agent が最初に読む Skill 順序

提出依頼・「CLI で提出」・「zip で出す」が来たら **この順で** 読む（推測で手順を書かない）:

1. **`kaggle-submission-validator`** — L0–L2 PASS 確認
2. **本ファイル（NOTEBOOK-LINKED-SUBMIT）** — 方式 1 / 2 / 2b / 3 の選択
3. **`kaggle-kernels-runbook`** — `run-log.md` · Version N · `kernels push` 待機
4. **`kaggle-cli-ops`** — preflight · 公式 CLI 参照 · トラブルシュート

`kernels push` · `competitions submit` は **ユーザー明示 OK 後のみ**（`.cursor/skills/_shared/PERMISSIONS.md`）。

---

## 前提（validator PASS 後）

1. ローカル成果物で **`kaggle-submission-validator` PASS**
2. Code Comp: **`check-codecomp-submit-kernel.py` PASS**（コピー専用 NB はここで落とす）
3. **自 fork** に embedded zip 等を載せる（他者 zip のまま提出しない）
4. **Version N を作る**（下記「Version 作成」A または B）— **コンペデータから E2E 生成した Version**
5. 出力（例: `/kaggle/working/submission.csv`）のサイズ・SHA を確認（`kernels output` で実体）
6. `run-log.md` に `kernel_slug` · `output_version: N` を記録
7. `lifecycle-manifest.md` に `kernel` · `version` を記録

---

## Version 作成（Save Version 相当）

| 経路 | 誰が使う | 内容 |
|---|---|---|
| **A. Kaggle UI** | 手動 · 初回 fork | **Run All**（または **Submit** 時の自動実行）→ **Save Version** → Version N |
| **B. CLI `kernels push`** | 自動化 · 他 Kaggler 常用 | ローカル `kernel-metadata.json` + ipynb を push → Kaggle 上で実行 → **Version N** を stdout に表示 |

**UI と CLI の違い（よくある誤解）:**

| | UI「Submit to Competition」 | CLI `competitions submit -k/-v` |
|---|---|---|
| Notebook 実行 | 提出フロー内で Kaggle が実行することが多い | **保存済み Version N の出力ファイル名**を提出（`-f` は出力名） |
| Version | Submit 時に確定 | **事前に** Version N が存在している必要あり |
| 履歴 | `Notebook ... \| Version N` | 同上 |

CLI だけで UI に近い体験にするには **先に `kernels push`（経路 B）** する。

---

## 方式 1 — Kaggle UI

1. コンペページまたは Notebook 右上 → **Submit to Competition**
2. 対象 Version · 出力ファイル（`submission.zip` 等）を選択
3. 説明文を入力 → 提出

※ 初回は **Save Version** だけ先に行い、出力を確認してから Submit してもよい。

---

## 方式 2 — CLI（notebook 紐づけ · Version 済み）

**公式:** [Kaggle CLI tutorials — Submit](https://github.com/Kaggle/kaggle-cli/blob/main/docs/tutorials.md)

```powershell
.\scripts\kaggle-cli.ps1 competitions submit <COMPETITION_SLUG> `
  -f submission.zip `
  -k <KAGGLE_USERNAME>/<KERNEL_SLUG> `
  -v <VERSION_NUMBER> `
  -m "<短い説明>"
```

| 引数 | 意味 |
|---|---|
| `-f submission.zip` | **Notebook 出力ファイル名**（ローカルパスではない） |
| `-k` | `kazeneko77/neurogolf-7242-task-graft-with-explainations` 形式 · **自 kernel のみ** |
| `-v` | Save Version または `kernels push` 後の番号（例: `2`） |
| `-m` | 提出メッセージ（履歴に併記） |

**実績メモ:** `-k` / `-v` 付き提出は API で受理され、提出履歴に `Notebook ... | Version N` と表示される。zip-only は Notebook 列が空になる。

---

## 方式 2b — CLI 完結（`kernels push` → 提出）

ブラウザを開かず **CLI のみ** で Version 作成から Notebook 紐づけ提出まで行う標準パターン。

**公式:** [Update a Kernel](https://github.com/Kaggle/kaggle-cli/blob/main/docs/tutorials.md) · [kernel-metadata.json](https://github.com/Kaggle/kaggle-cli/blob/main/docs/kernels_metadata.md)

### Step 0 — フォルダ準備

```powershell
# 初回: pull で metadata 取得（-m 必須）
.\scripts\kaggle-cli.ps1 kernels pull <USERNAME>/<KERNEL_SLUG> -m -p my-notebook/<name>/
# embedded zip 差し替え等を ipynb に反映
# kernel-metadata.json の id / competition_sources を確認
```

### Step 1 — push（実行 + Version 作成）

```powershell
.\scripts\kaggle-cli.ps1 kernels push -p my-notebook/<name>/
# 成功時: "Kernel version N successfully pushed" → N を run-log.md に記録
```

### Step 2 — 完了待ち

```powershell
.\scripts\kaggle-cli.ps1 kernels status <USERNAME>/<KERNEL_SLUG>
# KernelWorkerStatus.COMPLETE まで待つ

.\scripts\kaggle-cli.ps1 kernels files <USERNAME>/<KERNEL_SLUG>
# 出力 submission.zip の size が妥当か確認（壊れた小さい zip を提出しない）
```

### Step 3 — Notebook 紐づけ提出（方式 2 と同じ）

```powershell
.\scripts\kaggle-cli.ps1 competitions submit <COMPETITION_SLUG> `
  -f submission.zip `
  -k <USERNAME>/<KERNEL_SLUG> `
  -v <N> `
  -m "<短い説明>"
```

### Step 4 — 記録

- `run-log.md` · `lifecycle-manifest.md` · `exp/exp-infer.md`（`Notebook ... \| Version N`）
- `submission-validations/*.md` に `submit_mode: notebook-linked`

---

## push 前チェックリスト（毎回 · これを飛ばすと失敗する）

`kernels push` は下記 4 点が揃わないと 403 / 別 slug 生成 / metadata not found で失敗する。

- [ ] **1. metadata `id` と title が resolve するか** — Kaggle は **初回作成時 title から slug を決める**。`kernel-metadata.json` の `id` 末尾 slug と `title` を kebab 変換したものが**一致**していないと、push が「別 slug の新規 kernel」を作る（`kernel title does not resolve to the specified id` 警告が出たら要注意）。既存 kernel を更新したいときは **既存の id をそのまま使い、title も変えない**。
- [ ] **2. `code_file` と実ファイル名が一致** — metadata の `code_file` に書いた `.ipynb` が push フォルダに**同名で**存在すること。改名した ipynb をコピーし忘れると `Notebook not found`。
- [ ] **3. push は自所有 slug のみ** — 他者 slug へ push すると 403。新規作成でも、既存の自 fork を更新する方が確実（新規 slug の 403 を避けられる）。
- [ ] **4. `-p <dir>` はラッパーで素通しされる** — 修正済み `kaggle-cli.ps1` は `-p` 等をそのまま kaggle へ渡す（旧版は `--%` が必要だった）。metadata は **`-p` で渡したフォルダ**から読まれる。cwd から読ませない。

## push 後チェック（壊れ zip を提出しない）

- [ ] **`kernels files` の size は信用しない** — API 表示が 871B 等の壊れ値を返すことがある（表示クセ）。**必ず `kernels output -p <dir>`** で実体を落とし、`Get-Item submission.zip | Select Length` と `sha256` で確認する。
- [ ] **status COMPLETE を待つ** — `KernelWorkerStatus.COMPLETE` になる前に output を取ると空 zip を掴む。

## よくある失敗 → 原因 → 対処（早見表）

| 症状 | 原因 | 対処 |
|---|---|---|
| `'cp932' codec can't ...` | 日本語 Windows の cp932 | ラッパーが `PYTHONUTF8=1` を設定済み（修正版）。旧環境は手動で `$env:PYTHONUTF8="1"` |
| `-p` が無効パラメータ / `Metadata file not found` | PowerShell が `-p`/`-v` を横取り | 修正版ラッパーで解消（`$args` 素通し）。旧版は `--%` を kaggle 引数の前に置く |
| `kernel title does not resolve to the specified id` → 別 slug 生成 | title と id 不一致 | push 前チェック 1。既存更新は id/title を変えない |
| `Notebook not found` | `code_file` と実ファイル名不一致 | push 前チェック 2 |
| 新規 slug push で `403 Forbidden` | 他者 slug / 新規作成の権限周り | 既存の自 fork を更新して Version を作る（push 前チェック 3） |
| 提出した zip が 871B 等で 0 点 | `kernels files` の表示値を鵜呑み | push 後チェック（`kernels output` で実体確認） |
| **Submission Scoring Error**（L0 は通過） | 固定提出物コピー NB（Dataset / kernel_sources）· hidden 再実行不能 | E2E で再生成し末尾昇格。`check-codecomp-submit-kernel.py` で事前検出 |
| 列名・ID が変 | 提出形式を勝手に変更 | **禁止** — Overview / `submission-rules.md` の形式に戻す |

---

## `-k` / `-v` の制約（必読 · Agent 違反禁止）

### 自 kernel のみ

| ルール | 内容 |
|---|---|
| **`-k` の slug** | **ログイン中アカウントが所有する notebook のみ**（例: `kazeneko77/neurogolf-chatgptloop`） |
| **他者 slug** | `boristown/...` 等 → API **`403 Forbidden`**（採点拒否ではなく **紐づけ権限なし**） |
| **403 時** | **zip-only（方式 3）へフォールバック禁止** — ユーザーが「NB 不要・緊急」と**明示**した場合のみ例外 |
| **正しい対処** | **自 fork を先に更新** → Version 作成（UI または `kernels push`）→ `-k <YOUR_USERNAME>/<SLUG> -v N` |

### 他者 zip · `kernels output` 取得後の標準手順

他者 notebook の出力 zip をローカル検証で GO になった場合でも、**そのまま zip-only 提出してはならない**。

1. ローカル validator **PASS**（G1 等）
2. **自 fork 更新** — embedded zip 差し替え · Input 更新 · 必要最小の notebook 編集（SUB-011 型）
3. **Version 作成** — UI **Save Version** または **`kernels push`**（Version N を `run-log.md` に記録）
4. CLI **`-k <YOUR_USERNAME>/<KERNEL_SLUG> -v N -f submission.zip`** または UI **Submit to Competition**

**反例（SUB-012 で発生 · 再発禁止）:** `kernels output boristown/...` → `-k boristown/...` で 403 → zip-only 提出。

---

## 方式 3 — zip 直提出（非推奨 · 例外）

> **403 Forbidden 時のフォールバック先にしてはならない。** 上記「自 fork 更新を先に」。

```powershell
# ローカル zip をそのまま送る — ファイル名は submission.zip 必須（neurogolf）
Copy-Item exp\work\<name>-submission.zip exp\work\submission.zip -Force
.\scripts\kaggle-cli.ps1 competitions submit <COMP> `
  -f "<絶対パス>\submission.zip" `
  -m "..."
```

- 採点は通るが **Notebook リンクなし**
- メダル · writeup · 公開解法では方式 1/2/2b を優先

---

## simulation との違い

| 項目 | simulation（コードコンペ） | notebook-output（neurogolf 等） |
|---|---|---|
| zip 直 `-f` | 多くは **400 拒否** | **受理**（ただし NB 非表示） |
| `-k` / `-v` | 必須に近い | **推奨**（UI と同等の紐づけ） |
| `kernels push` | 提出前の標準手段の一つ | embedded zip 更新後の **Version 作成**に使用 |
| Internet | 多く OFF 必須 | コンペ・notebook 依存 |

---

## 記録（提出後）

| ファイル | 追記 |
|---|---|
| `lifecycle-manifest.md` | `submit_ref` · `kernel` · `version` |
| `my-submitted-notebook/README.md` | kernel slug 列 |
| `exp/exp-infer.md` | `Notebook ... \| Version N` 形式で記載 |
| `submission-validations/*.md` | `submit_mode: notebook-linked \| zip-only` |

---

## Agent 境界

- `competitions submit` · `kernels push` は **ユーザー明示 OK 後のみ**
- OK を得た場合も **方式 1 / 2 / 2b** を案内。CLI なら **必ず `-k` / `-v`**（Version は `run-log.md` または push 出力から）
- **`-k` は自 kernel のみ** — 他者 slug で 403 → **自 fork 更新を先に**（zip-only 禁止）
- zip 直 `-f` のみは、ユーザーが「NB 不要・緊急」と明示したときだけ
- **提出形式はコンペ指定のまま**（変更禁止）
- **固定提出物コピー専用 NB で提出しない** — `check-codecomp-submit-kernel.py` PASS 必須
- ユーザーが「今日は提出しない」と指示したら **submit しない**（完走 GPU があっても）
- 提出手順をチャットに書く前に **本ファイルを読む**（Skill 飛ばし禁止）
