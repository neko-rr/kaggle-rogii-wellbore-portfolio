# Private向け · Public代理仮説 — CHK-610–617

> updated: 2026-08-03  
> Active 要約: [`experiment-checklist.md`](experiment-checklist.md)  
> 定規: [`../docs-ja/cv-lb-private-relation.md`](../docs-ja/cv-lb-private-relation.md) · Goal: [`../docs-ja/comp-strategy.md`](../docs-ja/comp-strategy.md)

---

## 目的（必読）

| 層 | 役割 |
|---|---|
| **最終目標** | **Private RMSE 向上**（順位の正） |
| **Public** | 隠れテスト約26%の **検査機・代理信号**。Public↑は「全体が上がる可能性」の **仮説**であり保証ではない |
| **Trust CV** | 枠1防衛・手法採択の主物差し（Private未公開期間） |
| **やってはいけない** | Public単独最適化 · Public差≲0.08で採用確定 · Trust悪化を無視してPublicだけ追う |

**1行:** Publicを上げにいく実験は、**Privateが上がることを祈る代理**として実行する。採用・Final2選定は Trust＋多様性＋ユーザー判断。

**既存との差:** 592–599＝傾向 · 600–607＝S0ゲート化 · **本表＝514/515反証から出た「載せる井の作り方」と提出運用**。

**共通契約**

1. F015: tip⊕gate のみ · 生 mid/Pack FINAL 禁止  
2. farvol 枠2は触らない（599）· 中間αの farvol 再スイープ禁止  
3. Agent は `competitions submit` しない · 提出はユーザー明示時のみ  
4. 同時Pareto追加スイープ禁止（598）  
5. GO判定は「Public改善のみ」では確定しない · Trust非破壊＋Private希望の説明が要る

---

## A. 優先（おいしい3本）

| ID | hypothesis | **やってよい** | **やってはいけない** | priority | acceptance | action_type | status |
|---|---|---|---|---|---|---|---|
| **CHK-610** | **逆井ゲート:** Trustで勝つ井型（HD/fracSpos高 · 514毒型）を tip固定し、それ以外だけ薄注入すると、Public検査が壊れにくく **Privateも同方向の可能性**がある | 井リスト+tip固定 · tip⊕薄いgate · 提出はユーザー | HD全面注入の再提出 · Trust無視のPublic専用面 | high | Trust非悪化（≦agree帯）· Publicは診断のみ · tipclone非悪化 | T3 | **rejected** · Trust29.13（+2.5）· HDがTrust寄与 · [`report`](work/wave31-neural-proposal/out-610-613-reverse-safe/report.md) |
| **CHK-613** | **515安全仕様:** 行ゲート＋注入率上限（frac≲0.15）を495/agreeに移植すると、515≈tipの成功を保ちつつ Trustを少し載せられる（Private希望） | frac上限付き tip⊕gate · CPU可 | 注入率無制限 · 生Pack | high | Trust≦26.768帯 · tipdist過大にしない · Publicは着弾後判定 | T3 | **done** · 追加cap NOGO · **558b**がTEST frac0.127で既達 |
| **CHK-612** | **新パートナー薄ブレンド** α∈{0.05,0.10}のみ（farvol以外の別系統）が Public検査を動かし、Private多様性も増やす | OPS-C/別SUB等×tip · α固定2点 | farvol再提出 · α中間スイープ · 同時Pareto | high | Public診断（σ考慮）· Trust報告 · 枠2差替はユーザー | T2 | pending |

## B. ゲート精密化（Trust寄せ · Public反応観察）

| ID | hypothesis | **やってよい** | **やってはいけない** | priority | acceptance | action_type | status |
|---|---|---|---|---|---|---|---|
| **CHK-611** | **安定性ゲート:** tip複数seedで井間ブレ大の井は tip固定 · 安定井だけ mid注入すると、Publicノイズ耐性とPrivate安定が両立しやすい | seed差→井マスク · tip⊕gate | Soft FINAL · tip Soft再スイープ | medium | Trust非悪化 · ブレ井の tipclone↑ | T3 | pending |
| **CHK-616** | **Agree∧Stable:** agree ∩ tip安定井だけ注入すると、558bと591空帯の間を埋められる（Public反応を見てPrivate候補に残す） | 交差マスク · tip⊕gate · 提出なし既定 | 591の tipdist強制スイープ | medium | Trust∈(26.629,26.768] か非悪化 · tipdist報告 | T3 | pending |
| **CHK-617** | **悪化井ブラックリスト:** 514/HDでPublic毒になった井型を以降の全ゲートで tip固定すると、代理検査を壊さず Trust改善を積みやすい | 負の学習リスト · 全ゲート共通 | 「Public良井だけ」の未開示組成当て | medium | リスト1枚 · Trust比較 · Publicは任意診断 | T4→T3 | pending |

## C. 提出運用（枠を減らす · Private判断の質）

| ID | hypothesis | **やってよい** | **やってはいけない** | priority | acceptance | action_type | status |
|---|---|---|---|---|---|---|---|
| **CHK-615** | **579着弾分岐表:** 悪化→farvol固定 / ≈tip→613安全仕様 / 明確改善→row系を枠2候補、を機械化すると Private向けFinal2選定ミスが減る | 決定木1枚 · Stop更新 | 579再提出 · 悪化後のrow連打 | high | 分岐表を checklist Stop に反映 | T4 | pending |
| **CHK-614** | **同一CSVを意図的に2回提出**して自σを測ると、以降 Δ≲0.08 の「勝ち」を採用しなくなる（Private過信防止） | ユーザー明示 · 同一ファイル2回 · σ記録 | 枠逼迫時の連打 · 改善主張に使う | low | σ報告1枚 · 以降の採択ルール更新 | T4 | pending |

## D. やらない（新規に見えても却下）

| 一見仮説 | 却下理由 |
|---|---|
| Public切片の井当て · 定数オフセット | 割り当て未開示 · Private破壊リスク |
| tip Soft再発明でPublic甘さ | F022–F040 · 過適合定石 |
| Trust最良をそのまま枠2 | 514/485 反証済 |
| tipdistだけ中間合わせスイープ | 591 空集合 |

---

## 既存CHKとの関係

| 既存 | 本表 |
|---|---|
| 595/596/597 | 運用ルール → **615** が決定木化 · **610/613** が具体メカニズム |
| 558b/579 | 候補面 → **616** がその間 · **612** は別系統ブレンド |
| 600–607 | S0信号化 · Public代理レーンではない |
| 598/599 | 規律維持 · **612** は farvol以外のみ |

---

## 実行順

1. **579着弾** → 即 **615** 分岐適用  
2. **610** 逆井 · **613** 515安全仕様（CPU並行可）  
3. **612** 新パートナー α0.05/0.10（ユーザー提出判断）  
4. **611/616/617** 余力  
5. **614** は提出枠に余裕があるときだけ  

FINAL-T2 / 600系 / 592 と **並行可**（GPUを奪わないT4/T3優先）。
