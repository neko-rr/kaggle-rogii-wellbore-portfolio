# Wave-31 intel hunt — Discussion / 公開NB refresh（2026-07-31）· CHK-422

> date: 2026-07-31 · status: **T4 GO（抽象仮説 ≥2）**  
> CHK: **CHK-422** · Bet: **B13** · action_type: **T4**  
> 入力: 既存 `docs-en/discussion/*` · `docs-ja/discussion/20260730-refresh.md` · literature · others-notebook  
> **CLI download なし**（追加 fetch 不要 · 07-30 refresh 以降の新規トピックなし前提を維持）

---

## 1. Refresh 要約（vs 20260730）

| ソース | 所見 |
|---|---|
| [`20260730-refresh`](20260730-refresh.md) | 戦略変更なし · 新規トピックなし · Hierarch=LB座標探索は**監視のみ** |
| `docs-en/discussion/*-refresh-20260730-raw.md` | 票微変 · Looking-for-Team · Host 未回答維持 |
| 公開 NB | tip/Q0522/Hierarch 同家系が先頭帯 · **tip非クローンの完成品は依然稀** |
| [`non-tip-lineage-references`](../others-notebook/non-tip-lineage-references.md) | 借りる価値は CV物差し・物理天井・否定実験 |

**再掲禁止:** 20260730-refresh の「戦略変更なし」だけで CHK を閉じない → 以下に **手法×期待効果** の仮説を新規抽出。

---

## 2. 監視のみ（CHK 化しない）

| 項目 | 理由 |
|---|---|
| blacklions Final Hierarch · 井単位 LB offset/slope | Public 座標探索 · Final/Active 不可 |
| my0705 6.391 改題 | tip クローン |
| gs×1.3 再チューニング（728712） | tip に既組込 · Private 根拠にしない（Nicolai） |
| Looking-for-Team / 票だけ変動 | 知見なし |

---

## 3. 抽象仮説（≥2 · tip非クローン）

### H-W31-D1 — field-group 最悪スライスを Trust 門番に併記

| 項目 | 内容 |
|---|---|
| **手法** | Discussion 727570（souldrive）: well-CV に加え **位置 k-means field-CV** と **worst-field** を、新面（B/E/F/G/I）の門番レポートに必須併記する |
| **期待効果** | well-CV だけ良い面の Private 事故を早期に落とす · 既存 tip-cv/hard20 を置換せず **補完** |
| **移植先** | レーン B/E/F/G/I の本評価 CHK（416/426/430/434/442）の acceptance 追記候補 |
| **衝突** | ≠ Public 最適化 · ≠ Hierarch LB プローブ |
| **dup** | ≠ 20260730「戦略変更なし」の再掲のみ · 手順として未チェックリスト化 |

### H-W31-D2 — 多スケール GR↔TW 整合特徴 → 神経提案入力（絶対TVT木禁止）

| 項目 | 内容 |
|---|---|
| **手法** | mycarta / literature: **multi-scale NCC / 自己相関ラグ特徴**を、行 tabular 絶対TVT（F007/F010/F011）ではなく **CHK-432 提案ネットの入力窓特徴**に限定移植 |
| **期待効果** | F033 Newton・F034 線形αより安定な条件付き提案 · tip soft/FINAL の Trust CV 改善 |
| **移植先** | レーン **G（432–434）** · 必要なら B の尤度特徴 |
| **衝突** | 絶対TVTの NCC+木は **F007/F010/F011** · tipノブ禁止 |
| **dup** | Wave-28 H-A2 は別スタックGBDT（閉鎖寄り）· 本仮説は **提案ネット入力のみ**で差分 |

### H-W31-D3 — 明示マルチモード事後の中点を selector 出力に（soft温存なし）

| 項目 | 内容 |
|---|---|
| **手法** | literature P2 / 二峰 Discussion: selector を単一 MAP 強制から **モード中点（または質量加重中点）**へ置換（CHK-424 仕様と整合） |
| **期待効果** | soft→selector 崖（B10/B14）縮小 · RMSE 有利な hedge を **FINAL 定義内**で実現 |
| **移植先** | レーン **E（425–426）** · H の post unlock と併用可 |
| **衝突** | ≠ Soft-Preserve（F041）· ≠ before_hedge 提出（F015）· ≠ F031 lock/swap 天井 |
| **dup** | tip 既存 branch_hedge ノブ再スイープではない（定義置換） |

---

## 4. Acceptance（CHK-422）

| 項目 | 判定 |
|---|---|
| 抽象仮説 ≥2 | **PASS**（D1, D2, D3） |
| Hierarch/LB座標は監視のみ | **PASS**（§2） |
| 手法×期待効果形式 | **PASS** |
| ≠20260730-refresh 再掲のみ | **PASS**（新規仮説カード） |
| tip非クローン | **PASS** |

→ **T4 GO** · 次 **CHK-423**（dedupe · レーン移植 or 棄却）

---

## 5. CHK-423 への申し送り（未実施）

| 仮説 | 推奨 | 備考 |
|---|---|---|
| D1 | Active の本評価 acceptance に1行追記 | 新CHK不要でも可 |
| D2 | G 設計（432）入力欄に既反映可 · 423で正式リンク | F010衝突チェック |
| D3 | E（424済）の smoke 仕様に明示 | A と合流可 |

---

## 6. Explicit Stop

- Hierarch / LB 座標探索の Active 化  
- tip クローン NB の fork 提出のみ  
- kaggle competitions/kernels **download の無断実行**  
- soft / 中間面提出
