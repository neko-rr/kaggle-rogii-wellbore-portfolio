# Wave-10 手がかりスタック結果（2026-07-25）

> ローカル CPU 診断 · 提出なし · GPU なし  
> 作業: [`exp/work/chk140-clue-stack/`](../exp/work/chk140-clue-stack/)

## 1 行

**tip を壊すメタゲート（CF / heel直線）は全滅。** 有用な手がかりは「遠MDが難しい」「heel整合品質が効く」「近傍150ftはデータ全体でもほぼ無い」。スコア直結の新面は未発見。

## CHK 結果

| CHK | 結果 | 要点 |
|---|---|---|
| **140** | **done（手がかり）** | tip RMSE × heel_gr_tw_corr **−0.34** · 遠MD tertile 7.7→**18.3** · az_proxy −0.51 |
| **141** | **done（警告）** | 手元3井ラベルでは中間面 RMSE≈0.005 ≪ final 1.10 — **train-copy 過適合**。Public F015 と矛盾 → サンプル診断を提出根拠にしない |
| **142** | **done** | 最新公開は pfcfg / Frontier 再掲中心 · 新機構なし |
| **143** | **NO-GO · F018** | 低整合井→CF で悪化（25.4 vs 14.87） |
| **144** | **NO-GO · F019** | 遠MD heel直線で壊滅（609 vs 14.87） |
| **145** | **done** | hard20 の &lt;150ft 近傍 **0%** · 全train でも **1.7%** のみ → F012 強化 |

## 次に効きうる方向（未検証・要承認）

1. ~~tip 内部の遠MD不確実性~~ → **Wave-11 CHK-150 実施済** · 厳格 NO-GO · SOFT f33-s08 のみ · [`wave11`](wave11-far-md-uncertainty-2026-07-25.md)
2. **heel GR↔TW 相関を監視指標**に残し、新機構の採択ゲートにする（機構そのものは別）
3. 公開 pfcfg 乱獲は Stop 維持

## Final

枠1 tip Trust CV · 枠2 Public Best 維持。SUB-8 SOFT は診断（PENDING）。GPU/追加提出なし。

詳細続き: [`wave11-far-md-uncertainty-2026-07-25.md`](wave11-far-md-uncertainty-2026-07-25.md)
