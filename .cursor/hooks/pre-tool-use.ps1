#Requires -Version 5.1
try {
    $ErrorActionPreference = 'Stop'
    . (Join-Path $PSScriptRoot '_hook-common.ps1')

    $inputObj = Read-HookInput
    if ($null -eq $inputObj) { Write-HookAllow }

    $toolName = if ($inputObj.tool_name) { [string]$inputObj.tool_name } else { '' }
    if ($toolName -notmatch '^(Write|StrReplace|ApplyPatch|EditNotebook)$') { Write-HookAllow }

    $path = ''
    $ti = $inputObj.tool_input
    if ($null -ne $ti) {
        if ($ti -is [string]) {
            try { $ti = $ti | ConvertFrom-Json } catch { Write-HookAllow }
        }
        if ($ti.PSObject.Properties['path']) { $path = [string]$ti.path }
        elseif ($ti.PSObject.Properties['target_notebook']) { $path = [string]$ti.target_notebook }
    }
    if ([string]::IsNullOrWhiteSpace($path)) { Write-HookAllow }

    if (Test-DatasetWriteBlocked -Path $path) {
        Write-HookDeny `
            -UserMessage 'Writes under dataset/ are blocked (except README.md and .gitkeep).' `
            -AgentMessage "Blocked dataset write: $path"
    }
    Write-HookAllow
}
catch {
    [Console]::Error.WriteLine("[kaggle-hook] pre-tool: $_")
    [Console]::Out.WriteLine('{"permission":"allow"}')
    exit 0
}
