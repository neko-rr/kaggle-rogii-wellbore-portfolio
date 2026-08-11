# Discussion 最近波（2026-07）追加要約 — 索引

> updated: 2026-07-26 UTC（729554 · DYNQ0130 · 728256）  
> 取得: `topics list -s new/active` + `topics show`（CLI 2.2.3）  
> 詳細は各 topic ファイル。全体索引は [README.md](README.md) · **[20260726-refresh](20260726-refresh.md)**

## 必読（今回追加）

| topicId | ファイル | 要点 |
|---|---|---|
| **719389** | [719389-cv-lb-correlation.md](719389-cv-lb-correlation.md) | **Trust your CV**。LB≈50 wells でノイズ。CV&lt;6 で相関崩れ報告あり |
| **717573** | [717573-score-without-tabular.md](717573-score-without-tabular.md) | tabular / 非tabular 両方可。物理単体 CV6.85/LB6.58。Tucker 非tabular で 5s |
| **723815** | [723815-worst-performing-well.md](723815-worst-performing-well.md) | 難井共有（例: `86454a6f`）。系列ドリフト・別手法の必要性 |
| **712037** | [712037-fork-the-ruler.md](712037-fork-the-ruler.md) | drift slope は合法特徴から学習困難。oracle harness。人間ノイズ床 ~9.5–20.5 ft |
| **711878** | [711878-pm15ft-bimodal-datum.md](711878-pm15ft-bimodal-datum.md) | **±15 ft 二峰 datum**（Milankovitch）。曖昧井は **中点予測が RMSE 最適** |
| **708367** | [708367-problem-breakdown.md](708367-problem-breakdown.md) | ドメイン入門。last TVT→LB **15.883**。GR 回転。Typewell 共有部分列 |
| **723647** | [723647-lowest-cv.md](723647-lowest-cv.md) | Tucker: single **5.4** / ens **5.0** · Trust CV |
| **721549** | [721549-pattern-matching-no-ml.md](721549-pattern-matching-no-ml.md) | 純 GR matching は flat 井で失敗しやすい。候補集合 oracle ~4.5 報告 |
| **720701** | [720701-medal-cutoff-predictions.md](720701-medal-cutoff-predictions.md) | Chris: **Private shake-up 大**。Tucker: Public 順位は無意味・CV を下げよ |
| **717445** | [717445-writeup-anchors-guarded.md](717445-writeup-anchors-guarded.md) | Working Note: anchors · guarded GR alignment |

## 参考（中優先）

| topicId | 要点 |
|---|---|
| 718670 | 公開 NB teardown（nvidia-kaggle）。公開 NB ≪ 非公開上位 |
| 721578 | GP + Typewell warping 物理パイプライン説明（コメントなし） |
| 722236 | 複雑 NN より表現・CV が決定要因 |
| 724669 | 悪井を学習から外すか — 未結論 |
| 719235 | 地質解釈 vs Typewell 不一致 — Host 未回答 |
| 727537 | 図解分析 · spatial kriging は dead end との自己報告 |
| **728712** | PF 公開NBの `gs`×1.3 — tip に既実装 · Final2禁止 | [要約](728712-gs-noise-scale-public-nb.md) |
| **728879** | Well Steerer 構想 — スコア非直結 | [要約](728879-trying-to-build-well-steerer.md) |
| 728022 | 有料 DB — Host 未回答 · **不使用** |
| **728256** | AI 支援 — コミュニティ可寄り · **Host 未回答** · [要約](728256-ai-coding-assistant.md) |
| **729554** | Submit Exception — 3井ログ≠hidden · [要約](error/729554-notebook-threw-exception.md) |
| **727570** | souldrive: well vs field-CV · `test/` identity · [要約](727570-local-validation.md) |

## スコア向上への横断メッセージ

1. **CV（well-group · マスク再現 · multi-seed · well/field 差）を信じる** — Public LB は友好地 ~50 wells
2. **二峰曖昧井はモードを当てに行かず中点/hedge**
3. **難井リストを共有し、系列ドリフト対策 or 別ルート**
4. tabular でも非tabular/物理でも **5台**は報告あり — 手法の質が天井
5. Private は大きく動く想定 — Final 2 は多様性
6. 手元 `test/` 3 wells は train コピー — **検証に使わない**
