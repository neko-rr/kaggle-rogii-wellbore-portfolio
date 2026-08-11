# exp-intel — rogii-wellbore

> type: external-intelligence  
> updated: 2026-08-06（**締切翌日 · Discussion 6本 · Chris Final規則 · HMM 構造**）  

**Discussion 索引:** [`docs-ja/discussion/README.md`](../docs-ja/discussion/README.md) · **[2026-08-06](../docs-ja/discussion/20260806-refresh.md)** · [2026-08-05](../docs-ja/discussion/20260805-refresh.md) · [2026-08-04 eve](../docs-ja/discussion/20260804-eve-refresh.md) · **[学習分析](../docs-ja/discussion/training-insights.md)**  
**Public LB 分析:** [`docs-ja/leaderboard.md`](../docs-ja/leaderboard.md)（**08-05 フル 6,140 · 自 6.190 #127 · 08-06 全件 DL 失敗**）  
**Final2 コミュニティ:** [`731550`](../docs-ja/discussion/731550-final-two-submissions-shakeup.md)（票28）· **[Chris 規則 732947](../docs-ja/discussion/732947-final2-requires-public-score.md)**（**締切前 Public 完了のみ Final 可**）  
**構造・hard 井:** [`732999`](../docs-ja/discussion/732999-hmm-viterbi-hard-wells.md)（HMM · TVT≈g−Z · GR 完全一致無意味）· [`733015`](../docs-ja/discussion/733015-competition-broke-me.md)（OOF〜8 · Cody CV5/LB8）  
**shake-up 警告:** [`732455`](../docs-ja/discussion/732455-leaderboard-thoughts.md)（密集=clone · 票22）  
**runtime:** [`732422`](../docs-ja/discussion/error/732422-private-lb-9h-runtime.md) · [`732903`](../docs-ja/discussion/732903-inference-time-cpu.md)（**Staff: 通常 NB の CPU 可変**）  
**提出可能な直し方ハント:** [`docs-ja/discussion/usable-fix-hypothesis-hunt-2026-07-30.md`](../docs-ja/discussion/usable-fix-hypothesis-hunt-2026-07-30.md)  
**Public / Private / CV:** [`docs-ja/cv-lb-private-relation.md`](../docs-ja/cv-lb-private-relation.md)  
**公開 NB 索引:** [`docs-ja/others-notebook/README-public-useful.md`](../docs-ja/others-notebook/README-public-useful.md) · [Ver2 コピー](../docs-ja/others-notebook/README-kazeneko-v2.md)  
**公開コード最右（参考）:** [`evansussex Q0522`](../docs-ja/others-notebook/rogii-public-score-frontier-lab-visuals-evansussex-Ver1.md) · [`DYNQ0196`](../docs-ja/others-notebook/prvsiyan-frontier-ii-dynq0196.md) · [`Final Hierarch`](../docs-ja/others-notebook/blacklions-final-hierarch-Ver.md) · [`Contact+U`](../docs-ja/others-notebook/yaroslav-contact-u-restore-Ver.md) · [`daniil 6.390`](../docs-ja/others-notebook/daniil-solution-6-390-Ver.md)  
**診断必読:** [`Georgy noise-floor`](../docs-ja/others-notebook/georgy-noise-floor-lever-Ver.md)  
**08-06 スキャン:** [`Raunak Ultra`](../docs-ja/others-notebook/raunak-ultra-sub-6-Ver.md) · [`Farhan best-score`](../docs-ja/others-notebook/farhan-best-score-wellbore-Ver.md) · [`Sumit v2`](../docs-ja/others-notebook/sumit-rogiiv2-Ver.md) · [`Ayush CatBoost`](../docs-ja/others-notebook/ayush-rogii-ayush-Ver.md)  
**08-05 スキャン:** [`Hellbore 捨て`](../docs-ja/others-notebook/hellbore-v6-Ver.md) · [`Anubhav LGBM`](../docs-ja/others-notebook/anubhav-wellbore-lgbm-challenge-Ver.md)  
**同家系以外の参考:** [`non-tip-lineage-references.md`](../docs-ja/others-notebook/non-tip-lineage-references.md)  
**EDA 専用:** [`docs-ja/others-notebook/eda/README.md`](../docs-ja/others-notebook/eda/README.md) · 原文 `others-notebook/eda/` · 日本語注釈 `others-notebook/eda-ja/`
  
