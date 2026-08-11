# CHK-203b 結果 — tip-cv upstream dump t2b

> date: 2026-07-26 · Kaggle GPU · **ERROR** · 提出なし

## 1 行

Selector 面までは完走（`tip_train_preds_selector.csv` 397333行 · hard20_balanced 80井）。  
その後段の **gold validate** で `RuntimeError: bad output length` → dump report 未生成。

## 原因

- tip-cv は train 井を test として注入するが、後段 gold が **本番 sample_submission 長**と照合して失敗
- learned skip は効いたが、**STOP_AFTER_SELECTOR / dump-only 経路が gold セルまで到達**
- override は train 井を test path で探し失敗（想定内フォールバック）

## 成果物（部分）

| ファイル | 状態 |
|---|---|
| `tip_train_preds_selector.csv` | **あり**（selector 完了） |
| `chk203_stage_dump_report.json` | **なし** |
| acceptance selector+≥1 upstream ok | **FAIL**（dump 未達） |

## 判定

**ERROR / 部分完走** — 上流 dump 目的は未達。204 は既に NO-GO のため **再実行優先度は低い**（selector 予測は副産物として保管）。

## 次（任意 · 低優先）

CHK-203c: `TIP_CV_STOP_AFTER_SELECTOR=True` を強制し gold セルをスキップする dump-only NB。ユーザー指示時のみ。
