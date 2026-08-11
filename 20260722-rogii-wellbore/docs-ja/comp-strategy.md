# コンペ戦略 — rogii-wellbore

> skill: （なし — SSOT テンプレ。Plan 議論の結果をここに固定）  
> participant: Kazeneko  
> comp-url: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction  
> last-updated: 2026-08-04（Public偏り · 732455 shake-up · 誤停止禁止）

**コンペ全体の賭け方 SSOT。** 数値の正は [`exp/exp-index.md`](../exp/exp-index.md)。日次は [`comp-timeline.md`](comp-timeline.md)。実験単位は [`exp/experiment-checklist.md`](../exp/experiment-checklist.md)。  
**EDA→戦略:** [`others-notebook/eda/strategy-from-eda.md`](others-notebook/eda/strategy-from-eda.md)  
**CV↔LB↔Private:** [`cv-lb-private-relation.md`](cv-lb-private-relation.md) · 予測帯: [`cv-public-private-forecast.md`](cv-public-private-forecast.md)  
**Final2 外部根拠:** [`discussion/731550-final-two-submissions-shakeup.md`](discussion/731550-final-two-submissions-shakeup.md)（Trust CV + Public1）  
**shake-up 外部根拠:** [`discussion/732455-leaderboard-thoughts.md`](discussion/732455-leaderboard-thoughts.md)（Public 密集=clone 過適合）  
**提出 runtime:** [`discussion/error/732422-private-lb-9h-runtime.md`](discussion/error/732422-private-lb-9h-runtime.md)（9h=全 test）  
**Wave-7 途中:** [`wave7-status-2026-07-25.md`](wave7-status-2026-07-25.md)

| レイヤー | ファイル | 更新頻度 |
|---|---|---|
| **comp-level** | **本ファイル** | 方針転換・週次・締切前 |
| **今日** | `comp-timeline.md` § 提出・実行戦略 | 日次 |
| **次の実験** | `exp/experiment-checklist.md` | Phase 1 / 項目追加時 |

---

## Goal（目標）

| 項目 | 値 |
|---|---|
| **最終目標** | **Private 上位**（現実帯: 銅〜銀。金は遠い — 分布は [`leaderboard.md`](leaderboard.md)） |
| **意思決定の重み** | **Private ≫ Trust CV ≫ Public（検査のみ）** |
| **Public** | 隠れテスト約26%の **固定・非代表スライス**上の検査機（精密だが Private の弱い推定）。**σ≈0.03 · 差≲0.08はノイズ**（[`cv-lb-private-relation`](cv-lb-private-relation.md)）。密集帯の ±0.05〜0.3 は改善根拠にしない |
| **中間→後段** | **勝ち分だけ**通し、後段はスコア最適化。tip 類似・mid全面残存は成功指標にしない（[`cascade §0`](../exp/work/wave31-selector-replace/pipeline-cascade-retest.md)） |

**1 行要約:** 枠1=**Trust強**（現行 SUB-14 防衛 · tip⊕row495 等が候補）· 枠2=**Public強**（farvol / OPS-C）。**CV↔Public 乖離は実験停止理由にしない**（Final2で各1可 · ユーザー明示 2026-08-03）。全面 mid FINAL 禁止（F042）。諦め提案禁止。OPS-FINAL2並行。  
**Public代理レーン（2026-08-03）:** CHK-610–617は Public検査を動かしつつ **Private向上を祈る**仮説。Public単独で採用確定しない。詳細 [`private-proxy-public-hypotheses`](../exp/private-proxy-public-hypotheses.md)。

---

## Ceiling（天井・ボトルネック）