**文献・公開データ:** [`docs-ja/literature-survey.md`](../docs-ja/literature-survey.md)

---

## 重要な外部知見

| 種別 | 出典 | 要点 | 自チームへの示唆 | 優先度 |
|---|---|---|---|---|
| **提出可能な直し方** | [hunt 2026-07-30](../docs-ja/discussion/usable-fix-hypothesis-hunt-2026-07-30.md) · mycarta · dalloliogm · vamsee · 文献 | soft形修正は F038/F039 で行き止まり。残り候補は **H-A1〜H-B2** → **CHK-363–368** | Wave-28 Active · OPS-FINAL2並行 | **高** |
| **CV↔LB↔Private** | [728477](../docs-ja/discussion/728477-public-lb-precise-but-biased.md) · [**Georgy noise-floor**](../docs-ja/others-notebook/georgy-noise-floor-lever-Ver.md) · [**732455**](../docs-ja/discussion/732455-leaderboard-thoughts.md) · [cv-lb-private-relation](../docs-ja/cv-lb-private-relation.md) | Public 固定スライスは精密 · **無編集再提出 σ≈0.03** · **Public 6.5–7.1 密集=clone → Private 崩落** 予測 | 採用=Trust CV · tip LB を追わない | **高** |
| Host 講評 | [727171](../docs-ja/discussion/Competition-Host_727171-working-note-winners.md) | Wiggle 無料・誤差は低周波。CV≠Public | oracle ladder · spatial leave-out | **高** |
| **GR 機器制限（08-05）** | [gr-instrument-limits-cv](../docs-ja/discussion/gr-instrument-limits-cv.md) · Twitter/Discussion · 727171 同型 | GR **欠損・水平揺動 = 機器制限** · 高周波はノイズ床 · **埋め込み≠信号** | **L/residual 本命維持** · GR 本命特徴禁止 · 811 GR 二次 | **高（運用）** |
| CV 方針 | [719389](../docs-ja/discussion/719389-cv-lb-correlation.md) · [701691](../docs-ja/discussion/701691-cv-lb-correlations.md) · [723647](../docs-ja/discussion/723647-lowest-cv.md) · [727570](../docs-ja/discussion/727570-local-validation.md) | Trust CV。CV&lt;6 で LB 相関崩れ。**well vs field-CV ≈+0.3** | multi-seed · field leave-out | **高** |
| LB 信頼 | [704273](../docs-ja/discussion/704273-how-much-trust-lb.md) · [701995](../docs-ja/discussion/701995-public-lb-26pct-fixed.md) | 手法でギャップ方向が違う · Public 26% 固定 | PF 系は Public 甘めに注意 | **高** |
| 公開 NB 過適合 | [707915](../docs-ja/discussion/707915-public-nb-overfitting-lb.md) | seed だけで 0.08+ 動く | tip 同家系 Final2 禁止 | **高** |
| 二峰 datum | [711878](../docs-ja/discussion/711878-pm15ft-bimodal-datum.md) | ±15 ft · 中点が RMSE 最適 | hedge CHK | **高** |
| 方位・近傍 | [726465](../docs-ja/discussion/726465-top-team-signal-below-line-oracle.md) | 方位分割 · &lt;150ft コピー | B1/B3 | **高** |
| 整合/校正 | [727149](../docs-ja/discussion/727149-sub6-regime-alignment-cv.md) · [712037](../docs-ja/discussion/712037-fork-the-ruler.md) | heel 校正 · slope 学習困難 · PF=gate | B2 | **高** |
| 物理/非tabular | [717573](../docs-ja/discussion/717573-score-without-tabular.md) | 物理 LB6.58 · 非tabular 5s | 経路を tabular に閉じない | **高** |
| 難井 | [723815](../docs-ja/discussion/723815-worst-performing-well.md) · [700340](../docs-ja/discussion/700340-oof-vs-lb-worst-well.md) | `86454a6f` 等 · worst-well 追跡 | hard-set | 中 |
| ベースライン | [708367](../docs-ja/discussion/708367-problem-breakdown.md) | last TVT=15.883 · GR 回転 | 必須超え · denoise | **高** |
| shake-up | [720701](../docs-ja/discussion/720701-medal-cutoff-predictions.md) | Chris: Private 大変動 | Final 2 多様性 | **高** |
| **公開コード最右 VISUALS** | [evansussex](../docs-ja/others-notebook/rogii-public-score-frontier-lab-visuals-evansussex-Ver1.md) · [DYNQ0130](../docs-ja/others-notebook/prvsiyan-frontier-blend-visuals-dynq0130.md) · [**DYNQ0196**](../docs-ja/others-notebook/prvsiyan-frontier-ii-dynq0196.md) | 6.390 Q0522 · +0.130 → **+0.196** 動的 | **Final採用不可** · tip同家系 | **高（監視）** |
| **train-copy / dummy** | [729837](../docs-ja/discussion/729837-train-copy-overlap.md) | hidden に train 重複なし · LLM が dummy を誤解 | 手元3井・override で LB 解釈しない | **高** |
| 提出 Exception / format | [729554](../docs-ja/discussion/error/729554-notebook-threw-exception.md) · [732296](../docs-ja/discussion/error/732296-notebook-threw-exception.md) · [730092](../docs-ja/discussion/error/730092-submission-format-error.md) | sample 依存危険 · **`assert len==14151` 禁止** · ハードパス禁止 | E2Eは200井規模 | 中 |
| tip+GBDT ゲート | blacklions well-level-gbdt-gate（refresh-20260729） | Q0522 アンカー + well-level residual | 同家系 · Final不可 | 低（監視） |
| **Final Hierarch** | [blacklions-final-hierarch](../docs-ja/others-notebook/blacklions-final-hierarch-Ver.md) | Q0522 **6.390 lock** + 井単位 LB 座標探索 | Public追い · **Final不可** | **中（監視）** |
| **Contact+U Restore** | [yaroslav-contact-u-restore](../docs-ja/others-notebook/yaroslav-contact-u-restore-Ver.md) | Q0522 + score-space アフィン · 仮説~6.30 | 同家系 · Final不可 | 低（監視） |
| **daniil 6.390 Solution** | [daniil-solution-6-390](../docs-ja/others-notebook/daniil-solution-6-390-Ver.md) | Contact-Gated / Q0522 看板 · 票 **199**（08-05） | 同家系 · Final不可 | 低（監視） |
| **shake-up / LB 密集** | [732455](../docs-ja/discussion/732455-leaderboard-thoughts.md) · [LB 08-05](../docs-ja/leaderboard.md) | Michael: clone→Private 崩落 · **Tucker: scale-up gains** · 密集 **6.0–6.5（1,434）** · 自 **6.190 #127** | **自方針追認 · tip 禁止 · L 質** | **高** |
| **AeroRidge v34（改題）** | [yaroslav](../docs-ja/others-notebook/yaroslav-aeroridge-v34-Ver.md) | Contact/U · Q2522 Consensus residual 0.12 | 同家系 · Final不可 | 低（監視） |
| **AkiiroLabs** | [brianbovell](../docs-ja/others-notebook/akiirolabs-tvt-Ver.md) | koolbox+fleongg PF | 捨て | 低 |
| **9h runtime** | [732422](../docs-ja/discussion/error/732422-private-lb-9h-runtime.md) | Andrey: **9h=全 test** · Privateは隠れだけ | 提出NB壁時計の見積もり | **高（運用）** |
| **Final2 選定** | [731550](../docs-ja/discussion/731550-final-two-submissions-shakeup.md) | Tucker: Trust CV · Civitasmass: CV1+Public1 · **08-05: CV改善でも LB 往復 · 0.07差=ノイズ** | **自方針追認 · 変更不要** | **高** |
| **Hellbore V.6** | [hellbore](../docs-ja/others-notebook/hellbore-v6-Ver.md) | 数式ポエム · 実装なし | 捨て | 低（捨て） |
| **Anubhav LGBM** | [anubhav](../docs-ja/others-notebook/anubhav-wellbore-lgbm-challenge-Ver.md) | typewell+LGBM residual starter | 教育のみ · Active不要 | 低 |
| **Final=Public完了必須** | [732947 Chris](../docs-ja/discussion/732947-final2-requires-public-score.md) | 締切前に Public スコアが無い提出は枠選択不可 | PENDING(633/802)は枠外 · **666+farvol 正しい** | **高（運用）** |
| **HMM/物理構造** | [732999](../docs-ja/discussion/732999-hmm-viterbi-hard-wells.md) | TVT≈g−Z · GR 完全一致無意味 · hard=勾配 prior | retro 必読 · GR本命禁止追認 | **高（retro）** |
| **OOF〜8 天井談** | [733015](../docs-ja/discussion/733015-competition-broke-me.md) | cycle skip · Cody CV5/LB8.3 | L dual 全滅と同方向 · リークスコア不可 | **高（retro）** |
| **CPU 可変** | [732903 Ryan](../docs-ja/discussion/732903-inference-time-cpu.md) | 通常 NB の CPU 機種ばらつき | 壁時計1回見積禁止 | **高（運用）** |
| **Raunak Ultra** | [ultra-sub-6](../docs-ja/others-notebook/raunak-ultra-sub-6-Ver.md) | 1井 shape residual · tip | Final不可 | 低（監視） |
| **Farhan / Sumit tip** | [farhan](../docs-ja/others-notebook/farhan-best-score-wellbore-Ver.md) · [sumit](../docs-ja/others-notebook/sumit-rogiiv2-Ver.md) | profile 切替 · koolbox | 捨て | 低（捨て） |
| **Ayush CatBoost** | [ayush](../docs-ja/others-notebook/ayush-rogii-ayush-Ver.md) | tabular CatBoost starter | 教育のみ | 低 |
| **同 ID train TVT** | [732917](../docs-ja/discussion/732917-train-test-same-id-tvt.md) | Host 無回答 | 不使用維持 | 中（リスク） |
| 提出時間 | [728152](../docs-ja/discussion/error/728152-scoring-stuck-timeout.md) | ×200 wells | 時間ベンチ | **高** |
| 外部データ | [728022](../docs-en/discussion/728022-external-data-commercial-databases.md) | Host 未回答 | **不使用** | 高（リスク） |
| PF `gs`×1.3 | [728712](../docs-ja/discussion/728712-gs-noise-scale-public-nb.md) | 公開 PF · **Nicolai: Private期待するな** | **tip に既実装** · Final2禁止 | 低（確認済） |
| **Connor 幾何 EDA** | [dz-dtvt-eda](../docs-ja/others-notebook/dz-dtvt-eda-Ver-latest.md) | `dTVT≈−dZ+drift` · LOO · 幾何天井〜10ft | 構造事実の補強 · 提出コードにしない | **高（教育）** |
| **GeoAnchor** | [rogii-geoanchor](../docs-ja/others-notebook/rogii-geoanchor-Ver-latest.md) | Dual-Champion suffix arbiter | 同家系 · 概念のみ · Final2禁止 | 中 |
| **A016 guard OFF** | [a016…](../docs-ja/others-notebook/a016-true-no-contact-guard-ablation-Ver-latest.md) | contact guard ablation · submit-safe | guard 理解用 · 盲目 OFF 禁止 | 中 |
| **文献 PF/Bayesian** | [literature-survey](../docs-ja/literature-survey.md) | GR–type log を PF/SMC で合わせ層位置推定が本流。RL は舵取り用で RMSE 本命に非適合 | PF 校正・多峰 hedge を自 CV | **高** |
| **GWC 公開データ** | Zenodo/DataverseNO · Georgy | 人間解釈の分散 · median 集約 | 学習に混ぜず CHK-032 根拠 | 中 |
| **制約付き DTW** | Samant 2025 等 | 素朴 DTW は危険 · heel anchor 付きのみ | **CHK-040 Active** | 中 |
| **多峰 posterior** | SPE-212544 · P2 | 単一 MAP より hedge | **CHK-041 Active**（023 後継） | **高** |

