# Fetch leaderboard + solution discussion intel (OAuth .venv)
# Usage: .\scripts\fetch-solution-intel.ps1 -Competition orbit-wars [-TopN 10] [-FetchBodies] [-Phase during-comp|post-comp]
param(
    [Parameter(Mandatory = $true)]
    [string]$Competition,
    [int]$TopN = 10,
    [int]$MaxTopics = 20,
    [ValidateSet("during-comp", "post-comp")]
    [string]$Phase = "during-comp",
    [switch]$FetchBodies,
    [string]$OutDir = ""
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Python = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$Script = Join-Path $PSScriptRoot "fetch-solution-intel.py"

if (-not (Test-Path -LiteralPath $Python)) {
    Write-Error ".venv not found. Run .\scripts\setup-kaggle-venv.ps1 first."
}

$argsList = @($Script, $Competition, "--top-n", "$TopN", "--max-topics", "$MaxTopics", "--phase", $Phase)
if ($FetchBodies) { $argsList += "--fetch-bodies" }
if ($OutDir) { $argsList += @("--out-dir", $OutDir) }

& $Python @argsList
exit $LASTEXITCODE
