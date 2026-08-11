# Repo .venv: Kaggle CLI and optional local sim packages
# Usage: .\scripts\setup-kaggle-venv.ps1 [-Profile cli|sim|full] [-Upgrade]
param(
    [ValidateSet("cli", "sim", "full")]
    [string]$Profile = "cli",
    [switch]$Upgrade
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$VenvDir = Join-Path $RepoRoot ".venv"
$ReqCli = Join-Path $RepoRoot "requirements-kaggle-cli.txt"
$ReqSim = Join-Path $RepoRoot "requirements-local-sim.txt"
$PipExe = Join-Path $VenvDir "Scripts\pip.exe"
$KaggleExe = Join-Path $VenvDir "Scripts\kaggle.exe"

if ($Profile -eq "full") {
    $Profile = "sim"
}

$ReqFile = if ($Profile -eq "sim") { $ReqSim } else { $ReqCli }

$filesToCheck = @($ReqCli)
if ($Profile -eq "sim") {
    $filesToCheck += $ReqSim
}
foreach ($f in $filesToCheck) {
    if (-not (Test-Path -LiteralPath $f)) {
        Write-Error "requirements file not found: $f"
    }
}

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Error "python not on PATH. Install Python 3.11+."
}

Write-Host "== setup-kaggle-venv =="
Write-Host "Repo: $RepoRoot"
Write-Host "Profile: $Profile"

if (-not (Test-Path -LiteralPath $VenvDir)) {
    Write-Host "Creating .venv ..."
    & python -m venv $VenvDir
    if ($LASTEXITCODE -ne 0) {
        Write-Error "python -m venv failed (exit $LASTEXITCODE)"
    }
} else {
    Write-Host ".venv exists - reusing"
}

if (-not (Test-Path -LiteralPath $PipExe)) {
    Write-Error "pip not found in venv: $PipExe"
}

$pipArgs = @("install", "-r", $ReqFile)
if ($Upgrade) {
    $pipArgs += "--upgrade"
}

Write-Host "Installing from $(Split-Path $ReqFile -Leaf) ..."
& $PipExe @pipArgs
if ($LASTEXITCODE -ne 0) {
    Write-Error "pip install failed (exit $LASTEXITCODE)"
}

if (-not (Test-Path -LiteralPath $KaggleExe)) {
    Write-Error "kaggle.exe not found after install: $KaggleExe"
}

$versionOut = & $KaggleExe --version 2>&1
Write-Host "OK: $versionOut"
$RuffExe = Join-Path $VenvDir "Scripts\ruff.exe"
if (Test-Path -LiteralPath $RuffExe) {
    $ruffVer = & $RuffExe --version 2>&1
    Write-Host "OK: $ruffVer (Agent static-check / CLI — not the editor extension)"
} else {
    Write-Warning "ruff.exe missing in .venv — static-check will WARN. Ensure requirements-kaggle-cli.txt includes ruff."
}
if ($Profile -eq "sim") {
    $prevEap = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $simPy = Join-Path $VenvDir "Scripts\python.exe"
    & $simPy -c "import kaggle_environments; print('kaggle-environments', kaggle_environments.__version__)" 2>$null
    if ($LASTEXITCODE -ne 0) {
        $ErrorActionPreference = $prevEap
        Write-Error "kaggle_environments import failed"
    }
    $ErrorActionPreference = $prevEap
    Write-Host "OK: kaggle-environments import verified"
}
Write-Host ""
Write-Host "Next:"
Write-Host "  .\scripts\check-kaggle-cli.ps1"
Write-Host "  .\scripts\run-static-checks.ps1   # Agent code gate (before train)"
Write-Host "  .\.venv\Scripts\kaggle.exe auth login"
Write-Host "  .\scripts\kaggle-cli.ps1 --version"
if ($Profile -eq "cli") {
    Write-Host "  (local sim) .\scripts\setup-kaggle-venv.ps1 -Profile sim"
}
