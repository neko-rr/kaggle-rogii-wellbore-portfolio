# コンペタイムライン — rogii-wellbore

> skill: kaggle-comp-timeline  
> participant: Kazeneko  
> comp-url: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction  
> last-updated: 2026-08-06 UTC  
> sources: Overview Timeline / Code Requirements / **Rules** · 終了後: `retro/`

**締切・フェーズ・提出制限の SSOT。** `AGENTS.md` と `exp/exp-index.md` は本ファイルへリンクする（重複記載しない）。  
**終了後分析** → [`../retro/retro-index.md`](../retro/retro-index.md) · コンペ中戦略ログ → [`comp-strategy.md`](comp-strategy.md)

---

## 現在のフェーズ

| 項目 | 値 |
|---|---|
| **フェーズ** | **COMP CLOSED**（最終提出締切済 · 実験停止） |
| **次の締切** | 終了後分析のみ（Private **取得済**） |
| **直近の注意** | Private **#596 / 9.142**（666）。終了後分析は `retro/`。提出・新規 train **なし** |

---

## マイルストーン

| id | イベント | 日時 UTC | 状態 | 残り日数 | notes |
|---|---|---|---|---|---|
| start | コンペ開始 | 2026-05-05 | 終了 | — | |
| writeup | Working Note Award 提出締切 | 2026-07-06 23:59 UTC | 終了 | — | Medal Zone 対象・任意賞 |
| entry | Entry / ルール同意締切 | 2026-07-29 23:59 UTC | 終了 | — | Rules Accepted 済 |
| merger | Team Merger 締切 | 2026-07-29 23:59 UTC | 終了 | — | |
| final-submit | 最終提出締切 | 2026-08-05 23:59 UTC | **終了** | — | Final2 凍結: 666 + farvol |
| private-select | Final Submissions 選択 | 最終提出締切まで | **終了（選択済み）** | — | 枠1=666 · 枠2=farvol |
| post-eval-end | 提出後評価 · Private LB | 2026-08-06（CLI） | **取得済** | — | Kazeneko **#596 / 9.142** · `retro/` |

**基準日:** 2026-08-06（コンペ終了後）。時刻未記載は **23:59 UTC**。

---

## 提出ルール

| 項目 | 内容 |
|---|---|
| 提出形式 | **Notebook 紐づけ** → 出力 **`submission.csv`**（列 `id,tvt`） |
| 1 日あたり上限 | **5 Submissions / day**（Rules §2.2.a · **他コンペ既定ではない**） |
| Final 選択 | **最大 2 Final Submissions** が最終判定に使用（Rules §2.2.b） |
| チーム上限 | **最大 5 人**（Rules §2.1.a） |
| Merger 条件 | 合算提出数 ≤（1日上限 × コンペ経過日数）。Merger Deadline 前 |
| Private LB 枠 | = Final 2 選択。**Public ≈ テスト26%**（見える順位）· **Private ≈74%**（最終） |
| 実行制約 | CPU/GPU ≤ **9h** · **Internet OFF** · 公開外部データ・pretrained 可（Reasonableness） |
| 賞金・メダル要件 | 順位賞 $50k · Working Note 締切済 · Winner は Non-exclusive 付与 + コード提出義務 |
| source | Rules §2 · Overview Timeline |

**時刻:** 締切は **23:59 UTC**（公式デフォルト）。会話・要約も UTC を正とする。

---

## メダル帯（参考 · 最終）

> 公式: https://www.kaggle.com/progression/competitions · Skill `kaggle-competition-constraints` · % は floor

| 項目 | 値 |
|---|---|
| medals 対象 | はい（Featured） |
| チーム数 N | **6125**（**1000+** バンド） |
| Gold | rank ≤ 10 + floor(0.002×6125) = **22** |
| Silver | rank ≤ floor(0.05×6125) = **306** |
| Bronze | rank ≤ floor(0.10×6125) = **612** |
| Kazeneko Private | **#594 / 9.142** → **Bronze**（594 ≤ 612 · 銀 306 外） |

---

## 提出・実行戦略（今日）

> **日次更新。** run 詳細は `exp/run-ledger.md`。方針の正は [`comp-strategy.md`](comp-strategy.md)。

