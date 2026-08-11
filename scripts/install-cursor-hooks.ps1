#Requires -Version 5.1
<#
.SYNOPSIS
  Cursor Agent hooks (Kaggle repo) を .cursor/hooks/ に配置する。

.DESCRIPTION
  SSOT は scripts/templates/cursor-hooks/。here-string は使わず Copy-Item で配置する
  (PowerShell 5.1 の UTF-8 文字化け回避)。

.EXAMPLE
  cd ./<comp-or-project-root>
  powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-cursor-hooks.ps1
  .\scripts\test-cursor-hooks.ps1
#>
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Tpl = Join-Path $PSScriptRoot 'templates\cursor-hooks'
$Hooks = Join-Path $Root '.cursor\hooks'
$HookFiles = @(
    '_hook-common.ps1',
    'before-shell-execution.ps1',
    'pre-tool-use.ps1',
    'after-shell-execution.ps1',
    'README.md'
)

if (-not (Test-Path -LiteralPath $Tpl)) {
    throw "Template dir not found: $Tpl"
}

New-Item -ItemType Directory -Force -Path $Hooks | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $Hooks 'audit') | Out-Null

foreach ($name in $HookFiles) {
    $src = Join-Path $Tpl $name
    if (-not (Test-Path -LiteralPath $src)) {
        throw "Missing template: $src"
    }
    Copy-Item -LiteralPath $src -Destination (Join-Path $Hooks $name) -Force
}

$hooksJsonSrc = Join-Path $Tpl 'hooks.json'
$hooksJsonDst = Join-Path $Root '.cursor\hooks.json'
Copy-Item -LiteralPath $hooksJsonSrc -Destination $hooksJsonDst -Force

$gi = Join-Path $Root '.gitignore'
if (Test-Path -LiteralPath $gi) {
    $c = [System.IO.File]::ReadAllText($gi)
    if ($c -notmatch '(?m)^\.cursor/hooks/audit/') {
        $utf8 = New-Object System.Text.UTF8Encoding $false
        [System.IO.File]::AppendAllText($gi, "`n# Cursor hooks audit log`n.cursor/hooks/audit/`n", $utf8)
    }
}

Write-Host "OK: Cursor hooks installed"
Write-Host "  templates: $Tpl"
Write-Host "  hooks dir: $Hooks"
Write-Host "  config:    $hooksJsonDst"
Write-Host "Next: .\scripts\test-cursor-hooks.ps1"
