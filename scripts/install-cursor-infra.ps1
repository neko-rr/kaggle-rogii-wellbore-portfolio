#Requires -Version 5.1
<#
.SYNOPSIS
  Cursor Agent hooks + カスタムサブエージェントを一括インストールする。

.DESCRIPTION
  SSOT: scripts/templates/cursor-hooks/ · scripts/templates/cursor-agents/
  新コンペリポジトリ生成直後、または sync-project-infra 後に実行する。

.EXAMPLE
  .\scripts\install-cursor-infra.ps1
  .\scripts\install-cursor-infra.ps1 -SkipTest
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [switch] $SkipTest
)

$ErrorActionPreference = 'Stop'

$hooksScript = Join-Path $PSScriptRoot 'install-cursor-hooks.ps1'
$agentsScript = Join-Path $PSScriptRoot 'install-cursor-agents.ps1'
$testScript = Join-Path $PSScriptRoot 'test-cursor-hooks.ps1'

foreach ($path in @($hooksScript, $agentsScript)) {
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Required script not found: $path"
    }
}

if ($PSCmdlet.ShouldProcess('Cursor infra', 'Install hooks + agents')) {
    & $hooksScript
    & $agentsScript
}

if (-not $SkipTest) {
    if (-not (Test-Path -LiteralPath $testScript)) {
        throw "Test script not found: $testScript"
    }
    if ($PSCmdlet.ShouldProcess('Cursor hooks', 'Run test-cursor-hooks.ps1')) {
        & $testScript
    }
}

Write-Host ''
Write-Host 'OK: Cursor infra installed (hooks + agents)'
Write-Host 'Next: Cursor -> Developer: Reload Window'
