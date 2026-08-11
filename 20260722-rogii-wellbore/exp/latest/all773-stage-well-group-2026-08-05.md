# all773 · 工程別 × 井戸グループ分析（773 だから見えた）

> **date:** 2026-08-05  
> **run:** `20260804-115307` · **提出禁止**  
> **親:** [`chk-final-t2-all773-cv-2026-08-05.md`](chk-final-t2-all773-cv-2026-08-05.md)  
> **数値:** [`all773-stage-group-summary.json`](../work/colab-final-t2/runs/20260804-115307/all773-stage-group-summary.json) ·  
> per-well tipdist [`all773-per-well-tipdist.csv`](../work/colab-final-t2/runs/20260804-115307/all773-per-well-tipdist.csv) ·  
> mid vs tip（y） [`all773-per-well-mid-vs-tip-y.csv`](../work/colab-final-t2/runs/20260804-115307/all773-per-well-mid-vs-tip-y.csv)  
> **≠** T2 residual 面 `041247`（mid 幾何が全く別）

---

## 0. 結論（先に）

| レンズ | 773 で得た本命 | 運用 |
|---|---|---|
| **誤差の偏り** | hard20（2.6% 井）が SSE の **≈20%** · top **100 井≈62% SSE** | dual 三点 + worst/Q4 必須 · pool 単独 GO 禁止 再確認 |
| **mid（本 face）** | label 上 **win25 / hurt21 / タイ727** · tipdist ほぼ 0 | **T2 の mid win77 を外挿しない** · tip⊕ 終了 |
| **S0 tip** | 非 hard 井 mean **≈8.0** · hard **≈26.8** · pool **10.84** | tip は「易井ロット」では既に強い。尾だけ別問題 |
| **S1 L** | tipdist L も **≈0.05 未満** 多数 · sign 一致≈1 | この dump の L は tip 近傍 · raw FINAL 禁止（F015） |
| **本命レバー** | tip⊕・本 mid では hard/SSE 尾が動かない | **L retrain dual + residual 041247** |

---

## 1. 井戸グループ別

### 1.1 hard20 vs 非 hard（753）

| 群 | n 井 | mean tip RMSE | tipdist mid（mean） | tipdist L | SSE 寄与（tip） |
|---|---:|---:|---:|---:|---:|
| **hard20** | 20 | **26.83** | **0.009** | 0.024 | **≈20.2%** |
| **その他** | 753 | **8.02** | 0.025 | 0.046 | ≈79.8% |
| 行数 | — | — | — | — | hard 行 ≈ **2.8%** のみ |

- hard は **井数 2.6% · 行 3% 弱 · SSE 2 割** → Private でも尾が順位を焼く構造。  
- tip⊕(B) の hard 平均改善 **≈ −0.008**（ほとんど無）。  
- T2 で言っていた「hard こそ mid/residual 主戦場」は **residual α 面**の話。**本 all773 mid では hard の tipdist が一番小さい**（ほぼ tip 固定）。

### 1.2 誤差パワー（773 でのみ見える）

近似 SSE = `well_rmse² × n_rows`（tip A）:

| 上位井バンド | SSE 累積シェア |
|---|---:|
| top **20** | **≈29%** |
| top **50** | **≈46%** |
| top **100** | **≈62%** |

**知見:** 773 に広げても「多数の易井の平均」が信頼残差を隠す。  
pool 10.84 は **半分近くが top50 の悪井任せ**。  
→ 学習・dual は **重量井 / hard / Q4 側**が必須。weight 系・812 WATCH は正当。

### 1.3 非 hard の tip RMSE 四分位（753 → 4×≈188）

| 帯 | mean tip | mean tipdist mid | tip⊕ B の Δmean |
|---|---:|---:|---:|
| Q1e（易） | 3.26 | 0.002 | ≈0 |
| Q2e | 5.29 | 0.015 | ≈0 |
| Q3e | 7.92 | 0.038 | −0.005 |
| **Q4e（非hard最悪帯）** | **15.64** | 0.044 | −0.016 |

**知見:** 非 hard 内部にも **3.3 → 15.6** の階梯。  
「hard20 以外＝全部楽」ではない。ただし tip⊕ はいずれの帯でも **ゲイン <0.02**。

### 1.4 mid vs tip on **label**（773 井フル）

| 結果 | n 井 | 比率 |
|---|---:|---:|
| mid **勝**（mid RMSE < tip） | **25** | 3.2% |
| mid **敗** | **21** | 2.7% |
| 実質同点 | **727** | **94%** |
| hard 内 mid 勝/敗 | 1 / 0 | — |

mean (RMSE_mid − RMSE_tip) ≈ **−0.005**（ノイズ級）

**vs T2 residual 物語（win77 / hurt3）:**

| 面 | win / hurt | 読み |
|---|---|---|
| T2 mid residual（041247 系） | **77 / 3** | mid 工程の存在意義 |
| **all773 tip-cv mid_before_hedge** | **25 / 21 / タイ727** | **tip の複製に近い中間面** |

→ これは **「mid が無効」ではなく「この dump の mid は residual 中間面ではない」**。  
工程 SSOT としては **mid 勝ち記録は T2 尺で保持** · all773 で書き換え禁止。

### 1.5 tipdist 分布（井）

| tipdist_mid 閾値 | 超える井の割合 |
|---|---:|
| > 0.05 | 5.3% |
| > 0.5 | 1.2% |
| > 1.0 | **0.26%**（2 井級） |

**知見:** 人口の **≈95% は tip≈mid**。ゲート注入の対象体積がそもそも無い。

### 1.6 既存タイプ（A–H）との対応（773）

