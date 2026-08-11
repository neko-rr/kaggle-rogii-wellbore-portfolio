# Discussion 有用情報インデックス — rogii-wellbore

> created: 2026-07-23 UTC · **refresh: 2026-08-10 UTC（終了後 Solution 追記）**  
> source: `kaggle competitions topics list/show`（CLI 2.2.3）  
> 原文: `docs-en/discussion/` · 解法本文 `docs-en/solution/`  
> 選定方針: Host/Staff · 高票 · Solution writeup · CV/リーク  

**最近波の入口:** **[2026-08-10](20260810-refresh.md)** · [2026-08-06](20260806-refresh.md) · [2026-08-05](20260805-refresh.md) · [2026-08-04 eve](20260804-eve-refresh.md)  
**終了後解法統合:** [`../../retro/retro-solutions.md`](../../retro/retro-solutions.md)  
**Public LB:** [`../leaderboard.md`](../leaderboard.md)  
**学習（Training）分析:** [training-insights.md](training-insights.md)  
**EDA→戦略:** [`../others-notebook/eda/strategy-from-eda.md`](../others-notebook/eda/strategy-from-eda.md)

### 2026-08-10 refresh（差分 · 終了後 Solution）

| topicId | 変化 | 示唆 |
|---|---|---|
| **733860** | **新規** · 17th Falcon | estimator 三層 + 難易度帯 CV · [要約](733860-17th-place-solution.md) |
| **733845** | **新規** · 20th / Pub3 | RAFT grtx · 無相関 path · Pub σ · [要約](733845-20th-raft-grtx-matcher.md) |
| **733895** | **新規** · 3581→429 | fold-safe geology delta · [要約](733895-3581-to-429-shakeup.md) |
| **733598** | **新規** · 25th | 66 cand soft path（統合は retro-solutions） |
| **733341** | Host wrap · 票27 | Host 内部 **RMSE≈8.0** · [要約](Competition-Host_733341-thats-a-wrap.md) |
| **733595** | Staff recap | N=6125 · 161k 提出 · [要約](Kaggle-Staff_733595-recap-winners.md) |
| Top1–6 | 票微増（#1=160 等） | 骨格は 08-08 済み · 変更なし |

総括: [`20260810-refresh.md`](20260810-refresh.md)

### 2026-08-06 refresh（差分 · 締切翌日）

| topicId / NB / LB | 変化 | 示唆 |
|---|---|---|
| **732999** | **新規** · HMM/物理 · hard 井 | TVT≈g−Z · GR 完全一致無意味 · [要約](732999-hmm-viterbi-hard-wells.md) |
| **733015** | **新規** · OOF〜8 · Cody | CV5→LB8.3 · cycle skip · [要約](733015-competition-broke-me.md) |
| **732947** | **Chris** Final 規則 | 締切前 Public 完了のみ選択可 · [要約](732947-final2-requires-public-score.md) |
| **732903** | **Staff Ryan** CPU | 通常 NB の CPU 機種可変 · [要約](732903-inference-time-cpu.md) |
| 733099 / 732917 | エージェント · 同 ID TVT | 低優先 · Host 無回答 · 使わない |
| tip NB | Farhan/Raunak/Sumit · Ayush CatBoost | Final 不可 · [Ayush](../others-notebook/ayush-rogii-ayush-Ver.md) 他 |
| LB | 全件 DL 0B · show 上位入れ替え微 | Private 未 · **枠変更なし** |
| 自チーム | 変更なし | Final2 **666+farvol** · 実験停止 |

総括: [`20260806-refresh.md`](20260806-refresh.md)

### 2026-08-05 refresh（差分 · 締切日）

