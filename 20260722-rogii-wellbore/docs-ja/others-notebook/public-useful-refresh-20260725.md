# 公開 NB refresh — 2026-07-25

> scanned: vote / hotness / dateCreated（CLI）  
> pulled: `others-notebook/public-useful-refresh-20260725/`  
> コード抽出: `docs-en/others-notebook/*-Ver-latest.py`（本バッチ分）  
> 既存索引: [README-public-useful.md](README-public-useful.md)

## 1 行結論

最新公開帯の大半は **Contact-Gated / pfcfg / MHA / VISUALS の再掲**。新規で読む価値があるのは **(A) Connor `dz-dtvt-eda`（純幾何の研究ログ）** と **(B) lucifer19 `geoanchor`（suffix arbiter 叙述）**、検証用に **(C) A016 contact-guard ablation**。  
Discussion [728712](../discussion/728712-gs-noise-scale-public-nb.md) の `gs`×1.3 は、現行 tip（`opencv411/rogii-luck-is-all-you-need`）コードに **既に入っている**（3本の tip 系 pull はコード SHA 同一）。

## 取得した 6 本

| slug | 作者 | 判定 | 使い方 |
|---|---|---|---|
| `connortynan/dz-dtvt-eda` | Connor Tynan | **S（教育・物理）** | 必読。`dTVT≈−dZ+drift` · LOO 紀律 · 幾何天井の証拠。Final 提出コードではない |
| `lucifer19/rogii-geoanchor` | Krizsó | **A（同家系+叙述）** | dual-champion **suffix arbiter** · prefix guard。概念は参考、丸写し Final2 禁止 |
| `zongzishuang/a016-true-no-contact-guard-ablation` | charlotte | **A（ablation）** | `DISABLE_GUARDED_CONTACT_OVERRIDE=True` のみ · submit-safe。guard の効き確認用 |
| `hjyact/ultimate-pf-config-strategy-a-reproducible-score` | hjyact | **B（tip 同一）** | 728712 の出典。現行 tip と **コード同一** |
| `youill0317/rogii-ultimate-pf-gs130-public-repro` | youill0317 | **B（tip 同一）** | タイトルは GS1.3 明示 · 実体は tip と同一 |
| `opencv411/rogii-luck-is-all-you-need` | opencv411 | **既分析（tip）** | refresh 再取得 · `gs*1.3` 行を確認更新 |

## 捨てたもの（意図的に未 DL）

| パターン | 理由 |
|---|---|
| `rogii-pfcfg-*` / Frontier Lab VISUALS | tip ハイパラ乱獲 · 票≠新規知見 |
| `rogii-shift-*` / det-mha / MHA*sep* | Contact-Gated 同家系の数値スイープ |
| `takumashiga/rogii-v3*` · fleongg yuanzhe blend | 同スタック再掲（必要なら後で差分だけ） |
| 空タイトル / 1票の probe | 再現コストに見合わない |

## 技術メモ（重要）

### tip 三本はコード同一

`ultimate-pf-config` · `gs130-public-repro` · `luck-is-all-you-need` のコードセル連結 SHA は同一。  
いずれも PF 側に:

`gs = clip(nanstd(...), 10, 60) * 1.3`

がある。→ **728712 を「未実装の枠1微調整」としては扱わない**（既実装の確認のみ）。

### A016

- ベースは公開 7.091 系（A013）  
- **唯一の意図変更:** guarded contact override を無効化  
- `gs*1.3` は **付けていない**（tip 現行とここが違う）  
- submission フォールバックを厚くした「提出安全」方針が本命

### dz-dtvt-eda

- GR をわざと使わない幾何梯子（LB ~10 帯）  
- 自チーム EDA（souldrive TVT identity · ±15ft）と整合する **構造事実の補強**  
- 「幾何だけで sub-6 は無理 → GR/整合の価値」の定量感を与える

### geoanchor

- 二 champion を immutable に固定し、hidden suffix だけ合意条件付きで動かす  
- ローカル rollback + 全体 audit rollback  
- エンジンは dual-track / SP45 / fleongg 近縁 → **別予測面ではない**

## 自チーム行動（この refresh から）

| する | しない |
|---|---|
| Connor EDA を戦略・CV 叙述の根拠に残す | tip/`gs` の再スイープで Final2 を埋める |
| A016 を「guard ON/OFF」理解の参照にする | contact guard を盲目で OFF にして提出 |
| geoanchor の arbiter **条件**だけメモ | geoanchor を Final2 の別経路と主張 |

**checklist 反映（2026-07-25 追記）:** Active に重い CHK は **増やさない**。代わりに  
[`experiment-checklist.md`](../../../exp/experiment-checklist.md) へ **Parked CHK-110–112** · **明示 Stop** · 判断木を載せた。  
`gs*1.3` は tip 吸収済（CHK 不要）。昇格・GPU はユーザー承認後のみ。

## 個別要約

| ファイル | 対象 |
|---|---|
| [dz-dtvt-eda-Ver-latest.md](dz-dtvt-eda-Ver-latest.md) | Connor 幾何研究ログ |
| [a016-true-no-contact-guard-ablation-Ver-latest.md](a016-true-no-contact-guard-ablation-Ver-latest.md) | contact guard ablation |
| [rogii-geoanchor-Ver-latest.md](rogii-geoanchor-Ver-latest.md) | Dual-Champion Suffix Arbiter |
| [rogii-luck-is-all-you-need-tip.md](rogii-luck-is-all-you-need-tip.md) | tip（`gs*1.3` 追記） |
