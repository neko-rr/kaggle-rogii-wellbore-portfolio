# Decision Flow — Kaggle 汎用（入口地図）

> **1 枚で「次に何をするか」を固定する。** 詳細は各 Skill / SSOT。  
> コンペ固有の数字（Public%、Final 本数）は `docs-ja/` のみ。

---

## Day0（コンペ開始 · 必須 3 ファイル）

| # | ファイル | 書くこと | Skill |
|---|---|---|---|
| 1 | `docs-ja/comp-timeline.md` | 締切 UTC · 1日上限 · Final **N** / sim **K** | `kaggle-comp-timeline` · `kaggle-competition-constraints` |
| 2 | `docs-ja/comp-strategy.md` | レーン · shake · compass · Final スロット方針 | `kaggle-lanes-final-strategy` |
| 3 | `docs-ja/cv-design.md` | **cv_unit** · shippable · smoke · knowledge A | `kaggle-cv-design` |

Day0 必須 3 ファイルのあと: `requirements-local.txt` + `setup-comp-venv.ps1`（Skill `kaggle-comp-deps`）。

---

## 通常実験ループ

```text
exp-index 読む
  → checklist Active の 1 CHK（lane: + shippable acceptance）
  → ローカル計算: setup-comp-venv（requirements-local）· ImportError ならリスト追記
  → Agent がコードを書いたら run-static-checks.ps1（**必須 · 拡張 Ruff 不可換**）
  → ban-gate pre（soft: lane · cv_unit）
  → shape smoke 済み？（CHK-00S）でなければ性能 CHK を始めない
  → pretrain-gate（長時間時）
  → 本実験
  → ban-gate post · table · train/infer
```

**毎 CHK でやらない:** SA-7 · Full Final レビュー · timeline 再発明  
**コード変更 CHK では毎回やる:** `kaggle-static-check`（SA-8 可）

---

## 高コスト判定（SA-7）

| 直前 | mode | Skill / Agent |
|---|---|---|
| Bet / Wave 大改訂 | pre-bet | `/kaggle-adversarial-review` |
| Final / 有効枠 | pre-final | 同上 |
| 他者・外部本採用 T1 | pre-adopt | 同上 |
| cv_unit 固定 | pre-cv-lock | 同上 + `kaggle-cv-design` |
| harvest / promote | pre-harvest | 同上 + knowledge harvest/promote |

GO は **親 Agent + ユーザー**。SA-7 は裁決しない。  
SSOT: `_shared/ADVERSARIAL-REVIEW.md`

---

## 3 段ゲートとの関係

```text
static-check  →  形 smoke / pretrain-gate  →  本実験（runbook）  →  submission-validator  →  （ユーザー）提出
```

| ゲート | 役割 | 代替に使わない |
|---|---|---|
| **static-check** | 構文 · notebook · private · ruff CLI | エディタ Ruff 拡張 |
| ban / Fnnn | 既知禁止の型 | SA-7 の論証穴チェック |
| lanes / CV Rule | 物差しの誤用禁止 | validator |
| SA-7 | 今回の論証の穴 | ban-gate · pretrain |
| pretrain | 即死・無意味学習 | Final 枠選び |
| validator | 提出形 | GO 戦略そのもの |

---

## 役割分担（衝突防止）

| 仕組み | 仕事 |
|---|---|
| **static-check + ruff CLI** | Agent 執筆コードの構文・notebook 即死を実行前に止める |
| **comp deps + setup-comp-venv** | コンペ計算依存（numpy 等）をリスト再現 |
| **ban-gate + Fnnn** | 台帳に載った抽象仮説の再実行阻止 |
| **SA-7 adversarial** | 高コスト提案の論証殺し |
| **lanes + CV design** | どの指標で勝つ・どの split が shippable か |
| **constraints / medals** | N · 日次上限 · UTC · メダル帯の計算（捏造禁止） |
| **knowledge** | 過去 apply/avoid · axis A→C→B |

---

## post-comp

```text
retro-setup → private / LB / solutions / lessons
  → SA-7 pre-harvest（推奨）
  → knowledge harvest → validate → audit → knowledge-store push
```

---

## エージェント入口

| 迷い | 読む |
|---|---|
| どの Skill？ | `kaggle-comp-router` · `docs-ja/comp-profile.md` |
| サブに振る？ | `kaggle-subagent-delegate` · `_shared/SUBAGENT-BRIEF.md` |
| infra 範囲 | `_shared/INFRA-SCOPE.md` |

エージェント配置の正本: **`scripts/templates/cursor-agents/`** → `install-cursor-agents.ps1`  
（`.cursor/agents/` は生成物。直編集禁止）
