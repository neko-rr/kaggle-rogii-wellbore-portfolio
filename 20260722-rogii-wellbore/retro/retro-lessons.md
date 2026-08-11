# rogii-wellbore 教訓 — 次コンペへ

> コンペ固有と汎用を分ける。**汎用は A/B/C に分ける**（性質が異なる）。  
> updated: 2026-08-10（**#17/#20/Host 追記 · 難易度帯 CV · 無相関 multi-path**）  
> 根拠: failures · Final2 · Private CLI · writeup Top1–7 · 公開コード · **08-10 #17/#20/#429/Host**  
> **前提:** ほぼすべて **条件付き（conditional / L0）**。コンペ型・メトリクス・リーク構造が違うと無効・逆効果になりうる。Agent は `apply` を満たすときのみ仮説化し、`avoid` に当たるとき採用しない。

---

## harvest 記法（Agent / 機械）

`## 汎用` 直下のみ対象。各項目は **番号 + 太字タイトル** + 次のフィールド（`- key: value`）:

| key | カード先 | 意味 |
|---|---|---|
| `body` | mechanism + intervention | 何を・なぜ（1〜2文） |
| `apply` | conditions | **このとき有効（成立条件）** |
| `avoid` | contraindications | **このときは使うな／無意味** |
| `origin` | tags `origin-*` | `own` · `topsolution` · `ops` · `mixed` |
| `domain` | tags `domain-*` | 既定 `kaggle`。AHC専用は `ahc`、両方に効く抽象は `shared` |
| `evidence` | 参考 | 根拠ポインタ（カード source_refs は行番号） |

`### A/B/C` → `knowledge-axis-*` タグ。

---

## 軸の定義

| 軸 | 問い | 例 |
|---|---|---|
| **A. CV・物差し** | 何を測り、何を信じ、何を残すか | Lane-split · Group CV · Final2 |
| **B. 解法** | 何をどう作るか | path · PF bank · synth |
| **C. 運用** | どう取る・置く・提出するか | CLI · E2E · archive |

---

## 汎用

### A. CV・物差し・提出判断

1. **提出受容の物差しをレーン分離する**
   - body: Trust（hard group CV / dual）と Public を同一 GO/NO-GO に混ぜない。小 Public 悪化だけで Trust レーンを止めない。
   - apply: Public が全テストの一部だけ · または Trust 用の別物差しがある
   - avoid: Public≈全データで信頼性高い · Trust 物差しが未定義のまま「分割した気になる」
   - origin: own
   - domain: kaggle
   - evidence: Final2 666+farvol · Rule public-lb-bias-stop · retro-private

2. **Public Best 1 本だけを Final にしない（小スライス LB）**
   - body: Public 頭は Private で崩れうる。Final 複数枠なら Trust 物差しの提出を1本残す。
   - apply: Final 2 本以上 · Public が非代表スライス（目安 ≲30–40% など開示あり）
   - avoid: Final 1 本のみ · Public=ほぼ全評価で CV≈LB が実証済み
   - origin: own
   - domain: kaggle
   - evidence: farvol Pub強/Priv弱 vs 666 採用

3. **グループ構造があるとき、行単位 CV を採択根拠にしない**
   - body: row/random KFold は楽観しグループ特徴リークを隠す。単位は well/patient/site 等。
   - apply: 同一グループが train/test に跨る · グループ特徴が使える
   - avoid: 行が実質 i.i.d. · グループ分割不能なほど n_group が小さいだけの言い訳 CV
   - origin: mixed
   - domain: shared
   - evidence: F003 · 上位 whole-well GroupKFold

4. **offline の oracle / 地図勝ちを、live dual・shippable OOF の GO にしない**
   - body: オフライン天井と online dual は符号不一致がありうる。出荷可能な評価だけを GO にする。
   - apply: dual / 多段 / 診断用 oracle があるパイプライン
   - avoid: 単段で offline 評価がそのまま提出可能と一致している
   - origin: own
   - domain: kaggle
   - evidence: F046 · Pack D vs dual NO-GO

5. **損失・行 weight の一機構いじりの後は、後段 dual を必須にする**
   - body: 単一 OOF/損失の改善だけでは GO にしない。残差・hard 帯・中間面崩壊を見る。
   - apply: 行 weight / 損失形を変え、後段 residual や中間面がある
   - avoid: 単段モデルで後段が無い · weight 実験ですらない
   - origin: own
   - domain: kaggle
   - evidence: F044 · F045 · L dual 全 NO-GO

6. **CV が測っている「本体」と、改善実験の対象を一致させる**
   - body: tip/残差 dual だけ主物差しだと実験棚が微調整に寄り、表現改革が劣後する。strict OOF は出荷全体へ。
   - apply: 多段パイプライン · 中間面と FINAL が違う
   - avoid: 単段 end-to-end で CV=出荷と一致している
   - origin: mixed
   - domain: kaggle
   - evidence: 自 dual vs 上位 path/PF · retro-solutions

