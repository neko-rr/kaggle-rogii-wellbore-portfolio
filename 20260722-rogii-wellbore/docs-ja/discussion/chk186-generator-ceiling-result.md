# CHK-186 結果 — tip lik-PF seed-oracle 天井（2026-07-25）

> 作業: [`exp/work/chk186-generator-ceiling/`](../../exp/work/chk186-generator-ceiling/)  
> 計画: [`chk186-generator-ceiling-plan.md`](chk186-generator-ceiling-plan.md)  
> 前提: CHK-185（tip+SOFT 選択残差 +0.15）

## 1 行結論

**分岐は mixed。** tip FINAL の pooled は seed-oracle に対し **+0.20 のみ**（8.33→8.13）。  
`frac_hit_le_4.5=46%` だが、易井では tip 後段が生シードを上回る。難井（hard20）は oracle でも 12.9 で **4.8 帯未達**。  
→ **CHK-188 は自動開始しない** · **CHK-189 は Park** · **OPS-FINAL2 優先**。

---

## 何を測ったか

| 項目 | 内容 |
|---|---|
| 候補源 | tip `_pf_lik_allseeds` · **128 seeds × 500 particles**（tip CFG 同） |
| FINAL | 既存 T2 `tip_train_preds.csv`（再提出なし） |
| 範囲 | T2 allowlist **80井**（hard20 + sample60） |
| 実行 | ローカル CPU/numba · ~15 min · **提出なし** |

---

## 数値（T2 80）

| 指標 | 値 |
|---:|---:|
| pooled tip FINAL | **8.330** |
| pooled seed-oracle | **8.132**（Δ **+0.198**） |
| pooled pf_scale_3（尤度重み） | **13.327** |
| `frac_hit_le_4.5` | **0.463**（37/80） |
| `frac_hit_le_6` | **0.613**（49/80） |
| `frac_gap_final ≥ 0.5` | **0.325**（26/80） |
| mean / median `gap_final` | **−0.06** / **−0.74** |

### 層別

| 層 | pooled FINAL | pooled oracle | hit≤4.5 | gap≥0.5 | 読み |
|---|---:|---:|---:|---:|---|
| **hard20** | 14.87 | **12.88** | 30% | 75% | シードに余地あり · でも oracle 12.9 ≫ 4.8 |
| **sample60** | **3.62** | 5.40 | 52% | 18% | tip 後段が生シードを支配的に上回る |

---

## Kaggler 解釈

1. **CHK-185 との整合**  
   SOFT 選択残差 +0.15 と同型で、**tip FINAL に対する PF シード oracle も pooled +0.20 級**。4.8 帯には届かない。

2. **PF 内部の選択ギャップは大きい**  
   `pf_scale_3` pooled 13.3 ≫ seed-oracle 8.1。尤度重みは「最良シード」から遠い。  
   ただし tip FINAL は後段（BH / gold / learned 等）でその大半を吸収済み。

3. **CHK-188（温度/重み微小）**  
   PF 段単体の仮説としては成立しうるが、**tip FINAL への pooled EV は ~0.2 が天井感**。  
   **自動では走らせない**（ユーザー明示時のみ · F013 大切替禁止）。

4. **CHK-189（粒子・gs・窓の大改修）**  
   hard20 oracle 12.9 のままでは 4.8 帯に届かない。**既定 Park**（締切近・EV低）。

5. **次にやるべきこと**  
   - **OPS-FINAL2**（枠1 tip Trust / 枠2 Public Best）  
   - 任意: CHK-187（中間面ディスク診断 · 提出昇格禁止）  
   - 任意: Wave-14 と結合して「易井は現状維持 / 難井は受容」

---

## 分岐表（実行しない）

| 186 の読み | 次 | 本結果 |
|---|---|---|
| hit高 · gap大 | CHK-188 | **否**（全体 mean_gap≈0 · pooled +0.20） |
| hit低 · gap小 | Park 189 · FINAL2 | hard20 はこちらに近い |
| 井型混在 | Wave-14 結合 | **採用** |

---

## 成果物

- [`chk186-report.json`](../../exp/work/chk186-generator-ceiling/chk186-report.json)
- [`chk186-per-well.csv`](../../exp/work/chk186-generator-ceiling/chk186-per-well.csv)
- `seed-dumps/{well}.npz`（best-seed · liks · pf_scale_3/8）
