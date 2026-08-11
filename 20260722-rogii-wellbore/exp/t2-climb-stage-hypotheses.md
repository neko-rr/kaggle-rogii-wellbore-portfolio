# T2 CV向上 · 工程分解後の新仮説 — 2026-08-04

> source: [`latest/t2-stage-well-map-2026-08-04.md`](latest/t2-stage-well-map-2026-08-04.md) · カタログ [`t2-catalog-report.md`](work/colab-final-t2/t2-catalog-report.md)  
> 先行: [`t2-climb-hypotheses.md`](t2-climb-hypotheses.md)（**620–626** · soft_diag本線 · 重複登録しない）  
> Active: [`experiment-checklist.md`](experiment-checklist.md)  
> 物差し: **T2≈80井 pooled RMSE** · 提出禁止既定 · Soft/learned 生FINAL禁止

---

## 優秀なKagglerとしての傾向読み（工程分解後）

| # | 傾向 | 定量 | 作戦への含意 |
|---|---|---|---|
| 1 | **勝ち分は「mid全面」に集中** | tip 17.03→mid **12.28**（Δ−4.75）· win **77**/hurt **3** | ゲート絞りではなく **注入面の質** が本命（620系維持） |
| 2 | **agree≡mid（frac=1）** | 同点 12.279 | T2では同意ゲート再発明は無意味 · 592/600型は打ち切り |
| 3 | **絞るほど悪化** | row 12.33 · HD **13.89** | H-D/部分注入は T2 Trust では損 · 514 Public と同型 |
| 4 | **tip↔mid選択の天井は薄い** | 3井 tip固定 **12.217** · 行oracle(漏洩)でも **12.18** | tip/mid切替だけでは **≪0.1** しか伸びない · **面の更新が必須** |
| 5 | **learned 方向に mid を寄せると大きく下がる** | mid+0.15(L−m)≈**11.27** · +0.3≈**10.31**（local診断） | **合成 residual は F015 自動禁止ではない**（α=1 生Lのみ禁止）· Public は F042 帯を tipdist で警戒 |
| 6 | **learned単独 6.81** | F015診断 | 天井示唆のみ · 提出禁止 |
| 7 | **517 hard20「mid悪化」物語は別面** | T2面 hard20 **20/20 win** | 旧H-D救済デザインをT2に持ち込むな |
| 8 | **soft_diag は未dump** | hard20 19.54のみ | 従来 **621→620** が第一本命のまま |

**1行:** 12.279 を本気で抜く経路は (A) soft_diag注入面 620 · (B) mid→learned方向の**薄い残差** · (C) 新mid。tip/mid切替とHDは小幅かマイナス。

---

## A. 工程分解から出た新規仮説（CHK-640–）

| ID | hypothesis | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|
| **CHK-640** | T2 map の **固定3井**（`70925e23` `ab3ced07` `19871e7f`）だけ tip 固定し他は mid にすると pooled **&lt; 12.279**（期待≈12.22） | high | T2&lt;12.279 · 他井非悪化 · 提出なし | **625の具体実装** · ≠602 ESS | T3 | **GO_small 12.217** |
| **CHK-641** | mid を土台に **α∈{0.10,0.15,0.20,0.30}·(learned−mid)** を加算（**α=1 の L単独のみ F015** · 合成は F015外）すると T2 が 12.279を明確更新 | critical | T2&lt;12.1 かつ sample非悪化 · Soft/L **生のみ**でない · anti-promote | ≠F015生L · ≠623 soft | T3 | **GO_t2 best α0.30=10.309** · E2E診断 ref **55223002** · 再提出禁止 |
| **CHK-642** | tip vs mid の **井単位 LOO oracle**（漏洩なし）上限が Δ&lt;0.15 なら、以降は **面更新のみ**（切替ゲート停止） | high | LOO天井報告1枚 · Stop更新 | 行oracle診断を超える | T4 | **done_stop Δ=0.062** |
| **CHK-643** | S2–S6 個別面を T2 dump し、tip→mid の **Δ−4.75 の発生工程**を特定すると、以後の改修を1工程に絞れる | medium | 工程別 RMSE 表 · 主因1つ | stage map 穴埋め | T3 | **pending** |
| **CHK-644** | 640+641 併用（3井 tip · 他 mid+α(L−m)）が単独より良い | medium | T2&lt;min(640,641) | 640/641後 | T3 | **pending**（641後·価値低） |
| **CHK-645** | T2設計から **「H-D救済」「fracを減らして安全」** を明示廃止すると、無駄CHKが減る | high | Explicit Stop 追記 · 追加実験0 | 分析確定済み | T4 | **done_stop** |

## B. 既存本線（再掲のみ · 新規にしない）

| ID | 役割 |
|---|---|
| **621→620** | soft_diag T2 dump→注入 · **第一本命** |
| **622/623** | soft絞り・soft≻mid · 620後 |
| **626** | 新 mid 面 · 面系全滅後 |
| **625** | 一般残留切替 → **640 に具体化** |

## C. やらない

| 禁止 | 理由 |
|---|---|
| HD / row / agree 微スイープで 12.279 更新 | 工程分解で否定 |
| tip×mid 0.5 ブレンド | T2で 14.61 に悪化（soft αと同型） |
| learned / mid 生 FINAL | F015 |
| 517の「mid悪化井→H-D」を T2 に移植 | 面が違う · T2 hard20 全勝 |

---

## 実行順（T2 CV特化）— 2026-08-04 更新

1. ~~**642** 天井~~ → **STOP_SWITCH**（Δ0.062）  
2. ~~**640** 3井 tip~~ → **GO_small**（12.217）  
3. ~~**641** mid+α(L−m)~~ → **GO_t2**（best 10.309 · 提出禁止）  
4. **621→620** soft_diag（面dump要 · 本命A · **次**）  
5. **643** S2–S6 dump（長 · 余力）  
6. **644** 併用任意 · **626** 面改  
7. ~~**645** Stop~~ → **done**

---

## 診断メモ（ラベル漏洩注意）

local 即席: mid+0.15(L−m)≈11.27 · mid+0.3(L−m)≈10.31 は **train ラベルで採点した傾向**であり、学習漏れではない（L/mid は同一 allowlist dump）が、**αは T2 上で格子固定し、E2E/別seedで再確認**する。αをラベルで直接 optimize しない。
