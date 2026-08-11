#Requires -Version 5.1
<#
.SYNOPSIS
  Generic exp/work trash cleanup. Protects ROLE best_artifact from work-protect.json
  (and optional work/current-best link). Does not hardcode competition tip names.

.EXAMPLE
  .\scripts\cleanup-exp-work.ps1 -ExpDir ".\20260701-my-comp\exp"
  .\scripts\cleanup-exp-work.ps1 -ExpDir ".\exp" -Aggressive -IncludeOldArtifacts -PurgeWorkZips
#>
[CmdletBinding()]
param(
    [string]$ExpDir = "",
    [string]$CompRoot = "",
    [switch]$IncludeOldArtifacts,
    [switch]$IncludeTrashInputs,
    [switch]$IncludeKernelOutputs,
    [switch]$IncludeDonors,
    [switch]$PurgeWorkZips,
    [switch]$Aggressive,
    [double]$MinFreeGB = 0,
    [switch]$WhatIf
)

$ErrorActionPreference = "Continue"

function Resolve-ExpDir {
    param([string]$ExpDir, [string]$CompRoot, [string]$ScriptRoot)
    if ($ExpDir -and (Test-Path -LiteralPath $ExpDir)) {
        return (Resolve-Path -LiteralPath $ExpDir).Path
    }
    if (-not $CompRoot) {
        $CompRoot = Split-Path -Parent $ScriptRoot
    }
    $direct = Join-Path $CompRoot "exp"
    if (Test-Path -LiteralPath $direct) {
        return (Resolve-Path -LiteralPath $direct).Path
    }
    $found = Get-ChildItem -Path $CompRoot -Directory -ErrorAction SilentlyContinue |
        ForEach-Object {
            $p = Join-Path $_.FullName "exp"
            if (Test-Path -LiteralPath $p) { $p }
        } |
        Select-Object -First 1
    if ($found) { return (Resolve-Path -LiteralPath $found).Path }
    return $null
}

function Get-DiskFreeGB {
    $free = (Get-PSDrive C).Free
    return [math]::Round($free / 1GB, 2)
}

function Get-ProtectSets {
    param([string]$ExpDir, [string]$WorkDir)
    $dirs = New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
    $files = New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)

    $protectPath = Join-Path $ExpDir "work-protect.json"
    if (Test-Path -LiteralPath $protectPath) {
        try {
            $raw = [System.IO.File]::ReadAllText($protectPath, [System.Text.UTF8Encoding]::new($true))
            $doc = $raw | ConvertFrom-Json
            foreach ($key in @("best_artifact", "best_zip")) {
                $v = [string]$doc.$key
                if ($v) {
                    if ($v -like "*.zip") { [void]$files.Add((Split-Path -Leaf $v)) }
                    else { [void]$dirs.Add((Split-Path -Leaf $v)) }
                }
            }
            foreach ($d in @($doc.extra_protect_dirs)) {
                if ($d) { [void]$dirs.Add((Split-Path -Leaf ([string]$d))) }
            }
            foreach ($f in @($doc.extra_protect_files)) {
                if ($f) { [void]$files.Add((Split-Path -Leaf ([string]$f))) }
            }
        } catch {
            Write-Warning "work-protect.json parse failed: $($_.Exception.Message)"
        }
    } else {
        Write-Warning "work-protect.json missing under $ExpDir — only report/json patterns are hard-protected"
    }

    # Role link: exp/work/current-best -> actual artifact dir
    $link = Join-Path $WorkDir "current-best"
    if (Test-Path -LiteralPath $link) {
        try {
            $item = Get-Item -LiteralPath $link -Force
            $target = $null
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                # Directory symlink / junction
                if ($item.Target) {
                    $t0 = @($item.Target)[0]
                    if ($t0) { $target = $t0 }
                }
                if (-not $target) {
                    $target = (Get-Item -LiteralPath $link).FullName
                }
            } else {
                $target = $item.FullName
            }
            if ($target) {
                $leaf = Split-Path -Leaf $target
                if ($leaf -and $leaf -ne "current-best") {
                    [void]$dirs.Add($leaf)
                }
                # If current-best is a real folder containing files, protect the link name too
                [void]$dirs.Add("current-best")
            }
        } catch {
            Write-Warning "current-best resolve failed: $($_.Exception.Message)"
        }
    }

    return @{ Dirs = $dirs; Files = $files }
}

function Test-IsReportFile {
    param([string]$Name)
    return ($Name -like "verify-*-report.json") -or
        ($Name -like "compare-*.json") -or
        ($Name -like "validate-*-zip.json") -or
        ($Name -eq "work-protect.json")
}

function Remove-WorkPath {
    param([string]$Path, [string]$Label, [bool]$DoWhatIf)
    if ($DoWhatIf) {
        Write-Host "[whatif] remove: $Label"
        return
    }
    if (Test-Path -LiteralPath $Path) {
        Remove-Item -Recurse -Force -LiteralPath $Path -ErrorAction SilentlyContinue
    }
}

