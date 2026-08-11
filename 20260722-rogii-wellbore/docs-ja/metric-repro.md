# Metric ローカル再現 — rogii-wellbore

> skill: （専用 Skill なし — `comp-profile.md` / `kaggle-pretrain-gate` から参照）  
> participant: Kazeneko  
> comp-url: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction  
> last-updated: 2026-07-23 UTC

**目的:** LB 本番の採点と手元検証のズレを防ぐ。公式 Metric の有無に応じて手順を切り替える。

**SSOT:** 評価再現の手順・パラメータ差分・holdout は本ファイル。コンペ固有の深掘りは `docs-ja/others-notebook/` へ。

---

## 公開状況（最初に記入）

| 項目 | 値 |
|---|---|
| **visibility** | **rules-only** |
| 公式 Metric URL | Overview Evaluation（RMSE 定義のみ） |
| ローカルコピー | 自前 `rmse(y_true, y_pred)` で可 |
| 詳細分析ドキュメント | — |
| 最終確認日 UTC | 2026-07-23 |

### visibility の選び方

| 値 | 意味 | 典型 |
|---|---|---|
| **public** | Kaggle 上で **閲覧・fork 可能** | Host が Metric Notebook を公開 |
| **private-kernel** | Metric は動くが **非公開 kernel**（提出者のみ / Host のみ） | コンペ中は fork 不可 |
| **rules-only** | Overview / Evaluation タブに **文言のみ** | 自前で `verify()` を再実装 |
| **community-repro** | 参加者・上位者の **再現 Notebook** のみ | 公式未公開時の代替（要検証） |
| **none-yet** | まだ **何もない** | コンペ直後〜Metric 公開待ち |

**Agent 規則:** visibility が `public` 以外のとき、**「公式と同一」は主張しない**。proxy 検証と LB 提出枠のバランスを `comp-timeline` と合わせて判断する。

---

## 取得手順（visibility 別）

### A. `public` — 公式 Metric が公開されている

1. Kaggle で公式 Metric Notebook を開く（Competition → Evaluation または Host 投稿のリンク）
2. **Copy & Edit** または **Download** でローカルに保存
   - 推奨パス: リポジトリルート `{metric-notebook}.ipynb` または `my-local-eval-notebook/metric-fork.ipynb`
3. Input データ・Models のパスを README にメモ
4. `score()` / `verify()` の **デフォルト引数** を読み、下の「LB 差分表」を埋める
5. 分析が増えたら `docs-ja/others-notebook/{Comp}-Metric-Ver1.md` に転記（本ファイルは手順 SSOT のまま）

### B. `private-kernel` / `none-yet` — 公式 fork 不可

公式 Notebook が **まだ手に入らない** ときの順序:

| 優先 | 手段 | 信頼度 | 注意 |
|---|---|---|---|
| 1 | Overview / **Evaluation タブ**の採点説明を転記 | 高 | パラメータ名・閾値をそのまま表にする |
| 2 | Host / Staff の **Discussion 告知** | 高 | Metric 更新・締切後公開の有無を changelog に |
| 3 | **LB 提出**（`comp-timeline` の 1 日上限・有効枠を確認） | 本番同等 | コスト高。ローカル proxy が無いときの最終手段 |
| 4 | **community-repro** Notebook | 中〜低 | `exp-intel.md` に出典・差分を記録。「未検証」と明記 |
| 5 | 自前で最小 `verify()` 実装（`rules-only` へ昇格） | 中 | Rules の数式・文字列一致ルールをコード化 |

**やってはいけないこと:**

- 非公開 Metric を **推測だけ** で再現し、ローカルスコアを LB と同一とみなす
- community ノートを **検証なし** で SSOT に昇格させる

**公開待ちのとき:** visibility を `none-yet` のまま維持し、Host 公開後に `public` へ更新 + changelog。

### C. `rules-only` — ルール文のみから再現

1. Evaluation タブから **正解判定**（数値誤差、文字列一致、特殊形式）を抽出
2. 最小スクリプトまたは Notebook セルで `verify(pred, truth)` を実装
3. train の一部を holdout に使い、**相対順位** の確認に留める（絶対値は LB と一致しない前提）
4. 公式 Metric が **後から public** になったら、自前実装と diff を `others-notebook/` に記録

### D. `community-repro` — コミュニティ再現を使う

1. 出典 Notebook URL・作者・Public LB を `exp-intel.md` に記録
2. 公式 Rules と **食い違う点** があれば本ファイルの notes に列挙
3. Tier 2 / holdout では **「参考」** 扱い。採用は公式 `public` 後に再検証

---

## LB 本番 vs ローカル default 差分表

> **必須。** Notebook の `score()` デフォルトと LB 本番が違うコンペが多い。ローカル CV では **LB 本番列を明示指定** する。

