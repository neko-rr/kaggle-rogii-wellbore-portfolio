# S0 残仮説 — 誤解防止付き（CHK-600–609）

> updated: 2026-08-03 · 別セッション実験用  
> Active 要約: [`experiment-checklist.md`](experiment-checklist.md)  
> 関連: [`f015-f013-correct-reading.md`](../docs-ja/f015-f013-correct-reading.md) · [`s0-gate-ban-correct-reading.md`](../docs-ja/s0-gate-ban-correct-reading.md) · F041/F023/F025/F036 は下表の **許可列** を必ず読む

---

## 必読（F015 と同じ型の誤解を防ぐ）

| 台帳 | **禁止すること** | **禁止しないこと（本バックログ）** |
|---|---|---|
| **F041** | Soft / soft-bank を **FINAL・提出面・選択加重の本体**にする | Soft残差・soft_diag を **ゲート特徴だけ**に使う |
| **F023** | soft RMSE 改善を **tip-cv採択根拠**にする | soft_diag / ESS / mode を **ゲート入力**にし、採択は tip⊕gate の Trust |
| **F025** | T∈{0.10–0.3} の **FINAL CSV≡T0.15 を再提出**する | 温度で差が出る **mid/pack面**をゲート材料・診断に使う |
| **F036** | 同じ tipバンクを **別スコアで tip soft差し替え**する | hard信号を **ゲート特徴**だけに使う |
| **F022** | tip-cv の **scalar weight 再スイープ** | （本レーン対象外 · 再開しない） |
| **F026–F040** | PF生成・spr・Newton·ESS-MCMC生成中の言い換え | **再開しない**（本バックログに載せない） |
| **F015/F042** | mid/Soft/learned の **生FINAL・全面mid提出** | tip土台＋ゲート部分注入のみ |

**共通契約（全 CHK-600–609）**

1. `submission.csv` に Soft / raw Pack / mid を丸ごと書かない  
2. acceptance の主指標は **tip⊕gate の Trust**（または tip-cv）· soft RMSE 単独でGOにしない  
3. Public 再提出はユーザー明示時のみ · Agentは submitしない  
4. 「S0を触るな」「Soft禁止」と短絡しない · 上表の許可列だけやる

---

## A. 未実施（スコアなし）

| ID | hypothesis | **やってよい** | **やってはいけない** | priority | acceptance | status |
|---|---|---|---|---|---|---|
| **CHK-600** | Soft残差（または soft−tip）を **行/井ゲート特徴**にすると、agree-only 26.629 を更新できる | tip⊕mid495 注入 · Softは特徴のみ · 提出なし | Soft FINAL · soft-bank選択 · Soft提出 | critical | Trust&lt;26.629 · anti-promote · ≠F041 | **rejected** · Softゲート+mid注入は不足 · **注入面=soft_diagが本命（618）** |
| **CHK-601** | **beam** ON/OFF の短T4が Pack/Trust代理を動かす（動かなければ表記削除） | 既存フラグ1回 · 短時間 · FINALなし | 長GPU連打 · BIN hold上げ（F024） | high | Δ報告1枚 | **blocked** · GPU要 |
| **CHK-602** | P-495の **peaky井**（ESS≈1 / top_w≈1）だけ tip固定すると sample/Trustが安定する | 井リスト+tipフォールバック · tip⊕gate | 448全面mass · ungated mid FINAL | high | Trust非悪化 · peaky井改善 | **rejected** |
| **CHK-603** | 450の副特徴（`top_soft_w` / mass_balance）をゲートに足すと peak系単独より良い | ゲートadd-onのみ | Soft面置換 · tip soft差し替え | medium | Trust比較表 | **done** · softW∩soft注入19.55 |

## B. 誤解でFINALだけ閉じた → ゲートとして再開

| ID | hypothesis | **やってよい** | **やってはいけない** | ban | priority | status |
|---|---|---|---|---|---|---|
| **CHK-604** | soft_diag / ESS / mode をゲート入力にすると tip⊕gate Trustが伸びる | ゲート入力 · 採択=Trust tip⊕gate | soft改善をtip-cv採択根拠（F023） | F023境界 | high | **done** · ESS+soft注入21.37 |
| **CHK-605** | LIK_TEMPで **midが動く**差をゲート材料にすると（FINALはT0.15のまま）勝ち行が取れる | mid面診断 · ゲート · tip FINAL固定 | T0.10–0.3 FINAL再提出（F025） | F025境界 | high | **done** · soft-mid合意 soft注入19.49 |
| **CHK-606** | hard専用信号（late_het等）を **ゲート特徴だけ**に使うと agreeを補完する | 特徴ablation · tip⊕inject | tipバンク soft差し替え（F036） | F036境界 | medium | **done** · absMid∩soft 21.62 |
| **CHK-607** | F041境界の Soft教師を蒸留せず、**ゲートlogitsだけ**に使うと F041を避けつつ信号が残る | ゲートlogits · 提出なし | Soft-Preserve ranker言い換え | F041境界 | medium | **done** · logits+mid NOGO · logits+soft=618系 |

## C. やらない（明示 · 載せないが Stop 用）

| 禁止 | 理由 |
|---|---|
| tip Soft / weight / PF多様性 / Newton / 学習proposal / 生成中ESS-MCMC の再スイープ | F022–F040 |
| Soft / soft-bank FINAL | F041 |
| raw495 / Soft 全面 FINAL | F015/F042 |
| T≤0.10 tip-cv 再開 | F025帯 · Δ微小 |

---

## 既存IDとの関係

| 旧 | 扱い |
|---|---|
| CHK-557 / 589 | **→600/607 に統合**（Activeの「Kaggle残 Soft」は本表へ） |
| CHK-588 | **→601** |
| tip Soft 再発明 | **禁止のまま** · 600系と混同しない |

---

## 実行順（別セッション）

1. **600** Soft→ゲート特徴（最優先・誤解修正の本丸）  
2. **602** peaky井 tip固定  
3. **604 / 605**（F023/F025の正しい読みで）  
4. **601** beam 短T4  
5. **603 / 606 / 607** 余力  

FINAL-T2 / 579 / 592–599 と **並行可**（GPUを奪わないT4優先）。
