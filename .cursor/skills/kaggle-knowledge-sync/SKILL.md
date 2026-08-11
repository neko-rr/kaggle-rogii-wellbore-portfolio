---
name: kaggle-knowledge-sync
description: >-
  Private knowledge-store とローカル knowledge/ の同期。git pull/push 優先。
  Git 未使用時のみ peer フォルダへ ID 確認付き・削除なし・既定ドライランで同期する。
---

# Kaggle Knowledge Sync

横断知見の接続。**第一選択は Private GitHub `kaggle-knowledge-store` の clone / pull / push。**  
Git が使えない・別ディスク peer があるときだけ `run-kaggle-knowledge.ps1 -Action sync`。

SSOT: `_shared/PRIVATE-KNOWLEDGE-AND-INFRA.md` · Rule `kaggle-knowledge-isolation`

## 推奨（Git · Private knowledge-store）

```powershell
# 未配置
git clone https://github.com/neko-rr/kaggle-knowledge-store.git knowledge
# または $env:KAGGLE_KNOWLEDGE_GIT_URL

# 取り込み（他コンペの harvest 後）
cd knowledge
git pull origin main

# 収穫後の反映
git add -A
git commit -m "harvest: <comp-slug>"
git push origin main
```

`store_id` を壊すな。空の `init` で新 UUID を作らない。

## peer 同期（Git 代替）

### 安全規則

- Skill に PC 固有パスを保存しない。peer は実行時の相対パス
- 既定ドライラン。`-Apply` はユーザー確認後
- 削除・上書き・競合自動解決をしない
- `store_id` 不一致は停止
- `-AdoptStore` はコピー先が空のときだけ
- sync 前に audit PASS 必須

### ドライラン

```powershell
./scripts/run-kaggle-knowledge.ps1 -Action sync `
  -PeerRoot "../<other-kaggle-project>/knowledge" `
  -Direction pull
```

空ストア参加:

```powershell
./scripts/run-kaggle-knowledge.ps1 -Action sync `
  -PeerRoot "../<source-project>/knowledge" `
  -Direction pull -AdoptStore
```

確認後 `-Apply`。その後 `-Action validate`。

## Agent

1. まず `knowledge/.git` の有無を見る → あれば `git pull` / harvest 後 `push`  
2. 無ければ clone URL を提示してから peer sync  
3. Public へ push しない  