---

## 学習NB Scout（2026-07-24 · CHK-070/071）

| slug | 学習有無 | GPU | DS依存 | 枠2向き | 採用 |
|---|---|---|---|---|---|
| mitchgansemer/drift-targeting-ncc… | 本編は推論（offline modeling 未公開） | — | models DS 欠落 | 概念のみ | 仕様参照 |
| romanrozen/catboost-baseline | **あり** residual+CatBoost+GroupKFold | **ON** | コンペのみ | **Yes**（tip低相関狙い） | **CHK-070 Private fork** |
| pavloivanin/baseline-lightgbm-with-groupkfold | **あり** 絶対TVT+LGBM | OFF→ON化 | コンペのみ | No（tabular同系統） | **CHK-071 Private fork** |
| llkh0a/rogii-lgbm-aug-online-training | あり | ? | 要確認 | 副候補 | 温存 |
| sgy2512/rogii-lgb-v48 | あり（PF+LGBM混在） | ? | 複雑 | tip近縁リスク | 温存 |
| sadamtorres/rogii-lgbm-xgb-catboost-ensemble | あり | ? | 要確認 | 副候補 | 温存 |

ローカル pull: `others-notebook/train-scout/`

---

| Notebook | 作者 | 再現性 | 強み | 自チームで試すこと |
|---|---|---|---|---|
| **公開有用 19本 + refresh** | 各種 | 取得済 | 検証・物理・教育 · **2026-07-25** Connor/geoanchor/A016 | [README-public-useful](../docs-ja/others-notebook/README-public-useful.md) · [refresh](../docs-ja/others-notebook/public-useful-refresh-20260725.md) |
| **EDA 12本** | Chris / n0 / souldrive 他 | 取得済 | 直感・構造・難井 | [eda/README](../docs-ja/others-notebook/eda/README.md) · `eda-ja/` |
| Connor dz-dtvt | connortynan | **S** | 純幾何 · LOO · 天井〜10ft | 必読 · 提出不可 |
| GeoAnchor | lucifer19 | A | suffix arbiter 叙述 | 概念のみ |
| A016 guard OFF | zongzishuang | A | contact ablation | 参照のみ |
| fork-the-ruler… | Georgy | **S** | oracle ladder · leave-field-out | **自 CV の型**に移植 |
| GWC precision | Georgy | S | ラベル=人間 · median 集約 | Final 哲学 · LB直接は不可 |
| Sunny physical | sunnywu27 | S | PF128 · GR補間 · 非tabular | Final 2 多様性候補 |
| honest carry-forward | n0Rollback | A | CF ≫ 軌道 HGB | 否定実験テンプレ |
| beginners 7 visuals | n0Rollback | A | png / GR 直感 | EDA 起点 |
| Chris EDA / XGB | cdeotte | A | GroupKFold · CV~15 | 行寄り ML 天井の証拠 |
| Mitch NCC drift | mitchgansemer | A | drift 目標 · multi-NCC | 特徴 CHK（LB 旧） |
| Pilkwang WN/EDA | pilkwang | A | target-free 整合叙述 | B2 手順抽出 |
| Yusuke another* | yusuketogashi | B | 実験ログ | 同スタック · 差分のみ |
| Ravaghi ridge | ravaghi | B | artifacts 祖先 | 家系理解 |
| Roman geology-aware | romanrozen | B | fleongg blend | Ver2 と同族 |
| FOYSAL gold/exp | FOYSAL | B | 失敗開示 | 校正は CHK、盲目不可 |
| **Kazeneko Ver2** | 自 fork | 済 | Best 6.644 | [README-kazeneko-v2](../docs-ja/others-notebook/README-kazeneko-v2.md) |

