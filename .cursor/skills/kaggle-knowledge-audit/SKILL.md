---
name: kaggle-knowledge-audit
description: Kaggle横断知見の秘密情報・絶対パス・出典・ライセンス・転載リスクを検査する。knowledge同期前、外部知見追加後、上位解法分析前に使う。
---

# Kaggle Knowledge Audit

`knowledge/` を **Private knowledge-store への git push** または **peer sync** する前に、秘密情報と外部由来の provenance を検査する。

## 実行

```powershell
./scripts/run-kaggle-knowledge.ps1 -Action audit
```

## FAIL

- API key、token、private key、認証情報らしい文字列
- 絶対パス
- 外部由来なのにHTTPSの`source_url`がない
- 外部コードのlicenseが`unknown`

## WARN

- 公開解法・Discussionのlicenseが未確認
- provenance reviewが未完了
- 外部本文を大量転載した可能性

外部知見は原文を保存せず、要約・source URL・license・再配布条件を記録する。  
**audit FAIL 時は push / peer sync しない。** 秘密候補の値をチャットやログへ再掲しない。  
push 手順: `_shared/PRIVATE-KNOWLEDGE-AND-INFRA.md`
