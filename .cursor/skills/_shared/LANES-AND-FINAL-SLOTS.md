# レーン（物差し）· Final 枠 · LB 信頼性（Kaggle 汎用 SSOT）

> 全コンペ共通の**型**。Trust / Public などの**固有名は使わない**（呼び名はコンペの `comp-strategy` でエイリアス可）。  
> 数値（Public 割合・Final 本数・小差閾値）は **Overview / Rules / 当該コンペの docs** のみ。

---

## 1. レーン（Lane）— 何を信じて実験を進めるか

### 定義（3 種まで · 足りる）

| Lane ID | 役割 | 典型の物差し | GO/NO-GO の主判定 |
|---|---|---|---|
| **primary** | **主物差し**（最終順位に効くと信じるもの） | group/time CV · 手元 protocol · Private 推定用スコア | **このレーンの acceptance** |
| **public** | **見える LB**（進行中フィードバック） | Public LB · 日次 skill rating | public レーン専用 CHK のみ |
| **diagnostic** | **診断**（出荷・停止判断に使わない） | oracle · leak 疑い probe · ablation 片側 | 診断完了のみ。**他レーンを止めない** |

コンペ固有の呼び名（Trust / tip-cv / OOF 等）は **エイリアス**:

```text
primary  ≒ (このコンペでの名前): ________
public   ≒ Public LB / …
diagnostic ≒ …
```

### 必須手続き（Agent）

1. **CHK / Bet / GO·NO-GO には必ず `lane:` を書く**（未記入は「全体停止」前提にしない）
2. **あるレーンの悪化だけ**で、**別レーン**の Bet・Wave・実験全体を止めない  
3. **診断レーン**の結果だけで提出 Final や primary を NO-GO にしない  
4. レーン間の**小差**を「改善確定」にしない（閾値はコンペ `comp-strategy` に書く。無いときは断定禁止）  
5. Host が Public 構成を開示していないとき、**「Public＝易しい／特定セグメント」と断じて Stop を設計しない**

### 正しい停止

- 当該 `lane` の acceptance 割れ  
- 提出形壊れ · Scoring Error · 台帳 **Fnnn** 言い換え  
- ユーザー明示 Stop  
- **全レーン共通**の法的・ライセンス・時間制限

---

## 2. Final / 有効提出枠（N はコンペ固有）

### 枠数 N

| ソース | 記入先 |
|---|---|
| Overview / Rules「Final Submissions」等 | `comp-timeline` **Private LB / Final 枠** · 整数 **N** |
| simulation「最新 K のみ LB」 | **K**（選択 UI と混同しない · Skill constraints） |
| 未確認 | `要確認`。**既定で 2 と決めない**（よく 2 だが 1 のコンペもある） |

### 多様性格納（N ≥ 2 のとき推奨型）

| スロット | 既定の意図（上書き可） | 物差し |
|---|---|---|
| **slot-1** | **primary 最良**（信頼物差し） | primary |
| **slot-2** | **diversify** — public 強い / 別系統 / 相関の低い保険 | public または primary 別 family |
| **slot-k** | N>2 なら同様に **系統を分ける** | 混ぜない |

**条件付きの強い指針（カード級）:**

- **適用 (apply):** N≥2 かつ shake-up リスクが medium/high、または Public がテストの**一部**と開示されている  
- **禁止に近い推奨:** Final 全部を **public 最適化 1 系統だけ**にしない  
- **非適用 (avoid):** N=1 · Public がほぼ全評価で CV≈LB が実証済み · sim が「最新1」のみ  

N=1 のときは **slot-1 = primary 最良**を既定とし、diversify 議論はしない。

### Final 前チェック（1 行でも checklist / strategy に残す）

```text
[ ] Final N=… 確認済（source: Overview）
[ ] slot-1 … (lane=primary) 
[ ] slot-2 … (lane=… · diversify 理由: …)   ※N≥2
[ ] 全 slot が public-only 系統になっていない（N≥2 かつ shake med+ のとき）
[ ] SA-7 pre-final または kill-list 自問（`_shared/ADVERSARIAL-REVIEW.md`）
```

---

## 3. LB 信頼性 · shake-up · 改善の道しるべ

`docs-ja/comp-strategy.md` の **「LB・shake プロファイル」** に、Discussion / 実験から埋める。

### 記入フィールド（コンペごと）

| フィールド | 取りうる値 | 根拠の例 |
|---|---|---|
| **public_scope** | full-ish / partial / unknown | Host「約 X%」· Evaluation 文 |
| **shake_risk** | low / medium / high | 部分 Public · 時系列 split · グループ稀 · 上位も CV≠Pub を書く |
| **cv_lb_agreement** | strong / mixed / weak / unknown | 自チーム表 · intel |
| **primary_definition** | 1 文 | 何を primary と呼ぶか |
| **improvement_compass** | 今週の矢印 1〜3 | 「primary を上げる」「public は監視のみ」等 |

### 道しるべの読み方（Agent）

| shake_risk / public_scope | スコア改善の主方向 |
|---|---|
| high + partial | **primary 優先** · public は監視・枠保険 |
| low + full-ish + strong agreement | public 改善 ≈ primary でも可 · 仍 dual 保険は N 依存 |
| unknown | **決めつけない** · primary を先に定義してから Bet |
| diagnostic only signals | 道しるべに使わず、primary を測る実験へ |

Intel / Discussion 更新のたび:

1. ホスト・上位の **CV vs LB** 言及を `exp-intel` に  
2. `comp-strategy` の shake / compass を 1 行更新  
3. 新規 CHK の `lane:` と Bet を compass に合わせる  

---

## 4. ファイル役割

| ファイル | 書くこと |
|---|---|
| **`docs-ja/comp-strategy.md`** | レーン定義 · shake プロファイル · Final スロット方針 · compass |
| **`docs-ja/comp-timeline.md`** | **N / K の数値** · 今日の有効枠状態 |
| **`exp/experiment-checklist.md`** | 各 CHK の **`lane:`** · Final 前チェック |
| **`exp/exp-index.md`** | 主戦略 1 行に compass 要約 + strategy リンク |

スコア・% の再掲は strategy / timeline に置き、checklist ヘッダに Best を書き散らかさない。

---

## 5. 他 Skill との分担

| Skill | 役割 |
|---|---|
| **本 SSOT** | 型の定義 |
| `kaggle-competition-constraints` | N・K・提出上限の数値確認 |
| `kaggle-experiment-checklist` | lane 付き CHK · Final 前行 |
| `kaggle-adversarial-review` | Final / Bet 前の red-team（SA-7 · 毎 CHK 禁止） |
| `discussion-summary` | shake / Public 比率・Host 示唆 → strategy 更新トリガ |
| `post-comp-private-retrospective` | 枠選択の事後検証 |
| Rule `kaggle-lanes-and-final-slots` | 毎セッションの誤停止禁止 |

---

## 6. コンペ固有に落としてはいけないもの

- 特定コンペの「Public 26%」「σ≈0.03」を **全コンペ Rule にハードコード**  
- Trust / farvol / tip 名を **generic テンプレ本文**に書く  
- sim の「最新 K」を「Final 選択 N」と同一スロット表に混同したまま放置（注記必須）
