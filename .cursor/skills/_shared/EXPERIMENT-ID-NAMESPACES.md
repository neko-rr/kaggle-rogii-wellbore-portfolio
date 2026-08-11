# 実験・知見 ID 名前空間（Kaggle 汎用 SSOT）

> 全コンペ共通。**文字の意味をコンペごとに変えない。**  
> Agent / 人間が別コンペのメモを読んでも誤読しないための規約。

---

## 正表（覚えるのはこれだけ）

| 接頭辞 | 意味 | SSOT 置き場 | 用途 |
|---|---|---|---|
| **CHK-** | **仮説検証チケット**（作業キュー上の1項目） | `exp/experiment-checklist.md` | これから／いま試す。gate の `-ChkId` |
| **F** / **Fnnn** | **禁止確定（Failure / Forbidden）** | `exp/improvement-loop-failures.json` の `id` | 言い換え再実行を止める抽象失敗のみ |
| **T0–T4** | 実験の**型**（action_type） | ban gate · failures の `action_types` | baseline / 取込 / blend / 自前 / screen |
| **LES-**（任意） | コンペ内の**学びメモ**（まだ knowledge 未登録） | `retro/retro-lessons.md` · `exp/latest/` 等 | 残したい学び。**禁止と混ぜない** |
| **KGL-** | 横断知見の **card / candidate** | `knowledge/candidates/` · `cards/` | harvest / promote 後の共有 ID |
| **train_ / infer_ / SUB- 等** | 学習・推論・提出の記録 ID | `hyperparameter-table` · exp-train / exp-infer | 設定・LB 追跡（CHK の代理にしない） |

形式の目安:

- CHK: `CHK-001`（ゼロ埋め3桁以上）
- F: `F001`（JSON `id`。表記ゆれで `F-001` を見たら **F001 と同義**と読む）
- LES: `LES-001`（任意。必須ではない）
- KGL: `KGL-{comp}-{kind}-{fingerprint}`（`kaggle_knowledge.py` が生成）

---

## 明確に禁止する誤用

| 誤り | 正しい扱い |
|---|---|
| **F を「知見」「Finding」「分かったこと」に使う** | 学びは **LES-** または harvest → **KGL-**。F は禁止のみ |
| CHK に「もうやらない確定」だけを書いて台帳を空のまま | **failures.json に F** を書いて keywords を残す |
| 禁止パターンを CHK Active に残し続ける | archive し、参照は **`Fnnn`** |
| knowledge カードを `F001` と呼ぶ | 常に **KGL-…** |
| 他コンペの F 数字を意味共有する | **番号はコンペローカル**。中身（keywords）だけ抽象再利用 |

---

## ライフサイクル（典型）

```text
候補仮説
  → CHK-xxx を Active に載せる（hypothesis × acceptance）
  → ban-gate pre（ChkId=CHK-xxx · ActionType=T*）
  → 実験 · 記録（table / train|infer）
  → GO: done → archive ·（学びがあれば LES または harvest）
  → NO-GO が「型として確定」: failures に Fnnn を1件追記
       id: Fnnn
       keywords: [...]
       reason: ...
       source_chk: "CHK-xxx"
  → harvest: lessons → KGL-… (kind=lesson)
               failures → KGL-… (kind=anti-pattern) ※台帳 F と別 ID でよい
```

**CHK と F は 1:1 固定ではない。** 1 CHK が複数 F になることも、複数 CHK が1概念 F にまとまることもある。

---

## Agent 規則

1. 新しい禁止を確定したら **必ず `Fnnn` を failures に**（CHK の status だけでは不十分）
2. チャットで「F001 によると…」と言う前に **当該コンペの failures.json** を読む（他コンペの F 番号を流用しない）
3. 「知見 Fxxx」と書いたドキュメントを見つけたら **誤用** — 読み替え: 禁止なら failures、学びなら LES/KGL
4. Rule `kaggle-hypothesis-ban-ledger` と本書が食い違う場合は **本書 + Rule の F=禁止** を優先

---

## 関連

| 資産 | 役割 |
|---|---|
| Skill `kaggle-experiment-checklist` | CHK キュー |
| Rule `kaggle-hypothesis-ban-ledger` | F 台帳 + T0–T4 gate |
| Skill `kaggle-knowledge-harvest` | → KGL |
| `exp/improvement-loop-failures.json` | F の機械可読 SSOT |
| `_shared/KAGGLE-MEDALS-AND-CONSTRAINTS.md` | 別件（制約・メダル） |
