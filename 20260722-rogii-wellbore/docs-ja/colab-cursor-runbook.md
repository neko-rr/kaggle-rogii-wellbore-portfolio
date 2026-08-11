# Colab × Cursor 実行メモ — rogii-wellbore

> Skill: **`cursor-colab-runtime`**（推奨: **Colab MCP** · 代替: VS Code/Cursor 拡張）  
> 汎用接続: グローバル **`google-colab-mcp`**  
> 公式 MCP: https://developers.googleblog.com/announcing-the-colab-mcp-server-connect-any-ai-agent-to-google-colab/  
> 公式拡張: https://developers.googleblog.com/google-colab-is-coming-to-vs-code/  
> コンペ固有の Input / データパス / GPU 方針のみここに書く。接続手順 SSOT は Skill 本体。

## 本コンペでの Colab 用途

| 用途 | ノート配置 | GPU |
|---|---|---|
| **Final Trust T2→773（CHK-FINAL-T2）** | `my-local-eval-notebook/tip-cv-final-t2-colab/` | **要** · Drive 必須 |
| tip-train-cv バックアップ（CHK-014） | `my-local-eval-notebook/tip-train-cv-colab/` | T4 等 |
| _（例: 長時間学習）_ | `my-notebook/` | T4 等 |

**FINAL-T2 Drive ROOT:**  
`/content/drive/MyDrive/Kaggle/rogii-wellbore/20260722-rogii-wellbore/exp/work/colab-final-t2/`

**レーン判断 SSOT:** [`tip-cv-kaggle-vs-colab.md`](tip-cv-kaggle-vs-colab.md)  
（主=Kaggle Ver3 · 副=Colab。依存 DS が多いため Colab は再失敗／9h 超時）

## 経路（本コンペ）

| 経路 | いつ | Agent |
|------|------|-------|
| **A. Colab MCP（推奨）** | Agent にブラウザ Colab 上でセル操作させたいとき | 接続後にセル追加・実行可（操作対象は同時1本） |
| **B. Colab 拡張（代替）** | MCP 不可 · ローカル `.ipynb` をカーネル接続したいとき | 手順提示 · 編集のみ（実行はユーザー UI） |

Web 上の並列ランタイムはユーザー側。MCP の「操作対象1本」とは別概念。

## データ

| データ | 取得方法 | Colab 上のパス |
|---|---|---|
| コンペ + tip 依存 DS（7本） | **Colab Secrets** → Kaggle API DL（Bootstrap セル · 鍵は出力禁止） | `/kaggle/input/competitions/...` · `/kaggle/input/datasets/...` |
| 大容量・永続 | **Drive マウント**（必要時） | `/content/drive/MyDrive/...` |
| 代替（経路 B・小ファイル） | Mount Server → `sample_data/kaggle.json` と手動配置 | tip が読む `/kaggle/input` 相当に symlink |

Secrets 名・手順の詳細は Skill **`cursor-colab-runtime`** § Colab 上の Kaggle API。  
提出・Public 作成・push はユーザー明示 OK が必要（Rule `kaggle-private-assets` · `kaggle-comp-confidentiality`）。

## 実行後

- `my-ran-notebook/{nb-name}/run-log.md` — Skill `kaggle-kernels-runbook`
- `lifecycle-manifest.md` — state: `ran`
- 長時間 GPU 前は **pretrain-gate PASS**（Kaggle / Colab 共通）

## アクセス手順（短縮）

ユーザーが「Colab 接続」と言ったら Skill **`cursor-colab-runtime`** を開き、次を案内する:

1. **経路 A:** 対象ノートを [colab.research.google.com](https://colab.research.google.com) で開く → MCP 接続（グローバル `google-colab-mcp`）
2. **経路 B:** Cursor で `.ipynb` → Select Kernel → Colab → ユーザーがセル実行 · 終了時 Disconnect
