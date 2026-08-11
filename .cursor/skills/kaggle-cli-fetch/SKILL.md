---
name: kaggle-cli-fetch
description: >-
  Kaggle CLI（v2.2+）で Discussion・提出履歴等を取得し、
  docs-en/discussion/ 等のローカルファイルに保存する。Kaggle CLI、topics show、
  competitions submissions、Discussion 取得、API 認証、kaggle auth login と言ったときに使う。
  データセットのダウンロードはユーザー明示指示時のみ。要約は Skill discussion-summary に任せる。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| kaggle-cli.ps1 · check-kaggle-cli.ps1 | Kaggle HTTPS（読取） | 読取のみ。token/.env をログ・Git 禁止 | repo · comp-root | docs-en/discussion/ · exp/（dataset/ 上書き禁止） |

**要ユーザー明示 OK:** competitions download · datasets download · models 重 DL

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle CLI Fetch

Kaggle CLI で **読み取り専用** にデータを取得し、既存 kebab-case フォルダへ保存する。要約・分析は行わない。

## 役割分担

| Skill | 担当 |
|---|---|
| **本 Skill** | CLI 実行、認証確認、原文ファイル保存 |
| `kaggle-cli-ops` | venv preflight · **DL 前チェック表**（容量 · 部分 workspace） |
| `discussion-summary` | Discussion の日本語要約 → `docs-ja/discussion/` |
| `experiment-result-management` | 提出結果 → `exp/exp-infer.md` |
| `post-comp-private-retrospective` | Private 振り返り（ユーザー報告 + CLI 補助） |

## 前提