| 項目 | 値 |
|---|---|
| **更新日** | 2026-07-26 |
| **本日提出** | SUB-9 gated `54972467` Public **6.484**（新Best）· SUB-8 Soft `54970975` **6.582**（打ち切り） |
| **推奨** | **CHK-184**（承認後）· **OPS-FINAL2**（枠1 gated / 枠2 旧Best保険）· [`ops-lb-89`](ops-lb-89-sub89-public-2026-07-26.md) |
| **Final 仮** | 枠1=gated SUB-9 **6.484** · 枠2保険=旧Best **6.524** |
| **GPU** | tip-soft-selfline Ver1 完了 · 追加申請なし |
| **CPU** | Wave-10/11 ローカル完了 |
| **推奨** | **Wave-13 A**（採点待ち並行 CPU）· Public 後 OPS-LB-89 · **OPS-FINAL2** · [`wave13`](wave13-plan-2026-07-25.md) |
| **避ける** | F001–**F020** 言い換え · 無許可追加 submit |

### 締切までの方針

| フェーズ | 方針 |
|---|---|
| Entry/Merger（7/29）まで | gated Best 維持 · portable 上積みは承認後 |
| final-submit（8/5）まで | 枠1=gated · 枠2=旧Best保険 · UI選択（OPS-FINAL2） |

### 次の run 候補

| 優先 | 内容 | env | verdict |
|---|---|---|---|
| 1 | OPS-LB-89 · SUB-8/9 Public 反映 | — | **done** |
| 2 | CHK-184（承認後）| CPU/GPU | pending |
| 3 | Final2 UI | — | go |
| 4 | 新機構 | — | 承認後のみ |

---

## 評価・LB 補足

- Metric: **RMSE**（行単位 `tvt`）· **pooled**（mean-per-well と混同しない）
- **Public ≈ テストの 26% · Private（最終）≈ 74%**（Kaggle 公式 Leaderboard 文 · [`conditions.md`](conditions.md)）
- 手元 `test/` は例示。**hidden ≈ 200 wells** で採点・時間もその規模
- **2026-06-11** Staff: Private の outlier well を採点除外（Public 不変）— topic [707695](../docs-ja/discussion/Kaggle-Staff_707695-private-test-rescore.md)
- 上位帯の目安（Discussion 報告）: well-group CV ≈5 · LB ≈5.7（ノイズあり）
- CV↔LB 運用: [`cv-lb-private-relation.md`](cv-lb-private-relation.md)

---

## 更新履歴（changelog）

| updated_utc | source | 変更内容 |
|-------------|--------|----------|
| 2026-07-23 | overview / timeline 貼付 | 初版。マイルストーン・残り日数・Code Comp 制約を記入 |
| 2026-07-23 | Rules 貼付 | 日次5・Final2・チーム最大5・Merger 合算ルール・private-select 確定 |
| 2026-07-23 | Discussion CLI | Private outlier 除外・hidden≈200・CV/LB 目安を評価補足に追記 |
| 2026-07-24 | F012 · Final選抜 | 残り日数更新 · 今日戦略を tip維持/枠1CV/枠2Public に同期 |
| 2026-07-25 | Leaderboard 公式 26%/74% を評価補足へ（「Overview 未記載」を訂正） |
| 2026-07-25 | SUB-4–7 Public 確定 · F015 · Final仮=tip/Best |
| 2026-07-25 | Wave-8 CHK-120 KILL · F016 · B4 閉鎖 |
| 2026-07-25 | Wave-9 CHK-130 NO-GO · F017 · B5 閉鎖 |
| 2026-07-25 | Wave-10/11 · F018–F020 · SUB-8 PENDING |

---

## 関連ファイル

| ファイル | 役割 |
|---|---|
| [`comp-strategy.md`](comp-strategy.md) | Goal / Bets / Stop |
| [`conditions.md`](conditions.md) | 概要・評価指標 |
| [`../docs-en/comp-timeline.md`](../docs-en/comp-timeline.md) | 原文メモ |
| `exp/exp-index.md` | 実験索引 |
| `exp/run-ledger.md` | run 詳細 |