| topicId / NB / LB | 変化 | 示唆 |
|---|---|---|
| **731550** | コメ **24→37** · Pavel/Tucker/Tony 終盤 | **CV 改善でも Public ノイズ** · 0.07 LB 差無視 · Final2=Trust CV · [要約](731550-final-two-submissions-shakeup.md) |
| **732455** | 票 17→20 · 本文なし | 密集崩落論 · scale-up 維持 · [要約](732455-leaderboard-thoughts.md) |
| **LB 全件** | 6,140 teams · 密集 6.0–6.5=**1,434** | Kazeneko **6.190 #127** · [leaderboard](../leaderboard.md) |
| Hellbore / Geologia / Anubhav | ポエム · 空 · LGBM starter | Final不可 · [Hellbore](../others-notebook/hellbore-v6-Ver.md) · [Anubhav](../others-notebook/anubhav-wellbore-lgbm-challenge-Ver.md) |
| 新規 Discussion トピック | **なし** | 戦略変更なし |
| 自チーム | 変更なし | Trust CV · 枠2 farvol · 本命 L |

総括: [`20260805-refresh.md`](20260805-refresh.md)

### 2026-08-04 eve refresh（差分）

| topicId / NB / LB | 変化 | 示唆 |
|---|---|---|
| **732455** | 票17·コメ9 · **Tucker scale-up** | 重いモデル拡大に gains · L 質改善と整合 · tip 密集は依然危険 · [要約](732455-leaderboard-thoughts.md) |
| **LB 全件** | 6,118 teams · 1位 4.608 · 密集=6.0–6.5 | Kazeneko **6.190 #122** · Public のみ · [leaderboard](../leaderboard.md) |
| AeroRidge v34 / Akiiro | 本日 run · tip 改題 | Final不可 · [AeroRidge](../others-notebook/yaroslav-aeroridge-v34-Ver.md) · [Akiiro](../others-notebook/akiirolabs-tvt-Ver.md) |
| 新規 Discussion トピック | **なし** | 戦略変更なし |
| 自チーム | 変更なし | Trust CV · 枠2 farvol · 本命 688 |

総括: [`20260804-eve-refresh.md`](20260804-eve-refresh.md)

### 2026-08-04 refresh（日中差分）

| topicId / NB | 変化 | 示唆 |
|---|---|---|
| **732455** | **新規·必読** · LB thoughts（票11） | Public 6.5–7.1 密集=clone過適合 · Private 崩落予測 · [要約](732455-leaderboard-thoughts.md) |
| **731550** | コメント+5 | Tucker: spatial CV は不要に hard · 保険 ensemble · Final2 不変 |
| **732296** | `assert len==14151` 罠 | sample 行数固定は Submit で落ちる |
| tip 量産 NB | robust-ensemble-v3 / best-score / gold-calibra fork | 同家系 · Final不可 |
| 自チーム | 変更なし | Trust CV + 枠2 Public · tip 禁止 |

総括: [`20260804-refresh.md`](20260804-refresh.md)

### 2026-08-03 refresh（差分）

| topicId / NB | 変化 | 示唆 |
|---|---|---|
| **732422** | **新規·運用必読** · Private 再採点の 9h | Andrey: **9h=全 test** · [error](error/732422-private-lb-9h-runtime.md) |
| **732432** / **732443** | teammate ban · scoring 8h | メダル経験談 · キュー待ち · [732432](732432-teammate-ban.md) · [732443](error/732443-scoring-time.md) |
| **731550** | コメント+5 | 軌道観察追記 · Final2 変更なし |
| **daniil 6.390** | 高票看板 | tip/Q0522 同家系 · Final不可 · [分析](../others-notebook/daniil-solution-6-390-Ver.md) |
| 自チーム | 変更なし | Final2 · Trust CV 維持 |

総括: [`20260803-refresh.md`](20260803-refresh.md)

### 2026-08-02 refresh（差分）

| topicId / NB | 変化 | 示唆 |
|---|---|---|
| **731550** | **新規·必読** · Final2 の選び方（票16） | Tucker: Trust CV · Civitasmass: CV1+Public1 · [要約](731550-final-two-submissions-shakeup.md) |
| **732296** / **730983** | Exception · 提出5h | 既知の hidden/採点待ち · [error](error/732296-notebook-threw-exception.md) |
| **yaroslav Contact+U** | Q0522 + score-space アフィン | 同家系 · Final不可 · [分析](../others-notebook/yaroslav-contact-u-restore-Ver.md) |
| 自チーム Final2 | 変更なし | コミュニティ合意と一致 |

総括: [`20260802-refresh.md`](20260802-refresh.md)

### 2026-07-30 refresh（差分）

