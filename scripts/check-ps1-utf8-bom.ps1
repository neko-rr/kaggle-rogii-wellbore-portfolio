#Requires -Version 5.1
<#
.SYNOPSIS
  PowerShell 5.1 向け: 日本語等を含む .ps1 が UTF-8 BOM 付きか検査する。

.DESCRIPTION
  PS 5.1 は BOM 無し UTF-8 を ANSI (CP932 等) と誤読し、日本語入り .ps1 で構文エラーになる。
  判定:
    - 先頭が EF BB BF → PASS
    - BOM 無しかつ非 ASCII あり → FAIL（-Fix で BOM 付与）
    - BOM 無しかつ ASCII のみ → PASS（警告なし）

.EXAMPLE
  .\scripts\check-ps1-utf8-bom.ps1
  .\scripts\check-ps1-utf8-bom.ps1 -Fix
  .\scripts\check-ps1-utf8-bom.ps1 -Staged
  .\scripts\check-ps1-utf8-bom.ps1 -Path .\scripts -Recurse
#>
[CmdletBinding()]
param(
    # 検査対象ディレクトリ（省略時: リポジトリ scripts/）
    [string[]] $Path,

    # サブディレクトリも走査
    [switch] $Recurse,

    # git staged の .ps1 だけ検査（pre-commit 用）
    [switch] $Staged,

    # FAIL 対象に UTF-8 BOM を付与して書き直す
    [switch] $Fix,

    # テンプレ root の scripts も検査
    [switch] $IncludeTemplate
)

$ErrorActionPreference = 'Stop'

function Get-RepoRoot {
    # PS 5.1 + ErrorAction Stop だと git の stderr で止まるため一時緩和
    $prev = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $fromGit = & git rev-parse --show-toplevel 2>$null
        if ($LASTEXITCODE -eq 0 -and $fromGit) {
            return ([string]$fromGit).Trim()
        }
    }
    finally {
        $ErrorActionPreference = $prev
    }
    return (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
}

function Test-HasUtf8Bom {
    param([byte[]] $Bytes)
    return ($Bytes.Length -ge 3 -and $Bytes[0] -eq 0xEF -and $Bytes[1] -eq 0xBB -and $Bytes[2] -eq 0xBF)
}

function Test-HasNonAscii {
    param([byte[]] $Bytes)
    $start = 0
    if (Test-HasUtf8Bom -Bytes $Bytes) { $start = 3 }
    for ($i = $start; $i -lt $Bytes.Length; $i++) {
        if ($Bytes[$i] -gt 127) { return $true }
    }
    return $false
}

function Add-Utf8Bom {
    param([string] $FilePath)
    $bytes = [System.IO.File]::ReadAllBytes($FilePath)
    if (Test-HasUtf8Bom -Bytes $bytes) { return $false }
    $bom = [byte[]](0xEF, 0xBB, 0xBF)
    $combined = New-Object byte[] ($bom.Length + $bytes.Length)
    [System.Buffer]::BlockCopy($bom, 0, $combined, 0, 3)
    [System.Buffer]::BlockCopy($bytes, 0, $combined, 3, $bytes.Length)
    [System.IO.File]::WriteAllBytes($FilePath, $combined)
    return $true
}

function Get-TargetFiles {
    $files = New-Object System.Collections.Generic.List[string]

    if ($Staged) {
        $root = Get-RepoRoot
        if (-not (Test-Path -LiteralPath (Join-Path $root '.git'))) {
            Write-Host '[ps1-utf8-bom] not a git repo — staged check skip'
            return $files
        }
        $prev = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        Push-Location $root
        try {
            $staged = @(& git diff --cached --name-only --diff-filter=ACMR 2>$null)
            if ($LASTEXITCODE -ne 0) { $staged = @() }
        }
        finally {
            Pop-Location
            $ErrorActionPreference = $prev
        }
        foreach ($rel in $staged) {
            if ($rel -notmatch '\.ps1$') { continue }
            $full = Join-Path $root ($rel -replace '/', '\')
            if (Test-Path -LiteralPath $full) {
                $files.Add((Resolve-Path -LiteralPath $full).Path)
            }
        }
        return $files
    }

    $roots = New-Object System.Collections.Generic.List[string]
    if ($Path -and $Path.Count -gt 0) {
        foreach ($p in $Path) {
            $roots.Add((Resolve-Path -LiteralPath $p).Path)
        }
    }
    else {
        $roots.Add((Resolve-Path -LiteralPath $PSScriptRoot).Path)
    }

    if ($IncludeTemplate) {
        $tpl = Join-Path $env:USERPROFILE '.cursor\kaggle-template\root\scripts'
        if (Test-Path -LiteralPath $tpl) {
            $roots.Add((Resolve-Path -LiteralPath $tpl).Path)
        }
    }

    foreach ($root in $roots) {
        $gciParams = @{
            Path        = $root
            Filter      = '*.ps1'
            File        = $true
            ErrorAction = 'Stop'
        }
        if ($Recurse -or -not $Path) {
            # 既定の scripts/ 走査は直下のみ（comp 配下の大量一時 ps1 を避けつつ、
            # リポジトリ scripts は浅い）。-Recurse で明示時のみ再帰。
            if ($Recurse) { $gciParams['Recurse'] = $true }
        }
        Get-ChildItem @gciParams | ForEach-Object { $files.Add($_.FullName) }
    }

    # 重複除去
    return @($files | Select-Object -Unique)
}

$targets = @(Get-TargetFiles)
if ($targets.Count -eq 0) {
    Write-Host '[ps1-utf8-bom] no .ps1 targets — skip'
    exit 0
}

$fail = New-Object System.Collections.Generic.List[string]
$fixed = New-Object System.Collections.Generic.List[string]
$passCount = 0

foreach ($file in $targets) {
    $bytes = [System.IO.File]::ReadAllBytes($file)
    $hasBom = Test-HasUtf8Bom -Bytes $bytes
    $nonAscii = Test-HasNonAscii -Bytes $bytes

    if ($hasBom -or -not $nonAscii) {
        $passCount++
        continue
    }

    if ($Fix) {
        if (Add-Utf8Bom -FilePath $file) {
            $fixed.Add($file)
        }
        $passCount++
        continue
    }

    $fail.Add($file)
}

Write-Host ("[ps1-utf8-bom] scanned={0} pass={1} fail={2} fixed={3}" -f `
    $targets.Count, $passCount, $fail.Count, $fixed.Count)

foreach ($f in $fixed) {
    Write-Host ("  FIXED (BOM added): {0}" -f $f) -ForegroundColor Yellow
}
foreach ($f in $fail) {
    Write-Host ("  FAIL (non-ASCII without UTF-8 BOM): {0}" -f $f) -ForegroundColor Red
}

if ($fail.Count -gt 0) {
    Write-Host ''
    Write-Host 'NG: PowerShell 5.1 will misread these as ANSI. Re-save as UTF-8 with BOM,' -ForegroundColor Red
    Write-Host '    or run: .\scripts\check-ps1-utf8-bom.ps1 -Fix' -ForegroundColor Red
    exit 1
}

Write-Host '[ps1-utf8-bom] PASS' -ForegroundColor Green
exit 0
