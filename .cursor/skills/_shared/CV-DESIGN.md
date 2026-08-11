# CV 設計（Kaggle 汎用 SSOT）

> 採択根拠になる交差検証を、**コンペの構造に合わせて**設計するための横断規定。  
> コンペ固有の fold 本数・グループ列名は **`docs-ja/cv-design.md`** に書く（本ファイルは型のみ）。

関連: `_shared/LANES-AND-FINAL-SLOTS.md`（primary 物差し）· `_shared/EXPERIMENT-ID-NAMESPACES.md` · knowledge axis **A（cv-validation）**

---

## 1. CV unit（分割の単位）— 必須宣言

| unit ID | 意味 | いつ使う |
|---|---|---|
| **row** | 行（サンプル）単位。random/stratified KFold など | 行が実質 i.i.d. で、同一実体が train/test に跨らない |
| **group** | 井・患者・ユーザ・site・session 等の **グループ**ごと | 同一 group が train と test に出るとリーク・楽観になる |
| **time** | 時間・イベント順で未来を holdout | 時系列・発表順・ラウンドで分布が変わる |
| **stratified-*** | 上と併用（例: group 内層化） | クラス不均衡等 |
| **custom** | 公式・Host 指定の split | Discussion / Rules に明示 |

### 必須ルール

1. **戦略 CHK を載せる前**に、当該コンペの **`cv_unit`** を `docs-ja/cv-design.md` に宣言する  
2. **`cv_unit=row`（または random KFold）を採択根拠にする場合**は、**group/time リークが無い理由を1段落**書く。書けないなら **採択根拠に使わない**  
3. primary レーンの GO/NO-GO は、宣言した unit の **shippable OOF / dual** 上でのみ（§2）  
4. 他コンペの「GroupKFold した」だけをコピーしない — **unit の根拠列をこのコンペのデータ辞書から特定**する

### Agent 禁止

- ❌ unit 未宣言のまま CV 改善を Best 採用  
- ❌ random/row KFold の良いスコアだけを Private 見込みの主根拠にする（group 構造がありうるのに）  
- ❌ knowledge の CV カードを apply 未確認で CHK 化  

---

## 2. Shippable GO vs offline / oracle（診断）

| 種類 | 使ってよい判断 | 使ってはいけない判断 |
|---|---|---|
| **shippable** | 提出パイプラインと **同じ入力・同じ特徴・リーク無し split** で測れる primary | — |
| **offline ceiling / oracle** | 上限診断 · diagnostic レーン完了 | **提出 GO · Final 採用 · primary 全体 NO-GO 覆し** |
| **leak-prone / phys 等** | 禁止または diagnostic に隔離 | 採択根拠 |

### acceptance テンプレ（checklist にコピペ）

**primary · shippable:**

```text
acceptance: shippable OOF（cv_unit=<unit> · fold定義=<path>）で primary が基準より改善し、
指定サブセットが非悪化。oracle/ceiling/leak 指標は引用しない。
```

**diagnostic · oracle/ceiling:**

```text
acceptance: 診断完了のみ（上限/仮説の当たり外れを記録）。
lane=diagnostic。提出・Final・primary の GO/NO-GO に使わない。
```

**public レーン:**

```text
acceptance: Public LB（または日次）の当該指標のみ。primary shippable の代替にしない。
```

---

## 3. 形 vs 性能 — Early smoke（本実験前）

「スコアを追う CHK」の前に、**形が通る**短い台を checklist または pretrain に置く。

### プロファイル分岐

| profile / シグナル | smoke 内容（例） |
|---|---|
| **csv / tabular 提出** | 行数 · 列名・dtype · id 完全一致 · sample_submission 整合 · NaN/Inf |
| **notebook-output / Code Comp** | 上記 + 実行時間予算の短 run · Internet OFF 想定 · 出力パス |
| **simulation** | 1 局完走 · timeout fallback · 観測パース単体 |
| **lora / zip** | 形式・rank 上限・展開サイズ |

### CHK の置き方

```text
- [ ] **CHK-00S** | high | lane:diagnostic | 
  shape smoke（id/列/行 · 1 mini-run）| acceptance: validator L0 PASS · 提出形OK。性能は見ない
```

性能 CHK は **smoke PASS 後**に `lane:primary` で追加。

---

## 4. knowledge を使った CV 組み立て

### 手順（必須順）

1. **データ構造を読む**（group 列候補 · 時系列 · host split）→ `docs-ja/dataset.md` / Overview  
2. **knowledge retrieve**（CV 軸を優先）:

```powershell
cd knowledge; git pull origin main
# 全体 prior
./scripts/run-kaggle-knowledge.ps1 -Action retrieve -CompRoot "./<inner>" -IncludeCandidates -Limit 20
```

3. `exp/prior-knowledge.md` から **axis A（cv-validation）** · tag `knowledge-axis-cv-validation` ·  
   body に CV/split/group/OOF が含まれるカードを抽出  
4. 各カードの **apply / avoid（conditions / contraindications）** をこのコンペ条件と突合  
5. **合ったものだけ**を `docs-ja/cv-design.md` の「knowledge 参照」表に載せ、採否を書く  
6. 不採用も 1 行理由（avoid に該当 等）  
7. pre-strategy **X3** と **A4（CV）** の証拠に `cv-design.md` をリンク  

### retrieve 時の Agent フィルタ（手動でよい）

| 優先 | 内容 |
|---|---|
| 高 | group / time / leak / OOF / dual / nested / target encode CV |
| 中 | fold 数・seed 安定性 |
| 低 | モデル本体だけのカード（CV 節に混ぜない） |

---

## 5. `docs-ja/cv-design.md` に書く必須ブロック

1. **cv_unit** + 根拠列・リーク危険  
2. **fold 法**（GroupKFold / TimeSeriesSplit / …）+ fold 数  
3. **primary との関係**（何のスコアが primary か）  
4. **shippable の定義**（どのスクリプト・OOF が提出と同型か）  
5. **禁止する採択根拠**（row-only · oracle 等）  
6. **knowledge 参照表**  
7. **early smoke 項目**（profile 別）  
8. **更新履歴**

---

## 6. ファイル・Skill 分担

| 資産 | 役割 |
|---|---|
| 本ファイル | 横断型 |
| Skill `kaggle-cv-design` | Day0〜CV 更新の手順 |
| `docs-ja/cv-design.md` | コンペ固有の宣言（**SSOT**） |
| `exp/pre-strategy-gate.md` A4/A5 · X3 | 機械ゲート |
| checklist Skill | acceptance テンプレ · smoke CHK |
| `kaggle-knowledge-retrieve` | prior · axis A |
| `kaggle-adversarial-review` | **cv_unit 固定前** SA-7 mode=`pre-cv-lock` |
| Rule `kaggle-cv-design` | 毎セッションの誤採択禁止 |

---

## 7. コンペ型クイック指針（決めつけ禁止 · 出発点）

| 状況の手がかり | 最初に疑う unit |
|---|---|
| 複数行が同一 ID/user/well/patient | **group** |
| 日付・ラウンド・時系列 test | **time** |
| 画像1枚=1行 · 明示 i.i.d. | row を検討（根拠必須） |
| ホスト指定 split | **custom** = ホスト準拠 |
| Public が一部 · shake 懸念 | shippable group/time を primary に寄せる |

最終決定は **データと Host 文** と knowledge の apply。
