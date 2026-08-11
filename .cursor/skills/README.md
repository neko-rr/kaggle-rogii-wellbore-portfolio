# Kaggle Skills（このリポジトリ）

ROGII 本コンペで使った **Cursor Agent Skills** です。親 Agent が必要時に `SKILL.md` を読み、手順・ゲート・禁止事項に従います。

> **配置:** コンペ ROOT の `.cursor/skills/` のみ（グローバル `~/.cursor/skills/` に Kaggle 実行系を置かない）。  
> **公開入口:** リポジトリ根の [README.md](../../README.md)（エージェント運用節）。

## まず見る Skill（本コンペの制御面）

| Skill | 役割 |
|---|---|
| [kaggle-experiment-checklist](kaggle-experiment-checklist/SKILL.md) | 仮説 1 件ずつの CHK ループ |
| [kaggle-static-check](kaggle-static-check/SKILL.md) | 本実験前の静的検査 |
| [kaggle-pretrain-gate](kaggle-pretrain-gate/SKILL.md) | 長時間学習前ゲート |
| [kaggle-lanes-final-strategy](kaggle-lanes-final-strategy/SKILL.md) | Trust / Public / diagnostic · Final 枠 |
| [kaggle-cv-design](kaggle-cv-design/SKILL.md) | CV 単位宣言 · shippable vs oracle |
| [kaggle-submission-validator](kaggle-submission-validator/SKILL.md) | 提出前検証 |
| [kaggle-git-security](kaggle-git-security/SKILL.md) | dataset / 秘匿の Git 境界 |
| [experiment-management](experiment-management/SKILL.md) · [experiment-result-management](experiment-result-management/SKILL.md) | exp SSOT |

## 共有 SSOT（`_shared/`）

| 文書 | 内容 |
|---|---|
| [DECISION-FLOW.md](_shared/DECISION-FLOW.md) | 判断ゲート地図 |
| [LANES-AND-FINAL-SLOTS.md](_shared/LANES-AND-FINAL-SLOTS.md) | レーン · Final N |
| [CV-DESIGN.md](_shared/CV-DESIGN.md) | CV 設計 |
| [STATIC-CHECKS.md](_shared/STATIC-CHECKS.md) | 静的検査 |
| [NOTEBOOK-LINKED-SUBMIT.md](_shared/NOTEBOOK-LINKED-SUBMIT.md) | Notebook 紐づけ提出 |
| [EXPERIMENT-ID-NAMESPACES.md](_shared/EXPERIMENT-ID-NAMESPACES.md) | CHK / Fnnn / T0–T4 |
| [PERMISSIONS.md](_shared/PERMISSIONS.md) | Agent が触ってよい境界 |

## CLI ゲート（同梱 scripts）

Skills だけでは足りない機械チェックは [`../../scripts/`](../../scripts/) 側:

- [`run-static-checks.ps1`](../../scripts/run-static-checks.ps1)
- [`run-hypothesis-ban-gate.ps1`](../../scripts/run-hypothesis-ban-gate.ps1)
- [`check-staged-secrets.ps1`](../../scripts/check-staged-secrets.ps1)
- [`validate-submission.ps1`](../../scripts/validate-submission.ps1)

## 常時 Rules

[`.cursor/rules/`](../rules/) の `.mdc`（例: [decision-gates](../rules/kaggle-decision-gates.mdc) · [public-lb-bias-stop](../rules/kaggle-public-lb-bias-stop.mdc) · [hypothesis-ban-ledger](../rules/kaggle-hypothesis-ban-ledger.mdc)）。

## その他の Skill

`kaggle-*/` · `post-comp-*` · `discussion-summary` · `notebook-analysis` など、フォルダ名が説明になっています。各 `SKILL.md` の description を参照。

## メンテメモ（作者向け）

並行コンペやテンプレ同期を行う場合の手順は従来どおり template 経由。  
公開リポを読むだけなら **上の表と各 SKILL.md で足りる**。
