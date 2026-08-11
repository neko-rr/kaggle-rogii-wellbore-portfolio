#Requires -Version 5.1
<#
.SYNOPSIS
  Cursor カスタムサブエージェントを .cursor/agents/ に配置する。

.DESCRIPTION
  SSOT (edit here only): scripts/templates/cursor-agents/
  .cursor/agents/ is GENERATED and overwritten by this script. Do not hand-edit.

.EXAMPLE
  .\scripts\install-cursor-agents.ps1
#>
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Tpl = Join-Path $PSScriptRoot 'templates\cursor-agents'
$Agents = Join-Path $Root '.cursor\agents'

if (-not (Test-Path -LiteralPath $Tpl)) {
    throw "Template dir not found (SSOT): $Tpl"
}

New-Item -ItemType Directory -Force -Path $Agents | Out-Null

Get-ChildItem -LiteralPath $Tpl -File -Filter '*.md' | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $Agents $_.Name) -Force
}

Write-Host "OK: Cursor agents installed (GENERATED from templates)"
Write-Host "  SSOT (edit here): $Tpl"
Write-Host "  Generated dir:    $Agents"
Write-Host "  Do NOT edit .cursor/agents/*.md directly; re-run after template edits."
Write-Host "Invoke: /kaggle-repo-explore , /kaggle-nb-scout , /kaggle-discussion-scout , /kaggle-eval-runner , /kaggle-adversarial-review , /kaggle-static-check"

