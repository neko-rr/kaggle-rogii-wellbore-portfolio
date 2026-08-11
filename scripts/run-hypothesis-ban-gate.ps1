#Requires -Version 5.1
<#
.SYNOPSIS
  Generic hypothesis-ban gate wrapper (pre/post).

.EXAMPLE
  .\scripts\run-hypothesis-ban-gate.ps1 -ChkId CHK-001 -ActionType T3 `
    -Hypothesis "short train with symbol focus" -Mechanism "lr 1e-4 x3 epochs" -Phase pre `
    -ExpDir ".\20260701-my-comp\exp"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ChkId,
    [Parameter(Mandatory = $true)]
    [ValidateSet("T0", "T1", "T2", "T3", "T4")]
    [string]$ActionType,
    [Parameter(Mandatory = $true)]
    [string]$Hypothesis,
    [string]$Mechanism = "",
    [ValidateSet("pre", "post")]
    [string]$Phase = "pre",
    [ValidateSet("GO", "NOGO", "NO-GO")]
    [string]$Verdict = "",
    [string]$ExpDir = "",
    [string]$OutPath = "",
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$PyCandidates = @(
    (Join-Path $Root ".venv\Scripts\python.exe"),
    (Join-Path $Root "python.exe"),
    "python"
)
$Py = $null
foreach ($c in $PyCandidates) {
    if ($c -eq "python") { $Py = $c; break }
    if (Test-Path -LiteralPath $c) { $Py = $c; break }
}
if (-not $Py) { throw "python not found (.venv preferred)" }

$Script = Join-Path $PSScriptRoot "check-hypothesis-ban-gate.py"
if (-not (Test-Path -LiteralPath $Script)) {
    throw "missing $Script"
}

$argsList = @(
    $Script,
    "--chk-id", $ChkId,
    "--action-type", $ActionType,
    "--hypothesis", $Hypothesis,
    "--phase", $Phase
)
if ($Mechanism) { $argsList += @("--mechanism", $Mechanism) }
if ($ExpDir) { $argsList += @("--exp-dir", $ExpDir) }
if ($Verdict) {
    $v = if ($Verdict -eq "NOGO") { "NO-GO" } else { $Verdict }
    $argsList += @("--verdict", $v)
}
if ($OutPath) { $argsList += @("--out", $OutPath) }
if ($Force) { $argsList += "--force" }

& $Py @argsList
exit $LASTEXITCODE
