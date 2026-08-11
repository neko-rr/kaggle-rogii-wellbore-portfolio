# Session preflight — .venv kaggle CLI
param(
    [switch]$Bootstrap,
    [ValidateSet("cli", "sim", "full")]
    [string]$Profile = "cli"
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Wrapper = Join-Path $PSScriptRoot "kaggle-cli.ps1"
$Setup = Join-Path $PSScriptRoot "setup-kaggle-venv.ps1"
$VenvKaggle = Join-Path $RepoRoot ".venv\Scripts\kaggle.exe"

Write-Host "== kaggle CLI preflight (venv-first) =="

if ($Bootstrap -or -not (Test-Path -LiteralPath $VenvKaggle)) {
    if (-not (Test-Path -LiteralPath $VenvKaggle)) {
        Write-Host "WARN: .venv\Scripts\kaggle.exe not found"
    }
    if ($Bootstrap -or -not (Test-Path (Join-Path $RepoRoot ".venv"))) {
        Write-Host "Running setup-kaggle-venv.ps1 -Profile $Profile ..."
        & $Setup -Profile $Profile
        if ($LASTEXITCODE -ne 0) {
            exit $LASTEXITCODE
        }
    }
}

try {
    $versionOut = & $Wrapper --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAIL: kaggle CLI returned exit code $LASTEXITCODE"
        Write-Host $versionOut
        Write-Host ""
        Write-Host "Fix: .\scripts\setup-kaggle-venv.ps1"
        exit 1
    }

    Write-Host "OK: $versionOut"
    $cacheFile = Join-Path $RepoRoot ".cache\kaggle-cli-path.txt"
    if (Test-Path -LiteralPath $cacheFile) {
        Write-Host "Path: $((Get-Content -LiteralPath $cacheFile -Raw).Trim())"
    }
    if (Test-Path -LiteralPath $VenvKaggle) {
        Write-Host "Venv: $VenvKaggle"
    }
    Write-Host ""
    Write-Host "Agent: .\scripts\kaggle-cli.ps1 <args>  |  bootstrap: .\scripts\check-kaggle-cli.ps1 -Bootstrap"
    exit 0
}
catch {
    Write-Host "FAIL: $($_.Exception.Message)"
    Write-Host ""
    Write-Host "Fix: .\scripts\setup-kaggle-venv.ps1"
    Write-Host "Doc: .cursor/skills/kaggle-cli-ops/SKILL.md"
    exit 1
}
