# Kazeneko Version 2 提出ノート分析 — 索引

> analyzed: 2026-07-23 UTC  
> participant: Kazeneko (`kazeneko77`)  
> 生データ: `others-notebook/kazeneko-v2-copies/`  
> コード抽出: `docs-en/others-notebook/*-latest.py`  
> **注意:** Private kernel の **特定 Version pull は API 403**。取得したのは各 slug の **最新版**（提出 Version 2 と一致するものが多い。Dual-Track のみ最新は v6 付近）

## 提出 Version 2 一覧（CLI submissions）

| Public LB | Kernel slug | 提出日 UTC | 状態 |
|---|---|---|---|
| **6.644** | `hahaha-nondet-agi` | 2026-07-21 | COMPLETE |
| 6.906 | `rogii-det-mha180sep3` | 2026-07-20 | COMPLETE |
| 6.979 | `rogii-det-mha140sep4` | 2026-07-19 | COMPLETE |
| 7.003 | `rogii-det-mha120sep4mpkg10` | 2026-07-18 | COMPLETE |
| 7.132 | `rogii-kim-om020` | 2026-07-16 | COMPLETE |
| 7.536 | `rogii-dual-pipeline-self-verifying` | 2026-06-16 | COMPLETE |
| （スコア欠） | `rogii-dual-track-...` Ver2 | 2026-07-17 | COMPLETE（同系列の後続 Ver は 7.06–7.12） |
| PENDING | `top-reproducible-pf-config-branch-conservative` | 2026-07-22 | PENDING |

## 家系図（コピー元の構造）

すべて **同一エコシステム**（公開パイプライン系の fork / パラメータ違い）。共通部品:

| 部品 | 役割 | 出典の痕跡 |
|---|---|---|
| `koolbox` | Trainer 等 | `phongnguyn23021656/koolbox-offline` |
| artifacts | 事前計算特徴/モデル | `ravaghi/wellbore-geology-prediction-artifacts` |
| fleongg models | 事前学習推論ブランチ | `fleongg/rogii-claude-models-pub` |
| pilkwang package | model package 補正 | `pilkwang/rogii-model-package` |
| 他 | nina2025/rogii-03, thbdh5765, needless090/tabicl | Dual-Track / Contact-Gated 系 |

```
[公開 dual-track / contact-gated / ridge-sp45 系]
        │
        ├─ Family A: Dual-Pipeline blend (+ fleongg) …… dual-pipeline-self-verifying (LB 7.54)
        │
        └─ Family B: Dual-Track / Contact-Gated + PF + LGBM/CatBoost + bimodal hedge
                ├─ det-mha* …… midpoint hedge の (alpha, seplo) グリッド
                ├─ dual-track-prefix-calibrated …… 同系統の本流タイトル
                └─ hahaha / kim-om020 / top-reproducible-pf …… Contact-Gated タイトルの設定差
```

## 手法サマリ（共通）

- **使用データ:** コンペ公式 + 上記 Private/公開 Dataset（Internet OFF）
- **前処理:** Typewell–lateral GR 相関、heel/prefix 校正、formation contacts、Savgol 等
- **モデル:** Track A = LightGBM/CatBoost + Ridge（GroupKFold by well）· Track B = **粒子フィルタ**（128 seeds × 複数 scale）+ beam search · 選択器
- **後処理:** bimodal midpoint hedge · guarded physical override（一部）· model package 補正（一部）
- **学習設定:** seed 固定の決定論バリアントあり（det-*）· 非決定論バリアント（hahaha-nondet）

## バリアント差分（重要）

| slug | 実質の差 | LB |
|---|---|---|
| **mha180sep3** | `_MH_ALPHA=1.8`, `_MH_SEPLO=3.0` · profile `conservative` | **6.906** |
| mha140sep4 | alpha **1.4**, seplo **4.0** | 6.979 |
| mha120sep4mpkg10 | alpha **1.2**, seplo **4.0** + **pilkwang model package ON** | 7.003 |
| hahaha-nondet-agi | Contact-Gated · nondet 設定 · フル DS セット | **6.644**（最良） |
| kim-om020 | Contact-Gated 同型（設定差） | 7.132 |
| top-reproducible-pf… | Contact-Gated · `BRANCH conservative` · PENDING | — |
| dual-pipeline | **2 パイプライン blend (0.55/0.45)** + prefix 検証 override | 7.536 |
| dual-track | Dual-Track 本流（取得は最新≠厳密 Ver2） | ~7.1 帯 |

## Kaggler としての評価

| 観点 | 判定 |
|---|---|
| コピーであるか | **はい** — 自前アーキテクチャではなく公開系の fork / ハイパラ・後処理スイープ |
| スイープの質 | det-mha* は **二峰 hedge の (α, sep)** を明示的に変えており、Discussion（±15ft / midpoint）と整合 |
| 最良 | **hahaha-nondet-agi (6.644)** — 同家系の中で最上位 |
| リスク | 全員同じ公開スタック → **Private shake-up で同時沈没**しやすい（Chris 指摘と整合） |
| ライセンス | 外部 DS/モデル多数 → `license-ledger` Tier R 必須（賞金時 A+） |
| 次にやるべき | (1) 最良1本の **独自差分**を明示 (2) well-group CV を自前で測る (3) 方位分割等の **未取り込み Discussion 知見**を CHK 化 |

## 個別要約

| ファイル |
|---|
| [hahaha-nondet-agi-Ver2.md](hahaha-nondet-agi-Ver2.md) |
| [rogii-det-mha-family-Ver2.md](rogii-det-mha-family-Ver2.md) |
| [rogii-dual-pipeline-self-verifying-Ver2.md](rogii-dual-pipeline-self-verifying-Ver2.md) |
| [rogii-contact-gated-siblings-Ver2.md](rogii-contact-gated-siblings-Ver2.md) |
