#Requires -Version 5.1
<#
.SYNOPSIS
  Cursor Kaggle hooks の簡易テスト（before-shell / pre-tool）。
#>
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$BeforeHook = Join-Path $Root '.cursor\hooks\before-shell-execution.ps1'
$PreToolHook = Join-Path $Root '.cursor\hooks\pre-tool-use.ps1'

function Invoke-Hook {
    param(
        [string] $HookPath,
        [string] $Json
    )
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = 'powershell.exe'
    $psi.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$HookPath`""
    $psi.RedirectStandardInput = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $p = [System.Diagnostics.Process]::Start($psi)
    $p.StandardInput.Write($Json)
    $p.StandardInput.Close()
    $out = $p.StandardOutput.ReadToEnd().Trim()
    $err = $p.StandardError.ReadToEnd()
    $p.WaitForExit()
    if (-not $out) { throw "Empty hook output. stderr: $err" }
    return [PSCustomObject]@{ Output = $out; ExitCode = $p.ExitCode; Json = ($out | ConvertFrom-Json) }
}

function Test-BeforeShell {
    param([string] $Json, [string] $ExpectPermission)
    $r = Invoke-Hook -HookPath $BeforeHook -Json $Json
    if ($r.Json.permission -ne $ExpectPermission) {
        throw "Expected permission=$ExpectPermission, got $($r.Json.permission). stdout=$($r.Output)"
    }
    Write-Host "OK before-shell $ExpectPermission : $Json"
}

function Test-PreTool {
    param([string] $Json, [string] $ExpectPermission)
    $r = Invoke-Hook -HookPath $PreToolHook -Json $Json
    if ($r.Json.permission -ne $ExpectPermission) {
        throw "Expected permission=$ExpectPermission, got $($r.Json.permission). stdout=$($r.Output)"
    }
    Write-Host "OK pre-tool $ExpectPermission"
}

Test-BeforeShell '{"command":"kaggle competitions list"}' 'deny'
Test-BeforeShell '{"command":".\\scripts\\kaggle-cli.ps1 --version"}' 'allow'
Test-BeforeShell '{"command":"pip install kaggle"}' 'deny'
Test-BeforeShell '{"command":"git push --force origin main"}' 'deny'
Test-BeforeShell '{"command":"powershell -NoProfile -File .cursor/hooks/before-shell-execution.ps1"}' 'allow'

Test-PreTool '{"tool_name":"Write","tool_input":{"path":"20260623-orbit-wars/dataset/derived/foo.csv"}}' 'deny'
Test-PreTool '{"tool_name":"Write","tool_input":{"path":"20260623-orbit-wars/dataset/README.md"}}' 'allow'
Test-PreTool '{"tool_name":"Write","tool_input":{"path":"scripts/foo.ps1"}}' 'allow'

Write-Host ''
Write-Host 'All hook tests passed.'
