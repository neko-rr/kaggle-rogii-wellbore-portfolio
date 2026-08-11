# S1 / S2 不足仮説バックログ — rogii-wellbore

> updated: 2026-08-03 · **pending digest 済** · [digest](work/wave31-neural-proposal/out-s1s2-pending-digest-20260803/report.md)  
> SSOT 読み: [`docs-ja/f015-f013-correct-reading.md`](../docs-ja/f015-f013-correct-reading.md)  
> Active 要約: [`experiment-checklist.md`](experiment-checklist.md)  
> **後続（L再学習·candgen 網羅）:** [`t2-candgen-learn-checklist-2026-08-04.md`](t2-candgen-learn-checklist-2026-08-04.md) **CHK-688–696**（ゲート524–570は済·再スイープしない）  
> 意図: learned（S1）· SP45（S2）を **やり尽くす**。生 FINAL 昇格はしない。

**共通制約（全 CHK）**

- `action_type` 既定: T4 screen → 良いものだけ T3 tip-cv / E2E  
- **提出禁止**（診断・tip-cv まで）。FINAL = tip 土台 + ゲート部分差し替えのみ可  
- Soft / 全面 mid FINAL / tip プロファイル言い換え = 禁止（F041 / F042 / F013）  
- acceptance 例: hard20 Trust &lt; 行ゲート 28.901、または H-D 28.283 を更新 · sample 非悪化

---

## A. 診断（信号が S1/S2 にどれだけあるか）

| ID | hypothesis | source | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|---|
| CHK-519 | S1 learned 面の tip距離・井別 RMSE マップを取ると、S9 ゲート材料になる勝ち井が特定できる | self · cascade | high | 井別表 + tipdist · 提出なし | 新規 · ≠F015昇格 | T4 | **done GO_screen** · [`s1s2`](work/wave31-neural-proposal/out-s1s2-t4-20260803/report.md) |
| CHK-520 | S2 SP45 面も同様に井別勝ち負けが取れ、learned と相関が低い（直交信号） | self | high | 相関・重複率を報告 | 新規 | T4 | **done GO_screen** · 同上 |
| CHK-521 | S0′: learned→sp45→w060→before_hedge の段差分を **現行 P-468** で再計測し、どこで勝ち分が消えるか更新できる | 501b 更新 | high | 段ごと tipdist 表 | 501b 再計測 | T4 | **GO** · mid残存 · [`521`](work/wave31-neural-proposal/out-521-583-s0prime/report.md) |
| CHK-522 | learned≡tip / SP45≡tip の井比率を出し、「触っても無駄な井」を除外リスト化できる | self | medium | 除外リスト JSON | 新規 | T4 | **NOGO** · ≡tip 0件 |
| CHK-523 | pack（456/495）と S1/S2 面の一致度を測り、上流強化が S1 に伝播しているか分かる | 495 · 456 | medium | pack vs learned 相関 | 新規 | T4 | **done GO_screen** · corr≈0.07 |

## B. ゲート特徴（提出面にしない）

| ID | hypothesis | source | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|---|
| CHK-524 | `sign(learned−tip)` または `abs(learned−tip)` を行ゲートに使うと、468-only 行ゲートより Trust が良い | 502 拡張 | high | Trust &lt; 28.901 | ≠生FINAL | T4 | **GO_screen** · signed∧row468 **28.246** · [`524-536`](work/wave31-neural-proposal/out-524-536-learned-trust/report.md) |
| CHK-525 | 井 `frac(learned&gt;tip)≥θ` ∧ row が H-D(468) を更新する | 512 拡張 | high | Trust &lt; 28.283 または LOO非悪化 | 512/513 | T4 | **GO_screen** · HD_learned∧row **28.272** · 同上 |
| CHK-526 | SP45 の fracSpos / meanAbsd が 468 と補完し、OR/AND 井ゲートで改善する | 512 | high | Trust 比較表 | 新規 | T4 | **NOGO** · sp45≡mid468 · [`526`](work/wave31-neural-proposal/out-526-sp45-or-and/report.md) |
| CHK-527 | H-E: ゲート=learned、注入=468 mid（または逆）が単親より良い | 512 H-E | high | Trust または tip-cv | 512 | T4 | **done** · mid-injectのみ有効 · learned注入F015 · [`524-536`](work/wave31-neural-proposal/out-524-536-learned-trust/report.md) |
| CHK-528 | 468∧learned 合意ゲート（符号一致）が H-B(461) より安定して Trust を下げる | 516 | medium | Trust &lt; row | 516 | T4 | **GO_screen** · agree∧row468 **28.062** · mid495へ転用で **26.655** · [`541b`](work/wave31-neural-proposal/out-541b-learned-gate-p495/report.md) |
| CHK-530 | learned と 468 の残差が逆符号の行は tip 固定にすると悪化井を減らせる | 517 | medium | HD 負け井の改善 | 517 | T4 | **GO_screen** · ≡agree∧row468 28.062 · [`524-536`](work/wave31-neural-proposal/out-524-536-learned-trust/report.md) |
| CHK-529 | `abs(SP45−tip)` を難易度プロキシにして、難井だけ mid 注入すると sample を守れる | wave14 | medium | sample 非悪化 + Trust↓ | 新規 | T4 | **NOGO** · sp45≡mid468 · [digest](work/wave31-neural-proposal/out-s1s2-pending-digest-20260803/report.md) |