| topicId / NB | 変化 | 示唆 |
|---|---|---|
| **新規 Discussion** | **なし** | 終盤 · Forum 静穏 |
| **blacklions Final Hierarch** | Q0522 **6.390 lock** + 井単位 LB 座標探索 | 同家系 · Public 追い · Final不可 · [分析](../others-notebook/blacklions-final-hierarch-Ver.md) |
| my0705 6.391 | tip クローン改題 | 捨て |
| farhan XGB starter | Chris 解説コピー | 教育のみ |

総括: [`20260730-refresh.md`](20260730-refresh.md)

### 2026-07-29 refresh（差分）

| topicId / NB | 変化 | 示唆 |
|---|---|---|
| **Georgy noise-floor** | **必読新NB** · 無編集再提出 σ≈0.03 | lever 微差を信じない · [分析](../others-notebook/georgy-noise-floor-lever-Ver.md) |
| **728477** | Georgy·souldrive コメント | seed 帯のサイズ付け · スレ未決着 · [728477](728477-public-lb-precise-but-biased.md) |
| **728712** | Nicolai: gs×1.3≠Private期待 | Final2禁止と整合 |
| **730092** | **新規** format error | ハードパス禁止 · [error/730092](error/730092-submission-format-error.md) |
| tip クローン | GBDT-gate / 「6.213」/ 6.520 | 同家系 · Final不可 |

総括: [`20260729-refresh.md`](20260729-refresh.md)

### 2026-07-27 refresh（差分）

| topicId / NB | 変化 | 示唆 |
|---|---|---|
| **729837** | **新規** · train-copy override / hidden 重複井？ | **Tucker: No overlap** · dummy 混同が fork 連鎖 · [729837](729837-train-copy-overlap.md) |
| **729879** | **新規** · 終了後 arXiv 方法論？ | Host 未回答 · スコア方針無影響 · [729879](729879-arxiv-post-comp-publication.md) |
| **729554** | OP·PC 追記 | `offset_inicio`←sample が罠 · **sample_submission 依存は危険** |
| **prvsiyan Frontier II** | **DYNQ0196**（+0.196） | DYNQ0130 延長 · 同家系 · Final不可 · [分析](../others-notebook/prvsiyan-frontier-ii-dynq0196.md) |
| タイトル紛らわし | romanrozen「beam-search」等 | 中身 Q0522/Frontier · 別経路と誤認しない |

総括: [`20260727-refresh.md`](20260727-refresh.md)

### 2026-07-26 refresh（差分）

| topicId / NB | 変化 | 示唆 |
|---|---|---|
| **729554** | **新規** · Submit で Notebook Threw Exception（sample 14151 OK） | ログ=3偽井 · hidden≈200 shape/mem · [error/729554](error/729554-notebook-threw-exception.md) |
| **728256** | コメント4（hongan · product-feedback リンク） | AI はコミュニティ可寄り · Host 未回答 |
| **prvsiyan VISUALS** | ホット · **DYNQ0130**（+0.130 動的 branch） | evansussex Q0522 の進化 · 同家系 · Final不可 · [分析](../others-notebook/prvsiyan-frontier-blend-visuals-dynq0130.md) |
| その他 topics | 本文ほぼ変化なし | 方針変更なし |

総括: [`20260726-refresh.md`](20260726-refresh.md)

### 2026-07-25 refresh（差分）

