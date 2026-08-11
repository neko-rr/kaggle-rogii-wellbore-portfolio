# CHK-234 結果 — selector BIN → force pf_scale_8_hold_0.2

> date: 2026-07-28 · GPU · `kazeneko77/tip-cv-gpu-sel-force-global-h20`

## 判定

**NO-GO.** tip-cv RMSE **30.223** · vs T0.15 **−0.324**（閾値 ≤29.599）。

## 含意

- hard20 の過半が使っていた **hold=0.05 は tip 面で負荷を持っていた**。
- 全 BIN を hold=0.2 に揃えると悪化。BIN routing 自体は残す。
- 次: code4/5 だけ hold 0.05→0.10 の弱い持ち上げ（234b）。

T4 audit: [`chk234-selector-audit.md`](chk234-selector-audit.md)
