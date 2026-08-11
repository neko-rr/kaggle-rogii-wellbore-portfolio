# private 20th · public 3rd — RAFT-refined GR↔typewell matcher

**Topic ID:** 733845  
**URL:** https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733845  
**投稿日:** 2026/08/08 · **取得:** 2026/08/10 UTC  
**作者:** Yannan Chen · **順位:** Private **≈20th** · Public **≈3rd**  
**票:** 5 · **コメント:** 0  
**原文:** [`docs-en/solution/topic-733845.txt`](../../docs-en/solution/topic-733845.txt)

---

## 要約

- 主力 **grtx**: 1D GR↔typewell を **shared encoder → Transformer → cost volume → 1D-RAFT 反復 refine** する registration。
- **無相関3路の和**: grtx（単井 GR）· physics（GPU PF + residual net/tree）· geometric（ANCC kriging + GR-free transformer）。弱 leg でも **相関が低いと blend が効く**。
- Public は著者推定 **≈50 井、bootstrap σ≈0.9**。**Pub と Priv の相関は負**になりうる例を表で示す。選抜は **local CV 優先**で金帯維持。
- **per-well ゲート / selection wall** は CV よく見えて **LB 死**。固定 distance decay 重みに留めた。

---

## スコア向上にとって重要だったこと

| 要素 | 内容 |
|---|---|
| sinh 状態グリッド | ドリフト分布の中心を細かく、尾を ±115ft までカバー |
| RAFT 反復 | readout CE で cost を整え、反復で bulk 改善（hard には逆効果もありうる） |
| landing-aware anchor slide | known/eval 分割を epoch で滑らせて実効 n を増やす |
| synth 三重 loader | real aug · whip（尾を埋める）· layer shift · forward GR sim で整合 |
| 幾何 path の距離減衰 | 近傍密で geo を信じ、孤立井で 0 に近づける（D を ancc/geotx で分ける） |
| GPU PF knobs | 10 パラメータ1コードパスで expert 量産 · raw OOF ~9.8 vs 粗 PF ~14 |

## 効果が弱かった / 危険

- **同一情報の residual 強化**は相関係数高で blend ゼロ。  
- **見た目リアルな synthetic** が CV 悪化（見た目≠訓練有用）。  
- Pub 高スコアの単一 grtx を Final にすると **Priv が悪い**。

## 選抜哲学（必読）

- 複数 grtx で **CV と Public が反相関**（例: CV 6.4 / Pub 5.08 / Priv 7.30 vs CV 5.94 / Pub 5.44 / Priv 6.69）。  
- Final では「CV が良いが Pub が悪い大型 ensemble」を採択 → Private で正。  
- さらに CV 一択なら **もっと良かった**と著者。

---

## 自チームとの関係

- Public 偏り・σ 論は自チーム Rule と完全一致（Yannan は数で明示）。  
- 主戦場の grtx=registration は **自チームに無かった第一表現**。  
- 「無相関 weak leg を積む」は farvol/666 二レーンとは粒度が違うが同型（多様化）。

**最新コメント:** なし（2026/08/10）。
