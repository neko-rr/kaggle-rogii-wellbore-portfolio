# Where does the top-team signal come from below the per-well line-oracle?

> Topic ID: **726465**  
> URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/726465  
> 投稿者: **stevenleehans**（883rd）  
> 投稿日時: **2026/07/15** UTC  
> 最新重要コメント: **2026/07/18** UTC（Tucker）· De DQ 全文はユーザー貼付で補完（2026/07/23）  
> 票: 12 · コメント: 19  
> 原文: `docs-en/discussion/726465-top-team-signal-below-line-oracle.md`  
> 投稿者順位は貼付時点

## 投稿者の診断（stevenleehans）

自スタック（Typewell clustering · IDW 転送 · particle filter · GBM）の well-group pooled CV **≈8.8**（773 wells）。

| Oracle | RMSE 目安 |
|---|---|
| best constant | 9.04 |
| best line | 6.70 |
| quadratic | 5.34 |
| smooth | 2.90 |

- 近傍 same-frame **&lt;150 ft**: RMSE ≈6.70（line-oracle）
- 近傍 **600 ft 以内なし**: RMSE ≈10.15（自 well 定数より悪い）
- 高周波 GR shape matching は真値から ~20 ft ズレでコスト最小（SNR&lt;1）→ dead 主張
- 上位 CV **5.7〜6.0** は line-oracle 超え（曲率）

## De DQ（2068th）· 2026/07/15 · [+10] — 全文反映

上位 CV ~5.7 の直感（複雑数学なし）:

| テーマ | 内容 |
|---|---|
| **信号の正体** | **近傍 well の TVT 軌跡のコピー＆ペースト**（full-curve transfer）。直線の line-oracle では取れない **stratigraphic wiggle（曲率）** を近傍から借りる。近ければ答えに近い |
| **GR matching 失敗理由** | GR がノイジーで細部マッチ不可。上位は完璧な GR 合わせに頼らず、**距離**を使う。近傍 **&lt;150 ft** なら岩は同一と仮定し、近傍 TVT を **自 well の開始点にシフト**して貼る。GR は粗い確認程度 |
| **「2グループ分割」** | **掘進方位（Azimuth）**。北西掘りと南東掘りで層を **逆順**に通過。全 well 一括学習は混乱。**方位で分割して別モデル**（または方位を明示特徴）→ しばしば大きな改善（「最も簡単な勝ち」） |
| **Particle Filter** | 多数の仮想 TVT パス（粒子）を進め、観測と合わないものを落とす。近傍整合に合うパスが残る |
| **次提出への助言** | 孤立 well で GR matching を無理しない（高誤差を受容）。**&lt;150 ft クラスタに注力**して形状コピー。**方位分割を先に** |

※ De DQ は近傍コピーを強調。一方 Tucker は **近傍無しでも pooled &lt;5** と主張 → 経路は複数ある。

## Tucker Arrants（8th）ほか

| 日時 UTC | 誰（順位） | 内容 |
|---|---|---|
| 2026/07/15 | **Tucker** [+8] | **近傍 well 無し**で単一モデル **pooled CV &lt;5 ft**。GR matching をかなり遠くまで伸ばせる |
| 2026/07/15–16 | Jeevan (25th) / GG Ayo | mean-per-well ≈5.2–5.4 でも **pooled 7+** — metric は pooled |
| 2026/07/16 | **Tucker** | **pooled**。**5-fold** best≈4.5 / worst≈5.3。outlier ~25 wells（&gt;12 ft）は特別扱いなし。**非 tabular**・サンプルは **well 全体** |
| 2026/07/16 | James Day (6th) | random group-by-well。地理層化なし。自 CV pooled 5.77（5-fold） |
| 2026/07/18 | **Tucker** | well-group CV · **test 時と同じ入力**（TVT_input マスク再現）。他にも 4.x 帯がいるはず |
| 2026/07/17 | victor | 近傍距離と line-oracle の対応が刺さった |

## スコア向上への示唆（優先順）

1. **掘進方位で分割／特徴化**（低コスト・De DQ「最も簡単」）
2. **近傍 &lt;150 ft** がある well は TVT プロファイル転送（シフト合わせ）を第一候補
3. **近傍無し経路**: Typewell/GR 整合の質（Tucker 経路）— 行単位 tabular ではない
4. 報告は必ず **pooled RMSE** · CV は well-group + 評価マスク再現
5. 孤立 well の高誤差を全部埋めようとしない（または不確実性で扱う）

## 効果が薄かった取り組み

- 単純高周波 GR shape matching
- master-frame 内 dip 転送 prior（RMSE 17.5）
- mean-per-well だけ見て pooled を見ない
- 全方位を一つのモデルに無理に混ぜる（De DQ）

## 矛盾・注意

- **近傍コピー（De DQ）** vs **近傍無し sub-5（Tucker）** — 両方あり得る。自チームは B1 で方位分割＋anchor、B2 で整合、近傍転送は別 CHK で検証
- De DQ / steven の順位は上位ではないが、方位・近傍の説明は物理的に妥当。Tucker/James の数値報告の信頼度が高い