| 項目 | 内容 |
|---|---|
| **主因（想定）** | **天井≠tip 断絶**（oracle↑でも tip 面は下がる／動かない）· 低周波 datum · Contact-Gated 同族飽和 · 孤立井 |
| **構造天井（EDA）** | [`strategy-from-eda.md`](others-notebook/eda/strategy-from-eda.md) §構造事実 |
| **枠2の壁** | GR照合・近傍転写は tip 同面になりやすい（F007–**F012**）→ 別面は未成立 |
| **Wave-22 教訓** | 天井バンク×**現行 tip soft T0.15** は失敗（**F027**）· 近傍クリップだけでは足りない |
| **Wave-23 教訓** | 既存バンクの選択・再初期化・校正・ランカーは全滅（**F028–F032**） |
| **Wave-24 教訓** | 観測尤度改修・guided/learned proposal·ESS+MCMCも hard20 全滅（**F033–F035**） |
| **Wave-25 教訓** | 難井専用の観測再重み・PN再生成は全滅（**F036–F037**） |
| **Wave-26 教訓** | コンパスはねじれ/逆向き · 代理寄せも失敗 → **移す系閉鎖（F038）** |
| **Wave-27 教訓** | ねじれの種類を全測定 · 欠測/区分は天井大だがラベル無し実装不可 → **形修正閉鎖（F039）** |
| **Wave-28 教訓** | 提出可能直し方ハント6仮説全滅 → **F040** |
| **Wave-30 教訓** | Soft-Preserve は tip-cv/CF可。生Pearson≈0.9995で一旦閉鎖したが、CHK-395で**生Pearson単独切捨は誤判定疑い**（誤差0.689・井中心化0.895）· Soft-Preserve再学習は F041 維持 · [`caveat`](gate-pearson-caveat.md) · [`close`](discussion/wave30-close-2026-07-30.md) |
| **Wave-29 教訓** | 別面(S1a/S1b)門番未達 · FINAL後段は soft→selector 支配で安全ノブ0 → **B7/B8閉鎖 · F041** · [`close`](discussion/wave29-close-2026-07-30.md) |
| **Wave-31 方針** | A〜J → 31b（448 NO-GO）→ **Wave-31c**（条件付きselector · 新パートナー · 新学習は設計先行）· [`checklist`](../exp/experiment-checklist.md) |

---

## Bets（今週〜コンペ終了）

| id | 賭け | 状態 |
|---|---|---|
| B1 | 掘進方位を **学習内**条件に（tip 後処理禁止） | **閉鎖（F014）** |
| B2 | Typewell/heel + 系列整合 → 学習 | **閉鎖（F011）** |
| B3 | GR類似度ゲート付き近傍転写 | **閉鎖（F012）** |
| **B4** | tip最終 × Best最終の **井単位アービター** | **閉鎖（F016）** |
| **B5** | heel 拘束 **band-limited DTW → TVT** | **閉鎖（F017）** |
| **B6** | **提出可能な直し方** | **閉鎖（F040）** |
| **B7** | **真・別面**（薄いS1a/S1b） | **閉鎖（F041）** |
| **B8** | **FINAL面パイプライン**（ノブ最大1） | **閉鎖（F041）** |
| **B9** | **Soft-Preserve Ranker** | **閉鎖（F041）** |
| **B10** | **selector崖の上流改修**（soft提出なし） | **Active** · 448全面 **NO-GO** · 後継 **CHK-450→451**（条件付き） |
| **B11** | **第2生成器厚化**（設計差分必須 · caveat門番） | **閉鎖（tip-clone · 416）** · 417–418 skip |
| **B12** | **tip×非soft 薄ブレンド**（408天井の提出可能版） | **Active** · CHK-421 · **CHK-452**新パートナー · 449は451後 |
| **B13** | **公開intel再ハント** → 仮説移植 | **閉鎖（done）** · 422–423 → A–J移植済 |
| **B14** | **Selector定義置換**（soft品質に近いFINALを直接） | **Active** · 全面置換は448で終了 · **条件分岐のみ継続（451）** |
| **B15** | **Soft教師蒸留**（推論時 soft 入力禁止 · GPU） | **Active(設計)** · 旧431 HOLD · 後継 **CHK-453→454**（残差・絶対TVT禁止） |
| **B16** | **神経提案 / 条件付き生成器**（≠F033/F034 · GPU） | **Active(設計)** · 旧435 HOLD · 後継 **CHK-455→456**（anti-clone必須） |
| **B17** | **Post崩壊無効化パイプライン**（選択がFINALまで残る） | **閉鎖（437 NO-GO）** · 438–439 skip |
| **B18** | **二段残差補正**（tip→GPU残差 · label-freeゲート） | **閉鎖（442 NO-GO）** · 443 skip |
| **B19** | **tip全面再実装**（互換捨て · GPU大型） | **閉鎖（446 tip-clone）** · 447 skip |

