# Private Knowledge · Infra リポジトリ運用

> Agent / Kaggler 向け SSOT。  
> コンペ本体 repo と **分離**した Private GitHub を使う（ディスク節約 · 並行コンペ · 知見の持ち運び）。

---

## 2 本の Private リポジトリ

| 用途 | GitHub（Private） | ローカル置き場 | 含むもの |
|---|---|---|---|
| **知見** | `https://github.com/neko-rr/kaggle-knowledge-store` | `<comp-repo>/knowledge/`（nested git） | candidates · cards · evidence · playbook · domain-policy |
| **インフラ** | `https://github.com/neko-rr/kaggle-infra` | `%USERPROFILE%\.cursor\kaggle-template\` | Skills · rules · scripts · 開始雛形 |

| 置かない | 置き場 |
|---|---|
| 公式 dataset / 大 weight | コンペ `dataset/` · Kaggle（Git 禁止） |
| `kaggle.json` / `.env` | マシンローカルのみ |
| 横断知見 | **knowledge-store のみ**（コンペ本体の `.gitignore` で除外） |

**Public にしてはいけない。** ポートフォリオ用は scrub した別 repo。

`store_id` SSOT: `knowledge/store.json`（現在 `7fde6393-4492-48cf-a94a-8eb4bc058f08`）。勝手に `init` し直さない。

---

## Agent 必須フロー

### 新コンペ開始（bootstrap 後）

1. コンペ **repo ルート** に `knowledge/` が無い / `store.json` が無い場合:
   ```powershell
   # 推奨: 共有 store を clone（新規 UUID を作らない）
   git clone https://github.com/neko-rr/kaggle-knowledge-store.git knowledge
   # URL 上書き: $env:KAGGLE_KNOWLEDGE_GIT_URL = "https://github.com/<you>/kaggle-knowledge-store.git"
   ```
2. `.\scripts\run-kaggle-knowledge.ps1 -Action validate`
3. `comp-profile` 確定後:
   ```powershell
   .\scripts\run-kaggle-knowledge.ps1 -Action retrieve `
     -CompRoot "./yyyyymmdd-slug" -IncludeCandidates
   ```
4. `exp/prior-knowledge.md` を **domain フィルタ → A→C→B → apply/avoid 確認** で読む  
5. 採用だけ checklist 仮説化（自動 CHK 化禁止）  
6. pre-strategy-gate X3 に prior 確認を記録

`init-comp-layout` や `knowledge init` は **空の新 store_id を作る**可能性がある。  
**共有倉庫があるなら clone を優先**し、空 init は「完全に新しい倉庫を始めるとき」だけ。

### 実験後 · 終了後

1. `retro-lessons` を A/B/C + apply/avoid/origin/domain で更新  
2. harvest + validate  
3. **knowledge に commit & push**（忘れない）:
   ```powershell
   cd knowledge
   git status
   git add -A
   git commit -m "harvest: <comp-slug> lessons/failures"
   git push origin main
   ```
4. promote はユーザー明示承認後のみ

### インフラ更新（Skills 改定後）

1. マスター（`kaggle-template` / `kaggle-infra`）を直す  
2. commit + push to `kaggle-infra`  
3. 既存コンペへ:
   ```powershell
   & "$env:USERPROFILE\.cursor\kaggle-template\scripts\sync-project-infra-from-template.ps1" `
     -CompRoot "<comp-root1>", "<comp-root2>"
   ```

### 別プロジェクトへ knowledge を寄せる

| 手段 | いつ |
|---|---|
| **git clone / pull**（推奨） | 同じ GitHub knowledge-store を共有 |
| **`kaggle-knowledge-sync`** | Git 無し · 別ディスク上の peer フォルダ · ドライラン→Apply |

いずれも **store_id 一致**が前提。audit FAIL なら同期しない。

---

## Skill 対応表

| Skill | Private repo 関連の役割 |
|---|---|
| `kaggle-comp-bootstrap` | clone knowledge · retrieve · infra path 確認 |
| `kaggle-knowledge-harvest` | candidates 更新後 **push を促す** |
| `kaggle-knowledge-retrieve` | prior · domain/axis · apply/avoid |
| `kaggle-knowledge-sync` | peer 同期（git 代替） |
| `kaggle-knowledge-audit` | push / sync 前 |
| `post-comp-retro-setup` | harvest → push knowledge |
| `kaggle-git-security` | knowledge は外側 repo に載せず nested Private |

---

## レッスンカードの最低要件（再掲）

```markdown
1. **タイトル**
   - body: ...
   - apply: ...
   - avoid: ...
   - origin: own|topsolution|ops|mixed
   - domain: kaggle|ahc|shared
   - evidence: ...
```

AHC 併存: `knowledge/personal/domain-policy.md`（**shared のみ抽象共有**）。

---

## 禁止

- knowledge を Public リポジトリに入れる  
- 外側コンペ repo に `knowledge/` を force-add する  
- 共有 store があるのに `knowledge init` で **新 store_id** を量産する  
- harvest 後に push せず他コンペへ「最新のはず」と retrieve する  
- L0 カードを apply 無視で自動 CHK 化する  
- Skill やカードに PC 絶対パスを書く  
