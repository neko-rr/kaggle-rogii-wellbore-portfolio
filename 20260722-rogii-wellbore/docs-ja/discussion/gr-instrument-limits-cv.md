# GR 欠損・水平揺動 = 機器制限（コミュニティ知見）— CV 含意

> type: domain-intel  
> recorded: 2026-08-05  
> source: Twitter / Discussion 共有（参加者報告 · Host 系見解と同型）  
> 関連 Host: [727171 Working Note winners](Competition-Host_727171-working-note-winners.md)（**wiggle 無料 · 誤差は低周波**）  
> 自実測: [CHK-811 proxy](../../exp/work/out-t3-cpu-harvest/cpu-parallel-p0p1-20260805/chk811_proxy_summary.json)  
> **提出・α・Final2 方針は変えない**

---

## コミュニティ報告（要約）

| 現象 | 述べられた主因 |
|---|---|
| **GR 欠損が多い** | センサー／ツールの **機器制限・計測条件**（欠測を単に「整理ミス」と見ない） |
| **水平区間で GR が揺れ動く** | **掘削中・水平ツール**の制限に由来するばらつき（高周波の多くは地質信号ではない） |

Host 727171（*The Wiggle Is Free*）と整合: 高周波 wiggle は軌道/計測由来で **「無料」**、RMSE に効くのは **低周波トレンド（datum/slope）**。

---

## モデリング含意

| 含意 | 詳細 |
|---|---|
| 欠損の型 | 完全に MCAR と断じない。**区間・環境依存**がありうる → 「埋めれば必ず信号」ではない |
| 高周波合わせ | GR 窓・jitter・粒子 GR 再重みの **言い換え再開は低優先・多くは閉鎖済み** |
| residual / L | L や residual 誤差の主レバーは **mid との差分・MD 位置・井タイプ**（811: mean_GR ほぼ無相関） |
| 信頼できる側 | tip/typewell 整合の **形状・低周波** · residual `mid+α(L−mid)` の L 質 |

---

## 実験・CV に与える影響（判定）

| 変更するか | 内容 |
|---|---|
| **変えない** | Trust dual 尺子 · faces 041247 · α0.35 · Final2 · L1 weight 順（761→804…） |
| **強化（運用）** | GR を **本命特徴 / 本命 loss 補助**にしない · 811 は **\|L−mid\|+md_frac 1 群** |
| **強化（禁止）** | 「機器だから GR 入力強化で CV 一発改善」系の **新規主 CHK 禁止**（締切局面） |
| **説明強化** | tip/PF が hard/Q4 で崩れる一因として **GR ノイズ床**を参照可（仮説差し替えはしない） |

---

## 関連する既出 NO-GO / 閉鎖（再掲）

- GR 窓再重み · guided GR proposal · jitter lik · 後段 GR lik 等（Wave-24–28 付近）  
- F033–F035 観測尤度手改修  
- Host: 表層 GR matching 成功報告より **失敗と wiggle 分解**が評価された  

---

## 次アクション（任意 · low）

| ID | 内容 | 優先 |
|---|---|---|
| — | dual 報告に `mean_GR` / GR missing_frac を **診断列**で出すだけ（GO 条件にしない） | 任意 |
| 811 | soft 注入禁止 · GR 二次 · **変更なしで維持** | 維持 |

**一行:** 機器制限 GR = **なぜ GR 頼りが危ないかのドメイン根拠**。**L residual 本命は変わらない。**
