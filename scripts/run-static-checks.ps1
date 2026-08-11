#Requires -Version 5.1
<#
.SYNOPSIS
  Agent-written code static preflight (syntax / notebook / private / ruff).

.DESCRIPTION
  MUST pass before local train, long eval, kernels push, or heavy GPU.
  Editor Ruff extension does NOT satisfy this gate — this script does.

.EXAMPLE
  .\scripts\run-static-checks.ps1
  .\scripts\run-static-checks.ps1 -CompRoot ".\20260101-slug"
  .\scripts\run-static-checks.ps1 -Path ".\my-notebook\foo.py"
#>
[CmdletBinding()]
param(
    [string]$RepoRoot = "",
    [string]$CompRoot = "",
    [string[]]$Path = @(),
    [switch]$NoRuff
)

$ErrorActionPreference = "Stop"

if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}
else {
    $RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
}

$PyCandidates = @(
    (Join-Path $RepoRoot ".venv\Scripts\python.exe"),
    "python"
)
$Py = $null
foreach ($c in $PyCandidates) {
    if ($c -eq "python") {
        $Py = $c
        break
    }
    if (Test-Path -LiteralPath $c) {
        $Py = $c
        break
    }
}
if (-not $Py) {
    throw "python not found (.venv preferred). Run .\scripts\setup-kaggle-venv.ps1"
}

$Script = Join-Path $PSScriptRoot "check-static.py"
if (-not (Test-Path -LiteralPath $Script)) {
    throw "missing $Script"
}

$argList = @($Script, "--repo-root", $RepoRoot)
if ($CompRoot) {
    $argList += @("--comp-root", ((Resolve-Path -LiteralPath $CompRoot).Path))
}
foreach ($p in $Path) {
    if ($p) { $argList += @("--path", $p) }
}
if ($NoRuff) {
    $argList += "--no-ruff"
}

Write-Host "== static-check (Agent gate; editor Ruff is NOT enough) =="
# Python prints a human summary on stderr; do not treat as terminating error in PS
$prev = $ErrorActionPreference
$ErrorActionPreference = "Continue"
& $Py @argList
$code = $LASTEXITCODE
$ErrorActionPreference = $prev
exit $code
