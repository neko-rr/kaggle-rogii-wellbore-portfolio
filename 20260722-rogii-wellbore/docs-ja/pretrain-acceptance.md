# Pretrain 合格基準 — rogii-wellbore

> skill: kaggle-pretrain-gate  
> participant: Kazeneko  
> comp-url: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction  
> pretrain-profile: **tabular**  
> last-updated: 2026-07-23 UTC

長時間学習・重い GPU 実行の前に満たす基準。**SSOT**。

---

## Baseline 参照

| 項目 | 値 |
|---|---|
| 現 Best CV / local metric | — |
| 現 Public LB | **6.644**（#444 / 5,491 · 2026-07-23） |
| 最低改善幅（採用目安） | Public では **≤6.3（~Top50）** を目安にしないと密集帯から抜けにくい。採用は **自前 CV 改善**優先 |

---

## Tier 必須（デフォルト）

| 実験種別 | 必須 Tier |
|---|---|
| 通常の新手法 | **0 + 1** |
| ensemble 候補・高コスト学習 | **0 + 1 + 2** |

CHK 行の `pretrain-tier` があればそちらを優先。

---

## Tier 0（静的）

- [ ] データ path・件数が期待通り（train wells / typewell 対応）
- [ ] train / test リーク候補なし（地層 tops は train only · well 単位分割）
- [ ] 提出形式と学習出力の整合（`id,tvt` · `submission.csv`）
- [ ] import・設定ファイルが読める
- [ ] `TVT_input` の評価区間 NaN 扱いが明示されている

## Tier 1（スモーク・数分）

- [ ] 1 step / 1 batch / 1 episode / 10行推論が動く
- [ ] 即エラー・OOM・timeout なし

## Tier 2（ミニ検証・任意〜30分）

- [ ] CV または holdout が baseline 以上（または acceptance 参照）
- [ ] ensemble: index 一致・相関 < 0.99
- [ ] 仮説（CHK acceptance）との一致
- [ ] **`metric-repro.md`**: visibility に応じた検証済み（`public` なら LB 本番パラメータで smoke）

---

## コンペ固有メモ

（Nemotron: `\boxed{}` 抽出、Orbit Wars: validation episode 等）

---

## 関連

| ファイル | 役割 |
|---|---|
| **`metric-repro.md`** | Metric 公開状況・LB 差分・holdout（Tier 2 の評価 SSOT） |
| `pretrain-gates/` | 1実験1ゲートログ |
| `exp/experiment-checklist.md` | CHK と tier |
| `kernels-runbook.md` | PASS 後の実行 |