- Kaggle CLI **v2.2.0 以上**（コンペ Discussion 用）。公式: [PyPI kaggle](https://pypi.org/project/kaggle/)
- Python **3.11 以上**（PyPI 要件）
- 認証済み（`setup.md` 参照）
- コンペ slug を特定済み（URL から: `nvidia-nemotron-model-reasoning-challenge`）

初回セットアップ: [setup.md](setup.md)

## 作業前チェック

```powershell
kaggle --version
kaggle competitions list -s nvidia 2>&1 | Select-Object -First 3
```

認証エラー（401/403）の場合は fetch を止め、ユーザーに `kaggle auth login` を案内する。

## 許可コマンド（読み取り専用）

### Discussion（優先）

```powershell
# コンペ Discussion 一覧
kaggle competitions topics list <competition-slug>

# 特定トピック + コメント全文
kaggle competitions topics show <competition-slug> <topic-id>
```

### 提出・コンペ（メタデータのみ・デフォルト）

```powershell
kaggle competitions submissions -c <competition-slug>
kaggle competitions files -c <competition-slug>
```

### データダウンロード（**ユーザー明示指示時のみ**）

容量が大きく PC に入り切らない場合がある。**Agent は勝手に実行しない。**

```powershell
# ユーザーが「dataset をダウンロードして」と指示した場合のみ
kaggle competitions download -c <competition-slug> -p <dataset-dir> --unzip
kaggle datasets download -d <owner/dataset> -p <path> --unzip
kaggle models instances versions download -m <owner/model> -v <version> -p <path>
```

実行前: Skill **`kaggle-cli-ops`** の **ダウンロード前チェック** 表をすべて PASS してから `kaggle-cli.ps1` で実行（容量見積もり · 書込先 · 部分 workspace · archive 失敗時は止める）。

### その他（メタデータ）

```powershell
kaggle datasets list -s <query>
kaggle datasets status <owner/dataset> --format json
```

### 禁止（ユーザー明示承認なし）

- **`kaggle competitions download` / `kaggle datasets download` / Models 重み download**
- `kaggle competitions submit`（ユーザー OK 時は **`NOTEBOOK-LINKED-SUBMIT.md`** — 方式 2 `-k/-v` または方式 2b `kernels push` → `-k/-v`）
- `kaggle competitions merge`
- `kaggle kernels push`（ユーザー OK 時は **`NOTEBOOK-LINKED-SUBMIT.md` §2b** · 公式 [tutorials](https://github.com/Kaggle/kaggle-cli/blob/main/docs/tutorials.md)）
- `kaggle datasets create` / `kaggle benchmarks tasks push`
- 認証情報のリポジトリへの書き込み

## 出力先

コンペフォルダ `yyyymmdd-コンペ名/` 基準:

| 取得対象 | 保存先 |
|---|---|
| Discussion 原文 | `docs-en/discussion/<filename>.md` |
| 提出履歴メモ | `exp/submissions-cli.log` またはユーザー指定 |
| コンペ data | `dataset/`（**編集禁止**・上書き前に確認） |

### Discussion ファイル名

`docs-en` / `docs-ja` で **突合できるよう topicId を共通で入れる**:

| 対象 | 形式 | 例 |
|---|---|---|
| **一般トピック（既定）** | `{topicId}-{Title-Slug}.md` | `693088-Question-About-ONNX-Runtime-Compatibility.md` |
| **Competition Host** | `Competition-Host_{topicId}-{Title-Slug}.md` | `Competition-Host_724226-Two-Submissions.md` |
| **Kaggle Staff** | `Kaggle-Staff_{topicId}-{Title-Slug}.md` | `Kaggle-Staff_691446-How-to-get-started.md` |
| **エラー系** | 上記名で `docs-en/discussion/error/` 配下 | |

ルール:

1. **topicId は必須**（`topics list` / URL から取得）
2. **一般参加者名はファイル名に付けない**（Host / Staff のみ例外プレフィックス可）
3. タイトルは kebab / Title-Case-Hyphens。長すぎる場合は先頭〜80文字程度に短縮
4. 既存ファイルがある場合は **上書きせず**、CLI 出力を比較して追記する
5. 日本語要約のファイル名は Skill `discussion-summary` と同じ規則（`docs-ja` 側）

## Discussion 取得ワークフロー

### Step 1: 一覧で topic-id を確認

```powershell
kaggle competitions topics list nvidia-nemotron-model-reasoning-challenge
```

### Step 2: 全文取得

```powershell
kaggle competitions topics show nvidia-nemotron-model-reasoning-challenge 704491
```

### Step 3: `docs-en/discussion/` に Markdown 化

CLI 生出力を次のヘッダ付き Markdown に整形して保存:

```markdown
# {Topic Title}

**Source:** kaggle-cli-fetch  
**Topic ID:** {id}  
**URL:** https://www.kaggle.com/competitions/{slug}/discussion/{id}  
**Fetched:** yyyy/mm/dd HH:MM UTC  
**CLI version:** {kaggle --version}

---

## CLI raw output

{topics show の全文をコードブロックまたはそのまま}

---

## Notes

- CLI では埋め込み画像・Notebook カードが欠ける場合あり（手動補完が必要）
```

### Step 4: `discussion-summary` へ引き渡し

保存後、ユーザーに確認:

- 「`docs-en/discussion/` に原文を保存しました。`discussion-summary` で要約しますか？」
- 要約依頼時は Skill `discussion-summary` を使い、`docs-ja/discussion/` に出力

## 提出履歴取得

```powershell
kaggle competitions submissions -c nvidia-nemotron-model-reasoning-challenge
```

- 出力を `exp/submissions-cli.log` にタイムスタンプ付きで追記可
- LB 報告の正式記録は Skill `experiment-result-management` → `exp/exp-infer.md`

## レート制限

- HTTP 429 時は **Retry-After** を尊重し、同コマンドを連打しない
- 一覧 → 個別 show は **1 topic ずつ**、必要最小限

## 品質チェック

- [ ] 読み取り専用コマンドのみ使用
- [ ] 認証情報を Git に含めていない
- [ ] `docs-en/discussion/` のファイル名が `{topicId}-...` 規約と一致（一般名プレフィックス禁止）
- [ ] CLI 欠落（画像等）を Notes に明記
- [ ] 要約は `discussion-summary` に分離している（ja も同一 topicId）

## 追加リソース

- **公式 PyPI:** https://pypi.org/project/kaggle/
- セットアップ・認証: [setup.md](setup.md)
- Kaggle 告知（v2.2.0 Discussion 対応）: https://www.kaggle.com/discussions/product-announcements/702989