**運用（Bets 外）:** tip 最終面への **生中間昇格禁止（F015）** · tip 離散プロファイル言い換え禁止（F013）· **S1/S2 工程改善・ゲート利用は許可**（[`f015-f013-correct-reading`](f015-f013-correct-reading.md)）· F023–**F042** の失敗済み**提出形**の言い換え禁止 · **諦め提案禁止**。  
**Wave-31c:** **Active** · B10/B12/B14（条件付き）+ B15/B16（設計→GPU）+ OPS-FINAL2（[`checklist`](../exp/experiment-checklist.md)）。  
**Wave-31b:** 448 NO-GO で収束終了 · 414/427 proxy closed。  
**Wave-31:** A〜J 探索完了分は archive（[`wave31-plan`](discussion/wave31-plan-2026-07-31.md)）。  
**Wave-30:** **CLOSED · F041** · B9。  
**Wave-29:** **CLOSED · F041** · B7/B8。  
**Wave-28:** **CLOSED** · B6 · F040。

checklist の CHK は Bets と整合。Bet に無い大きい実験は Phase 1 で却下するか、先に本表を更新。

---

## Final 2 選抜（ユーザー確定 2026-07-24 · **Wave-30 閉鎖後 2026-07-30**）

| 枠 | 選抜基準 | 意図 |
|---|---|---|
| **枠1** | **CV / Trust 強**（tip-cv · 現行 **SUB-14** 防衛 · tip⊕row495 等の Trust更新候補） | **Private 耐性** |
| **枠2** | **Public 強**（**farvol** / OPS-C · ユーザー選択） | Public hedge |

**選抜の読み（2026-08-03 追認）:** Discussion でも CV↔Public 乖離が話題だが、**両方の値が重要**で Final は2本。**どちらかに強ければ実験価値あり**（乖離＝停止理由にしない）。枠1候補は Trust で勝ち、枠2候補は Public で勝つものを別レーンで育てる。

**差替:**  
- 枠2候補: **OPS-C** と **farvol**（診断Public）。ユーザーが選ぶ。  
- Trust で tip を明確に抜いた FINAL（例: tip⊕row495）は枠1差替候補（ユーザー UI）。Public が悪くても Trust レーン実験は継続。  
- **B7/B8/B9/B11/B17–B19** の言い換え再探索はしない。

**別面門番:** CF / tip-cv / sample + caveat（[`gate-pearson-caveat`](gate-pearson-caveat.md)）。Soft-Preserve再学習は F041。

**別面判定（常設）:** tip相関を使う門番は誤差Pearson・井中心化を併記。詳細 [`gate-pearson-caveat`](gate-pearson-caveat.md) · checklist §別面門番チェック。

**除外（枠に載せない）:** Sunny（F004）· kernel_sources コピー（F005）· tip 中間面/mpkg単独（**F015**）· tip×Best アービター（**F016**）· heel-DTW（**F017**）· 仮説台帳 F001–F014 / F018–F020 / F026–**F041** の言い換え成果物。**全井 SOFT（SUB-8）**は Public 悪化で打ち切り。運用メモ [`ops-final2-prep`](ops-final2-prep-2026-07-26.md)。

候補の数値・予測帯は [`cv-public-private-forecast.md`](cv-public-private-forecast.md) のみに書く（本ファイルにスコア再掲しない）。

**日次 5 枠**は smoke / CV 確認用。乱打しない。

---

## Stop（試さない・優先しない）

詳細リストの正は [`exp/experiment-checklist.md`](../exp/experiment-checklist.md)「明示 Stop」と [`exp/improvement-loop-failures.json`](../exp/improvement-loop-failures.json)。  
**GO/NO-GO の誤判定表:** [`cv-lb-private-relation.md`](cv-lb-private-relation.md) §実験停止の誤判定禁止。

方針レベルで特に固定するもの:

