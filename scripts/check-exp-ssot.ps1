#Requires -Version 5.1
<#
.SYNOPSIS
  Treat exp-index as standing SSOT; flag Best/score re-stated in checklist header.

.PARAMETER CompRoot
  Competition root (.cursor / scripts). Default: parent of scripts parent.

.PARAMETER ExpDir
  Path to exp/. Default: CompRoot\exp or first */exp under CompRoot.

.PARAMETER ActiveMaxLines
  Soft cap for Active/Pending section length (WARN). Default 120.

.EXAMPLE
  .\scripts\check-exp-ssot.ps1 -CompRoot "<DESKTOP>/MyComp"
#>
[CmdletBinding()]
param(
    [string]$CompRoot = "",
    [string]$ExpDir = "",
    [int]$ActiveMaxLines = 120
)

$ErrorActionPreference = "Continue"
$script:fail = 0
$script:warn = 0

function Write-Fail([string]$Msg) {
    Write-Host "[exp-ssot] FAIL: $Msg" -ForegroundColor Red
    $script:fail++
}
function Write-WarnMsg([string]$Msg) {
    Write-Host "[exp-ssot] WARN: $Msg" -ForegroundColor Yellow
    $script:warn++
}
function Write-Ok([string]$Msg) {
    Write-Host "[exp-ssot] OK: $Msg" -ForegroundColor Green
}

if (-not $CompRoot) {
    $CompRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
    if (-not (Test-Path (Join-Path $CompRoot ".cursor"))) {
        $CompRoot = Split-Path -Parent $PSScriptRoot
    }
}
$CompRoot = (Resolve-Path -LiteralPath $CompRoot).Path

if (-not $ExpDir) {
    $candidate = Join-Path $CompRoot "exp"
    if (Test-Path (Join-Path $candidate "exp-index.md")) {
        $ExpDir = $candidate
    } else {
        $found = Get-ChildItem -Path $CompRoot -Directory -ErrorAction SilentlyContinue |
            ForEach-Object {
                $p = Join-Path $_.FullName "exp\exp-index.md"
                if (Test-Path -LiteralPath $p) { Join-Path $_.FullName "exp" }
            } |
            Select-Object -First 1
        if ($found) { $ExpDir = $found }
    }
}

if (-not $ExpDir -or -not (Test-Path -LiteralPath $ExpDir)) {
    Write-Fail "exp/ not found under CompRoot=$CompRoot (pass -ExpDir)"
    exit 1
}
$ExpDir = (Resolve-Path -LiteralPath $ExpDir).Path
Write-Host "[exp-ssot] CompRoot=$CompRoot"
Write-Host "[exp-ssot] ExpDir=$ExpDir"

$indexPath = Join-Path $ExpDir "exp-index.md"
$checklistPath = Join-Path $ExpDir "experiment-checklist.md"

if (-not (Test-Path -LiteralPath $indexPath)) {
    Write-Fail "missing $indexPath"
} else {
    $index = Get-Content -LiteralPath $indexPath -Raw -ErrorAction SilentlyContinue
    # Section title may be Japanese "genzaichi" heading
    if ($index -notmatch '(?m)^##\s+.+' ) {
        Write-WarnMsg "exp-index.md has no ## section"
    } else {
        Write-Ok "exp-index.md present"
    }
}

