---
name: kaggle-simulation-tracker
description: >-
  シミュレーション系 Kaggle コンペ（Games / エージェント提出）で、
  (1) 公開 Notebook 一覧の推移 と (2) 提出済み含む各 Notebook の
  パブリックスコア時系列 を記録する。Orbit Wars、シミュレーション、
  日次 leaderboard、公開 notebook 追跡、skill rating、パブリックスコア推移と言ったときに使う。
  dataset ダウンロードは行わない。
---

## Permissions（Agent 境界）

| shell | network | env | file_read | file_write |
|---|---|---|---|---|
| —（手動キャプチャ + 任意 CLI） | — | — | sim-track/ · Kaggle Web | sim-track/（append 規約遵守） |

**要ユーザー明示 OK:** —

**共通禁止:** competitions submit · public dataset · 秘匿を Git に含める · KAGGLE_* / token をログ出力

# Kaggle Simulation Tracker

**シミュレーション系コンペ専用。** タブラー ML・LoRA 提出コンペ（NVIDIA 等）には使わない。

**提出上限・「最新 K 件のみ LB 」** は本 Skill ではなく `docs-ja/comp-timeline.md`（Skill `kaggle-competition-constraints`）。  
「Final 2 を選ぶ」と「最新 2 が自動で効く」を混同しない。

2つの履歴を **別ファイル・別ワークフロー** で管理する:

| 追跡対象 | ファイル | 目的 |
|---|---|---|
| **公開 NB 一覧の推移** | `public-notebook-catalog.md` + `snapshots/catalog/` | ランキング帯の天気図（新規・脱落・順位変動） |
| **各 NB のパブリックスコア時系列** | `notebook-score-history.md` | 同一 notebook の score が時間とともにどう動いたか |