- コンペ中に「実験終了・Final運用だけ」を推奨結論にしない（ユーザー明示 2026-07-31）。OPS-FINAL2は並行防衛
- **CV↔Public 乖離 / Trust≠Public だけを理由に実験を止める**（Final2で Trust1+Public1 · ユーザー明示 2026-08-03）
- **Public 差≲0.08** や密集帯の順位変動だけで CHK GO・打ち切りを決める
- **「Public=易しい井だけ」** を前提にした停止や CHK 設計（組成は Host 未開示 · 固定偏りは認める）
- Public 密集帯の順位最適化・seed 乱獲
- 閉鎖済み言い換え（F011/F012 · F038–**F041** 等）
- Random / 行単位 CV を採択根拠（F003）
- Working Note 再提出 · 手元 `test/` チューニング · 有料地下 DB
- 無許可 submit · チーム外 Private Sharing · Competition Data の再配布

**正しい停止の例:** 当該レーンの主物差しが acceptance 割れ · Scoring Error / 形壊れ · F台帳言い換え · ユーザー明示 Stop。
---

## 並行コンペ（該当時）

| コンペ | 優先度 | 備考 |
|---|---|---|
| rogii-wellbore | 高（Final 8/5） | 本コンペ |

---

## 更新履歴

| updated_utc | source | 変更内容 |
|---|---|---|
| 2026-07-23 | overview / Plan | 初版 |
| 2026-07-24 | Discussion / EDA / F011 | B2 閉鎖 · B3 候補 |
| 2026-07-24 | F012 · ユーザー方針 | **B3 閉鎖** · Final2=枠1 TrustCV / 枠2 Public最良 · 重複をリンクへ |
| 2026-07-24 | Wave-7 計画承認 | **B1 再開** · CHK-100–103 |
| 2026-07-25 | Wave-7 途中停止 | **B1 一時停止** · Phase2 未ゲート · SUB-4/5 PENDING · [`wave7-status`](wave7-status-2026-07-25.md) |
| 2026-07-25 | Wave-7 完了 | **F014** · CHK-100/103 NO-GO · CHK-101≡tip |
| 2026-07-25 | SUB-4–7 Public | **F015** · 中間面全滅 · 枠2=Best 維持 · [`sub-4-7-lb-analysis`](sub-4-7-lb-analysis.md) |
| 2026-07-25 | Wave-8 承認 | **B4 Active** · tip×Best 井単位アービター · 提出禁止 · CPU許可 |
| 2026-07-25 | Wave-8 CHK-120 | **F016** · tip≡Best FINAL · B4 閉鎖 · Final 運用へ |
| 2026-07-25 | Wave-9 承認 | **B5 Active** · heel 拘束 DTW · CHK-130–133 |
| 2026-07-25 | Wave-9 CHK-130 | **F017** · DTW NO-GO · B5 閉鎖 · Final 運用へ |
| 2026-07-25 | Wave-10 | **F018/F019** · 手がかりのみ · 新面なし |
| 2026-07-25 | Wave-11 | **F020** · SOFT f33-s08 · SUB-8 PENDING · 枠1維持 |
| 2026-07-26 | Wave-13 | OPS-LB-89 · SUB-9 **6.484** 新Best · SUB-8 打ち切り · Final仮更新 |
| 2026-07-26 | OPS-LB-101112 | SUB-11 **6.530** · 10 **6.541** · 12 **6.556** · Best維持 · s05/portable 打ち切り |
| 2026-07-25 | Wave-14 | A/B=`tip_std_far/prox` · CHK-183 screen · CHK-184 Public後 |
| 2026-07-27 | SUB-14 · Wave-21 | T0.15 Best · tip-cv≃LB · CHK-231 **F022** · Active=上流/中間 |
| 2026-07-29 | Wave-22/23 | Wave-22 全滅 · **F027** · Active=**Wave-23** 天井→tip 橋渡し |
| 2026-07-29 | Wave-23/24 | Wave-23 全滅 · **F028–F032** · Active=**Wave-24** 生成器再設計 |
| 2026-07-30 | Wave-24 close | hard20全滅 · **F033–F035** · Active=**OPS-FINAL2** |
| 2026-07-30 | Wave-25 | 難井専用レーン · 易井凍結 · CHK-297–320 |
| 2026-07-30 | Wave-25/26 | Wave-25 閉鎖 F036–F037 · Active=**Wave-26** コンパス監査 |
| 2026-07-30 | Wave-26 close | 移す系 **F038** 閉鎖 · Active=**OPS-FINAL2のみ** · [`close`](discussion/wave26-compass-close-2026-07-30.md) |
| 2026-07-30 | Wave-27 close | ねじれ分解 → **F039** 形修正閉鎖 · Active=**OPS-FINAL2のみ** · [`close`](discussion/wave27-twist-close-2026-07-30.md) |
| 2026-07-30 | Wave-28 plan | **B6 Active** · CHK-363–368（提出可能直し方）+ OPS-FINAL2 · [`hunt`](discussion/usable-fix-hypothesis-hunt-2026-07-30.md) |
| 2026-07-30 | Wave-28 close | CHK-363–368 全NO-GO · **F040** · Active=**OPS-FINAL2のみ** · [`close`](discussion/wave28-usable-fix-close-2026-07-30.md) |
| 2026-07-30 | Wave-29 plan | **B7/B8 Active** · 枠2=別面門番優先 · CHK-369–373 + 380–382 · [`wave29-plan`](discussion/wave29-plan-2026-07-30.md) |
| 2026-07-30 | Wave-29 close | B7門番未達 · B8ノブ0 · Active=**OPS-FINAL2のみ** · 枠2=Public1 C · [`close`](discussion/wave29-close-2026-07-30.md) |
| 2026-07-30 | OPS-LB-ABCD | Cが表示Public1 · 枠2暫定C · A/B/D NO-GO · 微差を改善扱いしない |
| 2026-07-30 | Wave-30 close | Soft-Preserve **F041** · [`close`](discussion/wave30-close-2026-07-30.md) |
| 2026-07-31 | ユーザー方針 | **諦め提案禁止** · Wave-31候補をchecklistへ · OPSは並行 |
| 2026-07-31 | Wave-31 plan | **B10–B13 Active** · CHK-411–423 全載 · [`wave31-plan`](discussion/wave31-plan-2026-07-31.md) |
| 2026-07-31 | Wave-31 expand | **B14–B19** · CHK-424–447（E〜J）追加 · GPU/パイプライン本線 |
| 2026-08-01 | Wave-31b 整理 | B11/B13/B17–B19 閉鎖 · B15/B16 HOLD · Active=CHK-414/421/427/**448**/**449** · farvol枠2候補 |
| 2026-08-03 | Public偏り分析 | **誤停止禁止**を Stop に固定 · Trust≠Public≠レーン停止 · [`cv-lb`](cv-lb-private-relation.md) |

