# ライセンス台帳 — rogii-wellbore

> skill: kaggle-license-compliance  
> comp-url: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction  
> last-updated: 2026-07-23 UTC  
> sources: Rules タブ（ユーザー貼付）· Overview Code Requirements

コンペ Rules のライセンス要件と、使用技術 **BOM（Bill of Materials）** の SSOT。  
メダル・賞金審査前は Skill `kaggle-license-compliance` の **Tier A+** と併読。

---

## コンペ固有（Rules 抜粋）

| 項目 | 内容 | 根拠 |
|---|---|---|
| **Competition Data** | **Competition use only** — 参加・Kaggle フォーラム用途のみ。再配布・未同意者への提供禁止。不正利用は失格対象 | Specific Rules §4 / Data Access |
| **Winner License** | **Non-exclusive** — 勝者は Sponsor に対し、提出物・生成ソースの **世界規模・非独占・サブライセンス可・譲渡可・無償・永続・取消不能** の利用権を付与（商用含む） | Specific §1.6 / §2.5 |
| **市販ソフトウェア例外** | 自前所有でない一般市販ソフトで Sponsor が過大費用なく調達できるものは、上記ライセンス付与不要（調達方法の明示で可） | §2.5.a |
| **非互換 pretrained / 入力データ** | 非互換ライセンスの入力データ・pretrained を使った場合、**当該 data/model について** 上記 OSS 的付与は不要（※開示・Winner Obligations は別途） | §2.5.a |
| **External Data / Models** | 公開かつ全参加者が **無償・同等アクセス**、または General §2.6.b **Reasonableness**（過度な費用・地理制限で排除しない） | Specific §6 / Overview |
| **AMLT** | Google AutoML / H2O 等可。ただし Rules（Winner License・Obligations・Warranty）を満たす適切なライセンスが必要 | Specific §6.c |
| **公開コード共有** | フォーラム/コンペ NB での公開共有は可。**OSI 承認・商用制限なし** ライセンスとみなされる | General §3.6.b–c |
| **非公開共有** | チーム外への **Private Sharing 禁止**（コード・データ） | General §3.5.d / §3.6.a |
| **Internet on submit** | **disabled**（提出 rerun） | Code Requirements |
| **準拠法** | Texas 法 · Harris County, Houston 裁判所 | Specific §9 |

詳細要約: [`conditions.md`](conditions.md)

### Winner Obligations（賞金時・要点）

- 最終モデルの **学習コード + 推論コード**・必要計算環境・再現手順を Sponsor に提出
- 方法論の詳細説明（再現可能な記述）· リポジトリリンク
- 検証後、Sponsor との録画/パネル通話を求められる場合あり
- Prize 受諾書類・税務フォーム（W-9 / W-8BEN 等）

---

## 主催者明示許可（Host Permissions）

Discussion / Overview / Host 投稿で **主催が明示的に許可・推奨** した場合のみ追記する。

| id | 対象 | 許可内容 | 投稿者 | 日付 | URL | BOM 反映 |
|---|---|---|---|---|---|---|
| — | — | （未登録） | — | — | — | — |

**Host 返答待ち（GREEN 化しない）**

| 待ち | topic | 内容 | 2026/07/24 メモ |
|---|---|---|---|
| 外部有料 DB | 728022 | Enverus / IHS 等は可か — **使用禁止を維持** | コメント 0 · 変化なし |
| AI コーディング支援 | 728256 | Codex/ChatGPT の可否・開示義務 | コミュニティは Rules 上 **可寄り**（tennogh）。**Host 明示なし**のため本表の「主催者明示許可」には載せない |

Skill `discussion-summary` で Host 返答を見つけたら、本表を **必ず更新**（Tier R）。

---

## BOM（使用技術台帳）

