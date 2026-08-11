# CHK-185 計画（のみ）— tip 候補天井監査（generator × scorer）

> **状態:** 計画のみ。checklist Active 未登録 · 実験未実行 · 提出なし  
> **根拠 intel:** [`20260725-alt-lineage-intel.md`](20260725-alt-lineage-intel.md) S1–S3  
> **目的:** F001–F020 を言い換えず、「別系統の強い成分」が **選択／候補不足**のどちら側にあるかを数値で切り分ける

---

## 1 行仮説

tip（Contact-Gated）がすでに持っている **複数の内部候補**（シード／粒子／既存バリアント）について、  
井ごとに「最良候補の RMSE」と「実際に選ばれた tip の RMSE」の差を測ると、  
**選択ギャップが大きい井**と **候補自体が無い井**が分離できる。  
前者が多ければ「上手い合成＝選択」、後者が多ければ「別 generator」が本命。

---

## なぜ F台帳に触れないか

| やらないこと | 避ける F |
|---|---|
| 近傍井 TVT コピー・距離ゲート転写 | F002 · F012 |
| 方位分割学習・方位後処理 blend | F014 · F006 · F009 |
| heel+窓 NCC→drift 学習 · 行 tabular 残差 | F011 · F010 |
| 制約 DTW · heel 直線遠MD · CF フォールバック | F017 · F019 · F018 |
| tip×Best 井単位アービター · 中間面昇格 | F016 · F015 |
| 攻撃的 tip_self_line（strength≥0.15 / far≥0.5） | F020 |
| 新予測面の学習・GPU フル再学習 | （別 Bet） |

本 CHK は **予測を良くする提出**ではなく、**天井の診断（T4 screen）**。

---

## action_type · acceptance

| 項目 | 値 |
|---|---|
| **CHK ID** | **CHK-185**（仮） |
| **action_type** | **T4**（調査・screen のみ） |
| **Phase** | 承認後に ban-gate pre → 実行 → post |
| **GPU / 提出** | なし（ローカル CPU · 既存 OOF / 既存 tip 出力のみ） |
| **PASS（GO）** | 下記メトリクスを JSON で報告し、解釈が書けること（改善は不要） |
| **次段への昇格条件（別 CHK・要再承認）** | GO かつ「選択ギャップ」が支配的なときだけ、**既存候補からの選択ルール**を T0 で1本（新面禁止） |

### 計測メトリクス（必須）

井ごと（T2 allowlist または tip 既存 OOF 井）:

1. `rmse_selected` … 現行 tip 最終  
2. `rmse_oracle_cand` … 候補集合内の最小 RMSE（ラベル使用可 · **提出不可の oracle**）  
3. `gap = rmse_selected − rmse_oracle_cand`  
4. `has_good_cand` … `rmse_oracle_cand ≤ 閾値`（例: 6.0 または hard 井の中央値）  

全体:

| 指標 | 意味 |
|---|---|
| `frac_gap_ge_0.5` | 選択を直せば ≥0.5ft 拾える井の割合 |
| `frac_no_good_cand` | 候補不足井の割合（S3 対応） |
| `pooled_selected` vs `pooled_oracle` | 天井の幅（提出不可） |

### 候補集合の定義（実装時に1つ選ぶ · 優先順）

1. **最優先（低コスト）:** 既にディスクにある tip 系 OOF / multi-seed / BH・profile バリアントの予測 CSV を候補として結合（新規学習なし）  
2. **次:** tip 内部で既定の PF 粒子ログが取れるならそれを候補（コード変更は最小・診断用）  
3. **禁止:** 近傍転写・新 NN・DTW・Sunny CSV を候補に足して「多様に見せる」こと

候補が1本しか無い場合は **CHK-185 = INCONCLUSIVE** とし、無理に候補を増やさない（それが結果）。

---

## 解釈ルール（結果後）

| 結果パターン | 読み | 次にやってよいこと（要承認） | やってはいけない |
|---|---|---|---|
| gap 大 · good_cand 多 | **選択がボトルネック**（S2） | 既存候補の選択ヒューリスティック 1本（T0） | 学習 ranker の楽観 CV（Georgy 漏洩警告） |
| gap 小 · no_good_cand 多 | **generator 不足**（S3） | tip 本体の生成側（別設計・高コスト）または Final 運用のみ | F 閉鎖の近傍／方位の言い換え |
| 両方小さい | tip は候補内で既にほぼ最良 | 別系統探りは打ち切り · Final2 運用 | Public 乱打 |

---

## 作業見積（承認後）

| ステップ | 内容 | 目安 |
|---|---|---|
| 0 | ban-gate pre（T4 · 仮説文固定） | 5分 |
| 1 | 既存候補 CSV の棚卸し（`exp/work/**` · tip-cv-out） | 30–60分 |
| 2 | 井ごと oracle / gap 集計スクリプト | 1–2h |
| 3 | `chk185-report.json` + 短い docs 追記 | 30分 |
| 4 | ban-gate post · checklist に結果1行 | 10分 |

**合計:** 半日以内の CPU 診断。GPU・提出なし。

---

## ユーザー承認が必要な点

1. Active に **CHK-185** を載せてよいか  
2. 候補集合を「既存ディスク成果物のみ」に限定してよいか（推奨）  
3. PASS 後に選択ヒューリスティックへ進む場合は **別 CHK** として再承認すること

---

## 改訂

| 日付 | 内容 |
|---|---|
| 2026-07-25 | A の intel に基づき計画初版（未実行） |
| 2026-07-25 | **実行完了** · 結果 [`chk185-candidate-ceiling-result.md`](chk185-candidate-ceiling-result.md) |
