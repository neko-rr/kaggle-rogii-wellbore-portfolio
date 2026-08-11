#Requires -Version 5.1
<#
.SYNOPSIS
  リポジトリ相対の knowledge/ を操作する Kaggle 知見ラッパー。
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("init", "harvest", "audit", "duplicates", "alias", "feedback", "lifecycle", "promote", "retrieve", "sync", "validate")]
    [string]$Action,
    [string]$CompRoot = "",
    [string]$CardId = "",
    [string]$SourceCardId = "",
    [string]$TargetCardId = "",
    [ValidateSet("", "L0", "L1", "L2", "L3")]
    [string]$EvidenceLevel = "",
    [ValidateSet("", "active", "conditional", "disputed", "deprecated")]
    [string]$LifecycleStatus = "",
    [string]$Reason = "",
    [string]$ExperimentId = "",
    [ValidateSet("", "GO", "NOGO", "NO-GO", "MIXED")]
    [string]$Verdict = "",
    [ValidateSet("own-experiment", "top-solution")]
    [string]$EvidenceType = "own-experiment",
    [string[]]$SourceRef = @(),
    [string]$PeerRoot = "",
    [ValidateSet("pull", "push")]
    [string]$Direction = "pull",
    [int]$Limit = 10,
    [double]$Threshold = 0.72,
    [switch]$IncludeCandidates,
    [switch]$Approve,
    [switch]$Apply,
    [switch]$AdoptStore
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Script = Join-Path $PSScriptRoot "kaggle_knowledge.py"

if (-not (Test-Path -LiteralPath $Script -PathType Leaf)) {
    throw "missing knowledge script: $Script"
}

$PythonCandidates = @(
    (Join-Path $RepoRoot ".venv\Scripts\python.exe"),
    "python"
)
$Python = $null
foreach ($candidate in $PythonCandidates) {
    if ($candidate -eq "python" -or (Test-Path -LiteralPath $candidate -PathType Leaf)) {
        $Python = $candidate
        break
    }
}
if (-not $Python) {
    throw "python not found (.venv preferred)"
}

$arguments = @(
    $Script,
    $Action,
    "--repo-root", $RepoRoot
)
if ($CompRoot) { $arguments += @("--comp-root", $CompRoot) }
if ($CardId) { $arguments += @("--card-id", $CardId) }
if ($SourceCardId) { $arguments += @("--source-card-id", $SourceCardId) }
if ($TargetCardId) { $arguments += @("--target-card-id", $TargetCardId) }
if ($EvidenceLevel) { $arguments += @("--evidence-level", $EvidenceLevel) }
if ($LifecycleStatus) { $arguments += @("--lifecycle-status", $LifecycleStatus) }
if ($Reason) { $arguments += @("--reason", $Reason) }
if ($ExperimentId) { $arguments += @("--experiment-id", $ExperimentId) }
if ($Verdict) {
    $normalizedVerdict = if ($Verdict -eq "NOGO") { "NO-GO" } else { $Verdict }
    $arguments += @("--verdict", $normalizedVerdict)
}
if ($EvidenceType) { $arguments += @("--evidence-type", $EvidenceType) }
foreach ($reference in $SourceRef) {
    if ($reference) { $arguments += @("--source-ref", $reference) }
}
if ($PeerRoot) { $arguments += @("--peer-root", $PeerRoot) }
if ($Direction) { $arguments += @("--direction", $Direction) }
if ($Limit -gt 0) { $arguments += @("--limit", "$Limit") }
if ($Threshold -ge 0) {
    $thresholdText = $Threshold.ToString([Globalization.CultureInfo]::InvariantCulture)
    $arguments += @("--threshold", $thresholdText)
}
if ($IncludeCandidates) { $arguments += "--include-candidates" }
if ($Approve) { $arguments += "--approve" }
if ($Apply) { $arguments += "--apply" }
if ($AdoptStore) { $arguments += "--adopt-store" }

try {
    & $Python @arguments
    exit $LASTEXITCODE
} catch {
    Write-Host "ERROR: Kaggle knowledge command failed: $($_.Exception.Message)" -ForegroundColor Red
    throw
}
