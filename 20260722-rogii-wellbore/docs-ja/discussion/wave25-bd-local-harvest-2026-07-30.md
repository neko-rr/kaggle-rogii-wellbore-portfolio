# Wave-25 B/D local harvest — CHK-300–304 / 312–315（2026-07-30）

> tip soft pooled baseline hard20 ≈ **17.236** · acceptance ≥**+0.30** · 提出なし

## 結論

**観測再重み（300–304）・単一シード（312）・温度/区間/弱補正（313–315）はすべて NO-GO。**  
温度の oracle 上限でも Δ≈**+0.14** で acceptance 未達 → **選ぶ温度だけでは足りない**。

## 集計（best portable）

| CHK | best | Δ pooled | 判定 |
|---|---|---:|---|
| 300 遠MD重み | mix_pf_late… | **−7.48** | NO-GO |
| 301 anchor緩和 | anch_lam1 | +0.000 | NO-GO |
| 302 短長窓 | mix_pf_short… | **−7.48** | NO-GO |
| 303 スパイクマスク | mask_spike4 | **−12.4** | NO-GO |
| 304 TW局所スケール | mix_pf_twso… | **−7.85** | NO-GO |
| 312 単一シード | ess_gate | −0.17 | NO-GO |
| 313 井内温度 | T=0.12 | **+0.030** | NO-GO（閾値未満） |
| 314 ハイブリッド | （deepen） | ≦+0.03帯 | NO-GO |
| 315 形状保存 | （deepen） | ≦+0.03帯 | NO-GO |
| （診断）oracle per-well T | — | **+0.143** | 天井不足 |

## 含意

- 既存 tip 粒子上の尤度書き換えは **hard専用でも** tip soft を壊す（284/285 と同型、ゲートしてもダメ）
- 次の本命は **生成側**（306–310 GPU）かレーン縮小→OPS-FINAL2
- 成果物: `exp/work/wave25-hardwell-lane/chk300-314-report.json` · `chk313-315-deepen-report.json`

## Explicit Stop 候補

- hard-only でも **既存バンク上の late_het / spike-mask / TW-scale 再スコア**の言い換え再スイープ禁止（要 F036 追記判断）
