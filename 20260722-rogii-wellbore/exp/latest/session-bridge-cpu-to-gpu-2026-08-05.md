# セッション橋渡し — CPU 結果 → GPU セッション（2026-08-05）

> **用途:** GPU を別 Agent / 別チャットが回すときの **必読 1 枚**  
> **正の順番:** 本ファイル → [`exp-index.md`](../exp-index.md) → [`experiment-checklist.md`](../experiment-checklist.md) → [`l-improvement-laws-2026-08-05.md`](l-improvement-laws-2026-08-05.md)  
> **提出禁止** · residual α 閉（F043）· **F044** weight L mid-collapse · F015

---

## GPU 割当（2026-08-05 確定）

| レーン | 役割 |
|---|---|
| **Kaggle GPU** | **781 residual-path** train · COMPLETE 後は空ける |
| **Colab** | 802 済 NOGO · 784 等は本後工程外 · weight 禁止 |
| **local dual** | 781 COMPLETE 後必須 · [post-781](ops-chk781-post-pipeline-2026-08-05.md) |

## 781 後工程（必読）

**SSOT:** [`ops-chk781-post-pipeline-2026-08-05.md`](ops-chk781-post-pipeline-2026-08-05.md)

```text
harvest → dual → GO: E2E1 · NOGO: STOP
締切: 779/756/762/weight/α を捨てる
```

## Colab / 他（参考）

| # | アクション | 状態 |
|---|---|---|
| 804 / 802 | weight | **NOGO · F044 全閉** |
| 781 train | Kaggle | RUNNING / harvest 待ち |
| dual 813/815 | local | COMPLETE 直後 |

## Kaggle ladder（weight）

| CHK | hard Δ | d\|L−mid\| | 判定 |
|---|---:|---:|---|
| 688 | +0.52 | 軽 | NOGO |
| 804 | +0.74 | −1.43 | NOGO · F044 |
| 802 | +1.79 | −4.24 | NOGO · F044 |
| 782 / 761 | +3.8 / +4.0 | −7.93 | NOGO |

**やらない:** weight 再 · residual α · tip⊕ · GR · dual 前 Submit  

---

## CPU 済（再実行不要）

| パック | 1 行 |
|---|---|
| **CPU Pack D** | residual-path 地図 · 781 設計 · [ops](ops-cpu-pack-d-residual-path-2026-08-05.md) |
| dual weight 5 | 全 NOGO · F044 |

### Pack D → 781 設計要点

| 要点 | 値 |
|---|---|
| teacher | **L\*** soft path |
| β offline | **0.15–0.30** |
| 帯 | **q34 ∪ hard · excl midhurt** |
| stop | **residual RMSE**（807） |

---

## dual acceptance

- pool ∧ mean_worst3 ≤ old−**0.05** · max_band ≤ old+**0.5**  
- 812/813/815 · **TVT-OOF だけで PASS しない**  
- faces **`20260804-041247`** · α**0.35**  
- 詳細閾値: [post-781 §2](ops-chk781-post-pipeline-2026-08-05.md)

---

## Final2

| 枠 | 面 |
|---|---|
| 1 Trust | **666**（781 dual GO 時のみ差替検討） |
| 2 Public | **farvol 6.190** |
| 提出 | ユーザー明示のみ |

---

## 更新

- 2026-08-05 · **781 後工程 SSOT** 圧縮（post-781）· 802 F044 確定後
- 2026-08-05 夜 · CPU Pack D · 781 設計地図
