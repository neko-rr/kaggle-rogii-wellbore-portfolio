# Cursor Agent Hooks (Kaggle repo)

SSOT: `.cursor/hooks.json` and `.cursor/rules/kaggle-cli-venv.mdc`

## Events

| Event | Script | Role |
|---|---|---|
| beforeShellExecution | before-shell-execution.ps1 | CLI, submit, download, destructive git |
| preToolUse | pre-tool-use.ps1 | Block writes under dataset/ |
| afterShellExecution | after-shell-execution.ps1 | Audit validate-submission runs |

## Reinstall

```powershell
.\scripts\install-cursor-hooks.ps1
.\scripts\test-cursor-hooks.ps1
```

## Download (after user OK)

```powershell
$env:KAGGLE_HOOK_ALLOW_DOWNLOAD='1'; .\scripts\kaggle-cli.ps1 competitions download ...
```

## Audit log

`.cursor/hooks/audit/validate-submission-shell.log` (gitignored)

## Templates

Source files live in `scripts/templates/cursor-hooks/`. Edit templates, then rerun install.
