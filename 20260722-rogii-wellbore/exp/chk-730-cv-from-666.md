# CHK-730–744 — 666 発展 · CV 物差し / residual 信頼（SSOT）

> updated: 2026-08-04 · **提出禁止** · residual Public 禁止（679）· farvol 枠2固定  
> 結果 harvest: [`work/colab-final-t2/out-730-cv-from-666/`](work/colab-final-t2/out-730-cv-from-666/report.md)

## 目的

Trust 本命 **666** を壊さず、**平均 T2 だけ**に寄せた過適合や、E2E と train tipdist の食い違いを検出し、Final2 / residual 方針を固定する。

## 実行状態（2026-08-04）

| ID | 状態 | 要約 |
|---|---|---|
| **730** | **GO_method · NOGO_auto_promote** | T2+hard20+worst10+tipdist罰 composite · train 上位=L/高α → **E2E 無い自動昇格禁止** · Trust=666 維持 |
| **731** | **GO_stable** | field leave-out top1 flip **0** · 順位安定 |
| **732** | **applied** | worst5/10 を score CSV 常備 · composite に worst10 半量 |
| **733** | **NOGO_nested_α · lock α0.35** | train α mode 0.50 が test で a0.35 より +0.85 悪化 |
| **734** | **applied** | well RMSE p90 cap 補助列 `t2_wellcap_p90` |
| **735** | **GO_map** | (1−λ)tip+λ·666 · λ↑=T2↓&tipdist↑ · budget 内は λ小 |
| **736** | **pending** | 井内 MD 区間 α（faces だけでは薄い · 次セッション） |
| **737** | **pending** | conf ゲート残差 |
| **738** | **dup_733** | 井 LOO α ≈ 733 結論で **α0.35 固定** · 追加格子低優先 |
| **739** | **pending** | 別 seed allowlist 順位（コスト） |
| **740–743** | **pending** | 幾何 cluster · 2α ens · domain 監査（低優先） |
| **744** | **GO_ops** | tipdist budget Pareto 表 · Trust 枠1=666 |
| **725** | **LOCK** | Final2: Public=farvol · Trust=666 · 材料 697 · 閉鎖帯明記 |

## 尺子の読み方（重要）

1. **主尺子 Trust:** T2 + **E2E tipdist**（671 dual）· sample3  
2. **train tipdist**（pred vs tip_selector）は 666 家系で **E2E と桁が違う**ことがある → 単独禁止  
3. **composite 上位 ≠ 提出候補**（L 生 FINAL = F015）  
4. **blendLm_*** は faces 上の L–mid 線形 proxy · **pipeline SP45 とは別** · 昇格禁止  

## 併走 harvest（同日）

| CHK | tipdist E2E | 判定 |
|---|---:|---|
| **697** w0.50 | 3.298 | GO_map 材料 |
| **697b** w0.45 | **3.705** | **NOGO** vs 0.50 |
| **711** g0.10 | **0.327** | GO_map_only · Trust 外 |
| **702/710 w050 resid** | ≥3.4 | **closure** |
| **666** | **1.985** | Trust 現行 |

## 次にまだ実験していない本命

| 優先 | 内容 | 要件 |
|---|---|---|
| **1** | **CHK-688–693** L 再学習・再 dump → residual 再格子 | pretrain-gate · GPU · ユーザー明示 |
| **2** | **CHK-704–706** 尤度 σ/重み（≠F033） | T3 · dual |
| **3** | **CHK-712** ridge/tree residual 材料 | T4→T3 |
| **4** | **CHK-695** soft β **E2E tipdist**（local T2 済） | soft 面入り E2E |
| **5** | **CHK-701** mid SSOT ログ整理 | 文書 |
| **6** | 736/737/739 区間・conf・seed | 時間があれば |

## やらない（閉鎖）

- residual Public · 生 L/mid/soft FINAL · soft→mid 620 · w050 固定α residual · farvol 差替 · F033–035

## 入口

- Active: [`experiment-checklist.md`](experiment-checklist.md)  
- 結果: [`out-730`](work/colab-final-t2/out-730-cv-from-666/report.md)  
- 候補生成: [`t2-candgen-learn-checklist`](t2-candgen-learn-checklist-2026-08-04.md)