7. **stack / residual / ブレンド係数は nested または heldfold で閉じる**
   - body: Public 順は監視用。係数は leak-free 単位で fit · 固定領収書化も有効。
   - apply: 多段 stack · OOF ブレンド · 方向係数がある
   - avoid: ブレンド段がなく単モデル · nested 不能なほどデータ極少で素直な holdout しかない
   - origin: topsolution
   - domain: shared
   - evidence: 7th ruler · 9th heldfold · #14 seed roster

8. **CV と Public が衝突したら「何を信じるか」を先に決めて固定する**
   - body: 衝突のたびに方針を変えず、事前ルール（例: CV 優先）を宣言して守る。
   - apply: Pub と CV が頻繁に逆転しうる · 選択を伴う実験が多い
   - avoid: 衝突が起きない状況 · ルール無しで「今日の気分」採用
   - origin: topsolution
   - domain: shared
   - evidence: Ruby XY-neighbor · CV>Pub

9. **group 単位のレシピ切替ゲート閾値は OOF で決め、Public にフィットさせない**
   - body: 「この group では系 B」を OOF/固定閾値にし、Public で閾値探索しない。
   - apply: 系統が複数 · group 品質が不均一
   - avoid: ゲート無し 1系統のみ · n_group が極少で閾値が安定しない
   - origin: topsolution
   - domain: kaggle
   - evidence: #1 xy_safe · #14 well gate

10. **総合 RMSE だけで採否せず、group 難易度帯（easy/normal/hard）ごとに改善を確認する**
   - body: 少数 catastro が平方平均を動かす。hard 改善×normal 悪化を CV 良と誤認しやすい。
   - apply: group 難易度の分散が大きい · hard 少数が RMSE を支配しうる
   - avoid: 行 i.i.d. で帯が意味を持たない · 帯定義自体がリーク
   - origin: topsolution
   - domain: shared
   - evidence: #17 Falcon PF-RMSE 4帯 · 自 hard pack 類似

11. **ブレンドは「単体強さ」より「誤差の無相関」を優先する**
   - body: 強モデルと同方向 residual は blend 無。弱でも直交する geo/physics leg の方が効く。
   - apply: 複数 path または estimator · OOF 残差相関を測れる
   - avoid: 候補が1系統だけ · 相関測定が無い
   - origin: topsolution
   - domain: shared
   - evidence: #20 grtx+geo+pfnet · #6 bank

---

### B. 解法・モデリング本体

1. **連続パス／整列問題では、独立行回帰より候補軸×時間のパス表現を優先検討する**
   - body: cost/alignment volume + 分類→soft decode 等が上位で共通。点回帰1本は多峰で崩れる。
   - apply: 連続軌跡・matching・整列が問題の自然な形
   - avoid: 行独立な表回帰で十分 · 系列構造が無い
   - origin: topsolution
   - domain: kaggle
   - evidence: writeup #1/#2/#5/… · code #1/#14/#23

2. **多峰の位置決めは点回帰1本で潰さず、候補バンクを残してから融合する**
   - body: PF/HMM/multi-decoder 等を並列し、gate/NN/ridge で融合する。
   - apply: 多峰・曖昧 matching が主誤差源
   - avoid: 単峰で十分 · 候補生成コストを払えない制約
   - origin: topsolution
   - domain: kaggle
   - evidence: #3 SoftMax gate · #6 PF bag

3. **データが少ない大きい表現には、合成 pretrain → 短い real finetune（本物過剰コピー禁止）**
   - body: 合成は skill 用に harder/cleaner。統計コピー目的の synth は避ける。
   - apply: ラベル少 · 表現学習が必要 · synth 物理/生成過程が定義できる
   - avoid: ラベル十分 · synth が本物の歪んだコピーになるだけ
   - origin: topsolution
   - domain: kaggle
   - evidence: #5 · Tucker · residual bank

4. **二次 refine にほぼ正解の first-pass を食わせると copy する**
   - body: 壊した first-pass で distrust を学ばせてから refine させる。
   - apply: 二段 refine · first-pass が train で常に良い
   - avoid: 単段 · refine 自体が無い
   - origin: topsolution
   - domain: shared
   - evidence: 7th writeup 733154

5. **階層 stack は差方向×固定係数で増分を足す設計を優先検討する**
   - body: base + c·(scale差) + seed 方向等。α の無制限スイープより receipt 固定が上位帯で多い。
   - apply: multi-scale / multi-seed の同族モデルがある
   - avoid: 単一モデル · 差方向が意味を持たない
   - origin: topsolution
   - domain: kaggle
   - evidence: keith #14 Construction A

6. **地理・近傍チャネルは常時 ON にせず、品質条件付きの別レシピにする**
   - body: 地理が怪しい単位では GR-only 等へ切替。Pub 悪化でも CV が正なら CV 側を守りうる。
   - apply: 近傍・地図特徴があり品質がばらつく
   - avoid: 地理特徴が無い · 全単位で同じ品質
   - origin: topsolution
   - domain: kaggle
   - evidence: #1 Ruby

