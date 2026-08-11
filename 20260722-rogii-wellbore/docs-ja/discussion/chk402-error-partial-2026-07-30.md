# CHK-402 失敗分析 — matched tip-cv（2026-07-30）

> kernel: `kazeneko77/tip-cv-chk402-matched-exhard20` **Ver1 ERROR**  
> 提出なし · F015  
> 部分採点: [`chk402-partial-score.json`](../../exp/work/wave30-soft-preserve/chk402-partial-score.json)

## 1行

**本命の tip FINAL 再生成は完了している。** 失敗は終盤の監査セル（CHK-256と同バグ）だけ。

## 失敗箇所

| 項目 | 内容 |
|---|---|
| 状態 | `KernelWorkerStatus.ERROR` |
| セル | In [46]（notebook cell 56 · submission audit） |
| 例外 | `UnboundLocalError: cannot access local variable 'sample'` |
| 原因 | `_build_submission_audit` 内で global `sample` を読んでから `sample = ...` 代入 → Python が局所変数扱い |
| 既知 | CHK-256 Ver1/Ver2 と同じ（[`chk256-faces-result.md`](chk256-faces-result.md)） |
| 未達 | face score セル（cell 60）· `chk*_face_report.json` |

## 到達した成果物（使える）

| 面 | pooled eq-well RMSE（20井） | 行数 |
|---|---:|---:|
| selector / sp45 / gold / before_hedge | **10.5985** | 100988 |
| **final**（hedge後 `submission.csv`） | **10.6568** | 100988 |

- tip-cv inject OK · 20/20 wells · eval 100988行
- mpkg は tip-cv 下で disable（想定どおり）
- learned は tip-cv で空（`learned_trajectory_submission.csv` headerのみ）
- gold/contact override は test パス参照で全井 skip（tip-cvでは無害）

## 読み取り

1. **比較に必要な tip FINAL は Ver1 部分成果で既にある**（ローカル採点可）
2. hedge 後だけわずかに悪化（10.60 → 10.66）· CHK-256 hard20でも hedge 以外は面間差ゼロと同型
3. CHK-398 の ranker final≈14.81 / soft≈14.58 より、**同一20井の tip FINAL≈10.66 の方が明らかに良い**
4. Ver2 は audit の `sample` 変数名衝突を直せば face score まで完走見込み（再GPUは任意）

## 次アクション候補

| 案 | 内容 | GPU |
|---|---|---|
| **A** | 部分成果で ranker vs tip FINAL 比較を完了（402判定） | 不要 |
| **B** | audit バグ修正 → Ver2 push（face reportまで） | 要 |

推奨: まず **A**（目的は比較）。必要なら後で B。