| タイプ（handoff） | all773 での見え方 | 実験接続 |
|---|---|---|
| **A Attack hard** | SSE 20% 集中 · tip≈26.8 不動 | weight↑ 系 **維持**（761/804…） |
| **B Q4 MD** | 非 hard Q4e tip≈15.6 | 802/804/805 継続 · ただし **別 faces の residual** |
| **C resid>L** | 本 dump の L が tip 近傍なので residual 対照表は **041247** | 782 は residual 面で |
| **D 688 hurt** | all773 単体では未再測 · 仮説維持 | 789 protect 維持 |
| **E mid-hurt3** | 本 mid はほぼタイ集団 · T2 mid-hurt 定義は **T2 尺** | 809 は T2/residual リストで |
| **F L 強** | sign_agree tip·mid·L ≈ **1.0** → 方向一致だらけ · L 情報が薄い dump | F015 強化 |
| **G known/unk** | 未ラベル層別は別 pack · SSE 尾優先と同方向 | 804 known×Q4 |
| **H field** | 773 でも field Group 意義は残る（尾が局所クラスタしうる） | 785 |

---

## 2. 工程別

| 工程 | 773 full tip-cv face での事実 | 工程としての結論 |
|---|---|---|
| **S0 tip** | 非 hard mean **8.0** · pool **10.84** · hard **26.8** · SSE 尾 | **土台強い** · 触らない · hard 尺は別問題 |
| **S1 L（本 dump）** | tipdist L 小 · label FINAL 禁止 | **retrain 前の推論 L**（pretrained map）· 質改善は dual 用の別物 |
| **S2–S8** | 本 run は mid 手前 stop · プロセス材料は Drive ミラー | L1 前に触らない（従来どおり） |
| **S9 mid_before_hedge（本 dump）** | mid≈tip · win≈hurt · tip⊕ 死 | **residual mid と混同禁止** · 材料としての mid 勝ちは T2 で測る |
| **S9 residual α（別 faces）** | 本 CSV では未算出 | 頭は **666 / 041247** 維持 · α閉 F043 |
| **FINAL tip⊕（A/B/C/D）** | B≡C · Δpool −0.008 | **full CV では Final 根拠にしない** · Public tip⊕ 再提出も禁止維持 |

### 工程フロー（773 人口）

```text
[ tip S0 ] ──大部分の易井で RMSE 低──┐
                 hard20/SSE尾が高い │
                 ↓ tip⊕ mid は量が出ない
[ mid 本dump ] ≈ tip （94% 同点）  → ここで人口規模のブレークスルなし
[ residual 041247 ] mid 離れ & αL   → Trust 頭はここだけの世界
[ L retrain ] 尾 SSE を削る本命
```

---

## 3. 「773 だから分かった」知見（T2 80 では擬似的にしか見えない）

1. **誤差はほぼべき分布:** top100 井が SSE **6 割**。80 井サンプル（T2）はこの尾を **過剰に代表 or 欠落**しうる → trust 裁定は dual 三点必須。  
2. **pool 10.84 と hard 26.8 の乖離は「全部悪い」ではなく「2.6% が SSE 2 割」:** 改善は **weight / stop / protect** の方向性が正しい。  
3. **T2 「mid win77」は full tip-cv mid に複製できない:** 本 face は win25/hurt21。**工程論は面ごとに限定**。  
4. **tip は bulk では十分強い（非 hard mean 8）:** tip 再設計の ROI は低い · 締切局面で S0 触らないは合理。  
5. **learned の tipdist 小 + sign 一致≈1 → B≡C:** フル人口では「agree ゲート」が機能する差が無い。agree 系 Public 実験を full faces で再発明しない。  
6. **hard 群で tipdist が特に小さい:** hard 井は selector tip に張り付いたままで mid ブレンドが届かない → hard 突破は **L/resid 学習**以外に薄い。  
7. **非 hard 内にも Q4e mean 15.6 の「半 hard」層:** hard20 定義外の midtier が SSE に載る。weight を hard20 だけにすると取りこぼす（804 known×Q4 と整合）。  

---

## 4. 実験方針への落とし込み

| Do | Don't |
|---|---|
| L dual の go/nogo に **hard_mean + topSSE 井**を併記（**813**） | all773 tip⊕ を Final 候補に |
| residual 実験は **041247 尺**固定 | all773 mid で residual 井 win を再定義 |
| weight は hard+**Q4e**（**814**）· 易井 protect（**816**） | 「753 井すべて同じ weight」 |
| dual に hard unlock 診断（**815**） | pool だけ良で GO |
| tip 触らない · Public 枠2 farvol 固定 | tip 改修で pool 10.8 を更に攻める |

### 仮説 Δ（checklist と同期）

- **強化:** L dual · hard/Q4 weight · dual 三点  
- **閉鎖:** tip⊕ full · mid 外挿 · agree 再発明  
- **新規 CHK-813–816:** SSE WATCH · 半 hard · tip-stick · Q1e protect  
- 詳細: [`experiment-checklist.md#all773-cv仮説の変化`](../experiment-checklist.md#all773-cv仮説の変化) · [`handoff §4b`](../l-cv-hypothesis-handoff-2026-08-05.md)

---

## 5. 関連 SSOT

| 文書 | 役割 |
|---|---|
| 本ファイル | 工程×グループ＋773 固有知 |
| `chk-final-t2-all773-cv-2026-08-05.md` | A/B/C 総論 |
| `CURRENT-ALL773-FACES.md` | 面パス |
| `CURRENT-T2-FACES.md` | residual / T2 mid 物語 |
| `l-cv-hypothesis-handoff-2026-08-05.md` | タイプ A–H 設計 |
| `within-stage-comparisons.md` | 工程 Best グラフ |