$ExpDirResolved = Resolve-ExpDir -ExpDir $ExpDir -CompRoot $CompRoot -ScriptRoot $PSScriptRoot
if (-not $ExpDirResolved) {
    Write-Host "exp/ not found (pass -ExpDir)"
    exit 0
}
$WorkDir = Join-Path $ExpDirResolved "work"
if (-not (Test-Path -LiteralPath $WorkDir)) {
    Write-Host "work dir not found: $WorkDir"
    exit 0
}

$protect = Get-ProtectSets -ExpDir $ExpDirResolved -WorkDir $WorkDir
Write-Host "[cleanup] ExpDir=$ExpDirResolved"
Write-Host "[cleanup] protected dirs: $(($protect.Dirs | Sort-Object) -join ', ')"
Write-Host "[cleanup] protected files: $(($protect.Files | Sort-Object) -join ', ')"

$doTrashInputs = [bool]$IncludeTrashInputs
$doKernels = [bool]$IncludeKernelOutputs
$doDonors = [bool]$IncludeDonors
$doOldArtifacts = [bool]$IncludeOldArtifacts
$doPurgeZips = [bool]$PurgeWorkZips
if ([bool]$Aggressive) {
    $doTrashInputs = $true
    $doKernels = $true
    $doDonors = $true
}

$removed = New-Object System.Collections.Generic.List[string]
$freeBefore = Get-DiskFreeGB
Write-Host "C: free before: $freeBefore GB"
$whatIf = [bool]$WhatIf

function Add-Removed([string]$Name) {
    if ($Name) { [void]$removed.Add($Name) }
}

# Always: profiling traces
Get-ChildItem $WorkDir -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -eq "ort-traces" -or $_.Name -like "ort-traces-*" -or $_.Name -like "*-traces*" } |
    ForEach-Object {
        if ($protect.Dirs.Contains($_.Name)) { return }
        Remove-WorkPath -Path $_.FullName -Label $_.Name -DoWhatIf $whatIf
        Add-Removed $_.Name
    }

# Aggressive / flags: kernel outputs
if ($doKernels) {
    Get-ChildItem $WorkDir -Directory -Filter "kernels-output-*" -ErrorAction SilentlyContinue |
        ForEach-Object {
            if ($protect.Dirs.Contains($_.Name)) { return }
            Remove-WorkPath -Path $_.FullName -Label $_.Name -DoWhatIf $whatIf
            Add-Removed $_.Name
        }
}

# mutation / heavy inputs
if ($doTrashInputs) {
    Get-ChildItem $WorkDir -Directory -ErrorAction SilentlyContinue |
        Where-Object {
            $_.Name -like "*-mutation-input*" -or
            $_.Name -like "wave*-mutation-input*" -or
            $_.Name -like "*-mutation-input"
        } |
        ForEach-Object {
            if ($protect.Dirs.Contains($_.Name)) { return }
            Remove-WorkPath -Path $_.FullName -Label $_.Name -DoWhatIf $whatIf
            Add-Removed $_.Name
        }
}

# donor dumps
if ($doDonors) {
    Get-ChildItem $WorkDir -Directory -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -like "*-donor-*" -or $_.Name -like "donor-*" } |
        ForEach-Object {
            if ($protect.Dirs.Contains($_.Name)) { return }
            Remove-WorkPath -Path $_.FullName -Label $_.Name -DoWhatIf $whatIf
            Add-Removed $_.Name
        }
}

# old artifact dirs (e.g. *-onnx) — explicit only
if ($doOldArtifacts) {
    Get-ChildItem $WorkDir -Directory -ErrorAction SilentlyContinue |
        Where-Object {
            $_.Name -like "*-onnx" -or
            $_.Name -like "*-artifact" -or
            $_.Name -like "artifact-*"
        } |
        ForEach-Object {
            if ($protect.Dirs.Contains($_.Name)) { return }
            if ($_.Name -eq "current-best") { return }
            Remove-WorkPath -Path $_.FullName -Label $_.Name -DoWhatIf $whatIf
            Add-Removed $_.Name
        }
}

# work zips — explicit only
if ($doPurgeZips) {
    Get-ChildItem $WorkDir -File -Filter "*-submission.zip" -ErrorAction SilentlyContinue |
        ForEach-Object {
            if ($protect.Files.Contains($_.Name)) { return }
            if (Test-IsReportFile -Name $_.Name) { return }
            Remove-WorkPath -Path $_.FullName -Label $_.Name -DoWhatIf $whatIf
            Add-Removed $_.Name
        }
}

$freeAfter = Get-DiskFreeGB
$freed = [math]::Round($freeAfter - $freeBefore, 2)

if ($removed.Count -eq 0) {
    Write-Host "nothing to clean under $WorkDir"
} else {
    Write-Host "cleaned $($removed.Count) items"
    if ($removed.Count -le 20) {
        Write-Host "  $($removed -join ', ')"
    } else {
        $head = ($removed[0..9] -join ', ')
        Write-Host "  $head ... (+$($removed.Count - 10) more)"
    }
}
Write-Host "C: free after: $freeAfter GB (freed ~$freed GB)"

if ($MinFreeGB -gt 0 -and $freeAfter -lt $MinFreeGB) {
    Write-Warning "free space $freeAfter GB is below target $MinFreeGB GB"
    exit 2
}
exit 0
