#Requires -Version 5.1
<#
.SYNOPSIS
  git pre-commit: staged ファイルに dataset / 秘匿情報 / 大容量成果物が無いか検査する。
#>
$ErrorActionPreference = "Stop"

function Write-Block([string]$Message) {
    Write-Host "[kaggle-git-security] BLOCKED: $Message" -ForegroundColor Red
}

$root = git rev-parse --show-toplevel 2>$null
if (-not $root) {
    Write-Host "[kaggle-git-security] Not a git repo — skip"
    exit 0
}

Set-Location $root

$staged = @(git diff --cached --name-only --diff-filter=ACMR 2>$null)
if ($staged.Count -eq 0) {
    exit 0
}

# パスベース拒否（.gitignore と整合）
$allowedDatasetFiles = @(
    '(^|[\\/])dataset[\\/]\.gitkeep$',
    '(^|[\\/])dataset[\\/]README\.md$'
)

$blockedPathPatterns = @(
    '(^|[\\/])dataset[\\/].+',
    '(^|[\\/])\.kaggle([\\/]|$)',
    '(^|[\\/])kaggle\.json$',
    '(^|[\\/])\.env(\.|$)',
    '(^|[\\/])\.env$',
    '(^|[\\/])secrets([\\/]|$)',
    'submission\.zip$',
    '\.(safetensors|bin|pt|pth|ckpt|onnx)$',
    '(^|[\\/])\.ipynb_checkpoints([\\/]|$)'
)

foreach ($file in $staged) {
    $normalized = $file -replace '\\', '/'

    $isAllowedDataset = $false
    foreach ($allow in $allowedDatasetFiles) {
        if ($normalized -match $allow) {
            $isAllowedDataset = $true
            break
        }
    }

    if ($isAllowedDataset) {
        continue
    }

    foreach ($pattern in $blockedPathPatterns) {
        if ($normalized -match $pattern) {
            Write-Block "Path pattern '$pattern' matched: $file"
            Write-Host "  → dataset/ と大容量成果物は GitHub に載せない（Skill: kaggle-git-security）"
            exit 1
        }
    }
}

# テキスト内容の簡易スキャン（秘匿情報）
$secretPatterns = @(
    @{ Name = 'KAGGLE_KEY'; Pattern = 'KAGGLE_KEY\s*=\s*[^\s#]+' },
    @{ Name = 'kaggle.json inline'; Pattern = '"key"\s*:\s*"[a-f0-9]{20,}"' },
    @{ Name = 'OpenAI-style key'; Pattern = 'sk-[a-zA-Z0-9]{20,}' },
    @{ Name = 'Generic API key'; Pattern = '(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*["'']?[a-zA-Z0-9_\-]{16,}' },
    @{ Name = 'AWS key'; Pattern = 'AKIA[0-9A-Z]{16}' }
)

$textExtensions = @('.md', '.py', '.ipynb', '.json', '.yaml', '.yml', '.env', '.toml', '.cfg', '.ini', '.ps1', '.sh', '.txt', '.csv')

foreach ($file in $staged) {
    $ext = [System.IO.Path]::GetExtension($file).ToLowerInvariant()
    if ($textExtensions -notcontains $ext) {
        continue
    }

    $fullPath = Join-Path $root $file
    if (-not (Test-Path $fullPath -PathType Leaf)) {
        continue
    }

    try {
        $content = Get-Content -Path $fullPath -Raw -Encoding UTF8 -ErrorAction Stop
    }
    catch {
        continue
    }

    foreach ($rule in $secretPatterns) {
        if ($content -match $rule.Pattern) {
            Write-Block "$($rule.Name) pattern in: $file"
            Write-Host "  → 認証情報は .env / kaggle.json に置き、Git から除外する"
            exit 1
        }
    }
}

Write-Host "[kaggle-git-security] OK ($($staged.Count) file(s) staged)"
exit 0