## C. 工程内品質（S1/S2 そのものを良くする · FINAL は tip+gate）

| ID | hypothesis | source | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|---|
| CHK-531 | S3 混合比 w を 0.50–0.70 で再スイープ（親=現行 selector）すると before_hedge Trust 代理が動く | 462 | high | mid面 proxy 改善 | ≠F013 tip切替 | T4→T3 | **GO_screen** · w0.50 agree-inj495 26.667 · [digest](work/wave31-neural-proposal/out-s1s2-pending-digest-20260803/report.md) |
| CHK-532 | SP45 内部スケール/温度を変えず **混合前の SP45 品質**だけ改善するノブが1つ以上ある | intel | medium | sp45 vs tip tipdist 変化 + 後段非悪化 | F013外 | T4 | **DEAD** · sp45≡mid468 · 新SP45 GPU再生成が必要 |
| CHK-533 | learned_trajectory を TIP_CV で早期ダンプし、学習側ノブ（step/正則化相当の既存フラグ）が面を動かす | runbook | medium | 面が tip から有意に離れる | 新規 | T3 | **done GO** · TRAIN n=107478 tipdist≈22.96 · [`533-harvest`](work/wave31-neural-proposal/out-533-learned-dump-harvest/) |
| CHK-534 | S1 skip vs enable の before_hedge 差分が hard20 で有意なら、enable 経路を本線候補にする | cascade | high | ΔTrust または段差分 | 新規 | T3 | **GO_screen** · w0.5 vs 0.6 ΔagreeTrust=-0.041 · 同上 |
| CHK-535 | S2 単独投影を FINAL にせず、S3 入力品質指標（自己整合・接触）で選別できる | F013対照 | medium | 選別後 mid 改善 | 新規 | T4 | **NOGO** · quality-select は agree495 を抜けず · 同上 |

## D. 注入・再構成（F015 遵守の FINAL）

| ID | hypothesis | source | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|---|
| CHK-536 | FINAL=tip、ゲート行だけ `learned` 注入が 468 注入より Trust 良い | 504型 | high | Trust &lt; 28.901 | ≠生promote | T4 | **GO_train_opt only** · F015 FINAL禁止 · Trust~9.8は楽観 |
| CHK-537 | FINAL=tip、ゲート行だけ `SP45` 注入が有効 | 504型 | high | Trust &lt; 28.901 | ≠F013全面切替 | T4 | **NOGO** · ≡row468 |
| CHK-538 | FINAL=tip、ゲート行に `0.5*(468+learned)` 注入が単親より良い | 516 | medium | Trust 更新 | 516 | T4 | **GO_train_opt only** · F015 |
| CHK-539 | ゲート行のみ α(learned−tip) を載せる（α≤0.5）と薄ブレンドB0よりゲート整合が良い | 485対照 | medium | Trust↓ · tipdist診断 | ≠B0全面 | T4 | **GO_hard20 · T2は660へ** · F015誤解でstopしていた · [`539`](work/wave31-neural-proposal/out-539-alpha-residual/report.md) |
| CHK-540 | H-D(468) 井マスク × learned 行注入が H-D 単体を更新する | 513+524 | critical | Trust &lt; 28.283 | 本命対抗 | T4→T3 | mid≡HD468 · learned injectはF015楽観 |

## E. tip-cv / E2E（計測 · 提出禁止）

