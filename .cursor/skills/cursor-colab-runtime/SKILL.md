---
name: cursor-colab-runtime
description: >-
  Kaggle コンペで Google Colab を使う手順。推奨は公式 Colab MCP（Agent がセル操作）。
  代替は公式 Colab VS Code/Cursor 拡張。Drive マウント、Colab Secrets 経由の Kaggle API、
  GitHub 不要、MCP 操作はノート1本・Web上の並列実行は別。Colab 接続・MCP・Drive・
  Kaggle Secrets と言ったときに使う。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | Colab MCP（接続済み時） | — | .ipynb · docs-ja/colab-*.md · my-*-notebook/ | my-notebook/ · my-ran-notebook/run-log.md · lifecycle-manifest.md |

**要ユーザー明示 OK:** 長時間 GPU/TPU Colab 実行 · コンペ中の GitHub private 同期

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力 · コンペ中の Public 公開

# Cursor × Google Colab（Kaggle コンペ）

## 経路の選び方

| 経路 | 公式根拠 | Agent の役割 | いつ使う |
|------|----------|--------------|----------|
| **A. Colab MCP（推奨）** | [Colab MCP 発表](https://developers.googleblog.com/announcing-the-colab-mcp-server-connect-any-ai-agent-to-google-colab/) · [googlecolab/colab-mcp](https://github.com/googlecolab/colab-mcp) | ブラウザ Colab のセル追加・実行・更新 | Agent に Colab 上で作業させたいとき |
| **B. Colab VS Code 拡張（代替・公式）** | [Colab is Coming to VS Code](https://developers.googleblog.com/google-colab-is-coming-to-vs-code/)（2025-11-13） | 手順提示 · ローカル `.ipynb` 編集。**実行はユーザー UI** | MCP が使えない／ローカル ipynb をカーネル接続したいとき |

汎用の接続手順 SSOT: グローバル Skill **`google-colab-mcp`**（`~/.cursor/skills/google-colab-mcp/`）。  
本 Skill は **Kaggle コンペ固有**（フォルダ・run-log・提出分担・機密）を足す。

## GitHub は不要

- Colab 開始に GitHub は要らない（Google アカウント＋必要なら Drive）
- コンペ中に同期するなら Rule `kaggle-comp-confidentiality`: **private ＋ 事前承認**
- コンペ終了後の意図的 Public 化はユーザー判断（Agent は無断公開しない）

## 操作と並列実行の区別（重要）

| 概念 | 実態 |
|------|------|
| **Agent が MCP で操作できるノート** | **同時に 1 本だけ**（前面のブラウザ Colab に接続） |
| **Web 上で走らせるランタイム** | ユーザーが **複数セッションを並列実行してよい**（実績として最大3程度）。MCP の「操作対象」とは別 |

つまり「同時実行 3」と「Agent 同時操作 1」は矛盾しない。並列ジョブはユーザーが Web で起動し、Agent は接続中の 1 ノートだけ編集・実行指示する。

## 経路 A: Colab MCP（推奨）

詳細はグローバル `google-colab-mcp`。Kaggle 時の追加チェック:

1. ユーザーが対象ノートを [colab.research.google.com](https://colab.research.google.com) で開く
2. Agent: `mcp_auth`（必要時）→ `open_colab_browser_connection` → `get_cells` / `run_code_cell`
3. 大容量データは Drive マウント（FAQ: https://research.google.com/colaboratory/faq.html）
4. **Kaggle API が必要なら Colab Secrets 経由で利用可**（§ Colab 上の Kaggle API）
5. 長時間 GPU は `kaggle-pretrain-gate` PASS 後のみ
6. 実行後: `my-ran-notebook/` · `run-log.md` · `lifecycle-manifest.md`（`kaggle-kernels-runbook`）

Drive 例:

```python
from google.colab import drive
drive.mount("/content/drive")
ROOT = "/content/drive/MyDrive/<comp-or-project>"
```

## Colab 上の Kaggle API（Secrets）

**このユーザー環境では Colab に Kaggle 秘密鍵（Secrets）を設定済み。**  
Drive だけでなく、**Colab から直接 Kaggle CLI / API を使える**（データ取得・kernels 操作など）。

### Agent の使い方

1. ノート先頭付近で Secrets → 環境変数へ載せる（**値を print / ログしない**）
2. 必要なら `pip install -q kaggle`（未導入時のみ）
3. 読取系（download / list / status）は作業に応じて実行可
4. **提出・Public 作成・push は従来どおりユーザー明示 OK が必要**（`PERMISSIONS` · `kaggle-private-assets` · `kaggle-comp-confidentiality`）

```python
from google.colab import userdata
import os
from pathlib import Path

# Secrets 名はユーザー環境に合わせる（例: KAGGLE_USERNAME / KAGGLE_KEY）
os.environ["KAGGLE_USERNAME"] = userdata.get("KAGGLE_USERNAME")
os.environ["KAGGLE_KEY"] = userdata.get("KAGGLE_KEY")

# 一部ツールは ~/.kaggle/kaggle.json を要求する
cfg = Path.home() / ".kaggle" / "kaggle.json"
cfg.parent.mkdir(parents=True, exist_ok=True)
cfg.write_text(
    '{"username":"%s","key":"%s"}'
    % (os.environ["KAGGLE_USERNAME"], os.environ["KAGGLE_KEY"])
)
cfg.chmod(0o600)
# 絶対に username/key をセル出力へ出さない
```

### 禁止

- Secrets の値をセル出力・`run-log.md`・チャット・Git に書く
- ノートに API キーをハードコードする
- コンペ中の Public dataset / Public kernel 化
- ユーザー承認なしの `competitions submit` / 公開系操作

### 使い分け

| やりたいこと | 優先 |
|--------------|------|
| 大容量の永続置き場 | **Drive** |
| コンペ公式データ・Kernel 取得 | **Colab + Kaggle Secrets** |
| 提出・公式評価 | **Kaggle Notebook**（最終はここ） |

## 経路 B: 公式 Colab VS Code / Cursor 拡張（代替）

公式: https://developers.googleblog.com/google-colab-is-coming-to-vs-code/  
Open VSX（Cursor 等）でも配布。

### ユーザー向け手順（依頼時に提示）

1. Extensions で **Google Colab**（＋依存 **Jupyter**）を Install
2. ワークスペースの **`.ipynb`** を開く
3. **Select Kernel** → **Colab** → Sign in → Auto Connect または New Colab Server
4. CPU / GPU / TPU を選ぶ
5. セル実行は **ユーザーが UI で行う**（Agent はこの経路ではランタイムに直接接続しない）
6. 終了時 **Disconnect**（Compute 節約）

小〜中ファイル: `Mount Server to Workspace` → `sample_data/`（詳細は [reference.md](reference.md)）

**Agent は「拡張経路で実行完了」と報告しない。** ユーザーがセル実行を確認してから。

## Kaggle との分担

| 実行場所 | いつ |
|----------|------|
| **Colab + Drive** | 重い学習・大量 sim・**大量 episode/対戦ログ**（本体は Drive） |
| **Kaggle Notebook** | Input 固定・提出直前・公式評価 |
| **ローカル `.venv`** | smoke · 薄い検証のみ（大容量は書かない） |

### Drive 主戦場（simulation / 大容量ログ想定）

- 推奨実体: `G:\マイドライブ\Kaggle\<comp-slug>\<yyyymmdd-comp-slug>\`
- ローカルは同名パスを **ジャンクション** にして Cursor パスを維持してよい
- Colab: `/content/drive/MyDrive/Kaggle/<comp-slug>/<yyyymmdd-comp-slug>`
- **episodes / 対戦記録は必ず上記配下**（`exp/` · `sim-track/` 等）。C の Desktop 直下に置かない
- コンペ固有の実パスは各 ROOT の `cursor.md` を SSOT とする

自作 Kaggle Notebook / Dataset / Model は常に **Private**（`kaggle-private-assets`）。

## トラブルシュート（最短）

| 症状 | 対処 |
|------|------|
| MCP ツールが増えない | ノートを前面表示 → 再認証 → 再接続 → Cursor Reload |
| 拡張に Colab が出ない | Jupyter 導入 · Open VSX · 再起動 |
| Drive I/O 失敗 | FAQ どおりフォルダ件数整理 |
| 別ノートを触りたい | そのノートを開く → MCP 再接続（操作対象は常に1本） |

## 他 Skill / Rule

| 名前 | 役割 |
|------|------|
| グローバル `google-colab-mcp` | MCP 設定・接続の汎用手順 |
| `kaggle-kernels-runbook` | run-log · 実行記録 |
| `kaggle-pretrain-gate` | 長時間 GPU 前 |
| `kaggle-notebook-folders` | ipynb lifecycle |
| Rule `kaggle-comp-confidentiality` | コンペ中 Public 禁止 · GitHub 任意 |
| Rule `kaggle-private-assets` | Kaggle 資産 Private · 実行承認 |

詳細: [reference.md](reference.md)
