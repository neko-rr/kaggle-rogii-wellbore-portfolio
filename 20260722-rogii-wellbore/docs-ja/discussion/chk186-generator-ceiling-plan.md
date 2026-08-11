# Wave-16 — tip generator 天井診断（仮説設計 · 2026-07-25）

> 目的: CHK-185（SOFT 集合）で分かった **generator 不足** を、tip 本体の **PF/粒子・中間候補** まで分解する  
> 根拠: hengck23（707613）· Ochir（721549）· CHK-185 · tip `lik_pf` / `_pf_lik_allseeds`  
> 状態: **CHK-186 実行済（mixed）** · [`chk186-result`](chk186-generator-ceiling-result.md) · 188/189 は自動開始しない  
> F禁止: 近傍コピー · 方位分割学習 · NCC/DTW 新面 · 中間面の提出昇格（F015）

---

## 分析（優秀な Kaggler 読み）

CHK-185 は「tip + SOFT」の机だけを見た。  
tip の中ではすでに次が動いている。

| tip 内の「机」 | 中身 | CHK-185 で見たか |
|---|---|---|
| **lik-PF 128-seed** | `_pf_lik_allseeds` → `(n_seeds, n)` 軌跡 + likelihood | **未計測** |
| **パイプライン段** | pre-mpkg · pre-BH · FINAL ·（任意）gold/VP 候補 | 提出としては F015 · **診断 oracle は未計測** |
| SOFT / farvol | 最終面の後処理 | 計測済 · 天井 +0.15 |

Discussion の「候補 oracle≈4.5」は、だいたい **PF 系の豊かな候補**を指している可能性が高い。  
だから次の切り分けは1本:

```text
真値に近い軌跡が tip の PF シード集合に入っているか？
  YES → scorer（尤度重み・hedge）がボトルネック → 選択側の微小仮説へ
  NO  → generator（粒子・ノイズ・窓）不足 → 締切近は Final2 / 大改修は高コスト
```

---

## 仮説ツリー（checklist に載せるもの）

| ID | 層 | 仮説（1行） | 期待される分岐 |
|---|---|---|---|
| **CHK-186** | T4 診断 | tip lik-PF の **シード軌跡集合**に、真値に近い候補が入っている井が一定割合ある | hit高→選択側 · hit低→generator不足確定 |
| **CHK-187** | T4 診断 | tip **パイプライン中間面**の oracle が FINAL より有意に良い | 段選択の余地 · ただし提出昇格は F015 禁止のまま |
| **CHK-188** | T4→条件付き | 186 が「hit高・選択失敗」なら、**尤度温度/重みの微小変更**で seed-oracle に近づく | PASS時のみ T0 · F013 のプロファイル乱切替とは別 |
| **CHK-189** | Stop/Park | hit低なら「粒子数・gs・窓の大改修で 4.8」を狙う | **既定は Park** · 締切近・EV低 · 明示承認時のみ |

やらない（仮説にしない）: F011–F020 の言い換え · 学習 ranker 新規 · 近傍/方位の再掘り。

---

## メトリクス（CHK-186 想定）

井ごと（T2 allowlist 推奨）:

- `rmse_final` … tip 最終  
- `rmse_seed_oracle` … 128-seed（または CV 用シード数）軌跡の最小 RMSE  
- `gap = rmse_final − rmse_seed_oracle`  
- `hit_le_X` … `rmse_seed_oracle ≤ X`（X∈{6, 5, 4.5}）  

全体:

- `frac_hit_le_4_5` / `frac_hit_le_6`  
- `pooled_final` vs `pooled_seed_oracle`  
- `frac_gap_ge_0_5`  

解釈:

| パターン | 読み | 次 |
|---|---|---|
| hit_le_4.5 が高い · gap 大 | **選択がボトルネック**（PF は当たっている） | CHK-188 |
| hit_le_6 が低い · gap 小 | **generator 不足確定** | Final2 · CHK-189 は原則 Park |
| 中間 | 井型で分岐（Wave-14 と結合可） | 難井は受容 · 易井のみ選択 |

---

## 実装メモ（実行時）

- tip NB の `lik_pf` / `_pf_lik_allseeds` が候補源（新規モデル不要）  
- 診断用に seed 軌跡を train 評価区間へ dump · **提出に使わない**  
- GPU: tip 再推論が必要なら **承認後のみ** · 可能なら hard20 / T2 allowlist に限定  
- 中間面 CSV は既存 `submission_before_*` があればディスク優先（CHK-187）