---

## 関連ファイル

| ファイル | 役割 |
|---|---|
| `docs-ja/discussion/wave31-plan-2026-07-31.md` | Wave-31 計画 |
| `docs-ja/discussion/wave29-plan-2026-07-30.md` | Wave-29 並行レーン計画 |
| `docs-ja/discussion/wave29-close-2026-07-30.md` | Wave-29 クローズ（B7/B8未達） |
| `docs-ja/comp-timeline.md` | 締切・今日の戦略 |
| `docs-ja/wave7-status-2026-07-25.md` | Wave-7 途中スナップショット |
| `docs-ja/wave10-clue-stack-2026-07-25.md` | Wave-10 手がかり |
| `docs-ja/wave11-far-md-uncertainty-2026-07-25.md` | Wave-11 tip_self_line / SUB-8 |
| `docs-ja/wave12-difficulty-gated-soft-2026-07-25.md` | Wave-12 gated soft / SUB-9 |
| `docs-ja/wave13-plan-2026-07-25.md` | Wave-13 計画（gated 洗練 · Final） |
| `docs-ja/wave14-well-archetypes-2026-07-25.md` | Wave-14 井型 · A/B shape 分離 |
| `exp/experiment-checklist.md` | 実験 CHK |
| `exp/exp-index.md` | 現在地（数値の正） |
| `docs-ja/comp-profile.md` | comp-type |
