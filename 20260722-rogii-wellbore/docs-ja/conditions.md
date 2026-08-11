# コンペ条件要約 — rogii-wellbore

> skill: competition-conditions  
> participant: Kazeneko  
> last-updated: 2026-07-25 UTC  
> sources: Overview / Evaluation / Code Requirements / **Rules**（ユーザー貼付） · Leaderboard 26%/74% 公式表記

**締切・マイルストーン・提出上限の詳細は [`comp-timeline.md`](comp-timeline.md) に集約する。**  
**ライセンス BOM:** [`license-ledger.md`](license-ledger.md)  
**ルール同意:** 参加者 Kazeneko は Rules を **Accepted**（貼付時点）。

---

## コンペ背景

年間約 1 万本の水平坑井が掘削されるが、地層解釈の多くは専門家の手作業に依存する。目標層から外れると回収効率が落ち、是正掘削や環境負荷が増える。坑井・地震・検層は地下の一部しか見えず、層は断層で折れ曲がるため、ビットが地層のどこにいるかの把握が難しい。

## コンペ概要

| 項目 | 内容 |
|---|---|
| **正式名** | ROGII - Wellbore Geology Prediction |
| **主催** | ROGII（11750 Katy Freeway, Suite 780, Houston, Texas 77079） |
| **種別** | Featured **Code Competition** |
| **タスク** | 水平坑井に沿った地質（評価区間の **TVT = True Vertical Thickness**）を予測し、ジオステアリング自動化に寄与する |
| **タグ** | Multimodal / Geology / Mean Squared Error |
| **参加規模（貼付時点）** | Entrants 15,538 · Participants 6,025 · Teams 5,481 · Submissions 112,936 |

水平坑井の軌道・検層と、垂直参照ログ（Typewell）を用いて、評価区間の TVT を推定する回帰コンペ。

## 評価指標

- **RMSE（Root Mean Squared Error）** — 予測 `ŷ` と真値 `y` の二乗誤差平均の平方根
- 提出列: `id,tvt`（ヘッダ必須）
- `id` 形式: `{WELLNAME}_{row_index}`（例: `000d7d20_1442`）

```text
id,tvt
000d7d20_1442,0.0
000d7d20_1443,0.0
...
```

### Public / Private Leaderboard（公式表記）

Kaggle Overview / Leaderboard に記載の基準（**Agent 必読**）:

> This leaderboard is calculated with approximately **26%** of the test data.  
> The final results will be based on the other **74%**, so the final standings may be different.

| 項目 | 内容 |
|---|---|
| **Public LB** | 隠れテストの **約 26%** だけで計算される順位表（進行中に見えるスコア） |
| **Private LB** | 残り **約 74%** で最終順位を決定（締切後に公開。順位は変わりうる） |
| スライス | コミュニティ見解では Public 井集合は **固定**（毎回抽選し直さない）。揺れは主に seed / 非決定性 |
| 詳細・運用 | [`cv-lb-private-relation.md`](cv-lb-private-relation.md) · [`leaderboard.md`](leaderboard.md) |

**含意（規定レベル）:** 画面上の Public 順位・スコアは最終結果ではない。最終は Private。採用・Final 2 枠の判断は同ファイルの方針に従う。

### Working Note Award（任意・締切済）

- 対象: Public LB **Medal Zone** のチーム
- 評価観点: 探索の幅と深さ / 坑井・データ洞察 / 物理的妥当性 / 個別アイデアの寄与 / 不確実性推定
- 提出締切: **2026-07-06 23:59 UTC**（**終了**）— Award $2,500 × 2

## コンペ期間

- 開始: 2026-05-05 · 最終提出: **2026-08-05 23:59 UTC**
- Entry / Team Merger: **2026-07-29 23:59 UTC**
- 詳細・残り日数: [`comp-timeline.md`](comp-timeline.md)

## 賞金

| 順位 | 金額 |
|---|---|
| 1st | $25,000 |
| 2nd | $13,000 |
| 3rd | $7,000 |
| 4th | $5,000 |
| Working Note Award ×2 | $2,500 each |
| **合計** | **$50,000** |

Awards Points & Medals あり。

## 制限事項（Code Competition + Rules）

| 項目 | 内容 |
|---|---|
| 提出経路 | **Notebook 経由のみ**（Save Version 後に Submit） |
| 成果物名 | **`submission.csv`** 必須 |
| 実行時間 | CPU / GPU とも **≤ 9 hours**（**Public+Private の全 test** · Private は結果が隠れるだけ · [732422](discussion/error/732422-private-lb-9h-runtime.md)） |
| Internet | **disabled**（提出 rerun 時） |
| 日次提出 | **最大 5 Submissions / day** |
| Final 枠 | **最大 2 Final Submissions** を選んで最終判定 |
| チーム | **最大 5 人** · Merger 時は合算提出数が上限以内 |
| 外部データ | 公開・無償・同等アクセス、または **Reasonableness**（過度な費用の独占ツール不可） |
| AMLT | 利用可（適切なライセンス + Winner Obligations） |
| Competition Data | **Competition use only**（再配布・未参加者への提供禁止） |
| コード共有 | チーム外 Private Sharing **禁止** · フォーラム公開は OSI（商用制限なし）想定 |
| 可視 test/ | 手元の `test/` は train 由来の **例示のみ**。採点は hidden test（約 200 wells） |
| 複数アカウント | **禁止**（1 人 1 Kaggle アカウント） |

**ライセンス:** Winner = **Non-exclusive** を Sponsor に付与。詳細 → [`license-ledger.md`](license-ledger.md)

## 戦略上の要点（Kaggler 視点）

1. **評価区間だけ TVT が隠れる** — `TVT_input` は同列コピーだが評価区間は NaN（prefix 既知・suffix 予測）
2. **Typewell（垂直 GR + Geology）との相関**が中核。単純な行単位 tabular だけでは天井が低い可能性
3. **坑井単位のバリデーション**必須（同一 well の MD リーク、well 間分布差）
4. train のみの地層深度列（ANCC 等）を test 前提で使うと危険 — リーク設計を明示
5. Working Note 締切は過ぎたため、残りは **LB + 再現可能な最終解**に集中
6. **Public ≈26% / Private ≈74%** — 画面の順位を最終と思わない（[`cv-lb-private-relation.md`](cv-lb-private-relation.md)）

## コンペの URL

https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction

## 関連 SSOT

| ファイル | 役割 |
|---|---|
| [`cv-lb-private-relation.md`](cv-lb-private-relation.md) | Public 26% / Private 74% · CV との関係 |
| [`leaderboard.md`](leaderboard.md) | Public LB 分布分析 |
| [`dataset.md`](dataset.md) | データ・列定義 |
| [`comp-timeline.md`](comp-timeline.md) | 締切・今日の戦略 |
| [`comp-strategy.md`](comp-strategy.md) | Goal / Bets / Stop |
| [`comp-profile.md`](comp-profile.md) | 型・Skill ルート |
| [`submission-rules.md`](submission-rules.md) | 提出検証 |
| [`license-ledger.md`](license-ledger.md) | ライセンス BOM |
