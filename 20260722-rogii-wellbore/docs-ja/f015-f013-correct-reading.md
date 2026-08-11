# F013 / F015 — 正しい読み（Agent 必須）

> updated: 2026-08-03 · SSOT for **全セッション**  
> 関連: [`exp/improvement-loop-failures.json`](../exp/improvement-loop-failures.json) · [`cascade §0`](../exp/work/wave31-selector-replace/pipeline-cascade-retest.md) · Rule `kaggle-f015-f013-mid-stage`

---

## 1 行

| ID | 禁止すること | **禁止しないこと** |
|---|---|---|
| **F013** | tip の**離散プロファイル切替**を枠1改善として再スイープ | SP45/learned を**中間材料・ゲート特徴**として使う |
| **F015** | learned / mpkg / before_* を **無加工で submission=FINAL** にする | tip 土台 + 行/井ゲートで一部だけ載せる再構成 · S1/S2 品質改善 |

**誤解（2026-08-03 訂正）:** 「S1–S2 を一切打つな」「中間面を触るな」は **過大一般化**。空欄に見えたのはこの誤解の結果であり、やり尽くしではない。

---

## F013（CHK-090/091/093）

- やったこと: `vp_conservative` ≡ tip · SP45 0.5/0.5 を tip-cv 面にすると壊滅 · bimodal ≡ tip  
- 禁止: 「tip プロファイルを別 preset に切り替える」言い換え  
- 許可: SP45 投影を **S2 工程の出力**として改善し、S3 混合やゲート入力に使う

## F015（SUB-4–7 · 追認 SUB-18 / F042）

- やったこと: gated_mpkg / pre-BH / mpkg-only を **提出ファイルそのもの**にした → Public 悪化〜壊滅  
- 禁止キーワードの核: `*-as-submission` · `*-promote` · `*-only` FINAL  
- 許可:  
  - S1/S2/S3… の **中間品質を上げる**  
  - その面を **ゲート決定・注入値**に使う（504/514 型）  
  - tip を既定 FINAL のまま、勝ち行/井だけ差し替え  
  - **合成面** `mid + α·(L−mid)`（α∈(0,1)）・`tip + α·(L−tip)` on gate — これは **F015 ではない**（α=1 の L 生のみが F015）。  
    Public で mid 全面寄りが壊れた実績は **F042**（別ID）。Trust T2 では 641 が GO · 詳細 [`exp/t2-climb-geo-hypotheses.md`](../exp/t2-climb-geo-hypotheses.md) §7

## Agent チェック（毎回）

1. その CHK は **submission.csv に中間面を丸ごと書いていないか？** → 書いていれば F015  
2. tip 離散プロファイルの言い換えだけか？ → F013  
3. どちらでもなければ **S1/S2 実験は許可**（ユーザー起動許可は別途）

## 不足レーン

詳細仮説: [`exp/s1-s2-hypothesis-backlog.md`](../exp/s1-s2-hypothesis-backlog.md)（CHK-519–570）· Active: [`exp/experiment-checklist.md`](../exp/experiment-checklist.md)
