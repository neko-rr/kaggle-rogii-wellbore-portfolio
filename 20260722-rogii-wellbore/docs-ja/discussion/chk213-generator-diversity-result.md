# CHK-213 結果 — 上流 generator 多様性 screen

> date: 2026-07-26 · **ローカル CPU** · **提出なし**  
> 作業: [`run_chk213_generator_diversity.py`](../../exp/work/wave20-upstream/run_chk213_generator_diversity.py)  
> 数値: [`chk213-report.json`](../../exp/work/wave20-upstream/chk213-report.json)  
> 物差し: hard20 **seed-oracle**（baseline 12.881 · combo 208=11.633）

## 1 行

**init_spr=12（128 seeds）が命中最良: oracle 10.38（Δ+2.50）。**  
既知 combo（9×256）を **+1.25 上回る**。tip 面への無断採用は禁止（209 教訓）。

## ランキング（hard20 seed-oracle）

| 設定 | oracle | vs base | vs combo | pf_s5@T0.5 |
|---|---:|---:|---:|---:|
| **init_spr=12** | **10.383** | **+2.498** | **勝** | 19.17 |
| init_spr9 × seeds384 | 11.346 | +1.535 | 勝 | 18.91 |
| mix 128@4.5+128@9 | 11.994 | +0.887 | 負 | 19.15 |
| init_spr=15 | 12.171 | +0.710 | 負 | 22.77 |
| init_spr=7.5 | 12.619 | +0.262 | 負 | 20.27 |
| mix 64+64 | 12.862 | +0.019 | 負 | 19.55 |
| init_spr=6 | 13.049 | −0.168 | 負 | 21.87 |

参考: baseline 12.881 · init_spr9×128（207）11.936 · combo 9×256（208）11.633

## Kaggler 解釈

1. **散布幅の最適は 9 より広い（≈12）**  
   6 は悪化、7.5 は弱い、12 がピーク、15 で戻る。単調ではない。

2. **seeds を増やすより spr を合わせる方が安い**  
   9×384（+1.53）＜ 12×128（+2.50）。コスト効率は spr。

3. **混合散布は「保険」止まり**  
   mix は combo 未満。単一の良い spr に勝てない。

4. **局所 pf_s5@T0.5 は oracle と別物**  
   spr12 の s5T0.5=19.17 は baseline 級。**命中↑ ≠ 尤度面↑**（209/205b と同型）。  
   → tip に載せるなら **selector-face tip-cv 必須**（次 CHK 候補）。

5. **残難井**  
   combo 後も `1b1eba53` oracle≈40。spr12 でも難。別仮説（井型・観測モデル）が要る。

## 判定

| 仮説 | 判定 |
|---|---|
| 多様性ノブで oracle ≥+0.30 | **PASS**（spr12 +2.50） |
| combo を超える命中 | **PASS**（spr12） |
| tip CFG に即採用 | **しない**（面未検証） |

## 次（提案）

| 優先 | 内容 |
|---|---|
| 1 | **CHK-214（承認後）**: tip-cv selector-face で `init_spr=12`（±T=0.5）を測る |
| 2 | 難井 `1b1eba53` 専用診断（副） |
| 3 | tip 本番への spr12 は 214 PASS 後のみ |

## Explicit Stop

- spr12 を tip CFG に無断で載せない  
- seeds384 だけの再スイープで時間を溶かさない（spr の方が効く）
