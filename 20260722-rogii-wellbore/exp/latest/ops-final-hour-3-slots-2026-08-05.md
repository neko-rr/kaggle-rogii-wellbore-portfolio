# Final hour · 残り3枠（802/781 別セッション外）

> date: 2026-08-05 · **1h 作戦** · 提出はユーザー明示  
> 802 / 781 = **別セッション** · 本メモは **枠の使い方だけ**  
> Final2 LOCK: 枠1 **666** · 枠2 **farvol** · 自動差替なし

---

## 結論（1段）

**3 枠を「埋める」ことが目標ではない。**  
Final2 は既に OK_diverse。1 時間で起こせるのは **(A) 既存 COMPLETE Version の Submit** か **(B) 短時間 blend の Submit 起動** か **(C) 枠を残す** の3択。  
**residual（mid+αL）の新規は 1h 内で EV が最悪**（641/666/660/702/710 で Public 梯子は証明済み · F043）。

---

## 時刻制約の読み

| 仕事 | 1h 内に終わるか |
|---|---|
| Full tip E2E Save Version | **ほぼ不可**（通常 1h 超）· 締切前 Submit に間に合わない |
| **既に COMPLETE した Version を UI Submit** | **可（数分）** · 採点は 7h+ 後でも締切前 Submit でよい |
| tip×partner thin blend（face 再利用・軽 NB） | **条件付き可** · 既存 farvol/OPS 系と同型 |
| 802/781 residual E2E | 別セッション · **この枠計画に入れない**（GO 時だけ差し込み） |

採点待ちは問題ではない。**Submit ボタンを締切前に押せるか**が制約。

---

## 既知の地図（賭けないもの）

| 帯 | 状態 | 残り枠 |
|---|---|---|
| mid residual α（666/641/…） | Public 毒 · Trust only | **使わない** |
| tip residual α0.5（660） | 6.239 · 枠2未達 | **再提出禁止** |
| mid FINAL / w050（697） | GO_map · F015 境界 | **提出しない** |
| tip⊕ 強（711/618c 遠面） | Public 振れ or NO | **禁** |
| farvol α 中間 | グリッド済 | **追加 α 禁止** |
| row / HD 強 | 579/514 系 STOP | **禁** |

---

## 3 枠の推奨ポートフォリオ

### 原則

1. **枠1/枠2 は触らない**（666 × farvol）  
2. **3 枠はすべて “枠外診断 or 将来差替保険”** · Private 賭けは 666 のみ  
3. **他セッションの 781 が dual GO したら 1 枠だけ residual 用に譲る**  
4. 残り時間が 30 分切ったら **新規 Version 起動しない**（COMPLETE 済みだけ Submit）

### 枠割当（推奨）

| 枠 | 用途 | 条件 | 目的 |
|---|---|---|---|
| **S1（優先）** | **留保**（空 or 781 待機） | 781 dual+face が 45 分以内に来る見込みなら専用 | 唯一の Trust 上書き候補 |
| **S2** | **Public 薄ブレンド 未着弾 1 点** | COMPLETE Version がある、または **15–40 分**で終る blend NB | tip を壊さず farvol に近づくか **σ 外**かだけ見る |
| **S3** | **S2 と直交 or 空** | S2 が 40 分で Version 完走できなければ **空で締切** | 無理な 2 連打禁止 |

**「3 枠全部埋め」は非推奨。** 過去に residual/遠面で枠を溶かし、farvol は既に Best。

---

## S2 候補（Public · 1 時間帯）

優先順（既存 evidence）:

| 順 | 候補 | tipdist / 既知 | 判断 |
|---|---|---|---|
| **1** | **CHK-633 型** tip×**非 farvol** partner α**0.05**（OPS-C 面 or 515 面） | 612 screen 済 · **LB 未** | **唯一の情報価値** · farvol 再グリッドではない |
| **2** | 既 COMPLETE だが **Submit 未**の thin tip⊕（tipdist≲0.4 帯） | — | 既存 Version があれば S2 より先に押す |
| **×** | tip×farvol 新 α | グリッド済 | **禁止** |
| **×** | residual / Soft 遠面 / mid FINAL | F043·F041·F015 | **禁止** |

OPS-C 0.90 は既 **6.237**（farvol 次点級）。α0.05 は **別点**として意味がある。0.10 連打は 485 型で悪化しやすい。

---

## 1 時間タイムボックス

```text
T+0   Final2 UI 確認: 666 / farvol 選択済み
T+0–5  COMPLETE Version 一覧（Kaggle UI · 自 kernel · Submit 未）
        → あれば薄いものから最大 2 Submit（S2/S3）
T+5–10 「S2 を新規 Version で起こす必要があるか」判定
        → Yes なら thin blend 1 本のみ起動 · GPU
        → No なら枠は 781 待機 or 空
T+10–50 Version 監視 · 完走したら即 Submit · dual 不要（Public 診断）
T+50   新 Version 起動禁止
T+55   Final2 再確認のみ · 残枠は無理に埋ない
```

**Agent:** competitions submit しない · ユーザーが UI で押す。

---

## 781 / 802 差し込みルール（別セッション）

| イベント | 行動 |
|---|---|
| 781 dual **GO**（813/815） | **S1 1 枠のみ** residual E2E · α0.35 · faces 041247 · Final 差替は着弾後ユーザー判断 |
| 781 dual **NOGO** | Residual 提出しない · S1 は空 or S2 に回さない |
| 802 | **E2E 禁止** · 枠に使わない |

---

## 優秀 Kaggler の禁句（この1h）

- 「3 枠あるから何か residual を出す」  
- 「OOF が出たから Submit」（OOF 単独 GO 禁止）  
- 「farvol の α を微調整」  
- 「697 mid を FINAL にする」  
- 1h でフル tip E2E + dual + residual を完走しようとする

---

## 成功条件

| 良い | 悪い |
|---|---|
| Final2 無変更 + 不要枠未消費 | 締切直前 residual Public で 666 を落としてしまいそうな錯覚 |
| S2 が tip 近傍で「farvol に届かない」だけ確認 | mid FINAL / residual 梯子再実行 |
| 781 GO 時だけ 1 枠使う | 802 言い換え E2E |

---

## 今すぐユーザーがやること（Agent 実行待ちでない）

1. Kaggle UI: **Final 2 = 666 + farvol**  
2. Submissions から **COMPLETE ・未 Submit** がないか 3 分で確認  
3. 無ければ **S2 を 1 本だけ**（633 型 α0.05）起動可否を決め、無理なら **空**  
4. 781 は別タブ監視 · GO 出たらだけ residual E2E

**Agent への次指示例:**  
「S2 として tip×OPS-C α0.05 の提出 NB を 1 本作り、push まで」  
（明示がなければ作成・push・submit しない）
