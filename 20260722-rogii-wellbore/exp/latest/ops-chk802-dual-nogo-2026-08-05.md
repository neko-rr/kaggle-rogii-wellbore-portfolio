# CHK-802 dual · NOGO（2026-08-05）

## 結論

| 項目 | 値 |
|---|---|
| tag | `CHK-802-colab-fast2` |
| train tip-cv | OOF RMSE **9.3765**（FAST2 2fold · LGB×1） |
| dual L1_pass | **False** |
| next | **NOGO_L1** · weight 帯閉じ · **808→781** |
| ban-gate post | **NO-GO**（T3） |

## 主数値（α=0.35 · faces 20260804-041247）

| 尺 | Δpool（new−old · 悪化+） |
|---|---|
| hard20 residual | **+1.7854** |
| hybrid80 residual | **+0.7917** |
| 812 Q4 | **+1.0221**（ok=False） |
| 813 SSE top50 | **+0.9984**（ok=False） |
| 815 hard unlock | moved=True · d\|L−mid\| **−4.2412**（mid への開き **悪化寄り**） |

mid-hurt3 / Q4e / Q1e は **0.0000**（この L では未差分。本命 hard が悪化）。

## 面

- learned: Drive `out-t3-cpu-harvest/chk802-colab-face-fast2/` · 3 525 039 B
- dual out: Drive `out-t3-cpu-harvest/l-dual-CHK-802-colab-fast2/` · zip `dual_result_CHK-802-colab-fast2.zip`

## 解釈

MD-Q4 weight の FAST2 L は hard residual を **明確に悪化**。本命 B_Q4 も **+1.02**。d\|L−mid\| **−4.24** = mid-collapse 中等度。761/782/804 と同型の weight 帯失敗 → **言い換え再実行しない**（F044 確定閉じ）· **jump 781**。

## 提出・後工程

- residual E2E Submit（mid+α0.35·L802）：**ABORT**（計画は dual 並列前提だったが dual 完了で NOGO 確定）  
- 後工程 CV ロック: [`ops-chk802-post-pipeline-2026-08-05.md`](ops-chk802-post-pipeline-2026-08-05.md)

## 転送メモ（次セッション）

時間がかかった主因は dual 計算ではなく **MCP 経由の deps 分割アップロード**。  
次から軽 deps / face は **Private Kaggle Dataset**（zip 1 本）または Drive sync を優先。  
**ZIP 13KB の dual_deps は Dataset 化が最善。**

**SSOT（理由・終了後 Skill 修正リスト）:**  
[`docs-ja/colab-transfer-private-dataset.md`](../../docs-ja/colab-transfer-private-dataset.md) · `cursor.md` § 2026-08-05
