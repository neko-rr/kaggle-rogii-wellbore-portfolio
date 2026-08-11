#Requires -Version 5.1
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ArtifactPath,
    [Parameter(Mandatory = $true)]
    [ValidateSet("lora", "csv", "simulation", "notebook-output")]
    [string]$Profile,
    [string]$ExpectedColumns,
    [int]$ExpectedRows = -1,
    [string]$OutputPath = "",
    [string]$CompInner = "",
    [string]$LogPath = ""
)

$ErrorActionPreference = "Stop"
$errors = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]
$checks = New-Object System.Collections.Generic.List[string]

function Add-Check([string]$m) { $checks.Add("- [x] $m") | Out-Null }
function Add-Error([string]$m) { $errors.Add("- [ ] $m") | Out-Null }
function Add-Warn([string]$m) { $warnings.Add("- [!] $m") | Out-Null }

function Test-SecretPattern([string]$text) {
    $patterns = @(
        'AKIA[0-9A-Z]{16}',
        '(?i)api[_-]?key.{0,20}[A-Za-z0-9_\-]{16,}',
        '(?i)secret.{0,20}[A-Za-z0-9_\-]{16,}',
        '(?i)token.{0,20}[A-Za-z0-9_\-]{16,}'
    )
    foreach ($p in $patterns) {
        if ($text -match $p) { return $true }
    }
    return $false
}

