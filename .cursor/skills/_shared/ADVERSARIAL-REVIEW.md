# Adversarial Review（敵対的検証）— Kaggle 汎用 SSOT

> **目的:** 高コスト判定の前に、「なぜ通してはいけないか」だけを別コンテキストで書く。  
> **実装:** カスタム subagent **SA-7** `/kaggle-adversarial-review` · Skill `kaggle-adversarial-review`  
> **GO 権限:** **親 Agent + ユーザーのみ**。サブは裁決しない。  
> 関連: `LANES-AND-FINAL-SLOTS.md` · `CV-DESIGN.md` · `EXPERIMENT-ID-NAMESPACES.md` · `SUBAGENT-BRIEF.md`

---

## 1. 何をするか / しないか

| する | しない |
|---|---|
| 仮説・枠・CV・採用論証の **穴・リーク・混同** を列挙 | コード diff のバグ狩り（→ SA-5 bugbot） |
| **Kill shots**（事実 + どの SSOT に反するか） | 台帳 Fnnn の機械 match（→ ban-gate） |
| より安い実験案 1 行 | exp / checklist の書き換え |
| mode 別の課題点 | 提出・kernels push・データ DL |

**Sycophancy 対策:** SUPPORT でも条件を書く。**KILL / CHALLENGE を少なくとも 1 本探す**（無ければ `none found — residual risk: …`）。

---

## 2. mode（brief 必須）

| mode | いつ | 焦点 |
|---|---|---|
| **pre-bet** | primary Bet / Wave 昇格・方針固定 | lane · acceptance · コスト · ban 言い換え |
| **pre-final** | Final / 有効枠の選択直前 | N/K · diversify · shippable · shake |
| **pre-adopt** | 他者 pipeline · 外部成果物の本採用 | 写経 · ライセンス · 自データ適合 · リーク |
| **pre-cv-lock** | `docs-ja/cv-design.md` 固定・group 変更 | cv_unit · shippable≠oracle · knowledge axis A |
| **pre-harvest** | knowledge harvest / promote 前 | over-generalize · apply/avoid 空 · 条件付き教訓 |

1 依頼 = **1 mode**。混ぜない。

---

## 3. 発火条件（必須 vs 禁止）

### 必須に近い（親は SA-7 を起動するか、自問で同 checklist を埋める）

- primary **Bet** を新設・大きく変更する  
- **Final / 有効枠**を決める・差し替える（N≥1）  
- 他者/外部の **本採用**（T1 本実験）  
- **cv_unit** または fold 方式を固定する  
- **harvest** で横断カードをまとめて作る直前  

### 禁止（起動しない）

- 毎 CHK · typo · 表 1 行 · status 確認  
- shape smoke（CHK-00S）自体  
- T4 screen のみ · diagnostic-only の小実験  
- ユーザーが「すぐ実行」と明示し **スキップ承認**したとき（親が 1 行メモ）

---

## 4. 固定チェックリスト（毎回同じ 10 問）

親の brief に **mode + 対象（CHK/Bet/slot/path）** を載せ、サブはこの 10 問を埋める。

1. **leak / 境界** — train–test · group · time · ID 分割は守られているか  
2. **cv_unit** — `docs-ja/cv-design.md` 宣言と実装・CHK 根拠が一致するか（無宣言なら CHALLENGE）  
3. **shippable vs oracle** — primary GO に ceiling / offline / 非提出スコアを使っていないか  
4. **lane** — acceptance と GO/NO-GO が同一 lane か。他 lane 小差だけで止めていないか  
5. **Final / 有効枠** — N or K を Overview/timeline から取ったか。既定「2」や public 一系統だけか  
6. **ban / Fnnn** — 既知禁止の言い換え再実行か  
7. **shape smoke** — 性能勝負の前に形（id·列·短 run）を通したか  
8. **測定可能 acceptance** — 反証不能・「良くなった気がする」だけになっていないか  
9. **コスト** — GPU·提出 1 回の情報量に見合うか。より安い潰し方はあるか  
10. **knowledge** — retrieve の **avoid** 条件を踏んでいないか（カード空なら「未参照」と明記）

コンペ **固有 Rule / F キーワード本文は infra にハードコードしない**。  
`exp/improvement-loop-failures.json` · `docs-ja/comp-strategy.md` · `cv-design.md` を **そのコンペから読む**。

---

## 5. 返却フォーマット（SA-7 専用・必須）

共通 Answer/Findings に **加えて**、次を必須:

```markdown
### Verdict
SUPPORT | SUPPORT-WITH-GAPS | CHALLENGE | KILL

### Mode
pre-bet | pre-final | pre-adopt | pre-cv-lock | pre-harvest

### Kill shots
- (max 3) 事実 + SSOT パス/ルール名。無ければ "none found — residual risk: …"

### Unfalsifiable claims
- 測定不能の主張。無ければ "none"

### Missing smoke / evidence
- 箇条書き。無ければ "none"

### Checklist hits
- Q1 leak: PASS | FAIL | N/A — 1 行
- Q2 cv_unit: …
- … Q10 knowledge: …

### Cheaper alternative
- 同じ仮説をより安く潰す方法 1 行

### Parent decision note
- 無視してよい論点 / 無視不可（サブは裁決しない）
```

| Verdict | 親の扱い |
|---|---|
| **SUPPORT** | 続行可。残リスクを 1 行メモ |
| **SUPPORT-WITH-GAPS** | ギャップを埋めか、明示受容して続行 |
| **CHALLENGE** | 仮説・acceptance・lane を直してから本実験 |
| **KILL** | その提案は実行しない（型失敗なら Fnnn 検討は親） |

**誤停止禁止（サブも守る）:**  
他 lane の悪化・Public 小差・Trust≠Public 乖離**だけ**で KILL しない（lanes SSOT）。  
oracle が良いこと**だけ**で SUPPORT しない（CV-DESIGN）。

---

## 6. 親の手順

1. 高コスト判定に入る直前に mode を決める  
2. `/kaggle-adversarial-review`（または Task + agent）に brief:
   - mode · 対象 ID · 仮説 1 文 · 読むべきパス（exp-index / checklist / strategy / cv-design / failures）  
3. 返却を読む。**KILL / CHALLENGE** なら親が修正 or ユーザー確認  
4. 続けた場合は CHK メモまたは `exp/latest/` に  
   `adversarial: mode=… verdict=…` を 1 行残す（任意だが Final 前は推奨）  
5. 本実験・提出・harvest は **親 Skill** が続行

---

## 7. テンプレ brief（コピー用）

```text
You are SA-7 kaggle-adversarial-review (readonly).
Mode: {pre-bet|pre-final|pre-adopt|pre-cv-lock|pre-harvest}
Target: {CHK-id | Bet name | Final slots | pipeline path}
Hypothesis (one line): …
Must read (if exist): exp/exp-index.md, exp/experiment-checklist.md,
  docs-ja/comp-strategy.md, docs-ja/cv-design.md, exp/improvement-loop-failures.json
Do NOT edit files. Do NOT submit. Do NOT invent daily submit caps or Final N=2.
Use kill-list Q1–Q10 from ADVERSARIAL-REVIEW.md.
Return SA-7 format only.
```
