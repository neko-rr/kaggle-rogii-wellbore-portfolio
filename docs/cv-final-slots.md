# CV 設計 · レーン · Final

日本語の要約。ポリシーの骨格は README の「CV・LB・Final」「CV を複数持った理由」と一致する。

## 単位（cv_unit）

| 項目 | 設定 |
|---|---|
| 分割の単位 | **井戸（well / group）** |
| 使わないもの | 行ランダム KFold を **採択の主根拠** にすること |
| 評価対象 | 提出と同じ評価区間の **RMSE**（pooled） |
| 公式 LB | Public ≈ **26%** · Private ≈ **74%**（最終順位） |

## 物差しの役割

| 物差し | 使う | 使わない |
|---|---|---|
| ローカル Trust CV（階層あり） | 本採用 · Final 枠1 | Public 微差の言い換え |
| Public LB | 壊れ検知 · 枠2 の意図 | Private の点推定 · Trust 全体の停止 |
| Private LB | 最終順位 · 終了後の枠検証 | 競技中の主オプティマイザ |
| 診断・オラクル・pack | 天井・弱点の観察 | Final / primary GO 単独 |

## CV 階層（速度 × 信頼）

主物差しの **型**（well-group · 評価区間 RMSE）は固定。変えるのは **井集合・seed・フル再実行か faces 上か**。

| 段階 | 目安 | コスト | 用途 |
|---|---|---|---|
| 速い CV | hard 少数井 · seed 少 | 低い | 壊れ検知 · 粗選別 · **回数を稼ぐ** |
| 本採用 CV | ≈80 井級 | 中〜高（数時間 GPU 帯もあり） | graft / 手法の採否 |
| Final 向け | 同集合 + multi-seed、または固定 faces 上の残差監査 | 重い or 軽い（種別を必ず書く） | 枠1 確定 · 改善が seed バンドを超えるか |
| 診断 | フル井門番 · 空間監査など | 限定 | 楽観検出。Final 単独にしない |

**フル tip 再実行** と **固定 faces 上の residual スイープ** は別物。後者で速度を稼ぎ、前者／本採用 CV で固める。

## レーン

| レーン | 主物差し | 停止条件の例 |
|---|---|---|
| primary（Trust） | Trust CV · dual 健全性 | acceptance 割れ · 形崩れ · 禁止仮説 |
| public | Public LB | Public 用実験の acceptance のみ |
| diagnostic | オラクル等 | Final に使わない |

## Final（N=2 · このコンペ）

| 枠 | 面 | Public | Private | 意図 |
|---|---|---:|---:|---|
| 1 | **666** residual α≈0.35 | 6.509 | **9.142** | Trust · Private 用 |
| 2 | **farvol** tip×thin | **6.190** | 9.453 | Public · 多様性 |

終了後: 枠1 の方が Private で良い。Public 頭の二重掲載を避けた。

## うまくいったこと / 反省

- レーン分離と CV 階層を締切下でも回した。  
- 残差の Public 悪化だけで Trust を捨てなかった。  
- dual 未達の L 再学習を Final に押し込まなかった。  
- 事後: **702 / 641** など Private がより良い残留がある（当時 Public や dual で載せにくかった）。プロセス品質を優先した結果でも、**Trust 面の事後入替余地**は残った。