| パラメータ | LB 本番 | ローカル default | ローカル実行時の指定 | notes |
|---|---|---|---|---|
| metric | RMSE | RMSE | 同一 | √(mean((ŷ-y)²)) |
| 対象行 | test 評価区間（hidden） | train の擬似評価区間（`TVT_input` が NaN の行） | **評価区間のみ**採点 | 全行平均にしない |
| id 結合 | `id`=`{well}_{row}` | 自前で同じ形式 | sample_submission と一致 | |

**本コンペ:** 単純 RMSE。罠は「どの行を採点するか」と well リーク。

---

## holdout 設計

| 項目 | 値 |
|---|---|
| データソース | `train/` の horizontal_well（評価区間マスクを自作） |
| 分割方法 | **GroupKFold by WELLNAME**（推奨）。同一 well を train/val に割らない |
| サンプル数 | Tier 2: 少数 well（例: 5〜20）で煙テスト → 全 well OOF |
| 目的 | 相対 RMSE 比較・提出形式確認 |
| LB との関係 | holdout ↑ が LB ↑ を保証しない（hidden ≈200 wells・分布差あり） |
| Public / Private / CV | **詳細:** [`cv-lb-private-relation.md`](cv-lb-private-relation.md) — 採用は Trust CV · Public は検査機 · Final2 は多様性 |
| CV Tier（用途別） | **詳細:** [`cv-tiers.md`](cv-tiers.md) — T0 疎通 · T1 hard20 · T2 採用80井 · T3 Final multi-seed · T4 空間は条件付き |

### CHK-050 証明（2026-07-24）— Random CV 禁止

成果物: `exp/work/wave0-ruler/foundation-chk050-report.json` · `foundation-chk050-cv-table.csv`

| setup | RMSE（概数） | 読み |
|---|---|---|
| CF pooled（全井） | **15.91** | 学習なし門番 |
| Ridge safe · GroupKFold(well) | ~180 | 行 tabular は CF に大敗 |
| Ridge safe · Random KFold | ~179 | Group より **楽観 ~1.4** |
| Ridge safe+tops · GroupKFold | ~124 | tops で見掛け改善 |
| Ridge safe+tops · Random | ~119 | さらに楽観 ~4.9 |

**結論:** 採択根拠は **well-GroupKFold のみ**。Random / 行単位 CV は永久 Stop（`improvement-loop-failures.json` **F003**）。  
tip は ANCC 等を train 空間補間（DenseANCCImputer）で参照。train CV で tops を特徴にすると楽観リーク。heel/eval: `heel-eval-distribution.csv`。

### visibility 別の holdout 方針

| visibility | holdout の使い方 |
|---|---|
| `public` | 公式 `score(solution, submission, **LB本番params**)` を holdout に適用 |
| `private-kernel` / `none-yet` | 形式・抽出・短い proxy のみ。数値は LB 提出で確認 |
| `rules-only` | 自前 `verify()` + train 部分集合 |
| `community-repro` | コミュニティ metric と公式 Rules の **両方** で可能なら二重チェック |

---

## 弱点分析（debug 出力）

| 項目 | 値 |
|---|---|
| debug 出力名 | `oof_predictions.csv`（自作） |
| 有効化方法 | well 単位 OOF で残差を保存 |
| 分析列 | well_id, md, y_true, y_pred, residual, abs_err |
| 保存先 | `exp/work/` または run 出力 |

### 見るべき失敗パターン（コンペごとに追記）

- 特定 well / 地層ラベルだけ誤差が大きい
- 評価区間の先端・末端で系統バイアス（prefix 校正不足）
- Typewell GR と horizontal GR のスケール不一致
- 断層・層境界付近の不連続

分析結果の **次アクション** は `experiment-checklist.md` または `exp-intel.md` へ。生データの置き場所はここにリンクのみ。

---

## pretrain-gate Tier 2 との接続

長時間学習前（Tier 2）で最低限確認:

- [ ] 本ファイルの **visibility** が最新
- [ ] `public` ならローカル Metric パスが存在し、**LB 本番パラメータ** で smoke 済み
- [ ] `public` 以外なら **proxy か LB 提出** のどちらで判断するか決まっている
- [ ] holdout の結果が `pretrain-acceptance.md` の baseline 基準を満たす（または DEFER 理由を記録）

---

## 更新履歴（changelog）

| updated_utc | source | 変更内容 |
|---|---|---|
| 2026-07-24 | CHK-050 | Random vs GroupKFold 証明 · F003 · tops 楽観リーク注記 |
| 2026-07-23 | overview Evaluation | visibility=`rules-only` · RMSE · well-GroupKFold holdout |

---

## 関連ファイル

| ファイル | 役割 |
|---|---|
| `comp-profile.md` | このコンペの Metric 資産パス・型別ルーティング |
| `pretrain-acceptance.md` | Tier 2 合格基準 |
| `docs-ja/others-notebook/` | Metric 深掘り分析（公開後に充実） |
| `my-local-eval-notebook/` | Metric fork・検証 Notebook |
| `exp/exp-intel.md` | community-repro の出典・信頼度 |