---

## Discussion分析

| Discussion | 要点 | 信頼度 | 実験アイデア |
|---|---|---|---|
| 727171 Host winners | 低周波トレンド · CV 監査 | 高（Host） | B2/B3 をトレンド寄りに |
| 726465 / De DQ+Tucker | 近傍コピー vs 近傍無し sub-5 · **方位分割** | 高 | B1 方位 · B3 近傍転写 |
| 727149 / Georgy | heel校正 · PF=不確実性 · tops潰れる · field仮定禁止 | 高（実測） | heel校正 CHK · leave-field-out |
| 726834 OpPrime | 多モデル同誤収束 | 中 | 不確実性区間の検出 |
| 707695 Staff | Private outlier 除外 | 高 | Public 過信しない |
| 728022 / 728256 | 有料 DB 禁止維持 · AI はコミュニティ可寄り · Host 無 | 中 | Rules 再確認のみ |
| **729837 Tucker** | hidden train 重複なし · train-copy は fork 遺産 | 高 | 手元ラベル経路を本命にしない |
| **729879** | 終了後 arXiv（Host 未回答） | 低 | スコア無影響 · データ外出し禁止維持 |
| **727570 souldrive** | well vs field-CV ≈+0.3 · worst field · `test/` identity | 高 | field leave-out 監視 |

