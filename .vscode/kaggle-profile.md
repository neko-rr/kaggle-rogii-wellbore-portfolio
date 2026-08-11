# Kaggle-Light Profile セットアップ（汎用）

Kaggle コンペを Cursor で軽く作業するための **Profile + 設定ファイル一式**です。

---

## 起動方法（推奨）

```powershell
.\scripts\open-kaggle-light.ps1
```

**`Kaggle.code-workspace` は使わない**（チャット履歴が別セッションに分断される）。

## 新コンペの自動作成

```powershell
& "$env:USERPROFILE\.cursor\kaggle-template\scripts\new-kaggle-comp.ps1" -Name "<comp-slug>"
```

Skill: `kaggle-comp-bootstrap`

---

## 初回セットアップ（各 PC で 1 回）

1. Profiles → Import Profile → `.vscode/profiles/Kaggle-Light.code-profile`
2. コンペフォルダを `open-kaggle-light.ps1` で開く

---

## トラブルシュート

| 症状 | 対処 |
|---|---|
| チャットが消えた | フォルダで開き直す（`.code-workspace` を使わない） |
| Profile が効かない | `open-kaggle-light.ps1` で起動 |
| 新コンペを作りたい | `new-kaggle-comp.ps1` を実行 |

詳細: `<comp-root>/.cursor/skills/kaggle-comp-bootstrap/reference.md`  
Skill は **プロジェクト内のみ**（`~/.cursor/skills/` には置かない）
