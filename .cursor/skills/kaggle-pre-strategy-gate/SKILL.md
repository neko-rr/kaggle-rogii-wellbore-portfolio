---
name: kaggle-pre-strategy-gate
description: 戦略仮説（CHK）に入る前の機械的改善チェックゲート。knowledge/mechanical-improvements.md のカタログから comp-type に応じた項目を exp/pre-strategy-gate.md で潰し、check-pre-strategy-gate.ps1 PASS まで戦略CHKを作らない。コンペ開始時、experiment-checklist 着手前、pre-strategy、機械チェックの依頼で使う。
---

# 戦略前機械チェックゲート

戦略を考える前に、安価モデルでも上から潰せる機械的・一般的な改善点を先に確認する。
進捗が experiment-checklist に散らばって見落とすのを防ぐため、記録先は **`exp/pre-strategy-gate.md` の1ファイルだけ**。

## 2層構成

| ファイル | 役割 | 更新 |
|---|---|---|
| `knowledge/mechanical-improvements.md` | 目的別カタログ（C/A/O/S/G/R/X · 読み専用） | しない（テンプレ・sync で共有） |
| `<comp-root>/exp/pre-strategy-gate.md` | コンペ別の進捗（チェックボックス） | **ここだけ** |

## 手順

1. `docs-ja/comp-profile.md` で comp-type を確定する（未確定なら先に Skill `kaggle-comp-router`）
2. ゲートファイルが無ければ `scripts/init-comp-layout.ps1` で生成（`exp/pre-strategy-gate.md`）
3. カタログのマッピング表に従い、該当する型節の見出しを `## 必須 —`、非該当を `## N/A —` に変更する（`## 型別（未確定）` が残ると FAIL）
4. 上から順に潰す: `- [x]`（PASS · 行末に `— 証拠: <相対パス>`）/ `- [-]`（`N/A: 理由` 必須）
5. 判定を実行:

```powershell
.\scripts\check-pre-strategy-gate.ps1 -CompRoot .\<comp-root>
```

6. **PASS（exit 0）になってから** Skill `kaggle-experiment-checklist` で戦略CHKの作成に進む  
   （その前に Skill `kaggle-cv-design` で `docs-ja/cv-design.md` の **cv_unit** を宣言し、A4 の証拠にする）

## 禁止

- ゲート未PASSのまま experiment-checklist に新規の戦略CHKを作る
- 進捗（[x]/N/A）を CHK 行・retro・exp-index へ再掲する（リンクのみ可）
- カタログにコンペ固有名（tip名・提出番号等）を書く — 固有項目はゲートファイル末尾の「コンペ固有の機械項目」節へ

## SSOT

- カタログ: `knowledge/mechanical-improvements.md`（`kaggle-knowledge-sync` の同期対象）
- 進捗: `<comp-root>/exp/pre-strategy-gate.md`
- 判定: `scripts/check-pre-strategy-gate.ps1`（PASS = exit 0）