---

## 上位解法・writeup

| チーム / 作者 | 手法 | 勝因 | 再現に必要なもの |
|---|---|---|---|
| FOYSAL | Working Note: Anchors / Guarded GR | ガード付き整合 | writeup + `experimental-notebook` |
| Georgy | Fork the ruler · GWC precision | oracle/wall harness · 人間ラベル | **自 OOF に ruler 適用** |
| Pilkwang | Target-free Working Note | 整合叙述 | B2 CHK 化 |
| Sunny | Physical + PF | 非tabular 経路 | Final 多様性 |

### 別系統シグナル refresh（2026-07-25 · 実験なし）

- 要約: [`docs-ja/discussion/20260725-alt-lineage-intel.md`](../docs-ja/discussion/20260725-alt-lineage-intel.md)
- **CHK-185 実行済:** [`chk185-candidate-ceiling-result`](../docs-ja/discussion/chk185-candidate-ceiling-result.md) · tip+SOFT oracle **+0.15** のみ · **generator不足** · 4.8帯未達
- **CHK-186 実行済:** [`chk186-generator-ceiling-result`](../docs-ja/discussion/chk186-generator-ceiling-result.md) · lik-PF seed-oracle **+0.20** · mixed · **188/189 自動開始なし**
- **CHK-187 実行済:** [`chk187-stage-oracle-result`](../docs-ja/discussion/chk187-stage-oracle-result.md) · soft/中間 **+0.14** · F015再確認 · [`wave14×186`](../docs-ja/discussion/wave14-x-chk186-join-2026-07-26.md)
- manifest: [`intel/solution-writeups/`](../intel/solution-writeups/)
- **新シグナル本命（検証後）:** Discussion の候補oracle≈4.5は手元 tip 集合では再現せず。公開同家系合成は頭打ち
- **再確認のみ（F閉鎖）:** 近傍コピー・方位分割（F012/F014）

