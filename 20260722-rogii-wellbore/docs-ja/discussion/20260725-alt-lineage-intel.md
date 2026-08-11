# 別系統シグナル intel（2026-07-25 CLI refresh）

> **性質:** 収集・要約のみ。実験・提出なし。  
> **取得:** `kaggle-cli.ps1` topics list/show · leaderboard download  
> **注:** `fetch-solution-intel.py` はリポジトリに欠落のため、同等を手動 CLI で実施  
> **原文:** `docs-en/discussion/*-raw-20260725.md` · LB CSV `docs-en/leaderboard/publicleaderboard-2026-07-25.csv`  
> **方針の正:** [`comp-strategy.md`](../comp-strategy.md) · F台帳 `exp/improvement-loop-failures.json`

---

## Public LB（再取得 · 2026-07-25）

| Rank | Score | Team | メモ |
|---|---:|---|---|
| 1 | **4.859** | shu01 | 沈黙（質問にも未回答） |
| 2 | **4.902** | Yannan Chen | 微改善（旧4.905） |
| 3 | 5.108 | SaintLouis | |
| 4–5 | 5.237 / 5.265 | Rishikesh / Shrey | Shrey は Discussion 活発 |
| 6 | **5.283** | N&A&O&A | **新規浮上** |
| 8–10 | ≈5.44 | tremors / yu4u / **Tucker** | Tucker は CV 発言の主 |

チーム数 ≈ **5,679**。公式 writeup / “Top solution” スレは **まだ無し**（during-comp 想定どおり）。

---

## 「新しい別系統シグナル」だけ（F閉鎖と照合）

### ★ 本命として新しい／未掘り（Fに直接触れない）

| ID | シグナル | 出典 | 自チーム含意 |
|---|---|---|---|
| **S1** | 勝負は **generator（良い候補を出す）× scorer（選ぶ）**。NN追加より先に「真軌跡が候補に入るか」「スコアが TVT-RMSE と相関するか」を測れ | hengck23 [707613](../../docs-en/discussion/707613-raw-20260725.md) · [702474](../../docs-en/discussion/702474-raw-20260725.md) | tip は PF 家系。**候補天井の診断**は未実施 |
| **S2** | 候補集合の **oracle ≈4.5–… ft**（likpf/pf/beam/formation）。難しいのは選択。悪い negative で ranker を学ぶと漏洩 | Ochir [721549](../../docs-en/discussion/721549-raw-20260725.md) · Georgy [699853](../../docs-en/discussion/699853-raw-20260725.md) | 「4.8帯＝別面」ではなく **同じ候補プールの選択上手さ**の可能性 |
| **S3** | **~23% の井は良い候補が無い** → scorer をいくら良くしても天井 | Georgy 699853 | 難井は受容／別ルート。全井を無理埋めしない（Host・Tucker とも整合） |
| **S4** | 公開エンジン同士の誤差相関 **ρ≈0.89** → 重み再調整は <0.001。**同家系外の信号**が必要 | Georgy on [718670](../../docs-en/discussion/718670-raw-20260725.md) | tip×Best 同面（F016）と一致。**合成は「低相関面」が先** |
| **S5** | 2位は **提出2回で到達**した、という観測（Shrey）→ 公開フォーク乱打ではない系統の示唆 | [722236](../../docs-en/discussion/722236-raw-20260725.md) | 推測のみ。shu01 も低提出（17） |

### ○ 既知だが再確認（ほぼ F 閉鎖済み）

| シグナル | 出典 | 自チーム |
|---|---|---|
| 近傍&lt;150ft 形状コピー · 方位分割学習 | De DQ [726465](../../docs-en/discussion/726465-raw-20260725.md) | **F012 / F014** |
| 近傍無しでも pooled CV&lt;5（well単位・非tabular） | Tucker 726465 | tip 本体の質。後処理では届きにくい |
| 純物理単体 LB≈6.58 | Angus [717573](../../docs-en/discussion/717573-raw-20260725.md) | F004 近縁。詳細非公開 |
| tabular / 非tabular とも CV 5.x 可 | k256 / Tucker 717573 | 表現が天井 |
| 幾何 spline-kNN ≈LB 10.8（prior 候補） | Connor [711308](../../docs-en/discussion/711308-raw-20260725.md) | 単独では弱い · Final禁止寄り |
| 公開 dual-track の小技（blend 重み・gold overlay） | H. Ashida [722041](../../docs-en/discussion/722041-raw-20260725.md) | **同家系チューニング** · 別系統ではない |
| 素朴 DTW / window matcher | 697431 · 699853 | **F017** 等で壊滅寄り |

### ✕ 新シグナルにならないもの（今回）

- Host / Staff の新規解法開示なし
- shu01 / Yannan への粗質問 → **無回答**
- 726588 / 725086 / 721578 → 中身ほぼ空 or コメント無し
- 724669 悪井除外 → 結論なし

---

## 1 行結論（A）

**上位の「別系統」として Discussion が一番強く言っている未掘り穴は、近傍コピーでも方位分割でもなく、  
「候補は（一部井で）4.5台まで存在するのに、選ぶ側と・候補を出す側の天井を測っていない」こと（S1–S3）。**  
公開 Contact-Gated 沼の外に出るには、同家系の合成（S4）では足りない。

---

## 次（B）

探り CHK 1本の設計: [`chk185-candidate-ceiling-plan.md`](chk185-candidate-ceiling-plan.md)（**計画のみ · Active 未登録**）
