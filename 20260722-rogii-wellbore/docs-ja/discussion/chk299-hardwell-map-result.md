# CHK-299 結果 — 難井地図 + ノブ割当（2026-07-30）

> action: **T4** · 診断地図 · **提出なし**  
> 作業: [`run_chk299_hardwell_map.py`](../../exp/work/wave25-hardwell-lane/run_chk299_hardwell_map.py)  
> 地図: [`chk299-hardwell-map.csv`](../../exp/work/wave25-hardwell-lane/chk299-hardwell-map.csv) · 割当: [`chk299-knob-assignment.csv`](../../exp/work/wave25-hardwell-lane/chk299-knob-assignment.csv)

## 1行方針

**hard20 を MD×断絶×GR×方位で地図化し、型ごとに ≥1 ノブを割当（PASS）。** subtype は診断のみ（297で portable 否定）。

## 型カウント（hard20）

| type_key | n | primary CHK |
|---|---:|---|
| ranking_fail | 6 | CHK-312 |
| post_destroy | 5 | CHK-314 |
| ranking_fail+post | 4 | CHK-312 |
| soft_dilution(+post) | 3 | CHK-313 |
| generator_limit | 1 | CHK-306 |
| post_helps | 1 | CHK-300 |

地図セル: **19** · 型あたり仮説≥1: **PASS**

## 推奨次手（B/C 並列可）

1. **観測帯** CHK-300/301（ranking_fail / A_far）
2. **動力学/予算** CHK-306/308（generator_limit）
3. **選択/区間** CHK-312/313/314（279主因帯 · upstream PASS後に厚く）

いずれも **CHK-298 easy harness 必須** · 本番ゲートは **CHK-297 hard/easy** のみ。

## Explicit Stop

- 断絶 subtype を推論時スイッチにしない
- F026–F035 言い換えノブを地図に載せない
