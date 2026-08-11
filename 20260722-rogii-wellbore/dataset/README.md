# dataset/

Kaggle コンペの **公式データ**（Git 除外）。

**配置確認日:** 2026-07-23（ユーザー指示により CLI DL / 展開確認）

```text
dataset/
├─ README.md
├─ sample_submission.csv
├─ AI_wellbore_geology_prediction_task_en.pptx
├─ train/     # 773 wells
├─ test/      # 3 example wells（本番 hidden ではない）
└─ derived/
```

## 注意

- 公式ファイルは **編集しない**（加工は `derived/`）
- **Git / GitHub にコミットしない**
- 要約・実測: `docs-ja/dataset.md` · `exp/work/dataset-eda-20260723.json`
- 再 DL: `.\scripts\kaggle-cli.ps1 competitions download -c rogii-wellbore-geology-prediction -p <このフォルダ>`（`--unzip` 非対応 → Python/`Expand-Archive` で展開）
- 展開後の zip 控えは **2026-07-23 削除済**（再 DL で復元可）