| topicId | 変化 | 示唆 |
|---|---|---|
| **別系統 intel** | LB + 14 topics 再取得 · [`20260725-alt-lineage-intel`](20260725-alt-lineage-intel.md) | 本命=generator×scorer 天井 · 近傍/方位は F 再確認のみ |
| **CHK-185** | **実行 GO** · [`chk185-result`](chk185-candidate-ceiling-result.md) | tip+SOFT oracle +0.15 · **generator不足** · 4.8帯未達 |
| **CHK-186** | **実行 mixed** · [`chk186-result`](chk186-generator-ceiling-result.md) | lik-PF seed-oracle +0.20 · hit≤4.5 46% · **188/189 自動開始なし** |
| **CHK-187** | **実行 GO** · [`chk187-result`](chk187-stage-oracle-result.md) | soft中間 +0.14 · F015再確認 · [`wave14×186`](wave14-x-chk186-join-2026-07-26.md) |
| **中間改善レジャー** | [`intermediate-improvement-ledger`](intermediate-improvement-ledger-2026-07-26.md) | **実測Δ +0.05〜0.08** vs soft oracle +0.155 · 次回模索テンプレ |
| **Wave-16** | 仮説追加 [`chk186-plan`](chk186-generator-ceiling-plan.md) · checklist CHK-186–189 | tip lik-PF 天井診断 · **未実行** |
| **728712** | **確認済** · 公開 PF の `gs`×≈1.3（tip コードに既実装 · ultimate-pf と同一） | 追加移植不要 · Final2 禁止 |
| **728879** | **新規** · Well Steerer 構想（コメント0） | スコア方針変更なし |
| **697416** | コメント16→17（Antek 感謝）· 既存 BIT_Guber/Sharmi を要約追記 | 位置のみ本命禁止 · DTW 区間切り盲信禁止 |
| **694973** | コメント22→23 · Luis が Scoring Error 解消メモ（07/24） | hidden 規模の concat / sample id 順 |
| 728022 / 728256 / 727570 | 変化なし | 有料DB不使用 · AI Host待ち · field-CV 既存 |

### 2026-07-24 refresh（差分）

| topicId | 変化 | 示唆 |
|---|---|---|
| **727570** | **souldrive** が well-CV vs field-CV（≈+0.3）· worst-field · `test/` identity を追記 | Trust CV 補強 · field leave-out |
| **728256** | コメント 0→3（tennogh: Rules 上 LLM 可寄り）· **Host 未回答** | 支援ツールは実務可 · ledger は Host 待ちのまま |
| 728022 | 依然コメント 0 | 有料 DB **不使用**維持 |
| 728477 / エラー系 | 票のみ微増 · 本文変化なし | 方針変更なし |

## 必読（スコア・方針に直結）

| topicId | 要約ファイル | 要点 |
|---|---|---|
| **732455** | [732455-leaderboard-thoughts.md](732455-leaderboard-thoughts.md) | **Public 密集帯=clone 過適合** · shake-up 予測 |
| **731550** | [731550-final-two-submissions-shakeup.md](731550-final-two-submissions-shakeup.md) | **Final2:** Trust CV + Public1（コミュニティ追認） |
| **732422** | [error/732422-private-lb-9h-runtime.md](error/732422-private-lb-9h-runtime.md) | **9h=Public+Private 全 test**（Andrey） |
| **728477** | [728477-public-lb-precise-but-biased.md](728477-public-lb-precise-but-biased.md) | **Public は精密だがバイアス** · seed バンド · Private SE · **統合:** [`../cv-lb-private-relation.md`](../cv-lb-private-relation.md) |
| **727171** | [Competition-Host_727171-working-note-winners.md](Competition-Host_727171-working-note-winners.md) | Working Note 受賞。**CV≠LB** · wiggle 無料・誤差は低周波 |
| **(community)** | [gr-instrument-limits-cv.md](gr-instrument-limits-cv.md) | **GR 欠損・水平揺動=機器制限** · CV は L/residual 本命 · GR 本命禁止 |
| **726751** | [726751-beginners-map-rowwise-ml-fails.md](726751-beginners-map-rowwise-ml-fails.md) | 行単位 LGBM &lt; anchor-hold |
| **726465** | [726465-top-team-signal-below-line-oracle.md](726465-top-team-signal-below-line-oracle.md) | **方位分割** · 近傍&lt;150ft コピー · Tucker 近傍無しでも ~5 |
| **719389** | [719389-cv-lb-correlation.md](719389-cv-lb-correlation.md) | **Trust your CV**。LB≈50 wells。CV&lt;6 で相関崩れ |
| **701691** | [701691-cv-lb-correlations.md](701691-cv-lb-correlations.md) | 早期 CV–LB 表 · 後半逆転例 |
| **704273** | [704273-how-much-trust-lb.md](704273-how-much-trust-lb.md) | 手法で CV↔Public の向きが違う |
| **701995** | [701995-public-lb-26pct-fixed.md](701995-public-lb-26pct-fixed.md) | Public 26% **固定** · 0.5 揺れ=seed |
| **707915** | [707915-public-nb-overfitting-lb.md](707915-public-nb-overfitting-lb.md) | 公開 NB の LB 過適合 · seed バンド |
| **711878** | [711878-pm15ft-bimodal-datum.md](711878-pm15ft-bimodal-datum.md) | **±15 ft 二峰**。曖昧井は中点/hedge |
| **712037** | [712037-fork-the-ruler.md](712037-fork-the-ruler.md) | drift slope 学習困難 · oracle harness |
| **717573** | [717573-score-without-tabular.md](717573-score-without-tabular.md) | 物理 LB6.58 · 非tabular で 5s |
| **727570** | [727570-local-validation.md](727570-local-validation.md) | Tucker CV 4.98→LB 5.7 · **souldrive field-CV** |
| **727149** | [727149-sub6-regime-alignment-cv.md](727149-sub6-regime-alignment-cv.md) | heel校正 · PF=trust gate · tops非アンカー |
| **723815** | [723815-worst-performing-well.md](723815-worst-performing-well.md) | 難井共有（`86454a6f` 等） |
| **708367** | [708367-problem-breakdown.md](708367-problem-breakdown.md) | last TVT→**15.883** · GR 回転 |
| **700340** | [700340-oof-vs-lb-worst-well.md](700340-oof-vs-lb-worst-well.md) | worst-well 追跡（hard-set と整合） |