| ID | hypothesis | source | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|---|
| CHK-541 | 最良 S1/S2 ゲートを tip-cv hard20 で測ると tip 29.899 を抜く | 504並行 | high | tip-cv &lt; 29.899 | 504後 | T3 | **done GO_e2e** · Trust **26.655** · ≡local · tipdist 0.278 · **提出禁止** · [`541`](work/wave31-neural-proposal/out-541-e2e-analysis/report.md) |
| CHK-542 | S1/S2 ゲート FINAL の tip-cv が 514 相当（H-D 468）を上回る | 514 | high | tip-cv 比較 | 514後 | T3 | **GO_local_proxy** · Trust 26.655≪HD468 28.283 · tip-cv GPUは任意 · 同上 |
| CHK-543 | STOP_AFTER_S2 / S3 の成果物だけ保存する診断 NB が再現可能 | runbook | low | 成果物パス固定 | 新規 | T3 | pending |
| CHK-544 | anti-promote 検査: submission が tip と同一行率≥閾値（ゲート行以外）を機械検証できる | F015防衛 | high | validator スクリプト | 新規 | T4 | **done GO** · 541/579 PASS · [`544`](work/wave31-neural-proposal/out-544-anti-promote/report.md) |
| CHK-545 | Public 診断は tip-cv PASS 後のみ · 生 S1/S2 FINAL 候補はキューに載せない | ops | high | チェックリスト規律 | F015 | T4 | **GO_process** · 規律を checklist に固定 · 同上 |

## F. 明示的にやらない（禁止のまま）

| 禁止 | 理由 |
|---|---|
| learned / SP45 / mpkg / before_* を **そのまま submission** | **F015** · SUB-4–7 · SUB-18 |
| tip 離散プロファイル切替の言い換え | **F013** |
| 全面 mid≠tip FINAL | **F042** |
| Soft-Preserve 提出 | **F041** |

## G. 井・層・方位スライス（ゲート材料の厚み）

| ID | hypothesis | source | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|---|
| CHK-546 | learned 勝ち井が NW_N / 遠MD に偏るかで、方位×MD 条件付きゲートが要るか分かる | F-052 | high | スライス表 | 517≠H-G再スイープ | T4 | **GO_screen** · agree 9勝3敗 · [`546`](work/wave31-neural-proposal/out-546-agree-wellslice/report.md) |
| CHK-547 | SP45 勝ち井が learned 勝ち井と交差少ない井だけ OR ゲートすると sample を守れる | 520 | high | 交差率 + Trust | 526 | T4 | **NOGO** · sp45≡mid468 · 同上 |
| CHK-548 | heel 近傍だけ tip 固定・遠方だけ S1/S2 注入が Trust を下げる | wave1 | medium | MD帯別 Trust | 新規 | T4 | **NOGO** · heel tip-lock 悪化 · 同上 |
| CHK-549 | TVT 既知ゾーン内で learned が tip を超える率を測り、未知帯ゲートの事前確率にする | dataset | medium | 既知帯勝率 | 新規 | T4 | **GO_screen** · frac(L>tip)=0.642 · MD quartile · 同上 |
| CHK-550 | 井長/点数で層別し、短井は tip 固定・長井だけ mid 注入が安定する | 517 | medium | 層別 Trust | 新規 | T4 | **NOGO** · 長井層別 悪化 · 同上 |
| CHK-551 | bimodal 疑い井だけ S2 材料を捨て tip 固定にすると悪化井が減る | F013対照 | medium | 悪化井数↓ | ≠プロファイル切替 | T4 | **NOGO** · hard20 に bimodal 無し · 同上 |

## H. 特徴・閾値・合意（行ゲート拡張）

| ID | hypothesis | source | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|---|
| CHK-552 | `abs(learned−468)` 大の行は不確実として tip 固定が良い | 530拡張 | high | Trust / 悪化井 | 530 | T4 | **NOGO** · [`552-554`](work/wave31-neural-proposal/out-552-554-gate-harden/report.md) |
| CHK-553 | learned・SP45・468 の多数決符号が tip と違う行だけ注入が効く | 528 | high | Trust &lt; row | 528 | T4 | **NOGO** · 同上（maj∧agree≡agree∧row） |
| CHK-554 | 行ゲートに `rank(|learned−tip|)` 上位 q% だけ注入すると q スイープで最適がある | 502 | high | q×Trust 表 | 502 | T4 | **NOGO** · 同上 |
| CHK-555 | 井ゲート θ を fracSpos 以外（meanAbsd / medianAbsd）にすると H-D を更新する | 512 | medium | Trust &lt; 28.283 | 512 | T4 | **NOGO** · meanAbsd悪化 · [`558-555`](work/wave31-neural-proposal/out-558-555-pack-absd/report.md) |
| CHK-556 | 行ゲートと井ゲートの **不一致行**を tip に戻すと sample が守れる | 513 | medium | sample + Trust | 新規 | T4 | **NOGO** · XOR tip-lock 悪化 · 同上 |
| CHK-557 | Soft 教師残差を **ゲート特徴のみ**に使い提出面に載せないと F041 を避けつつ信号が取れる | F041境界 | medium | 特徴寄与表 · 提出なし | ≠Soft提出 | T4 | pending |
| CHK-558 | pack 残差と learned 残差の積が正の行だけ注入が効く | 523 | medium | Trust | 523 | T4 | **GO_screen→E2E** · agree-only Trust **26.629** · **558b GO_e2e** · [`558b`](work/wave31-neural-proposal/out-558b-e2e-analysis/report.md) |

