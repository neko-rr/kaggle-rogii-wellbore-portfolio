---
name: kaggle-adversarial-review
description: >-
  Kaggle 高コスト判定前の敵対的検証（red-team）。Final 枠・primary Bet・外部本採用・
  CV 固定・knowledge harvest の直前。SA-7 サブエージェント。読取専用。毎 CHK は不要。
  敵対的検証、adversarial review、red team、GO 前チェックと言ったときに使う。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| Task / カスタム agent 起動のみ | — | — | exp/ · docs-ja/ · failures · strategy · cv-design | —（親だけ記録） |

**禁止:** submit · kernels push · dataset DL · ファイル編集 · 裁決の GO 確定（親+ユーザー）

# Kaggle Adversarial Review（親オーケストレーション）

**詳細 SSOT:** [`_shared/ADVERSARIAL-REVIEW.md`](../_shared/ADVERSARIAL-REVIEW.md)  
**サブ:** `.cursor/agents/kaggle-adversarial-review.md` · **`/kaggle-adversarial-review`**（SA-7）  
**入口:** 本 Skill **または** `kaggle-subagent-delegate` → SA-7

---

## 4 ステップ

1. **mode を 1 つ選ぶ** — `pre-bet` | `pre-final` | `pre-adopt` | `pre-cv-lock` | `pre-harvest`  
2. **brief** を埋め（対象 CHK/Bet/slots + 仮説 1 文 + 必読パス）  
3. **/kaggle-adversarial-review** を起動（readonly）  
4. **親が判定:**
   - KILL / CHALLENGE → 仮説・枠・宣言を直すかユーザー確認  
   - SUPPORT / SUPPORT-WITH-GAPS → 本実験 or Final 選択 or harvest を **親 Skill** で続行  
   - 任意: `adversarial: mode=… verdict=…` を 1 行メモ

---

## 発火（短縮）

| 状況 | mode |
|---|---|
| Bet / Wave 方針固定 | pre-bet |
| Final / 有効枠 | pre-final |
| 他者 T1 本採用 | pre-adopt |
| cv_unit 固定 | pre-cv-lock |
| harvest / promote 直前 | pre-harvest |

**起動しない:** 毎 CHK · typo · CHK-00S 単体 · ユーザー明示スキップ

---

## 親が残す仕事

- `kaggle-experiment-checklist` · ban-gate · lanes · cv-design · harvest · validator  
- SA-7 の返却を **exp 全文に貼らない**（Verdict + Kill shots のみ）

## 関連

- Rule `kaggle-adversarial-review`  
- `kaggle-subagent-delegate` · `_shared/SUBAGENT-BRIEF.md` § SA-7
