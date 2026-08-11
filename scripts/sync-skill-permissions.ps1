# Insert or update ## Permissions block in each Skill from skill-permissions-map.json
param(
    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$MapFile = Join-Path $PSScriptRoot "skill-permissions-map.json"
$SectionFile = Join-Path $PSScriptRoot "skill-permissions-section.txt"
$FooterFile = Join-Path $PSScriptRoot "skill-permissions-footer.txt"
$DenyPrefixFile = Join-Path $PSScriptRoot "skill-permissions-deny-prefix.txt"
$SkillsRoot = Join-Path $RepoRoot ".cursor\skills"

foreach ($required in @($MapFile, $SectionFile, $FooterFile, $DenyPrefixFile)) {
    if (-not (Test-Path -LiteralPath $required)) {
        Write-Error "Missing $required"
    }
}

$sectionTitle = (Get-Content -LiteralPath $SectionFile -Raw -Encoding UTF8).TrimEnd()
$footerTemplate = Get-Content -LiteralPath $FooterFile -Raw -Encoding UTF8
$denyPrefix = (Get-Content -LiteralPath $DenyPrefixFile -Raw -Encoding UTF8).TrimEnd()
$map = Get-Content -LiteralPath $MapFile -Raw -Encoding UTF8 | ConvertFrom-Json
$updated = 0
$missing = @()

function Get-UserOkLine {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) { return "-" }
    if ($Value -eq "-") { return "-" }
    return $Value
}

function Format-PermissionsBlock {
    param($Entry)
    $userOk = Get-UserOkLine -Value $Entry.user_ok
    $footer = $footerTemplate.Replace("{USER_OK}", $userOk).TrimEnd()
    $lines = @(
        $sectionTitle,
        "",
        "| shell | network | env | file_read | file_write |",
        "|---|---|---|---|---|",
        "| $($Entry.shell) | $($Entry.network) | $($Entry.env) | $($Entry.file_read) | $($Entry.file_write) |",
        "",
        $footer,
        ""
    )
    return ($lines -join [Environment]::NewLine)
}

function Remove-PermissionsBlocks {
    param(
        [string]$Content,
        [string]$SectionHeader,
        [string]$DenyLinePrefix
    )
    $lines = ($Content -replace "`r`n", "`n") -split "`n"
    $out = New-Object System.Collections.Generic.List[string]
    $i = 0
    while ($i -lt $lines.Count) {
        if ($lines[$i] -eq $SectionHeader) {
            $start = $i
            $i++
            $limit = [Math]::Min($lines.Count, $start + 24)
            $found = $false
            while ($i -lt $limit) {
                if ($lines[$i].StartsWith($DenyLinePrefix)) {
                    $found = $true
                    $i++
                    break
                }
                $i++
            }
            if (-not $found) {
                Write-Warning "Malformed permissions block at line $($start + 1)"
                [void]$out.Add($lines[$start])
                $i = $start + 1
                continue
            }
            while ($i -lt $lines.Count -and [string]::IsNullOrWhiteSpace($lines[$i])) {
                $i++
            }
            continue
        }
        [void]$out.Add($lines[$i])
        $i++
    }
    return ($out -join "`n")
}

function Get-FrontmatterInsertIndex {
    param([string[]]$Lines)
    if ($Lines.Count -lt 2 -or $Lines[0] -notmatch '^---\s*$') {
        return -1
    }
    for ($i = 1; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i] -match '^---\s*$') {
            return $i + 1
        }
    }
    return -1
}

function Insert-PermissionsBlock {
    param(
        [string]$Content,
        [string]$Block,
        [string]$SectionHeader,
        [string]$DenyLinePrefix
    )
    $Content = Remove-PermissionsBlocks -Content $Content -SectionHeader $SectionHeader -DenyLinePrefix $DenyLinePrefix
    $normalized = $Content -replace "`r`n", "`n"
    $lines = $normalized -split "`n", -1
    $insertAt = Get-FrontmatterInsertIndex -Lines $lines

    if ($insertAt -ge 0) {
        while ($insertAt -lt $lines.Count -and [string]::IsNullOrWhiteSpace($lines[$insertAt])) {
            $insertAt++
        }
    } else {
        $insertAt = -1
        for ($i = 0; $i -lt $lines.Count; $i++) {
            if ($lines[$i] -match '^# ') {
                $insertAt = $i
                break
            }
        }
        if ($insertAt -lt 0) {
            $insertAt = 0
        }
    }

    $before = @()
    if ($insertAt -gt 0) {
        $before = $lines[0..($insertAt - 1)]
    }
    $after = @()
    if ($insertAt -lt $lines.Count) {
        $after = $lines[$insertAt..($lines.Count - 1)]
    }

    $parts = @()
    if ($before.Count -gt 0) {
        $parts += ($before -join "`n")
    }
    $parts += $Block
    if ($after.Count -gt 0) {
        $parts += ($after -join "`n")
    }
    return (($parts -join "`n").TrimEnd() + "`n")
}

Get-ChildItem -LiteralPath $SkillsRoot -Directory | ForEach-Object {
    $skillName = $_.Name
    if ($skillName -eq "_shared") { return }
    $skillFile = Join-Path $_.FullName "SKILL.md"
    if (-not (Test-Path -LiteralPath $skillFile)) { return }

    $entry = $map.$skillName
    if ($null -eq $entry) {
        $missing += $skillName
        return
    }

    $block = Format-PermissionsBlock -Entry $entry
    $content = Get-Content -LiteralPath $skillFile -Raw -Encoding UTF8
    $oldLineCount = @($content -split "`r?`n").Count
    $newContent = Insert-PermissionsBlock -Content $content -Block $block -SectionHeader $sectionTitle -DenyLinePrefix $denyPrefix
    $newLineCount = @($newContent -split "`r?`n").Count
    if ($oldLineCount -gt 25 -and $newLineCount -lt [Math]::Floor($oldLineCount * 0.6)) {
        Write-Warning "Skip $skillName - would truncate ($oldLineCount -> $newLineCount lines)"
        return
    }

    if ($WhatIf) {
        Write-Host "Would update: $skillName"
    } else {
        $utf8NoBom = New-Object System.Text.UTF8Encoding $false
        [System.IO.File]::WriteAllText($skillFile, $newContent, $utf8NoBom)
        Write-Host "Updated: $skillName"
    }
    $updated++
}

Write-Host ""
Write-Host "Updated skills: $updated"
if ($missing.Count -gt 0) {
    Write-Warning "Missing map entries: $($missing -join ', ')"
    exit 1
}
