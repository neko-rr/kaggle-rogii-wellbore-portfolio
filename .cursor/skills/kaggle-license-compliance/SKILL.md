---
name: kaggle-license-compliance
description: >-
  外部モデル・データ・API・他者 Notebook 追加時のライセンス台帳更新（Tier R）と、
  メダル/賞金前の BOM 監査（Tier A+）。Discussion で主催者明示許可があれば GREEN に昇格。
  ライセンス、Rules、外部データ、Winner License、Host 許可、Reasonableness と言ったときに使う。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| — | —（ライセンスカード確認はブラウザ） | — | docs-ja/license-ledger.md | docs-ja/license-ledger.md · license-audits/ |

**要ユーザー明示 OK:** 外部モデル/API 追加（Tier R 記録）

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle License Compliance

**全コンペ共通。** SSOT: `docs-ja/license-ledger.md`  
Rules 上のライセンス・外部データ・Winner License を **メダル圏でアウトにしない** ための台帳と監査。

`kaggle-git-security`（Git 再配布）・`kaggle-submission-validator`（zip 形式）とは **別レイヤー**。

---

## Tier

| Tier | トリガー | 必須 |
|---|---|---|
| **R（Register）** | 外部 base/adapter/data/API/AMLT/他者 NB を **新規採用** | **常時必須** |
| **A（Audit-lite）** | 通常 LB 提出前（任意） | RED が提出経路に無いか |
| **A+（Audit-full）** | Final 2 選択・メダル/賞金狙い | **必須** |

**外部依存を 1 つでも足したら Tier R を PASS するまで pretrain-gate / 長時間学習に進まない。**

---

## 主催者明示許可（Discussion）

Rules §2.6 や参加者間の慣行だけでは RED/YELLOW を GREEN にしない。

1. Discussion / Overview で **Competition Host / CPMP / Kaggle Staff（主催側）** の **明示許可・推奨** を確認
2. `license-ledger.md` の **「主催者明示許可」** 表に 1 行追加（URL・日付・要約）
3. 該当 BOM 行を更新: `host-perm` 列に id、`risk` を **GREEN（使用可）** または条件付き YELLOW に
4. Skill `discussion-summary` で Host 返答を見つけたら **Tier R として台帳更新**

参加者の「たぶん OK」は根拠にしない。

---

## Tier R ワークフロー

1. `docs-ja/license-ledger.md` を開く
2. BOM に 1 行追加（`license` 未確認なら `要確認`、`risk` は原則 YELLOW）
3. Rules §2.6（Reasonableness）・Winner License との整合を 1〜3 行メモ
4. Host 許可が既にあれば「主催者明示許可」表を先に確認し `host-perm` をリンク
5. **RED** → 採用禁止（CHK 却下）。**YELLOW** → 継続可だが A+ 前に解消方針を書く
6. `docs-ja/license-audits/YYYY-MM-DD-register-{id}.md` に R ログ（任意・推奨）

---

## Tier A+ ワークフロー

1. BOM 全行: RED=0、YELLOW は **開示文** または **Host 許可** 済み
2. 提出物（LoRA/CSV 等）の生成経路に RED/YELLOW が **直結していない** こと
3. 賞金時 CC BY 4.0（等）で公開できる範囲を明記。非互換は Rules 例外条項どおり列挙
4. `docs-ja/license-audits/YYYY-MM-DD-audit-full.md` — result: PASS | FAIL | PASS-WITH-WARNINGS
5. FAIL → Final 2 / 賞金提出を保留

---

## 3段ゲート・validator 連携

```
外部依存追加 → ① Tier R（本 Skill）→ pretrain-gate Tier 0
提出前 → submission-validator L0-L2 → （メダル狙い）L3 = Tier A+
```

| 連携先 | 追記 |
|---|---|
| `kaggle-pretrain-gate` Tier 0 | 新規 external あり → **Tier R PASS 必須** |
| `kaggle-submission-validator` | L3 = `license-ledger.md` + Tier A+ |
| `competition-conditions` | 初版 `license-ledger.md` 生成 |

---

## Agent 規則

1. **Tier R 未登録の外部依存で学習・提出経路を進めない**
2. ライセンスを **推測で GREEN にしない**（カード URL または Host 許可が必要）
3. Host 許可は **表に残してから** BOM を GREEN 化
4. 他人 LoRA / Notebook 丸コピーは原則 **YELLOW**（LB ≠ 賞金適格）
5. `dataset/` の Git 公開は `kaggle-git-security` — 本 Skill では BOM と Rules のみ

---

## テンプレート

`%USERPROFILE%\.cursor\kaggle-template\comp\docs-ja/license-ledger.md.template`
