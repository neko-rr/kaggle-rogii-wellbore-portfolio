#Requires -Version 5.1
<#
.SYNOPSIS
  コンペ固有の散乱生成物を artifact-routing.json に従って exp/work へ整理する。

.DESCRIPTION
  - 既定はドライラン。実移動には -Apply が必要
  - source_roots の直下だけを見る（再帰しない）
  - 未登録パターンは触らない
  - 削除しない。移動履歴を exp/work/generated-files-log.jsonl に残す

.EXAMPLE
  .\scripts\organize-generated-files.ps1 -ExpDir ".\20260701-my-comp\exp"
  .\scripts\organize-generated-files.ps1 -ExpDir ".\20260701-my-comp\exp" -Apply
#>
[CmdletBinding()]
param(
    [string]$ExpDir = "",
    [string]$CompRoot = "",
    [string]$RepoRoot = "",
    [string]$RouteFile = "",
    [int]$MaxPreview = 20,
    [switch]$Apply
)

$ErrorActionPreference = "Stop"

function Resolve-Directory {
    param([string]$Path, [string]$Label)
    if (-not $Path -or -not (Test-Path -LiteralPath $Path -PathType Container)) {
        throw "$Label not found: $Path"
    }
    return (Resolve-Path -LiteralPath $Path).Path
}

function Resolve-ExpDirectory {
    param([string]$ExplicitExp, [string]$ExplicitComp, [string]$DefaultRepo)
    if ($ExplicitExp) {
        return (Resolve-Directory -Path $ExplicitExp -Label "ExpDir")
    }
    if ($ExplicitComp) {
        $candidate = Join-Path $ExplicitComp "exp"
        return (Resolve-Directory -Path $candidate -Label "ExpDir")
    }
    $direct = Join-Path $DefaultRepo "exp"
    if (Test-Path -LiteralPath $direct -PathType Container) {
        return (Resolve-Path -LiteralPath $direct).Path
    }
    $found = Get-ChildItem -LiteralPath $DefaultRepo -Directory -ErrorAction SilentlyContinue |
        ForEach-Object {
            $candidate = Join-Path $_.FullName "exp"
            if (Test-Path -LiteralPath $candidate -PathType Container) { $candidate }
        } |
        Select-Object -First 1
    if (-not $found) {
        throw "exp/ not found. Pass -ExpDir."
    }
    return (Resolve-Path -LiteralPath $found).Path
}

function Resolve-SourceRoot {
    param([string]$Value, [string]$Repo, [string]$Comp)
    if ($Value -eq "repo-root") { return $Repo }
    if ($Value -eq "comp-root") { return $Comp }
    if ([IO.Path]::IsPathRooted($Value)) {
        return (Resolve-Directory -Path $Value -Label "source_root")
    }
    return (Resolve-Directory -Path (Join-Path $Comp $Value) -Label "source_root")
}

