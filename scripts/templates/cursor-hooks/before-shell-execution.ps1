#Requires -Version 5.1
try {
    $ErrorActionPreference = 'Stop'
    . (Join-Path $PSScriptRoot '_hook-common.ps1')

    $inputObj = Read-HookInput
    $cmd = if ($inputObj -and $inputObj.command) { [string]$inputObj.command } else { '' }
    if ([string]::IsNullOrWhiteSpace($cmd)) { Write-HookAllow }

    $normalized = $cmd -replace '\\', '/'
    $allow = @(
        'kaggle-cli\.ps1', 'check-kaggle-cli\.ps1', 'setup-kaggle-venv\.ps1',
        'open-kaggle-light\.ps1', 'sync-skill-permissions\.ps1', 'init-comp-layout\.ps1',
        'validate-submission\.ps1', 'check-staged-secrets\.ps1', 'install-git-hooks\.ps1',
        'install-cursor-hooks\.ps1', 'install-cursor-agents\.ps1', 'install-cursor-infra\.ps1', 'test-cursor-hooks\.ps1',
        'before-shell-execution\.ps1', 'pre-tool-use\.ps1', 'after-shell-execution\.ps1',
        '\.cursor/hooks/', '\.cursor\\hooks\\'
    )
    foreach ($p in $allow) { if ($normalized -match $p) { Write-HookAllow } }

    $pipKaggle = '(?i)(^|[\s;&|])(python\s+-m\s+pip|pip3?)\s+install(\s+[^\s;&|]+)*\s+kaggle(\s|$|[^\-])'
    if ($cmd -match $pipKaggle) {
        Write-HookDeny `
            -UserMessage 'pip install kaggle is blocked. Use setup-kaggle-venv.ps1 and kaggle-cli.ps1.' `
            -AgentMessage 'Blocked: pip install kaggle'
    }

    $rawKaggle = '(?i)(^|[\s;&|])kaggle(\.exe)?\s'
    if ($cmd -match $rawKaggle) {
        Write-HookDeny `
            -UserMessage 'Raw kaggle CLI is blocked. Use .\scripts\kaggle-cli.ps1.' `
            -AgentMessage 'Blocked: raw kaggle'
    }

    if ($cmd -match '(?i)competitions\s+submit') {
        Write-HookDeny `
            -UserMessage 'competitions submit requires explicit user OK in chat.' `
            -AgentMessage 'Blocked: competitions submit'
    }
    if ($cmd -match '(?i)kernels\s+push') {
        Write-HookDeny `
            -UserMessage 'kernels push requires explicit user OK in chat.' `
            -AgentMessage 'Blocked: kernels push'
    }

    $download = '(?i)(competitions\s+download|datasets\s+download|models\s+instances\s+versions\s+download)'
    if ($cmd -match $download) {
        $flag = 'KAGGLE_HOOK_ALLOW_DOWNLOAD\s*=\s*[''"]?1[''"]?'
        if ($cmd -notmatch $flag) {
            Write-HookDeny `
                -UserMessage 'Download blocked. Set KAGGLE_HOOK_ALLOW_DOWNLOAD=1 and use kaggle-cli.ps1 after user OK.' `
                -AgentMessage 'Blocked: download without flag'
        }
    }

    $destructive = @(
        '(?i)git\s+push\s+([^-\s]+\s+)*--force', '(?i)git\s+push\s+-f\b',
        '(?i)git\s+reset\s+--hard', '(?i)git\s+clean\s+-[a-z]*f',
        '(?i)git\s+branch\s+-D\b', '(?i)git\s+push\s+.*--delete'
    )
    foreach ($pat in $destructive) {
        if ($cmd -match $pat) {
            Write-HookDeny `
                -UserMessage 'Destructive git operations are blocked for Agent.' `
                -AgentMessage 'Blocked: destructive git'
        }
    }
    Write-HookAllow
}
catch {
    [Console]::Error.WriteLine("[kaggle-hook] before-shell: $_")
    [Console]::Out.WriteLine('{"permission":"allow"}')
    exit 0
}