if (-not (Test-Path -LiteralPath $checklistPath)) {
    Write-WarnMsg "experiment-checklist.md missing (skip checklist checks)"
} else {
    $lines = @(Get-Content -LiteralPath $checklistPath -ErrorAction SilentlyContinue)
    if ($lines.Count -eq 0) {
        Write-WarnMsg "checklist empty"
    } else {
        $headerEnd = $lines.Count
        for ($i = 0; $i -lt $lines.Count; $i++) {
            $line = $lines[$i]
            if ($line -match '^##\s+(Active|Pending|Archive|Done|Rejected)\b') {
                $headerEnd = $i
                break
            }
            if ($line -match '^##\s+.*Pending') {
                $headerEnd = $i
                break
            }
            if ($line -match '^##\s+.*Archive') {
                $headerEnd = $i
                break
            }
        }

        $header = ""
        if ($headerEnd -gt 0) {
            $header = ($lines[0..($headerEnd - 1)] -join "`n")
        }

        $hit = $false
        if ($header -match 'Best\s+SUB-\d+') { $hit = $true }
        if ($header -match 'SUB-\d+\s+Best') { $hit = $true }
        if ($header -match 'Public\s+LB') { $hit = $true }
        if ($header -match 'LB\s+\*?\*?\d{3,}') { $hit = $true }
        if ($header -match 'rolling\s+tip\s*=') { $hit = $true }
        if ($header -match 'patch-chk\d+') { $hit = $true }

        if ($hit) {
            Write-Fail "checklist header re-states Best/LB/tip. Put standing only in exp-index.md; header may link only."
        } else {
            Write-Ok "checklist header has no Best/LB/tip re-state patterns"
        }

        $activeStart = -1
        $activeEnd = $lines.Count
        for ($i = 0; $i -lt $lines.Count; $i++) {
            $line = $lines[$i]
            $isActive = $false
            if ($line -match '^##\s+(Active|Pending)\b') { $isActive = $true }
            if ($line -match '^##\s+.*Pending') { $isActive = $true }
            if ($isActive) {
                $activeStart = $i
                for ($j = $i + 1; $j -lt $lines.Count; $j++) {
                    if ($lines[$j] -match '^##\s+') {
                        $activeEnd = $j
                        break
                    }
                }
                break
            }
        }

        if ($activeStart -ge 0) {
            $activeLen = $activeEnd - $activeStart
            if ($activeLen -gt $ActiveMaxLines) {
                Write-WarnMsg "Active/Pending section is $activeLen lines (guide <= $ActiveMaxLines). Move done rows to checklist-archive."
            } else {
                Write-Ok "Active/Pending section length=$activeLen (guide <= $ActiveMaxLines)"
            }
            if ($activeEnd -gt $activeStart) {
                $activeText = ($lines[$activeStart..($activeEnd - 1)] -join "`n")
                $doneInActive = ([regex]::Matches($activeText, 'done\s+GO|done\s+NO-GO|\*\*done')).Count
                if ($doneInActive -ge 8) {
                    Write-WarnMsg "Active section contains many done markers ($doneInActive). Prefer archive for finished CHK rows."
                }

                $chkLines = @(
                    $lines[$activeStart..($activeEnd - 1)] |
                        Where-Object { $_ -match 'CHK-\d+' -and $_.TrimStart().StartsWith('-') }
                )
                if ($chkLines.Count -gt 0) {
                    $missingLane = @($chkLines | Where-Object { $_ -notmatch 'lane\s*:' })
                    if ($missingLane.Count -gt 0) {
                        Write-WarnMsg ("Active CHK lines without lane: = {0}/{1}. Add lane:primary|public|diagnostic." -f `
                            $missingLane.Count, $chkLines.Count)
                    }
                    else {
                        Write-Ok "Active CHK lines include lane: ($($chkLines.Count))"
                    }
                }
            }
        } else {
            Write-WarnMsg "no Active/Pending section heading found"
        }
    }
}

# cv-design soft gate (parent docs-ja)
$cvCandidates = @(
    (Join-Path (Split-Path $ExpDir -Parent) "docs-ja\cv-design.md"),
    (Join-Path $CompRoot "docs-ja\cv-design.md")
)
$cvFound = $false
foreach ($cv in $cvCandidates) {
    if (Test-Path -LiteralPath $cv) {
        $cvFound = $true
        $cvBody = Get-Content -LiteralPath $cv -Raw -ErrorAction SilentlyContinue
        if ($cvBody -notmatch 'cv_unit|cv-unit|GroupKFold|分割単位|unit:\s*(row|group|time|custom)') {
            Write-WarnMsg "cv-design.md present but no clear cv_unit declaration ($cv)"
        }
        else {
            Write-Ok "cv-design.md has unit signals ($cv)"
        }
        break
    }
}
if (-not $cvFound) {
    Write-WarnMsg "docs-ja/cv-design.md not found near exp/ — declare before primary CV work"
}

$agentsList = @(
    (Join-Path $CompRoot "AGENTS.md"),
    (Join-Path (Split-Path $CompRoot -Parent) "AGENTS.md")
)
foreach ($agentsCand in $agentsList) {
    if (Test-Path -LiteralPath $agentsCand) {
        $ag = Get-Content -LiteralPath $agentsCand -Raw -ErrorAction SilentlyContinue
        $hasScore = ($ag -match 'Public\s+LB' -and $ag -match '\d{3,}')
        $pointsToIndex = ($ag -match 'exp-index\.md' -and $ag -match 'kaggle-exp-ssot|SSOT')
        if ($hasScore -and -not $pointsToIndex) {
            Write-WarnMsg "AGENTS.md appears to hardcode Best/LB without pointing to exp-index. ($agentsCand)"
        } elseif ($hasScore -and $pointsToIndex) {
            Write-Ok "AGENTS.md has standing snapshot but points to exp-index SSOT"
        }
        break
    }
}

Write-Host ""
Write-Host "[exp-ssot] fail=$($script:fail) warn=$($script:warn)"
if ($script:fail -gt 0) { exit 1 }
exit 0
