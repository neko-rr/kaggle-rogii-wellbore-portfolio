#Requires -Version 5.1
<#
.SYNOPSIS
  kaggle-template と既存コンペ ROOT のインフラ差分を機械検知する。

.DESCRIPTION
  比較対象:
    - .cursor/rules/*.mdc（テンプレ側にあるもの）
    - .cursor/skills/*/SKILL.md（テンプレ側にあるもの）
    - scripts/*.ps1 / scripts/*.py（テンプレ側にあるもの）
    - requirements-kaggle-cli.txt / requirements-local-sim.txt
    - .githooks/pre-commit
  コンペ固有ファイルはテンプレに無いので対象外。
  exit 0 = 差分なし or 内容差分のみ（WARN）
  exit 1 = 欠落あり、または -Strict で内容差分あり

.EXAMPLE
  .\scripts\check-template-drift.ps1 -CompRoot .
  .\scripts\check-template-drift.ps1 -CompRoot . -Strict
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string] $CompRoot,

    [string] $TemplateRoot = (Join-Path $env:USERPROFILE '.cursor\kaggle-template\root'),

    [switch] $Strict
)

$ErrorActionPreference = 'Stop'

function Get-FileSha256([string] $Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
}

function Add-RelFiles {
    param(
        [System.Collections.Generic.List[string]] $List,
        [string] $Root,
        [string] $RelativeDir,
        [string] $Filter
    )
    $dir = Join-Path $Root ($RelativeDir -replace '/', '\')
    if (-not (Test-Path -LiteralPath $dir)) { return }
    Get-ChildItem -LiteralPath $dir -File -Filter $Filter -Force -ErrorAction SilentlyContinue |
        ForEach-Object {
            $rel = Join-Path $RelativeDir $_.Name
            $List.Add(($rel -replace '\\', '/'))
        }
}

if (-not (Test-Path -LiteralPath $TemplateRoot)) {
    throw "TemplateRoot not found: $TemplateRoot"
}
$comp = (Resolve-Path -LiteralPath $CompRoot).Path
$tpl = (Resolve-Path -LiteralPath $TemplateRoot).Path

$tplFiles = New-Object System.Collections.Generic.List[string]
Add-RelFiles -List $tplFiles -Root $tpl -RelativeDir '.cursor/rules' -Filter '*.mdc'
Add-RelFiles -List $tplFiles -Root $tpl -RelativeDir 'scripts' -Filter '*.ps1'
Add-RelFiles -List $tplFiles -Root $tpl -RelativeDir 'scripts' -Filter '*.py'
Add-RelFiles -List $tplFiles -Root $tpl -RelativeDir 'scripts/templates/cursor-agents' -Filter '*.md'
Add-RelFiles -List $tplFiles -Root $tpl -RelativeDir '.cursor/skills/_shared' -Filter '*.md'
foreach ($req in @('requirements-kaggle-cli.txt', 'requirements-local-sim.txt')) {
    if (Test-Path -LiteralPath (Join-Path $tpl $req)) { $tplFiles.Add($req) }
}
$hook = Join-Path $tpl '.githooks\pre-commit'
if (Test-Path -LiteralPath $hook) { $tplFiles.Add('.githooks/pre-commit') }

$skillsRoot = Join-Path $tpl '.cursor\skills'
if (Test-Path -LiteralPath $skillsRoot) {
    Get-ChildItem -LiteralPath $skillsRoot -Directory -Force | ForEach-Object {
        $skill = Join-Path $_.FullName 'SKILL.md'
        if (Test-Path -LiteralPath $skill) {
            $tplFiles.Add(('.cursor/skills/{0}/SKILL.md' -f $_.Name))
        }
    }
}

$tplFiles = @($tplFiles | Select-Object -Unique | Sort-Object)
$missing = New-Object System.Collections.Generic.List[string]
$changed = New-Object System.Collections.Generic.List[string]
$matched = 0

foreach ($rel in $tplFiles) {
    $src = Join-Path $tpl ($rel -replace '/', '\')
    $dst = Join-Path $comp ($rel -replace '/', '\')
    if (-not (Test-Path -LiteralPath $dst)) {
        $missing.Add($rel)
        continue
    }
    if ((Get-FileSha256 $src) -ne (Get-FileSha256 $dst)) {
        $changed.Add($rel)
    }
    else {
        $matched++
    }
}

Write-Host "[template-drift] template=$tpl"
Write-Host "[template-drift] comp=$comp"
Write-Host ("[template-drift] compared={0} match={1} missing={2} changed={3}" -f `
    $tplFiles.Count, $matched, $missing.Count, $changed.Count)

foreach ($m in $missing) {
    Write-Host "  MISSING: $m" -ForegroundColor Red
}
foreach ($c in $changed) {
    Write-Host "  CHANGED: $c" -ForegroundColor Yellow
}

# agents generated mirror: templates vs .cursor/agents (name presence)
$agentTplDir = Join-Path $tpl 'scripts\templates\cursor-agents'
$agentGenDir = Join-Path $comp '.cursor\agents'
$agentMissing = New-Object System.Collections.Generic.List[string]
if (Test-Path -LiteralPath $agentTplDir) {
    Get-ChildItem -LiteralPath $agentTplDir -File -Filter 'kaggle-*.md' -Force |
        ForEach-Object {
            $gen = Join-Path $agentGenDir $_.Name
            if (-not (Test-Path -LiteralPath $gen)) {
                $agentMissing.Add($_.Name)
            }
        }
}
if ($agentMissing.Count -gt 0) {
    foreach ($a in $agentMissing) {
        Write-Host "  MISSING agent (run install-cursor-agents.ps1): $a" -ForegroundColor Red
        $missing.Add(('.cursor/agents/{0}' -f $a))
    }
}

if ($missing.Count -eq 0 -and $changed.Count -eq 0) {
    Write-Host '[template-drift] PASS (in sync)' -ForegroundColor Green
    exit 0
}

Write-Host ''
Write-Host '[template-drift] To sync from template:' -ForegroundColor Cyan
Write-Host ('  & "$env:USERPROFILE\.cursor\kaggle-template\scripts\sync-project-infra-from-template.ps1" -CompRoot "{0}" -InstallCursorInfra' -f $comp)

if ($missing.Count -gt 0 -or ($Strict -and $changed.Count -gt 0)) {
    Write-Host '[template-drift] FAIL' -ForegroundColor Red
    exit 1
}

Write-Host '[template-drift] WARN (content drift only; use -Strict to fail)' -ForegroundColor Yellow
exit 0