## その他（recent）

| topicId | ファイル |
|---|---|
| 723647 | [723647-lowest-cv.md](723647-lowest-cv.md) |
| 721549 | [721549-pattern-matching-no-ml.md](721549-pattern-matching-no-ml.md) |
| 720701 | [720701-medal-cutoff-predictions.md](720701-medal-cutoff-predictions.md) |
| 717445 | [717445-writeup-anchors-guarded.md](717445-writeup-anchors-guarded.md) |
| 短記 | [20260723-recent-short-notes.md](20260723-recent-short-notes.md) |
| **728712** | [728712-gs-noise-scale-public-nb.md](728712-gs-noise-scale-public-nb.md) |
| **728879** | [728879-trying-to-build-well-steerer.md](728879-trying-to-build-well-steerer.md) |

## Host / Staff · 未回答 · エラー

| 種別 | 参照 |
|---|---|
| Host/Staff | [Competition-Host_697416-welcome.md](Competition-Host_697416-welcome.md) · [Kaggle-Staff_707695-private-test-rescore.md](Kaggle-Staff_707695-private-test-rescore.md) · [Kaggle-Staff_host-announcements-short.md](Kaggle-Staff_host-announcements-short.md) |
| Host 待ち | 728022 有料 DB（**不使用**）· [728256](728256-ai-coding-assistant.md) AI 支援（コミュニティは可寄り · Host 無）· [729879](729879-arxiv-post-comp-publication.md) 終了後 arXiv · 719235 地質解釈 |
| リーク/ダミー | [729837](729837-train-copy-overlap.md) hidden に train 重複なし · train-copy は LB 解釈に使わない |
| エラー | [error/732296-notebook-threw-exception.md](error/732296-notebook-threw-exception.md) · [error/730983-upload-submit-5hours.md](error/730983-upload-submit-5hours.md) · [error/730092-submission-format-error.md](error/730092-submission-format-error.md) · [error/729554-notebook-threw-exception.md](error/729554-notebook-threw-exception.md) · [error/728152-scoring-stuck-timeout.md](error/728152-scoring-stuck-timeout.md) · [error/727708-hidden-rerun-totalbytes-0.md](error/727708-hidden-rerun-totalbytes-0.md) |

## 横断メッセージ

1. **Trust CV**（well-group · マスク · multi-seed · **well vs field ギャップ監視**）  
2. **二峰は中点/hedge**  
3. 方位 · heel · 近傍&lt;150 · Typewell 整合  
4. 難井ルーティング · Private shake-up 大 → Final 2 多様性  
5. hidden ~200 で時間見積 · 手元 `test/` は検証不可  

## CLI 制約

長文欠落あり。726465/727149 は貼付補完済。