| id | 種別 | 名前 | 入手 | ライセンス | risk | host-perm | 根拠URL | 備考 |
|---|---|---|---|---|---|---|---|---|
| T001 | data | Competition dataset（rogii-wellbore） | Kaggle Comp | Competition use only | GREEN | — | Rules §4 | 参加用途のみ |
| T002 | tool | 公開 pretrained（使用時に行追加） | 公開 hub 等 | （使用時記入） | YELLOW | — | Rules §6 | |
| T003 | amlt | AMLT（使用時に行追加） | — | （使用時記入） | YELLOW | — | Rules §6.c | |
| T010 | data | ravaghi/wellbore-geology-prediction-artifacts | Kaggle DS | 要確認 | YELLOW | — | datasets/... | Ver2 全家系で使用 |
| T011 | data | phongnguyn23021656/koolbox-offline | Kaggle DS | 要確認 | YELLOW | — | | koolbox wheel |
| T012 | data | fleongg/rogii-claude-models-pub | Kaggle DS | 要確認 | YELLOW | — | | 事前学習ブランチ |
| T013 | data | pilkwang/rogii-model-package | Kaggle DS | 要確認 | YELLOW | — | | mha120 等で使用 |
| T014 | data | nina2025/rogii-03 · thbdh5765 · needless090/tabicl | Kaggle DS | 要確認 | YELLOW | — | | Contact-Gated/Dual-Track |
| T020 | notebook | 公開 dual-track / contact-gated / ridge-sp45 系 fork | Kaggle Code | 公開 NB 慣行 | YELLOW | — | | Ver2 提出の本体 |
| T015 | data | georgymamarin/geosteering-world-cup-2021-expert-interpretations | Kaggle DS | CC BY 4.0（NB記載） | YELLOW | — | NORCE/UiS GWC2021 | スコア用でなく監査用 |
| T016 | data | Zenodo GWC2021 10k interpretations (15190744) | Zenodo/GitHub | 要確認（オープン） | YELLOW | — | doi:10.5281/zenodo.15190734 | 学習混入禁止 · median 根拠のみ可 |
| T017 | data | DataverseNO GWC2020 typelog | DataverseNO | 要確認 | YELLOW | — | doi:10.18710/20VIVT | 論文再現用 · 提出モデルに不使用 |
| T021 | notebook | 公開有用 19本（Georgy/n0/Chris/Sunny/Mitch 等） | Kaggle Code | 公開 NB 慣行 | YELLOW | — | README-public-useful | 採用時に行分割 |
| T022 | code | mycarta/rogii-geosteering-toolkit 等（参照時） | GitHub | 要確認 | YELLOW | — | literature-survey | 概念参照 · 丸写し提出前にライセンス |
| T022 | notebook | opencv411/rogii-luck-is-all-you-need（tip Public 6.478） | Kaggle Code | 公開 NB 慣行 | YELLOW | — | code/opencv411/... | Contact-Gated 同家系 · Private fork tip · CHK-013 |
| T023 | notebook | sunnywu27/rogii-wellbore-tvt-physical-model（Final2 候補） | Kaggle Code | 公開 NB 慣行 | YELLOW | — | code/sunnywu27/... | 物理+PF · CPU · CHK-030b |
| T024 | notebook | mitchgansemer/drift-targeting-ncc（概念）+ 自前 `chk031-ncc-drift-smoke` | Kaggle Code / 自作 | 公開 NB 慣行 · 自前再学習 | YELLOW | — | CHK-031 | models DS 欠落のため写経推論不可 · NCC+drift を自前実装 |
| T025 | notebook | romanrozen/catboost-baseline → Private `chk070-catboost-drift-train` | Kaggle Code | 公開 NB 慣行 | YELLOW | — | CHK-070 | CatBoost residual GPU · GroupKFold |
| T026 | notebook | pavloivanin/baseline-lightgbm-with-groupkfold → Private `chk071-lgbm-tracka-retrain` | Kaggle Code | 公開 NB 慣行 | YELLOW | — | CHK-071 | LGBM GPU · 枠1副線 |
| T027 | notebook | connortynan/dz-dtvt-eda | Kaggle Code | 公開 NB 慣行 | YELLOW | — | refresh-20260725 | 幾何研究ログ · 提出コード不採用 |
| T028 | notebook | lucifer19/rogii-geoanchor | Kaggle Code | 公開 NB 慣行 | YELLOW | — | refresh-20260725 | dual-track 同家系 · 概念参照のみ |
| T029 | notebook | zongzishuang/a016-true-no-contact-guard-ablation | Kaggle Code | 公開 NB 慣行 | YELLOW | — | refresh-20260725 | contact guard ablation · 盲目採用禁止 |
| T030 | notebook | evansussex/rogii-public-score-frontier-lab-visuals（作者 Public 6.390 V1） | Kaggle Code | 公開 NB 慣行 | YELLOW | — | scriptVersionId=337186797 | Contact-Gated + Q0522 1井パッチ · Final採用不可 |
| T031 | notebook | prvsiyan/rogii-public-frontier-blend-research-visuals（DYNQ0130） | Kaggle Code | 公開 NB 慣行 | YELLOW | — | refresh-20260726 | Q0522進化 · +0.130動的 · Final採用不可 |
| T032 | notebook | prvsiyan/rogii-public-score-frontier-ii-visuals（DYNQ0196） | Kaggle Code | 公開 NB 慣行 | YELLOW | — | refresh-20260727 | +0.196動的 · DYNQ0130延長 · Final採用不可 |
| T033 | notebook | georgymamarin/measure-your-noise-floor-before-believing-a-lever | Kaggle Code | 公開 NB 慣行 | YELLOW | — | refresh-20260729 | 診断のみ · σ≈0.03 · 提出不採用 |
| T034 | notebook | blacklions/rogii-wellbore-geology-prediction-final-hierarch | Kaggle Code | 公開 NB 慣行 | YELLOW | — | refresh-20260730 | Q0522 lock + LB座標探索 · Final採用不可 |
| T035 | notebook | yaroslavkholmirzayev/rogii-contact-and-u-restore | Kaggle Code | 公開 NB 慣行 | YELLOW | — | refresh-20260802 | Q0522 + score-spaceアフィン · Final採用不可 |
| T036 | notebook | daniilkrasnovvv/rogii-solution-on-6-390-in-lb | Kaggle Code | 公開 NB 慣行 | YELLOW | — | refresh-20260803 | Q0522/Contact-Gated 看板 · Final採用不可 |
| T037 | notebook | raunakdey07/rogii-robust-ensemble-v3（+同型 fork 群） | Kaggle Code | 公開 NB 慣行 | YELLOW | — | refresh-20260804 | koolbox/contact_gated 量産 · Final採用不可 |

### risk 定義

| risk | 意味 | 提出 | メダル/賞金 |
|---|---|---|---|
| **GREEN** | OSI 相当・商用可・無料で全員アクセス可、または **Host 明示許可済**、または公式 Competition Data（用途制限内） | 可 | 開示のみ |
| **YELLOW** | 利用中だが **ライセンス未確認・他人成果・Reasonableness 要説明** | LB は可のことが多い | write-up 開示・独自性確認が必要 |
| **RED** | Rules 抵触または付与不能 | **禁止** | 不可 |

### 種別

`base` | `adapter` | `data` | `tool` | `api` | `notebook` | `amlt`

---

## 監査ログ

`docs-ja/license-audits/` に 1 監査 1 ファイル（Skill 参照）。

---

## 関連 SSOT

| ファイル | 内容 |
|---|---|
| `conditions.md` | Rules 要約 |
| `submission-rules.md` | 提出 L2 |
| `comp-timeline.md` | 日次 5・Final 2 |
| `exp/exp-intel.md` | 他者 NB・外部知見（BOM 候補の出所） |
