# GPU待ち — ローカル探索メモ（2026-08-03）

## いま GPU で回しているもの

| job | 状態 |
|---|---|
| **492b** tip-cv ess1.0 | RUNNING Ver3 |
| **496** 297-dual E2E | RUNNING Ver4 |
| **492** tip-cv ess1.2 | 枠待ち自動 push |

## ローカルでできたこと（済）

### CHK-501 — tip×472 勝ち分後段（tip-cv 代理）

[`../work/wave31-neural-proposal/out-501-tipcv-winparts/chk501-report.md`](../work/wave31-neural-proposal/out-501-tipcv-winparts/chk501-report.md)

| 候補 | Trust | メモ |
|---|---:|---|
| oracle 行選択 | **28.013** | 天井 |
| all_mid（F042） | **28.920** | 提出禁止 |
| **`lf_absd_ge_1`** | **28.920** | **最良デプロイ** ≈ all_mid |
| p297_all_mid | 28.960 | 易井契約と整合しやすい |
| lf_absd_ge_2 | 28.998 | 少し弱いが変更行少 |
| tip | 29.899 | 基準 |

**示唆:** tip-cv 物差しでは「\|mid−tip\|≥1 の行だけ mid」が **全面 mid とほぼ同じ Trust**。次の GPU 後は 492b 面に同じ政策を当てる。

### 既知（再確認）

- 491/494: mid は overlap 前まで残存 → FINAL≡tip（後段崩壊）
- 500 pack: hard20 mid勝ち 20/20 · 有力=297dual / all_mid

## 追加で済（501b）

- E2E 段マップ: FINAL≡tip · before_* は tip FINAL と rmse≈0.97 の差が残る  
- → 勝ち分注入点は **FINAL 直前**が本命

## CHK-502（済）

- **475 ≡ 472**（identical）→ 面差なし
- 最良デプロイ: **`signed_pos ∨ absd≥2` Trust 28.901** · `signed_pos` 28.908 · absd≥1 28.920
- corr(mid_better): absd≈0.25 · signed≈0.20 · **frac は負**（farほど mid勝ちしにくい）

## CHK-503（済）

- 491 before_* に政策適用（test · tip距離のみ）
- raw tip距離 **0.968** · `signed∨absd2` **0.907** · `signed_pos` **0.278**（削りすぎ）
- **FINAL≡tip** なので FINAL面への後付けは無意味 → **before_* を FINALに昇格する経路**が必要

## まだローカルでできる候補

1. well×stage 詳細距離
2. Discussion / LB 読み取り（提出なし）
3. 492b/496 harvest（GPU完了待ち）

## やらない（待ち時間でも）

- ブレンド提出 · mid 生 FINAL · Soft · 496/492b キャンセル
