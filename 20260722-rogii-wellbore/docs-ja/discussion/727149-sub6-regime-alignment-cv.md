# Is the sub-6 regime end-to-end learned, or engineered alignment?

> Topic ID: **727149**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/727149  
> 投稿者: **Murat A. Genc**（1025th）  
> 投稿日時: **2026/07/17** UTC  
> 最新コメント: **2026/07/22** UTC（**Georgy Mamarin** · 623rd）— ユーザー貼付で全文反映（2026/07/23）  
> 原文: `docs-en/discussion/727149-sub6-regime-alignment-and-CV.md`

## 要約（質問側）

within-field · well-group · particle-filter 系で pooled OOF **≈9.9**。drift slope は合法特徴から学習不能（field-group OOF R²&lt;0）。問い:

1. sub-6 は end-to-end か、明示 alignment 後の精緻化か  
2. ±90 ft モード誤収束は formation tops で解けるか  
3. random well-group 5.3–5.8 vs within-field ~10 は field リークか。hidden は同 field か  

## Georgy Mamarin（623rd）· 2026/07/22 — 全文反映

### 問1: end-to-end vs 明示整合

| 測定 | 結果 |
|---|---|
| Oracle 校正 + GR misfit | 約 **82%** の well で datum を局在化 |
| 弱い合法 fit（flat carried surface） | ~**8%** |
| 合法 fit（heel で gain/offset → 前方へ） | ~**80%**（GR-rotation denoise で 84%）≈ oracle |
| 解釈 | 校正ギャップはほぼ閉じる → **end-to-end の追加勝ちは「校正」より heel 線が外挿できない per-well shape / dip** 側にありそう |
| 明示手法比較（固定プロトコル） | DTW · 窓相関 · PF を比較 → **生き残ったのは PF のみ**（−0.18 ± 0.04 ft / 5 seeds）。価値は予測そのものより **不確実性**（事後幅と誤差の相関 **+0.23**）→ **行単位 trust gate** |
| DTW | wash（ほぼ無効） |
| Tucker（当時 rank 2 言及） | sub-6 は **非 tabular**。一方 k256: 非 tabular 最良 7.098 vs tabular 最良 **6.798** → その人では frontier は **matching** で model class ではない |
| Tucker | per-well のみで pooled ~**5**（train-CV、LB ではない） |

### 問2: formation tops / ブラインドスポット

- **ANCC 等は 6 アンカーではない**（franticXu）: **1 つの base surface + well ごとの定数オフセット 5 つ**（自由度ほぼ 1、厚さは typewell）→ **絶対層アンカーにはならない**
- 共有ブラインドスポット: Working Note 波は **「unobservable, not unrecovered」**（観測不能）。Anthony Yanza の取得物理（識別に効く GR 帯がスコア行では計測床下）
- 対応: モード間を **校正した重みで hedge**（pilkwang）。Julian Villa の note は hedge 利得が base 依存 → 実装前に読む価値

### 問3: field リークか

| 実験 | 結果 |
|---|---|
| 素朴 within-field 借用（最近傍他 lateral の surface + 自 heel で datum） | 近傍 **&lt;150 ft** のときだけ last-value に勝つ（628 中 **41** wells、median **6.1 vs 10.2**）。〜600 ft はコイン。それ以遠は悪化（**18.2 vs 11.0**） |
| 注意 | 素朴レシピは **明示借用の下限**。暗黙の within-field 吸収は leave-spatial-block-out（daulettoibazar）で見る |
| Georgy 自 selector | pooled ~**10** vs leave-whole-field-out ~**10.9** → 分割差は **1 ft 未満** |
| Tucker ~5 | **per-well only** → クロス well リークでは説明不可 |
| 結論（Georgy） | pooled vs within-field ギャップは **手法品質**寄り。hidden が同 field かは **Host 未言明 — どちらも仮定するな** |

## スコア向上への示唆

1. heel 校正（gain/offset）をきちんとやったうえで、勝ちは **尾部の shape/dip**
2. DTW 単体に期待しすぎない。PF は予測より **信頼度ゲート**向き
3. formation tops でモード曖昧性を「解く」期待は低い
4. 近傍借用は **&lt;150 ft** のみ期待；遠井は悪化しうる
5. random well-group の sub-6 を即座にリークと決めつけない（Tucker 反証）。ただし **spatial leave-out 監査は残す**
6. ブラインド区間は観測不能なら **hedge / 不確実性**が本筋

## 効果が薄かった取り組み

- flat surface だけの校正
- DTW 単体
- formation tops を絶対アンカー扱い
- 遠井への素朴近傍コピー

## 次アクション

- [x] Georgy 全文を要約へ反映
- [ ] docs-en に貼付全文を追記
- [ ] 方位分割（726465）+ heel 校正 + 近傍&lt;150 転送を CHK 化
- [ ] spatial leave-out / leave-field-out を metric-repro に
