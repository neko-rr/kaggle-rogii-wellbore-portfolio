#Requires -Version 5.1
<#
.SYNOPSIS
  Kaggle push 前に Notebook / Dataset / Model が Private 設定か検証する。

.DESCRIPTION
  - kernel-metadata.json: is_private が true（必須）
  - dataset-metadata.json: isPrivate が true（必須）
  - model-metadata.json: isPrivate が true（必須）
  FAIL なら exit 1（push 禁止）

.EXAMPLE
  .\scripts\assert-kaggle-private.ps1 -KernelDir my-notebook\planned\chk-363-g2-screen-s0
  .\scripts\assert-kaggle-private.ps1 -DatasetDir exp\work\chk363-g2-screen-input
#>
[CmdletBinding()]
param(
    [string[]]$KernelDir = @(),
    [string[]]$DatasetDir = @(),
    [string[]]$ModelDir = @()
)

$ErrorActionPreference = "Stop"
$failed = 0

function Test-JsonBoolTrue {
    param(
        [Parameter(Mandatory = $true)][object]$Obj,
        [Parameter(Mandatory = $true)][string]$Key,
        [Parameter(Mandatory = $true)][string]$Path
    )
    if ($null -eq $Obj.PSObject.Properties[$Key]) {
        Write-Host "FAIL: missing '$Key' in $Path" -ForegroundColor Red
        return $false
    }
    $v = $Obj.$Key
    # JSON true may deserialize as Boolean; also accept string "true"
    $ok = ($v -is [bool] -and $v -eq $true) -or ("$v" -eq "True") -or ("$v" -eq "true")
    if (-not $ok) {
        Write-Host "FAIL: $Key=$v (want true) in $Path" -ForegroundColor Red
        return $false
    }
    Write-Host "OK: $Key=true ($Path)"
    return $true
}

function Read-MetadataJson {
    param([string]$Path)
    try {
        return (Get-Content -Raw -Encoding UTF8 -LiteralPath $Path | ConvertFrom-Json)
    } catch {
        Write-Host "FAIL: metadata read/parse error ($Path): $($_.Exception.Message)" -ForegroundColor Red
        throw
    }
}

function Test-RequiredText {
    param([object]$Obj, [string]$Key, [string]$Path)
    if ($null -eq $Obj.PSObject.Properties[$Key] -or [string]::IsNullOrWhiteSpace([string]$Obj.$Key)) {
        Write-Host "FAIL: missing/empty '$Key' in $Path" -ForegroundColor Red
        return $false
    }
    Write-Host "OK: $Key=$($Obj.$Key)"
    return $true
}

function Assert-KernelPrivate {
    param([string]$Dir)
    $metaPath = Join-Path $Dir "kernel-metadata.json"
    if (-not (Test-Path $metaPath)) {
        Write-Host "FAIL: missing kernel-metadata.json under $Dir" -ForegroundColor Red
        return $false
    }
    $meta = Read-MetadataJson -Path $metaPath
    $ok = Test-JsonBoolTrue -Obj $meta -Key "is_private" -Path $metaPath
    $ok = (Test-RequiredText -Obj $meta -Key "id" -Path $metaPath) -and $ok
    $ok = (Test-RequiredText -Obj $meta -Key "title" -Path $metaPath) -and $ok
    $ok = (Test-RequiredText -Obj $meta -Key "code_file" -Path $metaPath) -and $ok

    if ($meta.id -and "$($meta.id)" -notmatch '^[^/]+/[^/]+$') {
        Write-Host "FAIL: kernel id must be <owner>/<slug>: $($meta.id)" -ForegroundColor Red
        $ok = $false
    }
    if ($meta.code_file) {
        $codePath = Join-Path $Dir ([string]$meta.code_file)
        if (-not (Test-Path -LiteralPath $codePath -PathType Leaf)) {
            Write-Host "FAIL: code_file not found: $codePath" -ForegroundColor Red
            $ok = $false
        } else {
            Write-Host "OK: code_file exists ($codePath)"
        }
    }
    if ($null -eq $meta.PSObject.Properties["enable_gpu"] -or $meta.enable_gpu -isnot [bool]) {
        Write-Host "FAIL: enable_gpu must be explicit JSON true/false in $metaPath" -ForegroundColor Red
        $ok = $false
    } else {
        $lane = if ($meta.enable_gpu) { "GPU" } else { "CPU" }
        Write-Host "OK: execution lane=$lane"
    }
    return $ok
}

function Assert-DatasetPrivate {
    param([string]$Dir)
    $metaPath = Join-Path $Dir "dataset-metadata.json"
    if (-not (Test-Path $metaPath)) {
        Write-Host "FAIL: missing dataset-metadata.json under $Dir" -ForegroundColor Red
        return $false
    }
    $meta = Read-MetadataJson -Path $metaPath
    return (Test-JsonBoolTrue -Obj $meta -Key "isPrivate" -Path $metaPath)
}

function Assert-ModelPrivate {
    param([string]$Dir)
    $metaPath = Join-Path $Dir "model-metadata.json"
    if (-not (Test-Path $metaPath)) {
        Write-Host "FAIL: missing model-metadata.json under $Dir" -ForegroundColor Red
        return $false
    }
    $meta = Read-MetadataJson -Path $metaPath
    return (Test-JsonBoolTrue -Obj $meta -Key "isPrivate" -Path $metaPath)
}

if ($KernelDir.Count -eq 0 -and $DatasetDir.Count -eq 0 -and $ModelDir.Count -eq 0) {
    Write-Host "FAIL: specify -KernelDir and/or -DatasetDir and/or -ModelDir" -ForegroundColor Red
    exit 1
}

foreach ($d in $KernelDir) {
    if (-not (Assert-KernelPrivate -Dir $d)) { $failed++ }
}
foreach ($d in $DatasetDir) {
    if (-not (Assert-DatasetPrivate -Dir $d)) { $failed++ }
}
foreach ($d in $ModelDir) {
    if (-not (Assert-ModelPrivate -Dir $d)) { $failed++ }
}

if ($failed -gt 0) {
    Write-Host "assert-kaggle-private: $failed check(s) failed — refuse push" -ForegroundColor Red
    exit 1
}
Write-Host "assert-kaggle-private: PASS"
exit 0
