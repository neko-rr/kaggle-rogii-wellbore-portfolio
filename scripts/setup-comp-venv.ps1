#Requires -Version 5.1
<#
.SYNOPSIS
  Install competition local deps into repo .venv (CLI + requirements-local.txt).

.DESCRIPTION
  1) setup-kaggle-venv -Profile cli (kaggle + ruff)
  2) pip install -r <CompRoot>/requirements-local.txt into the SAME .venv
  3) optional import smoke for listed packages

  SSOT: _shared/COMP-DEPENDENCIES.md · Rule kaggle-cli-venv

.EXAMPLE
  .\scripts\setup-comp-venv.ps1 -CompRoot ".\20260101-my-comp"
  .\scripts\setup-comp-venv.ps1 -CompRoot ".\20260101-my-comp" -Upgrade
  .\scripts\setup-comp-venv.ps1 -CompRoot ".\20260101-my-comp" -SkipCli
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$CompRoot,

    [switch]$SkipCli,
    [switch]$Upgrade,
    [switch]$NoSmoke
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$CompRoot = (Resolve-Path -LiteralPath $CompRoot).Path
$ReqLocal = Join-Path $CompRoot "requirements-local.txt"
$VenvDir = Join-Path $RepoRoot ".venv"
$PipExe = Join-Path $VenvDir "Scripts\pip.exe"
$PyExe = Join-Path $VenvDir "Scripts\python.exe"
$SetupCli = Join-Path $PSScriptRoot "setup-kaggle-venv.ps1"
$SmokePy = Join-Path $PSScriptRoot "check-comp-imports.py"

Write-Host "== setup-comp-venv =="
Write-Host "Repo: $RepoRoot"
Write-Host "Comp: $CompRoot"

if (-not (Test-Path -LiteralPath $ReqLocal)) {
    throw "Missing $ReqLocal — copy from kaggle-template comp/requirements-local.txt.template and edit."
}

if (-not $SkipCli) {
    if (-not (Test-Path -LiteralPath $SetupCli)) {
        throw "missing $SetupCli"
    }
    $cliArgs = @()
    if ($Upgrade) { $cliArgs += "-Upgrade" }
    Write-Host "Running setup-kaggle-venv.ps1 -Profile cli ..."
    & $SetupCli -Profile cli @cliArgs
    if ($LASTEXITCODE -ne 0) {
        throw "setup-kaggle-venv failed (exit $LASTEXITCODE)"
    }
}
else {
    if (-not (Test-Path -LiteralPath $PipExe)) {
        throw ".venv pip missing. Run without -SkipCli first."
    }
}

$pipArgs = @("install", "-r", $ReqLocal)
if ($Upgrade) { $pipArgs += "--upgrade" }
Write-Host "Installing competition deps from requirements-local.txt ..."
# pip writes progress to stderr; do not treat as terminating under $ErrorActionPreference=Stop
$prevEap = $ErrorActionPreference
$ErrorActionPreference = "Continue"
try {
    & $PipExe @pipArgs
    $pipExit = $LASTEXITCODE
}
finally {
    $ErrorActionPreference = $prevEap
}
if ($pipExit -ne 0) {
    throw "pip install -r requirements-local.txt failed (exit $pipExit)"
}
Write-Host "OK: competition requirements-local.txt installed into .venv"

if (-not $NoSmoke) {
    if (-not (Test-Path -LiteralPath $SmokePy)) {
        Write-Warning "check-comp-imports.py missing - skip import smoke"
    }
    else {
        Write-Host "Import smoke ..."
        $ErrorActionPreference = "Continue"
        try {
            & $PyExe $SmokePy --requirements $ReqLocal
            $smokeExit = $LASTEXITCODE
        }
        finally {
            $ErrorActionPreference = $prevEap
        }
        if ($smokeExit -ne 0) {
            throw "import smoke FAIL - fix requirements-local.txt or install errors"
        }
        Write-Host "OK: import smoke PASS"
    }
}

Write-Host ""
Write-Host "Next:"
Write-Host "  .\scripts\run-static-checks.ps1 -Path <edited files>"
Write-Host "  Local eval uses: $PyExe"
Write-Host "  Colab tip: %pip install -q -r requirements-local.txt  (from Drive-mounted path)"
