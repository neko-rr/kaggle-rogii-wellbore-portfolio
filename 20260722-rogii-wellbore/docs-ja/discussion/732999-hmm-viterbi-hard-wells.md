# HMM/Viterbi · 物理制約 · hard 井（symmys 共有）— 732999

> Topic ID: **732999**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/732999  
> 投稿者: **symmys**（初参加）  
> 投稿日時: **2026/08/05 14:11** UTC  
> 最新コメント: **symmys · 2026/08/05 15:58** UTC  
> 票/コメ（08-06）: **4 / 2**  
> 原文: `docs-en/discussion/732999-refresh-20260806-raw.md`  
> 関連: Geary 幾何 [`dz-dtvt-eda`](../others-notebook/dz-dtvt-eda-Ver-latest.md) · 文献 PF/Bayesian

## 要約（必読級の構造知見）

物理特徴のみの **HMM/Viterbi** で **CV≈LB≈8.0**。中央偏差は **3–4 ft** だが **少数の壊滅失敗**が pooled RMSE を押し上げる。

### 著者が得たデータ特性

1. **TVT 移動 ≈ Z 移動** · 地層面がほぼ不変だと `TVT = g − Z + datum` · 局所で **T' ≈ const − Z'** · 横方向の TVT 曲率 ≈ Z 曲率 · 勾配予測は区間内 **単一定数**寄り · **g' 一定の長さ 〜300 ft** と主張  
2. **typewell GR と水平 GR の完全一致は無意味**（TVT も完全一致しない）· 許容残差は **厚い尾の t 分布**  
3. **近傍 bedding は g' の良い prior**  
4. 容易井: GR emission 最良枝が真付近に乗りやすい · 図（CLI 欠落）で cubic-Z / Z*-Z が真に近い  
5. **深くなる / 難しい井**: TVT 勾配 prior が外れ · GR emission が偏差を打ち消しきらないと真路に引かれない  
6. 単一レバーは尽きた · **ensemble のみ**が残益 · hard の真 TVT には **決定的レバーが無い可能性**

### コメント

| 誰 | 日時 (UTC) | 要点 |
|---|---|---|
| **GG Ayo** | 2026/08/05 15:35 | 自分も HMM/Viterbi |
| **symmys** | 2026/08/05 15:58 | 公開 NB は PF+ML · **推論器の種類より物理制約が鍵** |

## スコア向上にとって

| 判断 | 内容 |
|---|---|
| **高（教育 · retro）** | 自チーム: GR 過信禁止 · residual/L · hard 井 · 中央良いのに pooled 悪い — **完全整合** |
| **高（構造）** | `dTVT≈−dZ` · heel/区間定数勾配 · 近傍 prior — 既存 Host/Connor 文脈と一致 |
| **中** | hard 井は ensemble trade-off のみ、という **悲観的収束** · L dual 全滅と同方向 |
| Final/Active | **締切済 · 新 CHK 不要** · retro の必須材料 |

## 効果が薄い

- 「HMM にする」こと自体の再実行（鍵は emission/prior コストの統計 · 図の欠落）  
- typewell GR 合わせ込み **単体**（著者自身が否定）
