---
name: kaggle-cv-design
description: >-
  Kaggle コンペの CV 単位（row/group/time）宣言、shippable vs oracle、形 smoke、
  knowledge（axis A）を参照した CV 設計を docs-ja/cv-design.md に固定する。
  CV 設計、GroupKFold、リーク、OOF、採択根拠、交差検証と言ったときに使う。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| knowledge retrieve（短） | — | — | dataset docs · Overview · knowledge · prior | docs-ja/cv-design.md · pre-strategy · checklist |

**共通禁止:** row KFold を根拠不十分なまま採択 · oracle を提出 GO に使う · competitions submit

---

# Kaggle CV Design

SSOT: `_shared/CV-DESIGN.md` · Rule `kaggle-cv-design`  
コンペ固有宣言: **`docs-ja/cv-design.md`**（テンプレ: `comp/docs-ja/cv-design.md.template`）

---

## いつ使うか

| タイミング | 動作 |
|---|---|
| Day0 · dataset 把握後 | `cv-design.md` 初版 · unit 宣言 |
| prior-knowledge 生成後 | axis A カードを cv-design に突合 |
| 戦略 CHK 追加前 | pre-strategy A4 証拠 = cv-design |
| CV 方針転換 | changelog + primary 定義の更新 |
| 「この CV でいい？」 | 本 Skill で unit / shippable / knowledge を点検 |

---

## ワークフロー

### Step 0 — 入力を集める

1. Overview / Evaluation · `docs-ja/dataset.md`  
2. `docs-ja/comp-profile.md`（comp-type）  
3. `docs-ja/comp-strategy.md`（primary レーン別名）  
4. **knowledge:**

```powershell
cd knowledge; git pull origin main
../scripts/run-kaggle-knowledge.ps1 -Action retrieve `
  -CompRoot "./<inner>" -IncludeCandidates -Limit 20
```

`exp/prior-knowledge.md` を **domain → A（物差し・CV）優先** で読む。

### Step 1 — unit を決める

| 問い | 結果の候補 |
|---|---|
| 同一実体が複数行？ | **group** + キー列名 |
| test が未来側？ | **time** |
| Host split 指定？ | **custom** |
| どれも弱い？ | row は **最後** · 根拠段落必須 |

`cv_unit` と **リークすると何が壊れるか** を1段落。

### Step 2 — shippable を定義する

- 提出と同型の入力で回る評価スクリプト / OOF の path  
- **oracle / ceiling / leak 指標の名前を「採用根拠に使わないリスト」へ**

### Step 3 — knowledge 表

| card_id (KGL-…) | 採否 | 理由（apply/avoid） | 取り込み内容 |
|---|---|---|---|
| | adopt / reject | | fold 型・注意点 |

不採用も残す（同じ失敗の再輸入防止）。

### Step 4 — early smoke

profile に応じ §3 の smoke 項目を `cv-design.md` と checklist **CHK-00S** に落とす。  
性能 CHK は smoke 後。

### Step 5 — ゲート連携

- `exp/pre-strategy-gate.md` **A4** 証拠 → `docs-ja/cv-design.md`  
- **A5** CV–LB は 2 点以上または unknown 明示  
- **X3** prior + axis A 参照を記録  
- 判定: `check-pre-strategy-gate.ps1` PASS 後に戦略 CHK  

### Step 6 — checklist へ

新規 primary CHK の acceptance は SSOT の **shippable テンプレ**を使う。  
oracle 実験は `lane:diagnostic` + diagnostic テンプレ。

---

## 品質チェック

- [ ] `cv_unit` 宣言あり  
- [ ] row の場合、group/time 不要な根拠がある  
- [ ] shippable 定義があり oracle と分離  
- [ ] knowledge A を見たか / 空なら「カード無し」と X3 に書いた  
- [ ] smoke 項目が performance CHK より前  
- [ ] primary alias が strategy レーンと一致  

---

## 他 Skill

| Skill | 関係 |
|---|---|
| `kaggle-knowledge-retrieve` | prior · axis A |
| `kaggle-pre-strategy-gate` | A4/A5/X3 |
| `kaggle-experiment-checklist` | acceptance · smoke CHK |
| `kaggle-lanes-final-strategy` | primary 物差し |
| `kaggle-pretrain-gate` | 長い学習前の別ゲート |
| `kaggle-submission-validator` | 形の最終確認（smoke の後段） |