function Write-Log([string]$content) {
    if ([string]::IsNullOrWhiteSpace($LogPath)) { return }
    $dir = Split-Path -Parent $LogPath
    if (-not [string]::IsNullOrWhiteSpace($dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    Set-Content -Path $LogPath -Value $content -Encoding UTF8
}

if (-not (Test-Path -LiteralPath $ArtifactPath)) {
    Add-Error "artifact not found: $ArtifactPath"
} else {
    $artifact = Get-Item -LiteralPath $ArtifactPath
    if ($artifact.Length -le 0) { Add-Error "artifact is 0 byte: $ArtifactPath" }
    else { Add-Check "artifact exists" }
}

$extension = [System.IO.Path]::GetExtension($ArtifactPath).ToLowerInvariant()
switch ($Profile) {
    "lora" { if ($extension -ne ".zip") { Add-Error "lora requires .zip" } else { Add-Check "lora extension ok" } }
    "csv" { if ($extension -ne ".csv") { Add-Error "csv profile requires .csv" } else { Add-Check "csv extension ok" } }
    "simulation" {
        if (($extension -ne ".py") -and ($extension -ne ".gz")) { Add-Error "simulation requires main.py or .tar.gz" }
        else { Add-Check "simulation extension ok" }
    }
    "notebook-output" { Add-Check "notebook-output profile selected" }
}

if ((Test-Path -LiteralPath $ArtifactPath) -and ($extension -in @(".py", ".csv", ".md", ".txt"))) {
    $raw = Get-Content -LiteralPath $ArtifactPath -Raw -Encoding UTF8
    if (Test-SecretPattern $raw) { Add-Warn "possible secret pattern found" }
    else { Add-Check "basic secret scan passed" }
} else {
    Add-Warn "secret scan skipped for binary/zip"
}

if (-not [string]::IsNullOrWhiteSpace($CompInner)) {
    $timelinePath = Join-Path $CompInner "docs-ja\comp-timeline.md"
    if (Test-Path -LiteralPath $timelinePath) {
        $timeline = Get-Content -LiteralPath $timelinePath -Raw -Encoding UTF8
        if ($timeline -match 'final-submit.*(closed|ended|expired)') { Add-Warn "final-submit appears closed" }
        else { Add-Check "timeline found (final-submit not marked closed)" }
    }
}

if (($errors.Count -eq 0) -and (Test-Path -LiteralPath $ArtifactPath)) {
    switch ($Profile) {
        "lora" {
            $tmpDir = Join-Path ([System.IO.Path]::GetTempPath()) ("validate-lora-" + [guid]::NewGuid().ToString())
            New-Item -ItemType Directory -Path $tmpDir | Out-Null
            try {
                Expand-Archive -LiteralPath $ArtifactPath -DestinationPath $tmpDir -Force
                $config = Get-ChildItem -LiteralPath $tmpDir -Recurse -File | Where-Object { $_.Name -eq "adapter_config.json" } | Select-Object -First 1
                if (-not $config) {
                    Add-Error "adapter_config.json not found in zip"
                } else {
                    Add-Check "adapter_config.json exists"
                    $json = Get-Content -LiteralPath $config.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
                    $rank = $null
                    if ($null -ne $json.r) { $rank = [int]$json.r }
                    elseif ($null -ne $json.rank) { $rank = [int]$json.rank }
                    if ($null -eq $rank) { Add-Error "rank (r/rank) missing in adapter_config.json" }
                    elseif ($rank -gt 32) { Add-Error "rank=$rank exceeds max 32" }
                    else { Add-Check "rank=$rank <= 32" }
                }
            } finally {
                if (Test-Path -LiteralPath $tmpDir) { Remove-Item -LiteralPath $tmpDir -Recurse -Force }
            }
        }
        "csv" {
            $rows = Import-Csv -LiteralPath $ArtifactPath
            if ($rows.Count -eq 0) { Add-Error "csv has no rows" } else { Add-Check "csv rows=$($rows.Count)" }
            if ($ExpectedRows -ge 0 -and $rows.Count -ne $ExpectedRows) { Add-Error "expected rows=$ExpectedRows, actual=$($rows.Count)" }

            $columns = @()
            if ($rows.Count -gt 0) { $columns = $rows[0].PSObject.Properties.Name }
            if (-not [string]::IsNullOrWhiteSpace($ExpectedColumns)) {
                $required = $ExpectedColumns.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
                foreach ($col in $required) {
                    if ($columns -notcontains $col) { Add-Error "missing required column: $col" }
                }
                Add-Check "required column check executed"
            }

            $idCol = $null
            foreach ($candidate in @("row_id", "id")) {
                if ($columns -contains $candidate) { $idCol = $candidate; break }
            }
            if ($null -ne $idCol) {
                $dup = $rows | Group-Object -Property $idCol | Where-Object { $_.Count -gt 1 } | Select-Object -First 1
                if ($dup) { Add-Error "duplicate value in ${idCol}: $($dup.Name)" }
                else { Add-Check "$idCol has no duplicates" }
            } else {
                Add-Warn "row_id/id column not found; duplicate check skipped"
            }
        }
        "simulation" {
            if ($extension -eq ".py") {
                $script = Get-Content -LiteralPath $ArtifactPath -Raw -Encoding UTF8
                if ($script -match 'def\s+agent\s*\(') { Add-Check "main.py contains agent()" }
                else { Add-Error "main.py missing agent()" }
            } else {
                $tmpDir = Join-Path ([System.IO.Path]::GetTempPath()) ("validate-sim-" + [guid]::NewGuid().ToString())
                New-Item -ItemType Directory -Path $tmpDir | Out-Null
                try {
                    tar -xzf $ArtifactPath -C $tmpDir | Out-Null
                    $mainPy = Join-Path $tmpDir "main.py"
                    if (-not (Test-Path -LiteralPath $mainPy)) {
                        Add-Error "main.py not found at archive root"
                    } else {
                        $script = Get-Content -LiteralPath $mainPy -Raw -Encoding UTF8
                        if ($script -match 'def\s+agent\s*\(') { Add-Check "archive main.py contains agent()" }
                        else { Add-Error "archive main.py missing agent()" }
                    }
                } finally {
                    if (Test-Path -LiteralPath $tmpDir) { Remove-Item -LiteralPath $tmpDir -Recurse -Force }
                }
            }
        }
        "notebook-output" {
            if ([string]::IsNullOrWhiteSpace($OutputPath)) { Add-Warn "OutputPath not provided; output check skipped" }
            elseif (Test-Path -LiteralPath $OutputPath) { Add-Check "OutputPath exists" }
            else { Add-Error "OutputPath not found: $OutputPath" }
        }
    }
}

$status = "PASS"
if ($errors.Count -gt 0) { $status = "FAIL" }
elseif ($warnings.Count -gt 0) { $status = "PASS-WITH-WARNINGS" }

$summary = @()
$summary += "# Submission Validation (auto)"
$summary += ""
$summary += "- status: $status"
$summary += "- profile: $Profile"
$summary += "- artifact: $ArtifactPath"
$summary += ""
$summary += "## Checks"
$summary += $checks
if ($warnings.Count -gt 0) {
    $summary += ""
    $summary += "## Warnings"
    $summary += $warnings
}
if ($errors.Count -gt 0) {
    $summary += ""
    $summary += "## Errors"
    $summary += $errors
}

$summaryText = ($summary -join "`n")
Write-Host $summaryText
Write-Log $summaryText

if ($status -eq "FAIL") { exit 1 }
exit 0