参考: [Orbit Wars](https://www.kaggle.com/competitions/orbit-wars) — Episodes 継続で **再実行なし** でも Public Score が変わる。

---

## 解釈上の注意（peak score / stale NB）

Kaggle **Code → Notebooks** 一覧の **Score は、その NB が達成した最高 Public Score（peak）** を表示することが多い。必ずしも **「今この瞬間の強さ」** ではない。

| パターン | 見え方 | 実際 |
|---|---|---|
| **stale peak** | `updated` が **3 日以上前** + score は上位 | 当時は強かったが、**今の meta では相対的に弱い**可能性 |
| **delta=0 が続く** | 複数キャプチャで score 不変 | Episodes 未反映 or **peak 固定表示**。他 NB の台頭で相対順位は下がりうる |
| **updated 新 + score 低** | 改造版・再 run 直後 | これから伸びる版の可能性（従来どおり） |

**Agent / intel の禁止:**

- catalog の `#` や `score` **だけ** で「真似すべき NB」「次の CHK」を決めない
- stale peak 疑いの NB を **現行最強** と書かない — `exp/exp-intel.md` には **「catalog peak・updated 古い」** と注記必須
- 1 回のスナップショットのみで notebook-analysis を優先付けしない — **2 回以上のキャプチャ** または `updated` + history を併読

**記録:** 各キャプチャで `score_kind=peak-ui`、`updated_stale_days`（キャプチャ日 − updated）を算出して catalog / history に書く。

---

## 対象コンペの判定

- Games / Simulation / RL タグ
- エージェント提出 + Episodes 評価
- Code タブに **Score・メダル・更新日** が並ぶ
- LB / Public Score が **日次〜数時間** で変動

---

## フォルダ構成

```text
sim-track/
├─ sim-track-index.md              # 索引・直近 delta・次アクション
├─ public-notebook-catalog.md      # 公開 NB 一覧の【最新】スナップショット
├─ notebook-score-history.md       # 全 NB の public score【時系列・append のみ】
├─ submitted-notebook-registry.md  # 自チーム提出済み NB の slug ↔ ローカル対応
├─ leaderboard-log.md              # 自チーム LB（順位・μ・best bot）
└─ snapshots/
   ├─ catalog/                     # 一覧の完全退避（上書き前に必ず保存）
   │   └─ 2026-06-17-0930-catalog.md
   └─ deltas/                      # 一覧の差分サマリ
       └─ 2026-06-17-0930-delta.md
```

**初回:** `sim-track/` が無ければ `kaggle-template/comp/sim-track/` から作成。

### ファイル役割（厳守）

| ファイル | 更新方式 | 内容 |
|---|---|---|
| `public-notebook-catalog.md` | **上書き**（退避後） | その時点の公開 NB 全件表 |
| `notebook-score-history.md` | **append のみ**（行削除・上書き禁止） | slug ごとの score キャプチャ列 |
| `submitted-notebook-registry.md` | 提出時に追記 | 自チーム NB の slug・ローカルパス・version |
| `leaderboard-log.md` | append | チーム LB（notebook score とは別系統） |
| `snapshots/catalog/` | 追記のみ | 過去の一覧完全コピー |
| `snapshots/deltas/` | 追記のみ | 前回一覧との差分 |

**ipynb 本体** は `others-notebook/` / `my-submitted-notebook/`。本フォルダは **メタデータのみ**。

---

## データ取得

### 1. ユーザー貼り付け（最優先）

Kaggle **Code → Notebooks** タブ一覧（title, Score, medal, Updated, comments 等）。

1回の貼り付けで **両方** を更新する:

- 一覧 → `public-notebook-catalog.md`（+ catalog 退避 + delta）
- 各行の score → `notebook-score-history.md` に append

### 2. Kaggle CLI（ユーザー指示時・軽量のみ）

```powershell
kaggle competitions leaderboard <slug> -s
kaggle competitions submissions <slug>
```

**禁止（指示なし）:** `competitions download`、notebook 一括取得、replay 大量 DL。

### 3. 自チーム提出 NB の登録

新規提出・公開時:

1. `my-submitted-notebook/` に凍結コピー
2. `submitted-notebook-registry.md` に slug / version / local_path を追記
3. 以降の score キャプチャで `owner=self` として `notebook-score-history.md` に記録

---

## 主キー（slug）

一覧・履歴の突合は **title ではなく slug** を使う。

| 優先 | 形式 | 例 |
|---|---|---|
| 1 | `author/notebook-slug` | `kienngx/orbit-wars-producer` |
| 2 | Kaggle notebook URL | `https://www.kaggle.com/code/...` |
| 3 | title（slug 不明時のみ・notes に注記） | 同名リスクあり |

slug が分からない行は `slug=—` とし、title + author で暫定突合。次回 slug 判明時に notes で紐付け。

---

## ワークフロー A: 公開 NB 一覧の推移

**トリガー:** ユーザーが Code タブ一覧を貼り付け / 「一覧を記録して」

### A1. 前回を読む

- `public-notebook-catalog.md`
- `sim-track-index.md`

### A2. 退避

現行 `public-notebook-catalog.md` を  
`snapshots/catalog/YYYY-MM-DD-HHMM-catalog.md` にコピー（UTC。同日複数回 OK）。

### A3. 新一覧を書く

`public-notebook-catalog.md` を更新:

| # | slug | title | score | score_kind | updated | updated_stale_days | medal | author | notes |

- `#` = 一覧上の順位（またはメダル帯内順）
- `score` = Code タブ表示値（**peak-ui 想定**）
- `score_kind` = 常に `peak-ui`（Kaggle UI が NB 史上最高 Public Score を表示）
- `updated` = UTC 換算 `yyyy/mm/dd`（「2d ago」はキャプチャ日から逆算）
- `updated_stale_days` = キャプチャ日 − updated（整数日。**≥3 → stale peak 候補**）

### A4. 一覧 delta

前回 catalog と比較し、`snapshots/deltas/YYYY-MM-DD-HHMM-delta.md` に:

- **新規登場**（slug / title）
- **一覧から消えた**
- **順位変動**（# の変化、上位帯入り）
- **メダル変化**
- **updated が新しい**（コード変更・再提出の兆候）
- **stale peak 候補**（`updated_stale_days ≥ 3` かつ score が上位帯 — 見かけより弱い可能性）

`sim-track-index.md` の「一覧 delta」に 3 行以内で要約。stale peak が上位帯にあれば **必ず 1 行** 触れる。

---

## ワークフロー B: パブリックスコアの時間推移

**トリガー:** ワークフロー A と **同時**（推奨）/ 「score だけ記録」/ 特定 NB の再キャプチャ

### B1. 前回 score を読む

`notebook-score-history.md` で同一 `slug` の最終行を参照。

### B2. append（1 NB = 1 行）

`notebook-score-history.md` に **末尾追記のみ**:

| captured_utc | slug | title | owner | public_score | score_kind | updated_stale_days | delta | medal | submitted_ref | source |

| 列 | ルール |
|---|---|
| `captured_utc` | `yyyy/mm/dd HH:MM UTC` |
| `owner` | `self`（registry 登録済み）/ `other` |
| `public_score` | Code タブの Score（数値。**peak 表示**） |
| `score_kind` | `peak-ui`（固定） |
| `updated_stale_days` | catalog と同値。`≥3` は notes または intel で stale 注記 |
| `delta` | 同一 slug の直前行との差。初回は `—`、変化なしは `0`（**0 でも相対弱化あり** — 解釈上の注意参照） |
| `submitted_ref` | self のみ `my-submitted-notebook/...` |
| `source` | `user-paste` / `cli` / `manual` |

**同一キャプチャセッション**（1回の貼り付け）では、一覧の **全行** を append する（score 不変でも可。`delta=0`）。

### B3. 自チーム提出 NB の解釈

`submitted-notebook-registry.md` にある slug は必ず `owner=self`。

- score 上昇 → 現行 bot が LB で勝ち続けている
- score 下降 → 新強敵出現 or 自身の bot 相対弱化
- updated 新しい + score 低い → これから伸びる改造版の可能性
- updated 古い + score 高い + delta=0 → **stale peak** — 真似優先度を下げる

### B4. 推移の読み方（Agent が要約するとき）

- 「Producer の推移」→ `notebook-score-history.md` を slug で filter
- 「自チーム提出 NB だけ」→ `owner=self`
- 「上位 10 の推移」→ 直近キャプチャの top10 slug を時系列 join
- 「今強い NB は？」→ **catalog 順だけ禁止**。`updated_stale_days` + 複数キャプチャの delta + 新規 updated を併読

---

## ワークフロー C: 自チーム LB（任意・別系統）

`leaderboard-log.md` に append（チーム順位・μ・σ・best_score）。

Notebook Public Score ≠ チーム LB best score（複数提出・notebook 経由提出の差）。**両方記録する。**

---

## 統合更新手順（1回の貼り付けで完走）

ユーザーが Code タブ一覧を貼り付けたら **partial progress 禁止** で以下をすべて完了:

1. A2 catalog 退避
2. A3 `public-notebook-catalog.md` 更新
3. A4 delta 作成 + index 要約
4. B2 全行を `notebook-score-history.md` に append
5. （あれば）C `leaderboard-log.md` append
6. `sim-track-index.md` 更新（最終キャプチャ時刻・注目 delta・次に分析する NB）

---

## Agent 規則

1. **dataset / replay / ログ大量 DL 禁止**（ユーザー明示時のみ）
2. `notebook-score-history.md` は **append only** — 行の編集・削除禁止
3. `public-notebook-catalog.md` 更新前に **必ず** `snapshots/catalog/` へ退避
4. score は **貼り付け or CLI 由来のみ** — 推測で書かない
5. 1回の更新で **A + B をセット** で完了（「一覧だけ」「score だけ」はユーザーが明示した場合のみ分割可）
6. 同日・同日内の **複数キャプチャを許可**（`HHMM` で区別）
7. catalog / history の score は **peak-ui** とみなし、`updated_stale_days ≥ 3` の上位 NB を **現行最強** と断定しない
8. `exp/exp-intel.md` へ書くとき peak・updated 古さを **必ず注記**（生データは sim-track のまま）

---

## ユーザー依頼別

| 依頼 | 動作 |
|---|---|
| 「今日の NB を記録して」+ 貼り付け | 統合更新手順 A+B+C |
| 「公開一覧の変動は？」 | 最新 delta + 前回 catalog 比較 |
| 「Producer の score 推移」 | `notebook-score-history.md` を slug で要約 |
| 「自チーム提出 NB の推移」 | registry + history `owner=self` |
| 「上位 NB の score 推移」 | top slug の時系列表 + stale peak 注記 |
| 「今真似すべき NB は？」 | catalog 単独禁止。stale 除外 + updated 新 + history 併読 |
| 「提出 NB を登録」 | registry 追記 + my-submitted-notebook リンク |
| 「sim-track 初期化」 | テンプレからフォルダ作成 |
| 「Error submission / Validation 失敗」 | **`docs-ja/agent-debug.md`** → `run-log.md` → `exp-infer` § simulation |

---

## 他 Skill との分担

| Skill | 役割 |
|---|---|
| **本 Skill** | 公開一覧推移 + public score 時系列 |
| **`docs-ja/agent-debug.md`** | **自チーム Error / Validation 失敗解析**（status=active 時） |
| `kaggle-notebook-folders` | ipynb の配置（submitted / others） |
| `notebook-analysis` | 1本 NB のコード深掘り |
| `experiment-result-management` | 自チーム提出・実験の exp 記録 |
| `leaderboard-analysis` | **コンペ終了後** の LB 総括 |
| `kaggle-cli-fetch` | Discussion / submissions CLI |

`exp/exp-intel.md` には delta の **戦略解釈のみ** 追記可（生データは sim-track に置く）。  
**必須注記:** catalog score は **peak-ui**、`updated_stale_days ≥ 3` の NB は「当時強・現 meta 不明」と書く。

---

## テンプレート

`%USERPROFILE%\.cursor\kaggle-template\comp\sim-track/`

シミュレーション系と判明した時点で初期化（全コンペで自動作成しない）。