function Get-SafeDestinationRoot {
    param([string]$Exp, [string]$Relative)
    if ([string]::IsNullOrWhiteSpace($Relative)) {
        throw "route destination is empty"
    }
    $expFull = [IO.Path]::GetFullPath($Exp).TrimEnd('\')
    $destFull = [IO.Path]::GetFullPath((Join-Path $Exp $Relative)).TrimEnd('\')
    if (-not $destFull.StartsWith($expFull + "\", [StringComparison]::OrdinalIgnoreCase)) {
        throw "route destination must stay under exp/: $Relative"
    }
    return $destFull
}

function Get-DateBucket {
    param([string]$Name, [string]$DateRegex)
    if ($DateRegex) {
        $match = [regex]::Match($Name, $DateRegex)
        if ($match.Success) {
            if ($match.Groups["date"].Success) {
                return $match.Groups["date"].Value
            }
            if ($match.Groups.Count -gt 1) {
                return $match.Groups[1].Value
            }
        }
    }
    return "undated"
}

function Get-CollisionSafePath {
    param([string]$Target, [string]$Source)
    if (-not (Test-Path -LiteralPath $Target)) { return $Target }
    $hash = (Get-FileHash -LiteralPath $Source -Algorithm SHA256).Hash.Substring(0, 8).ToLowerInvariant()
    $dir = Split-Path -Parent $Target
    $base = [IO.Path]::GetFileNameWithoutExtension($Target)
    $ext = [IO.Path]::GetExtension($Target)
    return (Join-Path $dir "$base-$hash$ext")
}

function Add-JsonLine {
    param([string]$Path, [object]$Data)
    $parent = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    $encoding = New-Object System.Text.UTF8Encoding($false)
    $writer = $null
    try {
        $writer = New-Object System.IO.StreamWriter($Path, $true, $encoding)
        $writer.WriteLine(($Data | ConvertTo-Json -Compress -Depth 8))
    } catch {
        Write-Host "ERROR: move log write failed ($Path): $($_.Exception.Message)" -ForegroundColor Red
        throw
    } finally {
        if ($writer) { $writer.Dispose() }
    }
}

if (-not $RepoRoot) {
    $RepoRoot = Split-Path -Parent $PSScriptRoot
}
$RepoRoot = Resolve-Directory -Path $RepoRoot -Label "RepoRoot"
$ExpDir = Resolve-ExpDirectory -ExplicitExp $ExpDir -ExplicitComp $CompRoot -DefaultRepo $RepoRoot
if (-not $CompRoot) {
    $CompRoot = Split-Path -Parent $ExpDir
}
$CompRoot = Resolve-Directory -Path $CompRoot -Label "CompRoot"

if (-not $RouteFile) {
    $RouteFile = Join-Path $ExpDir "artifact-routing.json"
}
if (-not (Test-Path -LiteralPath $RouteFile -PathType Leaf)) {
    throw "artifact routing file not found: $RouteFile"
}

try {
    $routing = Get-Content -LiteralPath $RouteFile -Raw -Encoding UTF8 | ConvertFrom-Json
} catch {
    Write-Host "ERROR: routing JSON read/parse failed ($RouteFile): $($_.Exception.Message)" -ForegroundColor Red
    throw
}

$sources = New-Object System.Collections.Generic.List[string]
foreach ($sourceValue in @($routing.source_roots)) {
    $resolved = Resolve-SourceRoot -Value ([string]$sourceValue) -Repo $RepoRoot -Comp $CompRoot
    if (-not $sources.Contains($resolved)) {
        [void]$sources.Add($resolved)
    }
}

$plans = New-Object System.Collections.Generic.List[object]
foreach ($route in @($routing.routes)) {
    if ($null -ne $route.enabled -and -not [bool]$route.enabled) { continue }
    $pattern = [string]$route.pattern
    if ([string]::IsNullOrWhiteSpace($pattern)) { continue }
    $destRoot = Get-SafeDestinationRoot -Exp $ExpDir -Relative ([string]$route.destination)
    foreach ($sourceRoot in $sources) {
        Get-ChildItem -LiteralPath $sourceRoot -File -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -like $pattern } |
            ForEach-Object {
                $bucket = Get-DateBucket -Name $_.Name -DateRegex ([string]$route.date_regex)
                $targetDir = Join-Path $destRoot $bucket
                $target = Get-CollisionSafePath -Target (Join-Path $targetDir $_.Name) -Source $_.FullName
                $plans.Add([PSCustomObject]@{
                    RouteId = [string]$route.id
                    Role = [string]$route.role
                    Source = $_.FullName
                    Target = $target
                    Bytes = [int64]$_.Length
                })
            }
    }
}

$mode = if ($Apply) { "APPLY" } else { "DRY-RUN" }
$totalBytes = [int64](($plans | Measure-Object -Property Bytes -Sum).Sum)
Write-Host "[organize] mode=$mode"
Write-Host "[organize] ExpDir=$ExpDir"
Write-Host "[organize] routes=$(@($routing.routes).Count) files=$($plans.Count) size=$([math]::Round($totalBytes / 1MB, 2)) MB"

$preview = @($plans | Select-Object -First $MaxPreview)
foreach ($plan in $preview) {
    Write-Host "[$($plan.RouteId)] $($plan.Source) -> $($plan.Target)"
}
if ($plans.Count -gt $preview.Count) {
    Write-Host "... (+$($plans.Count - $preview.Count) more)"
}

if (-not $Apply) {
    Write-Host "[organize] no files moved. Re-run with -Apply after review."
    exit 0
}

$logPath = Join-Path $ExpDir "work\generated-files-log.jsonl"
foreach ($plan in $plans) {
    try {
        $targetDir = Split-Path -Parent $plan.Target
        if (-not (Test-Path -LiteralPath $targetDir)) {
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        }
        Move-Item -LiteralPath $plan.Source -Destination $plan.Target -ErrorAction Stop
        Add-JsonLine -Path $logPath -Data ([ordered]@{
            timestamp = [DateTime]::UtcNow.ToString("o")
            route_id = $plan.RouteId
            role = $plan.Role
            source = $plan.Source
            target = $plan.Target
            bytes = $plan.Bytes
        })
    } catch {
        Write-Host "ERROR: generated file move failed ($($plan.Source)): $($_.Exception.Message)" -ForegroundColor Red
        throw
    }
}

Write-Host "[organize] moved=$($plans.Count) log=$logPath"
exit 0
