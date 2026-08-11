# Setup local kernel reproduction workspace (tabular / notebook comps)
# Usage: .\scripts\setup-kernel-workspace.ps1 -Kernel "owner/slug-or-url" [-Competition slug] [-DownloadInputs]
param(
    [Parameter(Mandatory = $true)]
    [string]$Kernel,
    [string]$Competition = "",
    [switch]$DownloadInputs,
    [switch]$SkipCompetition,
    [string]$OutDir = ""
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Python = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$Script = Join-Path $PSScriptRoot "setup-kernel-workspace.py"

if (-not (Test-Path -LiteralPath $Python)) {
    Write-Error ".venv not found. Run .\scripts\setup-kaggle-venv.ps1 first."
}

$argsList = @($Script, $Kernel)
if ($Competition) { $argsList += @("--competition", $Competition) }
if ($OutDir) { $argsList += @("--out-dir", $OutDir) }
if ($DownloadInputs) { $argsList += "--download-inputs" }
if ($SkipCompetition) { $argsList += "--skip-competition" }

& $Python @argsList
exit $LASTEXITCODE
