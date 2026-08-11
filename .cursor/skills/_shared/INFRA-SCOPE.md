# kaggle-infra の範囲（Kaggle 汎用のみ）

Private **`kaggle-infra`** / ローカル `%USERPROFILE%\.cursor\kaggle-template\` は  
**すべての Kaggle コンペで共通に使う** Skills · rules · scripts · 雛形だけを置く。

## 入れてはいけない（コンペ固有）

| NG 例 | どこに置くか |
|---|---|
| 特定コンペの手法禁止（例: F013/F015 解釈、工程内グラフ運用） | そのコンペの `.cursor/rules/` のみ |
| Public 26% 等の **当該コンペ固有** の LB 解釈 Stop ルール | 同上 · `docs-ja/` |
| tip 名・SUB 番号 · Private 順位 · 個人 LB | `exp/` · `retro/` · 当該 `AGENTS.md` |
| 仮説台帳の **failures 本文**（コンペ固有キーワード） | `exp/improvement-loop-failures.json` |
| dataset · submission · 学習コード | コンペ tree のみ |

**同期の向きは一方通行:**

```text
kaggle-infra (template)  ──sync-project-infra──▶  各コンペ root
```

- **コンペ → infra へ自動コピールールはない。**  
  マスターに上げるときだけ Agent/人が **汎用化した差分** を手で取り込む。
- `sync-project-infra-from-template.ps1` は **template をコンペへ重ねるのみ**。  
  コンペ側にしかない Rule（ファイル名が template に無いもの）は **削除しない**。

## 入れてよい（汎用）

- 提出上限の確認手順 · Final vs 最新 N · **UTC 既定**
- Competition Medals の公式バンド表と floor 計算法（例示数値は **架空 N**）
- **レーン（primary/public/diagnostic）· Final 枠 N の手続き · shake/compass の型**（固有 % はテンプレに書かない）
- **CV unit · shippable≠oracle · early smoke · knowledge axis A で CV 組み立て**（Skill `kaggle-cv-design`）
- **敵対的検証 SA-7** · 判定地図 `DECISION-FLOW.md` · 要約 Rule `kaggle-decision-gates`
- 3 段ゲート · Private 資産 · CLI venv · knowledge-store 接続 · 仮説 ban · 実験 ID 名前空間（CHK/F/LES/KGL）
- **コンペ依存リスト手続き**（`requirements-local.txt` · `setup-comp-venv` · **リスト内の固有 pin はコンペ側**）
- bootstrap · folder-map · start-checklist · retro の **型雛形**

### 二重管理を禁止する正本

| 資産 | 正本（編集先） | 生成物 / 参照 |
|---|---|---|
| checklist 雛形 | `comp/exp/experiment-checklist.md.template` | Skill 内 `checklist-template.md` はリンクのみ |
| カスタム agents | `root/scripts/templates/cursor-agents/` | `.cursor/agents/` は install 生成 · **直編集禁止** |
| Agent static 検査 | `scripts/run-static-checks.ps1` · Skill `kaggle-static-check` | エディタ Ruff 拡張は**人用のみ**（ゲート代替不可） |
| コンペ依存リスト | **各コンペ** `<inner>/requirements-local.txt` | 雛形のみ infra: `comp/requirements-local.txt.template` |

## マスター更新チェック（Agent）

infra に commit/push する前:

1. [ ] ファイル名・本文に **特定コンペ slug / LB 数字 / tip 名** が無いか
2. [ ] Rule 名が「当該コンペの実験規約専用」でないか  
   （例: `kaggle-f015-f013-mid-stage` · `kaggle-within-stage-graph` · `kaggle-public-lb-bias-stop` は **テンプレに載せない**）
3. [ ] 例示は架空 N・架空コンペ型で足りるか
4. [ ] knowledge カード実体は **`kaggle-knowledge-store`** 側（infra に候補 JSON を山積みしない）

## プロジェクト固有 Rule の置き方

新コンペで固有 rule が必要なら:

```text
<comp-root>/.cursor/rules/<comp-specific>.mdc
alwaysApply: true | false は必要な範囲だけ
```

`sync-project-infra` 後も残る（名前が template に無いため上書きも削除もされない）。  
**再利用したくなったら** キーワードを落として汎用化し、別 PR/commit で infra へ入れる。
