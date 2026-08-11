# Public LB · Private LB · ローカル CV の関係（実験 SSOT）

> updated: 2026-08-04  
> purpose: **採用・Final 2・提出枠・CHK 停止判定の判断基準**（スコア再掲の主場所ではない。数値の正は `exp/exp-index.md`）  
> 根拠 Discussion: 728477 · 719389 · 701691 · 704273 · 701995 · 707915 · 720701 · 723647 · 727570 · 712037 · 727149 · 700340 · 731550 · **732455** · Host 727171 · Staff 707695  
> **実測補強:** Georgy [noise-floor](others-notebook/georgy-noise-floor-lever-Ver.md) — 無編集再提出 **σ≈0.03 ft**（2026-07-29 refresh）  
> **終盤コミュニティ:** [732455 Leaderboard thoughts](discussion/732455-leaderboard-thoughts.md) — Public 6.5–7.1 密集帯は clone OOF≈10 報告 · shake-up 予測  
> 公式規定: [`conditions.md`](conditions.md) §Public/Private · Overview Leaderboard 文  
> 原文: `docs-en/discussion/*-raw.md` および既存 `docs-en/discussion/{topicId}-*.md`  
> **CHK 誤停止防止:** 下節 [実験停止の誤判定禁止](#実験停止の誤判定禁止agent必須) · [`comp-strategy`](comp-strategy.md) §Stop · checklist「Explicit Stop」

---

## 公式規定（Leaderboard 分割）

Kaggle が画面に出す基準文（そのまま）:

> This leaderboard is calculated with approximately **26%** of the test data.  
> The final results will be based on the other **74%**, so the final standings may be different.

| 名前 | 何のスコアか | いつ見えるか |
|---|---|---|
| **Public LB** | 隠れテスト全体のうち **約 26%** の行（井）だけで計算した RMSE | 提出直後〜コンペ終了まで |
| **Private LB** | 残り **約 74%** で計算した RMSE | **最終提出締切のあと**（順位の「本番」） |

つまり: 今見えている順位表は **テストの4分の1弱だけの試験**。本番は残りの約4分の3。**最終順位は変わりうる**、と公式が最初から言っている。

---

## 初学者向け：CV・Public・Private は何が違う？

試験に例えると分かりやすい。

| 物差し | たとえ | このコンペでの実体 | 何に使うか |
|---|---|---|---|
| **ローカル CV** | 自分で作った**過去問の模擬試験**（train 坑井を井単位で分けて測る） | well-GroupKFold / hard-set など | **手法を採るか捨てるか**の主判定 |
| **Public LB** | 先生が公開している**小テスト**（全体の **26%**） | 隠れテストの固定スライス ≈52 wells 前後 | 「提出が壊れていないか」「ざっくり同帯か」の検査 |
| **Private LB** | **本番の定期テスト**（全体の **74%**） | 残りの隠れテスト | **メダル・賞金・最終順位の正** |

よくある誤解と正しい読み方:

1. **「Public が良い = 優勝できる」ではない**  
   Public は一部の井だけ。別の井が多い Private で順位が入れ替わる（shake-up）のは普通。
2. **「Public が 0.05 良くなった = 確実に強くなった」ではない**  
   Georgy 実測では、**同じノートを無編集で出し直すだけ**でもブレの目安が **σ≈0.03 ft**（詳細は下の「Public スコアを評価するとき」）。差 **≲0.08** は多くがノイズ。昔の報告では 0.2〜0.5 動く例もある。
3. **「CV と Public が近い = Private も同じ」ではない**  
   同じ Public 井の上では CV と Public がほぼ一直線、という報告もある一方、Private は別の井集合なので話が別。
4. **だから優秀なチームはこうする**  
   - 採用: **CV（井グループ）**を信じる  
   - Public: 構造破綻・Scoring Error・大崩れの検知だけ（微差で CHK を GO にしない）  
   - Final 2 枠: **安定した CV の1本** + **別の狙いの1本（例: Public 最良）** — 本コンペ方針は [`comp-strategy.md`](comp-strategy.md)

自チームの数値の置き場は [`exp/exp-index.md`](../exp/exp-index.md)。提出ごとの予測帯は [`cv-public-private-forecast.md`](cv-public-private-forecast.md)。

---

## Public スコアを評価するとき（初学者向け・必読）

> 出典: Georgy [`noise-floor`](others-notebook/georgy-noise-floor-lever-Ver.md) · Discussion [728477](discussion/728477-public-lb-precise-but-biased.md) · [**732455**](discussion/732455-leaderboard-thoughts.md) · refresh [`20260804-refresh`](discussion/20260804-refresh.md)  
> **ここが Public 差分を読むときの判定ルールの正。**

### 体重計のたとえ

同じ体重計で測っても表示は少し揺れる。その「何もしていないのに出るブレ」が **ノイズ床（noise floor）**。  
サプリで −0.04 kg、と喜んでも、体重計のブレが ±0.03 なら、効果か測りムラか分からない。

Public LB も同じ。**同じ提出ノートを中身ゼロ変更で何度も出しても、スコアは揺れる。**

### Georgy の実測（2026-07 時点）

| 項目 | 値 | 意味 |
|---|---|---|
| **ノイズ床 σ** | **≈ 0.03 ft** | 無編集再提出の標準偏差の目安（fork A≈0.037 · B≈0.027） |
| **「改善」と信じにくい差** | **≲ 0.08 ft** | 1回ずつの比較では、偶然でも出やすい幅（だいたい 2σ 級） |
| **密集帯** | Bronze 付近に多数チーム | ±0.03〜0.04 の順位上下 ≠ 実力差 |

※ 2回だけの再提出では σ が読めない。Georgy / souldrive は **4〜5回**を推奨（締切近では枠コストに注意）。

### 判定チェックリスト（Public を見た直後）

| 質問 | YES のとき | NO / 曖昧のとき |
|---|---|---|
| Scoring Error・形壊れ（RMSE が異常に悪い）か？ | **要調査**（提出衛生） | — |
| 前回との差が **≳ 0.15〜0.20** か？ | 「方向」は議論可。それでも **採用は CV** | 差 **≲ 0.08** → **ノイズ扱い。CHK GO にしない** |
| 差が 0.08〜0.15 か？ | 「気になる」止まり。**Trust CV / tip-cv で確認**してから | Public だけで勝ち負けを決めない |
| tip 同家系の seed / 1パラメータだけ変えたか？ | ほぼノイズ or Public 過適合 | Final・Active にしない |
| **公開クローンで Public 6.5–7.1 だけ良い**か？（[732455](discussion/732455-leaderboard-thoughts.md)） | private 崩落リスク高 · **Trust CV / OOF 優先** | LB クローン追い |

### 自チーム運用への落とし込み

| する | しない |
|---|---|
| Public は **壊れていないか / 同帯か** の検査 | Public ±0.05 を「新 Best 根拠」や CHK 合格の主証拠にする |
| 採用・打ち切りは **Trust CV（tip-cv 等）** | 無編集再提出レースで日次枠を溶かす（終盤） |
| 枠2の「Public 1位」は **順位のラベル**（選抜軸）。その提出の「強さ」証明は CV | 「レバーを回して Public が 0.05 動いた」を Private 予測に使う |

数値の記録先: [`cv-public-private-forecast.md`](cv-public-private-forecast.md)（確定後に実測を書くとき、上表の閾値でコメントする）。

---

## 1 行結論

**採用は well-group CV（773 相当）優先。Public（公式≈26%）は「壊れていないか」の検査機。Private（公式≈74%）が最終順位 → Final 2 は「最良安定 CV」＋「別意図（例: Public 最良）」で組む。**

Public 上の **≲0.08（目安）〜0.3** の差は、多くの場合 **seed / 非決定性バンド**内で、Private 順位や手法採用の根拠にならない（Georgy σ≈0.03）。

---

## Public 26% の正体（偏り前提 · 2026-08-03）

| 確定 / 高信頼 | 内容 |
|---|---|
| **固定スライス** | Public ≈26%（≈52 / ~200 井）は **提出ごとに再抽選されない**（701995 Chris） |
| **非代表** | 同一スライス上では精密（yu4u r≈0.999）だが、オフセット定数（例 +0.32）＝**Private の良い点推定ではない**（728477） |
| **shake-up 前提** | Private で大逆転は設計上ありうる（720701 Chris · SE≈0.8 ft 級） |
| **手法依存の甘辛** | tip/PF 系は Public が甘く見えやすい · 空間系は厳しい（704273） |
| **Host** | CV↔Public 逆相関でも Public を追わないノートを表彰（727171） |
| **未開示** | 井の割り当て規則（ランダム / ID順 / 層別）は Host 未発言。**「やさしい井だけ」は主因として採用しない**（Georgy「friendly」と souldrive「厳しい」が矛盾） |

**運用含意:** Trust レーンと Public レーンは **別の物差し**。片方で負けても、もう片方のレーンを「失敗だから停止」と読まない。

---

## 実験停止の誤判定禁止（Agent 必須）

> checklist / CHK の GO・NO-GO・打ち切りは **この表を先に見る**。  
> 詳細運用: [`comp-strategy`](comp-strategy.md) §Stop · [`experiment-checklist`](../exp/experiment-checklist.md)「Explicit Stop」

### レーンを先に決める

| レーン | 主物差し | Public の役割 |
|---|---|---|
| **Trust / 枠1** | tip-cv · T2/T3 · hard-set 等 | 壊れていないか（任意の診断）。**悪化だけでの打ち切り禁止** |
| **Public / 枠2** | Public LB（構造健全な提出） | 枠2候補の順位。**Trust 悪化だけでの打ち切り禁止** |
| **診断のみ** | ユーザー明示の1回提出 | 結論を Final 自動差替にしない |

### これだけでは実験を止めない（誤停止）

| 観測 | 正しい読み | やってはいけないこと |
|---|---|---|
| **Trust≠Public**（例: Trust良・Public悪化） | Final2 前提。枠1候補は継続可 · 枠2には載せない | 「乖離＝手法失敗」で Trust レーンごと閉鎖 |
| **Public 差 ≲0.08**（σ≈0.03 帯） | ノイズ | CHK GO / Best 更新 / 打ち切りの根拠にする |
| **CV↔Public 乖離・逆相関** | 固定偏りスライス上では普通 | Active CHK や Bet を停止理由にする |
| **Public 順位が密集帯で下がった** | Private 推定力は弱い | 同家系 seed 乱打や Public 最適化スイープ |
| **「Public は易しい井だけ」仮説** | 未検証 · 主因にしない | その前提だけで CHK 設計や停止 |

### これなら止めてよい（正しい停止）

| 条件 | 例 |
|---|---|
| **当該レーンの主物差しが明確悪化** | Trust レーン: tip-cv / T2 が acceptance 割れ · Public レーン: 構造健全な提出で ≳0.15〜0.20 悪化かつ再現 |
| **構造破綻** | Scoring Error · RMSE 異常（10+ / 20 帯）· 形壊れ（F015 中間面など） |
| **閉鎖済み言い換え** | F013–F042 等 · `improvement-loop-failures.json` |
| **ユーザー明示 Stop** | 579 再提出禁止 · farvol 触らない · Soft FINAL 禁止 等 |
| **仮説台帳 / pretrain-gate FAIL** | gate 未通過のままフル評価しない |

### GO / NO-GO の書き方（混同防止）

- ❌「514 は Trust≠Public だから **実験全体 NO-GO**」
- ✅「514 は **枠2/Public 候補として NO-GO**。Trust レーンの別候補は継続」
- ❌「Public が微悪化したから Trust 改善 CHK を止める」
- ✅「Trust が acceptance を満たすなら枠1候補。Public は別レーンで診断」

---

## 矛盾に見えるが両立する事実

| 主張 | 意味 | 出典 |
|---|---|---|
| Public は CV とほぼ完全に並ぶ | **同じ固定 Public 井集合上**の比較では高精度（yu4u: r≈0.999 · 傾き≈1 · オフセット≈+0.32 · 残差≈0.028） | 728477 · 719389 |
| Public はノイジー | **再提出で 0.2〜0.5** 動く。原因は井の再抽選ではなく **パイプライン非決定性**（PF seed · GPU） | 701995 Chris · 719389 k256 · 707915 Georgy/pilkwang |
| CV&lt;~6 で CV–LB 相関が消える | 改善幅が seed バンドより小さくなり、**測定分解能不足**（相関が「壊れた」のではなく読めなくなった） | Tucker 719389 · 728477 解釈 |
| Private は大きく shake-up | Public 絶対値は Private の弱い推定。n≈52 の SE(RMSE)≈0.8 ft 級（実際は well 内相関で更に大きい） | 720701 Chris · 728477 |

**切り分け:** 「この 2 提出のどちらが **この Public スライス上**で良いか」と「どちらが **Private で残るか**」は別質問。前者では Public が精密、後者では CV（大 n）と多様性。

---

## 物差しの定義（混同禁止）

| 物差し | 何を測るか | 規模感 | 使い方 |
|---|---|---|---|
| **Local CV（自チーム）** | train 井の well-GroupKFold / hard-set | CF pooled ≈**15.9** · tip hard20 ≈**14.9**（Tucker 全井 ~5 帯とは **別スケール**） | **採用・graft 可否の主判定** |
| **上位者の train-CV** | 彼らの well-group pooled | ~**4.5–6** | 天井・プロトコル参考。自数値と直接比較しない |
| **Public LB** | hidden ≈200 の **公式約 26%（≈52 wells 前後）** | 自 Best 等は `exp-index` | 構造破綻の検知 · seed バンド測定 |
| **Private LB** | 公式 **約 74%**（outlier well 除外あり · Staff 707695） | 未公開 | **最終順位の正** |

### 手法によって CV↔Public の向きが変わる

| 系統 | 傾向（Discussion） | 含意 |
|---|---|---|
| 空間・近傍 offset | CV &lt; LB（Public が厳しい） | Public 楽観に騙されにくい |
| PF 系公開 NB | CV &gt; LB（Public が甘い） | Public 追いが過適合になりやすい |
| GBDT など大きめ改善期 | CV↓ と LB↓ が揃いやすい | 粗い変更の検証には使える |

出典: 704273（OP）· 701691（早期は相関あり · 後半は逆転例）

---

## コミュニティの数値アンカー（参考）

| 誰 | CV | Public | メモ |
|---|---|---|---|
| **Georgy** noise-floor | — | 無編集再提出 **σ≈0.03** | **Public 微差の物差し**（2026-07-29） |
| **yu4u**（上位） | 複数組 | CV+≈0.32 でほぼ線形 | 固定 Public 上の精密比較の証拠（728477） |
| **Tucker** | 4.98（5×5） / single≈5.4 · ens≈5.0 | ≈5.7 | per-well only · Trust CV（727570 · 723647） |
| **Tucker** | 改善 +0.7 でも LB 悪化あり | — | LB ノイズ · ラッキー提出あり（701691） |
| **Ruby** | 6.74→LB 6.48 · 6.22→LB **7.18** | 逆転 | 悪井支配の可能性 |
| **Gaurav** 早期表 | 31→10 台 | 35→9 台 | 粗い改善期は CV–LB 同方向 |
| **pilkwang** | — | 同一 NB 6 回 **7.201–7.286** | PF reseeding だけの seed バンド |
| **Host 受賞** | CV↔Public **逆相関**でも Public を追わないノートを評価 | — | 727171 |

---

## 自チームへの読み替え（2026-07-24）

| 観測 | 解釈 | 行動 |
|---|---|---|
| tip smoke **6.569** vs Best **6.524**（差 0.045） | **σ≈0.03 バンド内**（≦0.08） | **作者点・0.05 差を追わない** |
| tip 作者公開 **6.478** vs 自 smoke **6.569** | 同じ家系の運・環境差 | seed/α 乱獲 Stop 維持 |
| tip hard20 CV **14.87** ≫ Public **6.5** | hard-set は難井寄り · フル 773 ではない · Public は別井集合 | hard20 は **相対比較**用。絶対値を LB と同一視しない |
| CF pooled **15.91** | 門番 | これより悪い単独手法は rejected |
| tip↔Sunny 相関 **0.999**（CHK-053） | 形は似るが hard20 RMSE Sunny≈24≫tip≈14.5 | 相関≠多様性 |
| **Sunny SUB-1 Public 9.150** | CV 悪化が LB で実証 · seed バンド外 | **Final/予備禁止（F004）** |
| Contact-Gated 同族（tip / Ver2） | Public 密集帯の典型 | 別面未成立のため Final2 は **CV最良 + Public最良**（[`comp-strategy`](comp-strategy.md)） |
| 別面探索 F007–F012 | tip corr≈0.999 or 非改善 | 整合・近傍・NCC木の言い換え禁止 |

---

## 実験・提出での運用ルール

### A. 改善を採るとき

1. **well-GroupKFold（または同等の well-group）** で改善が multi-seed 平均として出る（yu4u / Trust-CV）
2. hard-set（CHK-024）悪化 ≤ 許容（既存 acceptance）
3. Public 提出は **構造確認・smoke** に限定。差分が自 seed バンド未満なら「改善」とみなさない
4. Random / 行単位 CV は永久禁止（F003 · `metric-repro.md`）

### B. Public を見るとき

**詳細・初学者向け判定:** 上節 [Public スコアを評価するとき](#public-スコアを評価するとき初学者向け必読)（**σ≈0.03 · 差≲0.08はノイズ**）。

| 見てよい | 見ない |
|---|---|
| 提出が壊れていないか（RMSE が 10+ や Error） | 密集帯の ±0.05〜0.1 順位争い |
| 同一 NB 再提出の **seed バンド幅**（測るなら4〜5回） | Public 順位最適化のハイパラ |
| 大きなパイプライン差（**≳0.15〜0.20**、できれば 1.0+）の方向 | tip smoke を Best にするために seed 乱獲 |
| CV と同符号か（粗い健全性） | 差 **≲0.08** を「レバー成功」と書く |

### C. Final 2（選抜方針の正は [`comp-strategy.md`](comp-strategy.md)）

| 枠 | 選び方 |
|---|---|
| **枠1** | **Trust CV 最良**（Private 耐性 · T2/T3 · 物理妥当） |
| **枠2** | **有効提出のうち Public 最良**（Error・F004/F005 除外） |

候補の数値は [`cv-public-private-forecast.md`](cv-public-private-forecast.md)。別予測面（NCC/近傍/整合）は F007–F012 で閉鎖。

**根拠（なぜ CV と Public を分けるか）:** Private ≈ 別井抽選 + shake-up（720701）· Public は固定スライス上では精密だが Private の弱い推定（728477）· Host は Public 過適合を嫌う（727171）。

### D. 終盤の提出枠

- 日次 5 は **CV で勝った変更の確認**と **Final 候補の seed 固定版**に使う
- LB ノイズ吸収のための乱打はしない（コストと過適合）

---

## Discussion 索引（本テーマ）

| Topic | 題（短） | 役割 |
|---|---|---|
| [728477](discussion/728477-public-lb-precise-but-biased.md) | Public は精密だがバイアス | **統合解釈（必読）** |
| [Georgy noise-floor](others-notebook/georgy-noise-floor-lever-Ver.md) | 無編集再提出 σ≈0.03 | **Public 微差の判定ルール（必読）** |
| [719389](discussion/719389-cv-lb-correlation.md) | Does CV correlate with LB? | Trust-CV · CV&lt;6 |
| [701691](discussion/701691-cv-lb-correlations.md) | cv and lb correlations | 早期表 · 逆転例 |
| [704273](discussion/704273-how-much-trust-lb.md) | How much trust LB? | 手法でギャップ方向が違う |
| [701995](discussion/701995-public-lb-26pct-fixed.md) | Public 26% fixed? | 固定スライス · 0.5 揺れ=seed |
| [707915](discussion/707915-public-nb-overfitting-lb.md) | Public NB overfit? | seed 過適合警告 |
| [720701](discussion/720701-medal-cutoff-predictions.md) | Medal cutoff | Private shake-up |
| [723647](discussion/723647-lowest-cv.md) | Lowest CV | Trust CV |
| [727570](discussion/727570-local-validation.md) | Local validation | Tucker 4.98/5.7 · **souldrive well vs field-CV ≈+0.3** · `test/` identity |
| [712037](discussion/712037-fork-the-ruler.md) | Fork the ruler | CV↔LB 幻影 |
| [727149](discussion/727149-sub6-regime-alignment-cv.md) | sub-6 / field CV | 校正 vs shape |
| [700340](discussion/700340-oof-vs-lb-worst-well.md) | OOF vs worst-well | hard-well 追跡 |
| [727171](discussion/Competition-Host_727171-working-note-winners.md) | Host Working Note | CV 規律 |
| [707695](discussion/Kaggle-Staff_707695-private-test-rescore.md) | Private rescore | Public 非可視 |
| [731550](discussion/731550-final-two-submissions-shakeup.md) | Final2 選び方 | Trust1+Public1 合意 |
| [732455](discussion/732455-leaderboard-thoughts.md) | LB thoughts · clone 密集 | **shake-up · Public 過適合警告（2026-08-04）** |

---

## 関連 SSOT

| ファイル | 関係 |
|---|---|
| [`exp/exp-index.md`](../exp/exp-index.md) | Best / tip / 次アクションの数値の正 |
| [`comp-strategy.md`](comp-strategy.md) | Final 2 · Stop |
| [`metric-repro.md`](metric-repro.md) | well-group のみ · Random 禁止 |
| [`cv-tiers.md`](cv-tiers.md) | T0–T4 用途別 CV · 採用/Final 判定式 |
| [`cv-public-private-forecast.md`](cv-public-private-forecast.md) | **CV/Public/Private 予測台帳（提出ごと更新）** |
| [`sub-1-3-lb-analysis.md`](sub-1-3-lb-analysis.md) | SUB-1/3 深掘り |
| [`submission-prep-cv.md`](submission-prep-cv.md) | tip CV 手順 |
| [`leaderboard.md`](leaderboard.md) | Public 分布 · shake-up |
| [`exp/experiment-checklist.md`](../exp/experiment-checklist.md) | Active CHK |

---

## 更新履歴

| date | 内容 |
|---|---|
| 2026-08-04 | **732455** · Public 6.5–7.1 clone 密集=shake-up 予測 · 判定行追加 |
| 2026-08-03 | **Public 26% 正体** · **実験停止の誤判定禁止**（Trust≠Public≠停止）· 731550 索引 |
| 2026-07-29 | **Public 評価節を追加** · Georgy σ≈0.03 · 差≲0.08はノイズ · 判定チェックリスト |
| 2026-07-25 | **公式 Leaderboard 文（26%/74%）**を冒頭に固定 · 初学者向け説明を追加 · [`conditions.md`](conditions.md) と同期 |
| 2026-07-24 | Discussion 再取得・分析に基づく初版（728477 を軸に統合） |
| 2026-07-24 | SUB-1 Sunny=9.150 を追記 · Final 予備除外 · [`sub-1-3-lb-analysis.md`](sub-1-3-lb-analysis.md) |
| 2026-07-24 | 予測台帳を [`cv-public-private-forecast.md`](cv-public-private-forecast.md) に分離（提出ごと更新） |
| 2026-07-24 | 727570 souldrive: field-CV / worst-field / `test/` identity を索引に反映 |
| 2026-07-24 | Final2=枠1 TrustCV / 枠2 Public最良（`comp-strategy`）· NCC本命表記削除 |
