# Wave-14 — 井アーキタイプ診断（2026-07-25）

> 作業: [`exp/work/wave14-well-archetypes/`](../exp/work/wave14-well-archetypes/)  
> 親: Wave-13 A [`wave13-a-best.json`](../exp/work/wave13-gated-refine/wave13-a-best.json)  
> 目的: **どの後処理がどの型に効くか**を多切り口で確定し、悪化井除外の portable 代理を検証する

## 1 行結論

**A/B の本命手がかりは `tip_std_far / tip_std_prox`（遠方が相対的にジグザグなら悪化型）。**  
方位代理除外は失敗したが、この shape 特徴は oracle 悪化5井と一致し T2 screen PASS。閾値は A/B フィットのため **Public 後に本CHK化**してから提出候補へ。

---

## 確定した仮説（反復後）

| ID | 仮説 | 判定 |
|---|---|---|
| **H1** | portable（複合ゲート+f33-s05）は ungated SOFT より sample を守る | **確定** · easy sample で ungated Δ≈−0.08、portable≈0 |
| **H2** | Far-self-dev には **助け型 A** と **悪化型 B** が同居（各15井） | **確定** · A: portable Δ≈**+0.17** · B: ≈**−0.07** |
| **H3** | `self_dev` だけでは A/B を分離できない | **確定**（定義上どちらも >8） |
| H4 | ゲート内悪化井を推論時メタで代理できる | **更新** · 方位代理は粗い → **`tip_std_far/prox` が本命**（下節） |
| **H5** | その代理で除外 graft すると sample↑だが pool が厳格割れ | **方位代理は NO-GO**（CHK-182） |
| **H5b** | `tip_std_far_over_prox≥0.84` 除外は oracle と一致し T2 厳格改善 | **screen PASS** · 閾値は A/B フィット注意 · Public 後に本CHK化 |
| **H6** | 人口全体では NW_N の ungated SOFT は平均プラス（+0.05）· SW_W はマイナス（−0.12） | **確定**（方位切り口） |
| **H7** | 着床 EGFDL/BUDA・空間疎は今回の後処理選択を変えない | **確定**（弱い／既閉鎖） |

**提出・枠1への含意:** 当面の安全側は Wave-13 portable。shape 除外は Public 継続時に専用 CHK で確定してから。

---

## アーキタイプ × 後処理（平均 Δ = tipRMSE − intervRMSE · 正=改善）

| 型 | n | ungated f33-s08 | portable s05 | two-stage k5 | 読み |
|---|---:|---:|---:|---:|---|
| **A_far_helped** | 15 | **+0.41** | **+0.17** | +0.17 | SOFT 本命帯 |
| **B_far_hurt** | 15 | **−0.36** | **−0.07** | −0.03 | 除外したいが代理が粗い |
| C_nwn_hard | 2 | +0.14 | 0 | 0 | ゲート外なら触らない |
| Cish_other_hard | 3 | −0.18 | 0 | 0 | ungated 有害 |
| **E_easy_sample** | 37 | **−0.08** | ≈0 | ≈0 | **触るな** · ゲートが防衛 |
| Eish_other_sample | 8 | +0.02 | 0 | 0 | 中立 |

全体介入ランキング（井平均）: compound s08 ≧ two-stage ≧ f40-s05 ≧ … だが **採用は T2 厳格＋sample** で Wave-13 portable。

---

## 切り口別メモ

| 切り口 | 所見 |
|---|---|
| **self_dev bin** | >8 で SOFT が効き始めるが、助け/悪化が混在 |
| **heel bin** | ゲート条件としては有効 · 悪化識別の単体 AUC≈0.5 |
| **az_bin** | NW_N: soft 平均プラス · SW_W/SE_S: マイナス寄り |
| **hard vs sample** | hard は gated soft で改善 · sample は ungated で必ず削られる |
| **landing** | hard20 のみ結合 · 後処理選択を変える信号なし |
| **portable_apply** | 適用井だけで pool 改善が集中 · 非適用井は Δ≈0 |

