#Requires -Version 5.1
<#
.SYNOPSIS
  exp/pre-strategy-gate.md（戦略前機械チェックゲート）を機械判定する。

.DESCRIPTION
  判定ルール:
  - 「## 必須」で始まる節の `- [ ]`（未完了）を数える。1件でも残れば FAIL
  - 「## 型別（未確定）」見出しが残っていれば FAIL（comp-type を確定してから戦略へ）
  - 「## N/A —」節は判定対象外
  - コンペ固有節（任意）の `- [ ]` と、理由のない `- [-]` は警告のみ
  PASS = exit 0 / FAIL = exit 1。安価モデル・hooks からも同じ判定を再現できる。

.EXAMPLE
  .\scripts\check-pre-strategy-gate.ps1 -CompRoot .\20260706-neurogolf-2026
  .\scripts\check-pre-strategy-gate.ps1 -GatePath .\20260706-neurogolf-2026\exp\pre-strategy-gate.md
#>
[CmdletBinding()]
param(
    [string] $CompRoot,
    [string] $GatePath
)

$ErrorActionPreference = 'Stop'

function Resolve-GatePath {
    param([string] $CompRootValue, [string] $GatePathValue)
    if ($GatePathValue) {
        return (Resolve-Path -LiteralPath $GatePathValue).Path
    }
    if ($CompRootValue) {
        $candidate = Join-Path $CompRootValue 'exp\pre-strategy-gate.md'
        return (Resolve-Path -LiteralPath $candidate).Path
    }
    # 引数省略時: リポジトリ直下の comp-root を探索（一意のときだけ採用）
    $repoRoot = Split-Path -Parent $PSScriptRoot
    $found = @(Get-ChildItem -Path $repoRoot -Directory |
        ForEach-Object { Join-Path $_.FullName 'exp\pre-strategy-gate.md' } |
        Where-Object { Test-Path -LiteralPath $_ })
    if ($found.Count -eq 1) {
        return $found[0]
    }
    throw "gate file not found or ambiguous ($($found.Count) hits). Use -CompRoot or -GatePath."
}

$gate = Resolve-GatePath -CompRootValue $CompRoot -GatePathValue $GatePath
$lines = Get-Content -LiteralPath $gate -Encoding UTF8

$sectionKind = 'none'   # mandatory / unconfirmed / na / optional / none
$mandatorySections = 0
$unconfirmedSections = @()
$incompleteIds = @()
$warnings = @()

foreach ($line in $lines) {
    if ($line -match '^##\s+(.+)$') {
        $title = $matches[1].Trim()
        if ($title -like '必須*') {
            $sectionKind = 'mandatory'
            $mandatorySections++
        }
        elseif ($title -like '型別（未確定）*') {
            $sectionKind = 'unconfirmed'
            $unconfirmedSections += $title
        }
        elseif ($title -like 'N/A*') {
            $sectionKind = 'na'
        }
        elseif ($title -like 'コンペ固有*') {
            $sectionKind = 'optional'
        }
        else {
            $sectionKind = 'none'
        }
        continue
    }
    if ($line -notmatch '^\s*-\s*\[(?<mark> |x|X|-)\]\s*(?<id>\S+)?') {
        continue
    }
    $mark = $matches['mark']
    $id = if ($matches['id']) { $matches['id'] } else { '(IDなし)' }
    if ($mark -eq ' ' -and $sectionKind -eq 'mandatory') {
        $incompleteIds += $id
    }
    elseif ($mark -eq ' ' -and $sectionKind -eq 'optional') {
        $warnings += "コンペ固有節に未完了: $id"
    }
    if ($mark -eq '-' -and $line -notmatch 'N/A') {
        $warnings += "N/A 理由なし: $id（行末に「N/A: 理由」を書く）"
    }
}

Write-Host "gate: $gate"
Write-Host "必須節: $mandatorySections · 未完了: $($incompleteIds.Count) · 型別未確定節: $($unconfirmedSections.Count)"
foreach ($w in $warnings) {
    Write-Warning $w
}

$failed = $false
if ($mandatorySections -eq 0) {
    Write-Host 'FAIL: 「## 必須」節が1つもない（ゲートファイルの書式を確認）' -ForegroundColor Red
    $failed = $true
}
if ($unconfirmedSections.Count -gt 0) {
    Write-Host 'FAIL: comp-type 未確定の型別節が残っている:' -ForegroundColor Red
    $unconfirmedSections | ForEach-Object { Write-Host "  - $_" }
    Write-Host '  → 該当型は「## 必須 —」、非該当型は「## N/A —」へ見出しを変更する'
    $failed = $true
}
if ($incompleteIds.Count -gt 0) {
    Write-Host 'FAIL: 必須項目に未完了が残っている:' -ForegroundColor Red
    $incompleteIds | ForEach-Object { Write-Host "  - [ ] $_" }
    $failed = $true
}

if ($failed) {
    Write-Host ''
    Write-Host 'NG: 戦略CHK（experiment-checklist の新規仮説）作成は禁止。先に上記を潰す。' -ForegroundColor Red
    exit 1
}

Write-Host 'PASS: 戦略前機械チェック完了。戦略CHKへ進んでよい。' -ForegroundColor Green
exit 0