7. **センサー非依存の geometric / surface anchor を平行系統として持つ**
   - body: 機器差・層ロックを避ける候補工場として価値がある。
   - apply: センサー系列が主特徴でバイアスが疑われる
   - avoid: センサーが信頼でき単系統で足りる
   - origin: topsolution
   - domain: kaggle
   - evidence: #6 writeup · code

8. **path 本体の後段としてだけ residual / surface router を薄く載せる**
   - body: residual を FINAL 主戦場にしない。生中間の FINAL 昇格は別禁止。工程改善は可。
   - apply: path/alignment 本体があり residual は補正
   - avoid: residual しか無い構成で無理に「本体」扱い
   - origin: mixed
   - domain: kaggle
   - evidence: #23 · F015 読み · 自 tip residual ギャップ

9. **近傍転送は絶対値ではなく anchor 差分（delta）でオフセットを消す**
   - body: 参照 well の定数オフセット混入を防ぎ、fold-safe に近傍を使える。
   - apply: 近傍 well または空間 prior を transfer する · Group fold がある
   - avoid: 近傍が使えない設定 · anchor が無い問題
   - origin: topsolution
   - domain: shared
   - evidence: #429 EGFDU delta · #25 cand cross-well shift

10. **1D 系列 registration は cost volume + 反復 refine（RAFT 型）を候補に入れる**
   - body: 曖昧 matching を CE で整形し反復で bulk を直す。hard には hurt もあり — 無相関 path と積む。
   - apply: ログまたは波形系列の整列が問題の本体
   - avoid: 表だけ · 多峰が主誤差でない
   - origin: topsolution
   - domain: kaggle
   - evidence: #20 grtx+RAFT

---

### C. 運用・post-comp / CodeComp

1. **Code Competition は固定成果物コピーだけの提出 NB を禁止する**
   - body: 採点は再実行する。Version はコンペデータから E2E 生成する。
   - apply: Code Competition / notebook-output 再実行採点
   - avoid: 単なる csv 提出コンペで NB 再実行が無い
   - origin: own
   - domain: kaggle
   - evidence: F005

2. **終了直後に自提出 privateScore 全履歴を CLI で取る**
   - body: Final 面以外の履歴最良が見える。チーム最終だけ見ない。
   - apply: Kaggle で privateScore が submissions API に出る終了後
   - avoid: 進行中で private が見えないフェーズを「取れた」と思う
   - origin: ops
   - domain: kaggle
   - evidence: competitions submissions

3. **終了後 Private 順位表は leaderboard -s。-d は public ファイルになりうる**
   - body: CLI の `-d` と `-s` を混同しない。
   - apply: Kaggle CLI で終了後 LB を取るとき
   - avoid: UI だけ使う · 別ホストのコンペ
   - origin: ops
   - domain: kaggle
   - evidence: 本コンペ CLI 実測

4. **終了後の上位公開 kernel は retro/archive/others-notebook/post-comp-top-YYYYMMDD/ に置く**
   - body: コンペ中 others-notebook と混ぜず rankNN- 命名する。
   - apply: 終了後に上位コードを保管する運用
   - avoid: コンペ中 tip を同フォルダに混ぜる
   - origin: ops
   - domain: kaggle
   - evidence: folder-map 2026-08-08

5. **AI agent 共同実験は「改善の定義」を固定し、方向クローズは human が拒否権を持つ**
   - body: agent は early に方向を閉じ・cheap 手法へ逃げる。採否は難易度帯基準など機械 + 人間判定。
   - apply: coding agent で大量 CHK を回す
   - avoid: agent 自由探索を無条件 GO · 採否基準が総合スコア1本のみ
   - origin: topsolution
   - domain: shared
   - evidence: #17 Falcon agent protocol

---

## コンペ固有（rogii · 転用禁止リスト）

1. tip/mid/L 残差 α · 生 mid FINAL（F015 読みの rogii 語彙）
2. residual Public NO-GO / 666 · farvol 数値
3. GR · Typewell · 地質
4. tip NB 密集帯 6.2–6.5
5. 固有モデル名・固有実装 ID

---

## すぐ試す / 条件付き / 避ける（要約）

| 区分 | 軸 | 施策 |
|---|---|---|
| すぐ試す | A | Lane-split · Group CV · 出荷 OOF（apply を確認） |
| すぐ試す | C | privateScore ヒスト · LB `-s` |
| 条件付き | B | path / bank / synth（**問題形が合うときだけ**） |
| 避ける | — | apply 無視の手法コピペ · Public 1本 Final · 条件空の promote |

---

## 横断参照

| 目的 | パス / Skill |
|---|---|
| harvest | `kaggle-knowledge-harvest` |
| AHC 併存方針 | `knowledge/README.md` · `knowledge/personal/domain-policy.md` |
| 詳細解法 | `retro-solutions.md` |

出典: retro-private · retro-solutions · failures · docs-en/solution · post-comp-top-20260808
