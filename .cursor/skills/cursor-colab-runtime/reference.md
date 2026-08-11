# Cursor × Colab — リファレンス（Kaggle）

## 公式 URL

| 項目 | URL |
|------|-----|
| **Colab MCP（Agent 操作・推奨）** | https://developers.googleblog.com/announcing-the-colab-mcp-server-connect-any-ai-agent-to-google-colab/ |
| Colab MCP 実装 | https://github.com/googlecolab/colab-mcp |
| **Colab VS Code 拡張（代替・公式）** | https://developers.googleblog.com/google-colab-is-coming-to-vs-code/ |
| Open VSX（Cursor 等） | https://open-vsx.org/ |
| Colab FAQ（Drive） | https://research.google.com/colaboratory/faq.html |
| Colab 本体 | https://colab.research.google.com/ |

## 経路の役割分担

| 経路 | Agent | ユーザー |
|------|-------|----------|
| MCP | セル追加・実行・更新（**操作対象ノートは同時1本**） | 対象ノートをブラウザで開く · Drive 認証 · 並列セッション起動 |
| VS Code/Cursor 拡張 | ipynb 編集 · 手順提示 | Select Kernel · セル実行 · Disconnect |

Web 上の **並列ランタイム**（実績として最大3程度）はユーザー側。MCP の同時操作上限とは別概念。

## 拡張の入手（経路 B）

- Cursor: Extensions → **Google Colab** を Install
- 見つからない場合: Open VSX
- 依存: **Jupyter**（Microsoft）

## データの渡し方

### 経路 A（ブラウザ Colab + MCP）

1. **Google Drive**（大容量の永続置き場）
2. **Kaggle API via Colab Secrets**（設定済み想定 · 値は出力禁止）
3. 公開 URL の wget / gdown

#### Kaggle Secrets 注意

- ユーザー環境では Colab Secrets に Kaggle 鍵が設定済み → Colab から直接 Kaggle 利用可
- `userdata.get(...)` で読み、**print / ログ / Git に出さない**
- 提出・Public 化はユーザー明示 OK が必要（ローカルと同じ禁止事項）

### 経路 B（Cursor 拡張）

1. **`Mount Server to Workspace`** → `sample_data/`（小〜中）
2. Drive（`drive.mount` は環境により不安定な報告あり → 小ファイルは Workspace マウント優先）
3. Kaggle API / wget

参考: [Zenn — Mount Server](https://zenn.dev/kotawatanabe/articles/f454f706c8d7e6)

## Compute / セッション

- 作業終了時 **Disconnect**（または Runtime → Disconnect and delete runtime）
- 並列セッションはクォータを消費する。不要なものは止める
- Pro ユーザーは Colab のランタイム一覧で確認

## 機密（Kaggle）

- コンペ中: GitHub Public 禁止 · 同期するなら private＋事前承認（`kaggle-comp-confidentiality`）
- 終了後: 意図的 Public 可（scrub 後 · ユーザー指示）
- Colab に GitHub は不要

## Cursor 固有

- **`.code-workspace` は使わない** — フォルダで開く
- Profile: **Kaggle-Light**（`open-kaggle-light.ps1`）
- グローバル接続手順: `~/.cursor/skills/google-colab-mcp/`