---

## CHK-181 / 182 数値

| 項目 | 値 |
|---|---|
| ゲート井 | 14 |
| portable 上の悪化井 | 5（= oracle k5） |
| 代理 | `az_nwn_affinity ≥ -0.064` · prec 0.5 · rec 1.0 · 除外10井 |
| CHK-182 | apply 4井のみ · Δpool **+0.040** · Δsamp **+0.004** · **NO-GO**（pool） |

過除外で助け型 hard（例: `1b1eba53`, `4c2208f5`）まで落とすのが pool 割れの主因。

---

## 効く変化マトリクス（運用）

| 型に見えたら | やってよい | やるな |
|---|---|---|
| A（高 self_dev · 助け） | 弱い gated self_line | 全井 SOFT · strength≥0.15 |
| B（高 self_dev · 悪化） | **`tip_std_far/prox` 高なら除外**（下記） | ラベル oracle 除外を提出に使う |
| Easy sample | 何もしない | あらゆる SOFT |
| NW_N hard | ゲートに自然に入るなら可 | NW_N 専用 graft（F006/F009） |
| Low heel | heel をゲート条件に使う | CF 置換（F018） |
| Isolated | — | 近傍転写（F012） |

---

## A/B を分ける手がかり（追加探索 · 2026-07-25）

> 詳細: [`ab-separation-report.json`](../exp/work/wave14-well-archetypes/ab-separation-report.json)

**結論:** `self_dev>8` の中でも分けられる。本命は **遠MDの tip 変動 ÷ 近MDの tip 変動**。

| 手がかり | 意味 | A（助け） | B（悪化） | AUC | 提出可？ |
|---|---|---:|---:|---:|---|
| **`tip_std_far / tip_std_prox`** | 遠方が相対的にジグザグか | **0.31** | **1.60** | **0.978** | **可**（tip予測のみ） |
| `tip_std_far` | 遠MD tip の標準偏差 | 3.4 | 7.7 | 0.86 | 可 |
| `tip_std_prox` | 近MD tip の標準偏差 | 11.8 | 5.7 | 0.84 | 可（高いほど A） |
| `prox_line_r2` | 近傍の tip 直線性 | 0.71 | 0.43 | 0.75 | 可 |
| `tip_far_self_dev` | 線からの外れ（従来） | 16.3 | 11.5 | 0.62 | 可だが弱い |
| `tip_rmse` | tip 誤差（参考上限） | 12.2 | 6.7 | 0.78 | **不可**（ラベル必要） |

**物理的読み:**

- **A:** 近傍 tip が大きく動いている（または遠方が相対的に滑らか）→ 遠方が「線から外れたドリフト」で、線形自己線へ寄せると直る  
- **B:** 遠方 tip の方が相対的に荒い → 地質の形を tip が既に持っており、直線に潰すと悪化する  

**単閾値:** `tip_std_far_over_prox ≥ 0.842` → B 予測 · prec **0.94** · rec **1.0**（A/B 各15井の screen）

**T2 screen（portable ゲート上）:** 同閾値で除外すると除外井が **oracle k5 と一致**し、Δpool **+0.072** · Δsamp **+0.004**（portable より両方改善）· [`ab-separation-t2-screen.json`](../exp/work/wave14-well-archetypes/ab-separation-t2-screen.json)

> 注意: 閾値は A/B 30井でフィット。ネストCVではない。Public 後に CHK 化してから枠候補にする。

---

## 成果物

| ファイル | 内容 |
|---|---|
| `archetype-per-well.csv` | 80井 · 型 · 介入Δ |
| `chk180-report.json` | 多切り口要約 |
| `chk181-hurt-proxy-report.json` | 代理特徴スコア |
| `chk182-report.json` | 除外 graft NO-GO |
| `wave14-best.json` | **KEEP_WAVE13_PORTABLE** |

## 次

- **OPS-LB-89**（SUB-8/9 Public）
- 悪化代理の精密化は Public 継続時のみ · 特徴乱獲禁止