---

## 更新履歴

| date | 内容 |
|---|---|
| 2026-08-06 | **CLI 総更新（締切翌日）**: Discussion **6本新規**（732999/733015/732947 Chris/732903 Staff 等）· tip NB 4本 · 全件 LB DL 失敗 · [`20260806-refresh`](../docs-ja/discussion/20260806-refresh.md) |
| 2026-08-05 | **CLI 総更新（締切日）**: **731550 終盤**（CV改善でも LB ノイズ · Final2=Trust CV）· 732455 票20 · Hellbore/空/Anubhav スキャン · **LB 6,140 / 自 6.190 #127** · [`20260805-refresh`](../docs-ja/discussion/20260805-refresh.md) · [`leaderboard`](../docs-ja/leaderboard.md) |
| 2026-08-04 eve | **CLI 総更新**: Discussion 差分ほぼ無し · **732455 Tucker scale-up** · AeroRidge/Akiiro 分析 · **Public LB 6,118 / 自 6.190 #122** · [`eve-refresh`](../docs-ja/discussion/20260804-eve-refresh.md) · [`leaderboard`](../docs-ja/leaderboard.md) |
| 2026-08-04 | **732455** LB thoughts · tip 量産スキャン · sample assert · [`20260804-refresh`](../docs-ja/discussion/20260804-refresh.md) |
| 2026-07-26 | **Discussion/NB refresh**: **729554** Exception · 728256+1 · **prvsiyan DYNQ0130** · [`20260726-refresh`](../docs-ja/discussion/20260726-refresh.md)
| 2026-07-26 | **公開コード最右** evansussex Frontier VISUALS **6.390** · Q0522 1井パッチ分析 · Final採用不可 |
| 2026-07-25 | **別系統 intel**: topics/LB CLI refresh · S1–S5 · **CHK-185 計画のみ**（未実行） |
| 2026-07-25 | **公開 NB refresh → checklist**: Parked CHK-110–112 · Stop（gs再乗算/pfcfg/純幾何Final等）· Active乱増なし |
| 2026-07-23 | CLI 16 topics 初回 · 726465/727149 全文補完 |
| 2026-07-23 | recent wave: 18 topics 追加取得 · CV/二峰/難井/物理/shake-up 要約 |
| 2026-07-23 | Kazeneko Ver2 8 kernels pull · 分析（公開 dual-track 家系） |
| 2026-07-23 | 公開有用 NB 19本 pull · 多様性優先で分析（README-public-useful） |
| 2026-07-23 | 文献・公開データ調査（`docs-ja/literature-survey.md`）· PF/Bayesian 裏付け · 外部データ GO/NO-GO |
| 2026-07-24 | CV/LB/Private Discussion 再調査 · **728477** · `cv-lb-private-relation.md` · Final2 方針強化 |
| 2026-07-25 | Discussion refresh: **728712** PF `gs`×1.3 · **728879** Well Steerer · Welcome/694973 追記 |
| 2026-07-24 | Discussion refresh: **727570** souldrive field-CV · **728256** コメント3 · 索引/ledger 更新 |
| 2026-07-24 | **学習 Discussion 分析** → `training-insights.md` · checklist **CHK-040 強化 + CHK-072** |
| 2026-07-24 | **EDA 公開NB** 12本を `others-notebook/eda/` 集約 · 日本語注釈 `eda-ja/` · [`eda/README.md`](../docs-ja/others-notebook/eda/README.md) |
| 2026-07-24 | **EDA→戦略** · その後 F012 · Final=枠1 CV / 枠2 Public — 正は [`comp-strategy`](../docs-ja/comp-strategy.md) |
| 2026-07-23 | 文献→CHK: 既存裏打ちマップ + **CHK-040/041** のみ Active 追加 |
