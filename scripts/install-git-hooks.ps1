#Requires -Version 5.1
<#
.SYNOPSIS
  .githooks/pre-commit を .git/hooks/ にインストールする。

.EXAMPLE
  git init
  .\scripts\install-git-hooks.ps1
#>
$ErrorActionPreference = "Stop"

$repoRoot = git rev-parse --show-toplevel 2>$null
if (-not $repoRoot) {
    # scripts/ からの相対でリポジトリルートを推定
    $repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
    if (-not (Test-Path (Join-Path $repoRoot ".git"))) {
        Write-Error "git リポジトリではありません。先に 'git init' を実行してください。"
    }
}

$srcHook = Join-Path $repoRoot ".githooks\pre-commit"
$destHook = Join-Path $repoRoot ".git\hooks\pre-commit"

if (-not (Test-Path $srcHook)) {
    Write-Error "フック元が見つかりません: $srcHook"
}

New-Item -ItemType Directory -Force -Path (Split-Path $destHook -Parent) | Out-Null
Copy-Item -Path $srcHook -Destination $destHook -Force

Write-Host "[kaggle-git-security] Installed: $destHook"
Write-Host "  検査スクリプト: scripts/check-staged-secrets.ps1"
Write-Host "  PS1 BOM 検査:   scripts/check-ps1-utf8-bom.ps1 -Staged"
