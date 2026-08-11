# オフライン2h — 上流・中間面整理（2026-08-03）

> Agent ローカルのみ · Kaggle push/提出なし · CLI preflight FAIL（access denied）

---

## 現状確認

| 項目 | 状態 |
|---|---|
| **504 tip-cv** | harvest 済だが **IndentationError** で tip-cv 未完 · mid 面は取得済 |
| **504 NB** | audit セル indent **ローカル修正済（SYNTAX_OK）** · **再push 待ち（要ユーザー許可）** |
| **514 / 515** | COMPLETE · tipdist 0.727 / 2.121 · Public PENDING · Final 触らない |
| **本命ゲート** | H-D `fracSpos≥0.7 ∧ signed∨absd2` Trust **28.283**（行のみ 28.901） |

---

## 実施した実験

| CHK | 仮説 | 結果 |
|---|---|---|
| **517** | H-G（方位/MD）· H-B proxy が HD を更新 | **HOLD_hd_still_best** · 更新候補 **0** |
| **518** | 504 train mid 面を Trust 採点 | **EQUIV_507** · `before_branch_hedge` ≡ mid507（identical） |

詳細: [`517`](../work/wave31-neural-proposal/out-517-wellslice-hg/chk517-report.md) · [`518`](../work/wave31-neural-proposal/out-518-504face-trust/chk518-report.md)

---

## 井スライス（517）要点

- HD が row より良い井 **5** · 悪い井 **2** · 平坦 13
- 勝ちの本質: `frac_spos<0.7` の井で **mid を載せない（tip ロック）** → 7e721392 / f88ddb26 / fef8af96 等
- S 方位は win 3 / lose 0 だが、`HG_az_S_*` 単独は HD を超えない
- MD 遠方ゲート・meanAbsd 追加も HD 未達

---

## 上流・中間の含意

1. **親 mid（468/507）は正しい** — 504 harvest ≡ 507 mid
2. **ローカルで取れるゲート改善は打ち止め** — 次は tip-cv 完走（504）のみが情報量を増やす
3. H-B 本 Trust は 461 train mid が無い → tip-cv / E2E 側で測る
4. 後段: 504 `submission.csv` は before_hedge から **4.4%行**だけ微変（rmse 0.099）· HD は不変

---

## 起床時にやること（ユーザー）

1. **504 Ver3 push 許可** → indent 修正済 NB を push · tip-cv 完走 → 504b 対照
2. 514/515 Public 着弾確認（Agent は submit しない · Final 差替なし）
3. tip-cv が tip 29.899 を明確に抜いたら Final2 議論 · 否则 枠維持 + final-day 483
