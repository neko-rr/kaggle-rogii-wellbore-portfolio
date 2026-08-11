# F041 / F023 / F025 / F036 — S0ゲート利用の正しい読み

> updated: 2026-08-03 · S0残仮説用  
> 実験キュー: [`../exp/s0-residual-hypotheses.md`](../exp/s0-residual-hypotheses.md)（CHK-600–609）  
> 類似: [`f015-f013-correct-reading.md`](f015-f013-correct-reading.md)

## 1 行

| ID | 禁止 | **禁止しない** |
|---|---|---|
| **F041** | SoftをFINAL/提出/soft-bank選択にする | Softをゲート特徴にする（600/607） |
| **F023** | soft改善をtip-cvの採択根拠にする | soft_diagをゲート入力にする（604） |
| **F025** | T0.10–0.3のFINAL≡T0.15再提出 | 温度で動くmidをゲート材料（605） |
| **F036** | tipバンクを別スコアでsoft差し替え | hard信号をゲート特徴（606） |

**誤解:** 「Soft禁止」「温度禁止」「S0完了」→ **過大一般化**。  
**正しい:** 提出面にしない · tip Soft再スイープ（F022–F040）は再開しない。