## I. S1/S2 工程品質（FINALは tip+gate）

| ID | hypothesis | source | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|---|
| CHK-559 | S1 enable 時の before_hedge が tip から離れる井だけ後段に渡す選別が有効 | 534 | high | 選別後 proxy | 534 | T4 | **NOGO** · top-k井選別 Trust悪化 · [`explore`](work/wave31-neural-proposal/out-kaggler-explore-20260803/report.md) |
| CHK-560 | S2 出力の自己整合スコアで低品質井を tip にフォールバックできる | 535 | high | mid proxy | 535 | T4 | pending（sp45≡468なら低優先） |
| CHK-561 | S3 w を井別に（learned信頼度で）変えると固定 w より良い | 531 | medium | Trust proxy | ≠F013 | T4 | **GO_screen_F015** · ≡fixed w0.50 · Trust楽観 · FINAL禁止 · [`explore`](work/wave31-neural-proposal/out-kaggler-explore-20260803/report.md) |
| CHK-562 | STOP_AFTER_S1 と STOP_AFTER_S2 の面を同一井で差分し、S2 が壊す井リストが取れる | 543 | high | 壊し井リスト | 543 | T4 | pending |
| CHK-563 | learned 面の平滑（MD 窓）後にゲートするとノイズ注入が減る | intel | medium | Trust | 新規 | T4 | **NOGO** · MD平滑ゲート 悪化 · 同上 |
| CHK-564 | SP45 を tip 方向へ clip（|Δ|≤κ）してからゲート材料にすると Public 危険が下がる | F015防衛 | medium | tipdist↓ + Trust | ≠全面切替 | T4 | **NOGO** · sp45≡mid468 · 同上 |

## J. 注入・ブレンド境界（F015 遵守）

| ID | hypothesis | source | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|---|
| CHK-565 | ゲート行に `α·learned+(1−α)·468`（α∈{0.25,0.5,0.75}）が単親より良い | 538 | high | Trust 表 | 538 | T4 | **GO_screen** · blendはF015楽観 · mid-ctrl≡agree · 同上 |
| CHK-566 | ゲート行のみ learned、非ゲートは tip（現行） vs 非ゲートも 468 薄混ぜの対照 | 485対照 | medium | Trust·tipdist | ≠B0全面 | T4 | **GO_screen** · elseTip learned楽観 / else468は tip-FINAL破壊 · 同上 |
| CHK-567 | 井ゲート ON の井だけ行内全点注入、OFF 井は tip 固定が H-D と同値か上回る | 540 | high | Trust ≤ 28.283 | 540 | T4 | **NOGO** · wellON-allrows は HD468 未更新 · 同上 |
| CHK-568 | 2段ゲート: 井で候補 → 行で精錬 が 1段より悪化井を減らす | 513 | high | 悪化井↓ | 新規 | T4 | **NOGO** · 2段ゲート 悪化 · 同上 |

## K. 負対照・規律（やり過ぎ防止）

| ID | hypothesis | source | priority | acceptance | dup-check | action_type | status |
|---|---|---|---|---|---|---|---|
| CHK-569 | **負対照:** learned 全面 FINAL の Trust/tipdist を再掲し F015 を数値で固定する | F015 | high | Public級悪化の再現メモ | 提出禁止 | T4 | **GO_local** · NEG_CTRL tipdist≈23 Public毒 · 同上 |
| CHK-570 | anti-promote CI: 提出 CSV と tip の一致率を閾値未満なら FAIL（544 実装） | 544 | critical | スクリプト PASS/FAIL | 544 | T4 | **GO_local** · anti-promote CI PASS · 同上 |

---

## 実行順（推奨）

1. **519–523** 診断（CPU/ローカル可）  
2. **524–530 · 546–558** ゲート特徴 screen  
3. **536–540 · 565–568** tip⊕注入 Trust  
4. **531–535 · 559–564** 工程ノブ（重い）  
5. **541–542** tip-cv（GPU · ユーザー許可）  
6. **544 / 570** を常設ゲート化 · **569** は文書固定のみ  

> 504/514/515 待ちと **並行して T4 から着手可**（GPU 枠を奪わないもの優先）。  
> 合計仮説: **CHK-519–570**（52件 · 禁止レーン F 除く）。
