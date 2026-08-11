#Requires -Version 5.1
try {
    $ErrorActionPreference = 'Stop'
    . (Join-Path $PSScriptRoot '_hook-common.ps1')

    $inputObj = Read-HookInput
    $cmd = if ($inputObj -and $inputObj.command) { [string]$inputObj.command } else { '' }
    if ($cmd -notmatch 'validate-submission\.ps1') { Write-HookAllow }

    $logPath = Join-Path $PSScriptRoot 'audit\validate-submission-shell.log'
    $exitCode = if ($inputObj.exit_code) { $inputObj.exit_code } elseif ($inputObj.exitCode) { $inputObj.exitCode } else { '' }
    $output = if ($inputObj.output) { [string]$inputObj.output } else { '' }
    if ($output.Length -gt 8000) { $output = $output.Substring(0, 8000) + '...' }
    $stamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss') + ' UTC'
    Add-Content -LiteralPath $logPath -Value "=== $stamp ===`nexit: $exitCode`ncommand: $cmd`n$output`n" -Encoding UTF8
    Write-HookAllow
}
catch {
    [Console]::Out.WriteLine('{"permission":"allow"}')
    exit 0
}
