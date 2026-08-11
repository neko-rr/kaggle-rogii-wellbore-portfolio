# Wave-17 結果 — 中間改善探索（2026-07-26）

> 作業: [`exp/work/wave17-mid-improve/`](../../exp/work/wave17-mid-improve/)  
> 制約: **F015** · F020 · 提出なし（採点待ち並行）  
> 物差し: [`intermediate-improvement-ledger`](intermediate-improvement-ledger-2026-07-26.md)

## 1 行

**次の上積みレバーは「新しい段」ではなく、既知の `tip_std_far/prox` による選択の確定。**  
入れ子遠MD（CHK-194）は NO-GO。two-stage は portable 再現可だが **farvol と井が重なるため重ねない**。

---

## 結果表

| ID | 仮説 | 判定 | 要点 |
|---|---|---|---|
| **CHK-192** | soft-helps を推論特徴で分離 | **GO** | `tip_std_far/prox` AUC **0.978**（低→helps）· farvol_keep prec1.0/rec0.93 |
| **CHK-193** | two-stage 半減を portable 代理 | **GO** | ゲート内 `tip_std` 上位k=5 が oracle 半減と **Jaccard 1.0** · T2 Δpool **+0.063** · Δsamp **+0.0005** |
| **CHK-193b** | farvol × two-stage 結合 | **GO（farvol単独）** | farvol-k0: **+0.072 / +0.004** · k3/k5 は pool 低下 → **重ねない** |
| **CHK-194** | 入れ子遠MD 弱い SOFT | **NO-GO** | 厳格で ref portable を samp 改善で超えず · 多くは Δpool&lt;0.05 |
| **CHK-195** | 段食い違いゲート | **skip** | 193/194 で EV 確定 · F015 境界の余力なし |
| **CHK-196** | ledger 固定 | **done** | 下記「次提出」 |

---

## 読み（Kaggler）

1. soft oracle 残りのうち、ラベル無しで取れるのはほぼ **farvol 除外（+0.07）** と **弱い two-stage（+0.06）**。  
2. 両者は同じ軸（`tip_std` 高＝SOFT 害）→ **どちらか一方**。farvol の方が pool/samp とも優位。  
3. 入れ子遠MD・段のいじりは期待値なし（187/194 一致）。  
4. SUB-10 が既に farvol 本採点中 → Wave-17 の新提出候補は **portable + tip_std two-stage（farvolなし）** のみ（SUB-12 との差分）。

---

## 次提出（承認後 · UTC 枠空き時）

| 優先 | 設定 | CV | 備考 |
|---|---|---|---|
| 1 | **待つ** SUB-10/11/12 Public | — | 先に枠比較 |
| 2 | portable + **tip_std hi-k5 two-stage** · f33-s05 · farvolなし | +0.063 / +0.0005 | CHK-193 · SUB-12 の上積み |
| — | farvol+two-stage | 劣後 | 193b で非推奨 |

---

## 成果物

- `chk192-report.json` · `chk192-feature-auc.csv`
- `chk193-report.json` · `chk193b-report.json`
- `chk194-report.json`
