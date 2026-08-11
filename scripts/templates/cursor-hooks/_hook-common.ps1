#Requires -Version 5.1

function Read-HookInput {
    try {
        $raw = [Console]::In.ReadToEnd()
        if ([string]::IsNullOrWhiteSpace($raw)) { return $null }
        return ($raw | ConvertFrom-Json)
    }
    catch { return $null }
}

function Write-HookAllow {
    [Console]::Out.WriteLine('{"permission":"allow"}')
    exit 0
}

function Write-HookDeny {
    param(
        [Parameter(Mandatory = $true)][string] $UserMessage,
        [Parameter(Mandatory = $true)][string] $AgentMessage
    )
    $payload = [ordered]@{
        permission    = 'deny'
        user_message  = $UserMessage
        agent_message = $AgentMessage
    }
    [Console]::Out.WriteLine(($payload | ConvertTo-Json -Compress))
    exit 2
}

function Normalize-PathForHook {
    param([string] $Path)
    if ([string]::IsNullOrWhiteSpace($Path)) { return '' }
    return ($Path -replace '\\', '/').Trim()
}

function Test-DatasetWriteBlocked {
    param([string] $Path)
    $n = Normalize-PathForHook $Path
    if ($n -notmatch '(^|[\\/])dataset[\\/]') { return $false }
    if ($n -match '(^|[\\/])dataset[\\/]\.gitkeep$') { return $false }
    if ($n -match '(^|[\\/])dataset[\\/]README\.md$') { return $false }
    return $true
}
