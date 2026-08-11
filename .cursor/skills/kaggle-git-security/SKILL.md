---
name: kaggle-git-security
description: >-
  Kaggle コンペリポジトリの Git / GitHub セキュリティ。dataset 非公開、秘匿情報禁止、
  .gitignore、pre-commit フック、コミット前チェック。git push、GitHub 公開、
  git init、コミット、dataset を載せて良いかと言ったときに使う。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| check-staged-secrets.ps1 · git（読取中心） | — | — | .gitignore · hooks | —（ルール提案。commit はユーザー） |

**要ユーザー明示 OK:** git push · 公開

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle Git Security

GitHub 公開の可能性を前提に、**コンペデータ・認証情報・大容量成果物** がリモートに載らないよう守る。

## 基本方針（Kaggler 視点）

| 載せる | 載せない |
|---|---|
| Notebook・スクリプト・Skill | **dataset/ 内の生データ・派生 CSV/JSONL** |
| exp/ retro/ docs（要約・記録） | **kaggle.json / .env / API キー** |
| `.gitignore` / フック / README | **submission.zip / LoRA 重み（*.safetensors 等）** |
| ダウンロード手順（`dataset/README.md`） | コンペ規約で再配布禁止のファイル |

**理由:** Kaggle コンペデータは **利用規約・ライセンス** により GitHub 再公開が禁止されることが多い。公開 repo は一度 push すると履歴に残る。

## コンペ開始時（bootstrap 後）

1. ルートに **`.gitignore`** が生成されていることを確認
2. `{comp}/dataset/README.md` にダウンロード手順のみ記載
3. Git を使う場合:

```powershell
git init
.\scripts\install-git-hooks.ps1
```

4. 初回コミット前: `git status` で `dataset/` 配下が **Untracked でも add されない** ことを確認

Skill `kaggle-comp-bootstrap` 実行時は `-InitGit` で 2〜3 を自動化可能。

## .gitignore の要点

テンプレート: `%USERPROFILE%\.cursor\kaggle-template\root\.gitignore`

- `**/dataset/**` を除外（`.gitkeep` / `README.md` のみ例外）
- `.kaggle/`, `kaggle.json`, `.env*`
- `submission.zip`, `*.safetensors`, `*.bin`, `*.pt` 等

**Agent は `.gitignore` を弱めたり dataset 例外を増やす提案をしない。** ユーザー明示指示時のみ。

## pre-commit フック

| ファイル | 役割 |
|---|---|
| `.githooks/pre-commit` | Git から呼ばれる入口 |
| `scripts/check-staged-secrets.ps1` | staged パス + テキスト秘匿パターン検査 |
| `scripts/check-ps1-utf8-bom.ps1 -Staged` | staged `.ps1` の UTF-8 BOM 検査（PS 5.1 対策） |
| `scripts/install-git-hooks.ps1` | フックインストール |

手動検査:

```powershell
.\scripts\check-staged-secrets.ps1
.\scripts\check-ps1-utf8-bom.ps1
# 日本語入り .ps1 の BOM 欠落を直す:
.\scripts\check-ps1-utf8-bom.ps1 -Fix
```

Rule: `kaggle-ps1-utf8-bom`（alwaysApply）
## Agent の禁止事項

- `dataset/` 配下を `git add` しない（`.gitkeep` / `README.md` 除く）
- API キー・トークンを Notebook / Markdown / コミットメッセージに書かない
- `.env` の中身をチャットやファイルに貼らないようユーザーに促す
- `git push --force` をユーザー明示なしに実行しない
- 大容量 LoRA / zip を Git LFS なしで push しない

## コミット前チェックリスト

- [ ] `git diff --cached --name-only` に `dataset/` データファイルが無い
- [ ] `.env` / `kaggle.json` が staged に無い
- [ ] staged の日本語入り `.ps1` が UTF-8 BOM 付き（`check-ps1-utf8-bom.ps1 -Staged`）
- [ ] Notebook にハードコードされた API キーが無い
- [ ] 公開 repo なら Private LB・個人メール・内部 URL を Markdown から除去

## GitHub 公開時の追加注意

- **Public** 前提で scrub（個人名は任意、メール・キー・生データは不可）
- 他者 Notebook の **丸コピー** は著作・規約リスク — `others-notebook/` は分析メモ中心
- 問題があれば `git filter-repo` 等で履歴除去（**事前にフックで防ぐ方が安全**）

### 横断知見 · インフラは **別 Private repo**（外側に載せない）

| 資産 | Private repo | ローカル |
|---|---|---|
| 知見 | `neko-rr/kaggle-knowledge-store` | `<comp-root>/knowledge/`（nested · outer `.gitignore`） |
| Skills/scripts | `neko-rr/kaggle-infra` | `%USERPROFILE%\.cursor\kaggle-template\` |

- 外側コンペ repo に `knowledge/` を add しない  
- knowledge / infra を **Public にしない**  
- 手順: `_shared/PRIVATE-KNOWLEDGE-AND-INFRA.md`

## 関連 Skill

- `kaggle-comp-bootstrap` — 新コンペ作成・`.gitignore` 同梱 · knowledge clone
- `kaggle-knowledge-harvest` / `sync` / `retrieve`
- `kaggle-cli-fetch` — データ取得は CLI、保存先は `dataset/`（Git 外）

## 追加リソース

- テンプレート: `%USERPROFILE%\.cursor\kaggle-template\root\.gitignore`
- フック: `%USERPROFILE%\.cursor\kaggle-template\root\scripts\`
