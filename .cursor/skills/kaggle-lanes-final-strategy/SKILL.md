---
name: kaggle-lanes-final-strategy
description: >-
  レーン（primary/public/diagnostic）定義、Final/有効枠 N の多様性格納、
  LB 信頼性・shake-up・improvement compass を comp-strategy に固定する。
  Trust vs Public、Final2、shake-up、提出枠方針、道しるべと言ったときに使う。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | 任意 Overview | — | Overview · Discussion · exp · docs-ja | docs-ja/comp-strategy.md · checklist · timeline |

**共通禁止:** 他コンペの N・Public% を流用 · competitions submit

---

# Lanes · Final · Compass

SSOT: `_shared/LANES-AND-FINAL-SLOTS.md` · Rule `kaggle-lanes-and-final-slots`

---

## いつ使うか

| タイミング | 動作 |
|---|---|
| Day0 · 概要作成後 | strategy にレーン・N・仮 compass を初版 |
| Discussion 要約後 | shake / Public 比率・Host 示唆を取り込み compass 更新 |
| 自チームで CV≠LB が観測された | agreement · shake_risk を改訂 |
| Final 締切前 | Final チェックリストを閉じる |
| 「どれを伸ばす？」 | compass + 次 CHK の lane を提示 |

---

## Step 1 — レーン定義（comp-strategy）

`docs-ja/comp-strategy.md` に:

```markdown
## レーン（物差し）

| Lane ID | このコンペでの別名 | 物差し | 用途 |
|---|---|---|---|
| primary | （例: OOF / group CV / …） | | 主 GO/NO-GO |
| public | Public LB | | 監視 · 枠保険 |
| diagnostic | （任意） | | 診断のみ |

### レーン停止規則
- primary の判断に public 小差だけを使わない
- public 専用 CHK は public で判定
- diagnostic で全体を止めない
- 小差閾値: （コンペで定義 or 未定義＝断定禁止）
```

---

## Step 2 — Final / 有効枠 N

1. Overview / Rules から **N**（Final 選択）または **K**（sim 最新）を読む  
2. `comp-timeline` に数値 + source  
3. strategy にスロット表:

| N | 方針 |
|---:|---|
| 1 | slot-1 = primary 最良のみ |
| ≥2 | slot-1 = primary · 他 slot = diversify（shake med+ または public partial） |
| sim latest K | 「選択」ではなく **最新 K**。diversify は提出系列で管理 |

**禁止:** 未確認のまま「Final 2」と断定。

---

## Step 3 — LB プロファイル · 道しるべ

Discussion · intel · 自結果から:

| 項目 | 記入 |
|---|---|
| public_scope | full-ish / partial / unknown + 根拠1行 |
| shake_risk | low / medium / high |
| cv_lb_agreement | strong / mixed / weak / unknown |
| improvement_compass | 1〜3 行の矢印（例: primary 優先 · public は枠2保険のみ） |

### 道しるべ → 実験

| compass | 次に載せる CHK の lane |
|---|---|
| primary 優先 | 大半 `lane: primary` |
| public 監視 | `lane: public` は少数 · 提出枠用 |
| 診断で原因切り分け | `lane: diagnostic` · 完了後 primary へ戻す |

Bet と CHK は compass と矛盾させない。

---

## Step 4 — Final 前ゲート（N 本）

```text
[ ] N/K を timeline で再確認
[ ] 各 slot に提出 ID と lane を記入
[ ] N≥2 かつ shake≥med → public-only 一系統だけで埋めていない
[ ] diagnostic 面を slot に載せていない（方針で明示した場合を除く）
```

結果は `comp-strategy` § Final と `exp-index` 次アクションへリンク。

---

## 出力・更新ファイル

| ファイル | 必須節 |
|---|---|
| `docs-ja/comp-strategy.md` | レーン · LB プロファイル · Final スロット · compass |
| `docs-ja/comp-timeline.md` | N/K 数値 |
| `exp/experiment-checklist.md` | CHK の `lane:` · Final 前チェック行 |
| `exp/exp-intel.md` | 根拠メモ（任意 1〜3 行） |

---

## 品質

- [ ] N を推測で書いていない  
- [ ] レーン未記入の GO/NO-GO が残っていない  
- [ ] 他レーン停止の言い回しが無い  
- [ ] compass が Discussion 更新後に古いままになっていない  
