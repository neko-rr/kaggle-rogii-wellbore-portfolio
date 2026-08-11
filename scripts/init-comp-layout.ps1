#Requires -Version 5.1
<#
.SYNOPSIS
  新コンペ comp-root にフォルダマップ・lifecycle · exp 4 層 · my-* README · sim-track を一括配置。

.DESCRIPTION
  new-kaggle-comp.ps1 実行後、または既存 comp-root に対して実行する。
  テンプレ SSOT: scripts/templates/

.EXAMPLE
  .\scripts\init-comp-layout.ps1 -CompRoot ".\my-comp\20260701-my-comp"
  .\scripts\init-comp-layout.ps1 -CompRoot "20260701-my-comp" -CompType simulation
  .\scripts\init-comp-layout.ps1 -CompRoot "20260701-my-comp" -WhatIf
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $true)]
    [string] $CompRoot,

    [ValidateSet('auto', 'simulation', 'tabular', 'notebook-output', 'csv', 'lora')]
    [string] $CompType = 'auto',

    [string] $Participant = 'Kazeneko',

    [switch] $Force,

    # 未インストール時、または明示指定時に Cursor hooks + agents を配置
    [switch] $InstallCursorInfra
)

$ErrorActionPreference = 'Stop'

function Resolve-CompRootPath {
    param([string] $InputPath)
    if ([System.IO.Path]::IsPathRooted($InputPath)) {
        return (Resolve-Path -LiteralPath $InputPath).Path
    }
    $repoRoot = Split-Path -Parent $PSScriptRoot
    $candidate = Join-Path $repoRoot $InputPath
    if (-not (Test-Path -LiteralPath $candidate)) {
        throw "CompRoot not found: $candidate"
    }
    return (Resolve-Path -LiteralPath $candidate).Path
}

function Get-CompMeta {
    param(
        [string] $Root,
        [string] $TypeOverride
    )
    $folderName = Split-Path -Leaf $Root
    $meta = @{
        CompSlug     = $folderName
        CompName     = $folderName
        CompType     = 'tabular'
        SubmitProfile = 'csv'
        CompUrl      = 'TBD'
        CompDeadline = 'TBD'
        CompDate     = (Get-Date -Format 'yyyy-MM-dd')
        Participant  = $Participant
    }

    $agentsPath = Join-Path (Split-Path -Parent $Root) 'AGENTS.md'
    if (-not (Test-Path -LiteralPath $agentsPath)) {
        $agentsPath = Join-Path $Root '..\AGENTS.md'
    }
    if (Test-Path -LiteralPath $agentsPath) {
        $agents = Get-Content -LiteralPath $agentsPath -Raw -Encoding UTF8
        if ($agents -match '\|\s*\*\*コンペ名\*\*\s*\|\s*([^|]+)\|') {
            $meta.CompName = $matches[1].Trim()
        }
        if ($agents -match 'https://www\.kaggle\.com/competitions/[^\s\|`]+') {
            $meta.CompUrl = $matches[0].Trim()
        }
        if ($agents -match 'comp-type:\s*(\S+)') {
            $meta.CompType = $matches[1].Trim()
        }
        if ($agents -match 'submission-profile:\s*(\S+)') {
            $meta.SubmitProfile = $matches[1].Trim()
        }
    }

    $profilePath = Join-Path $Root 'docs-ja\comp-profile.md'
    if (Test-Path -LiteralPath $profilePath) {
        $profile = Get-Content -LiteralPath $profilePath -Raw -Encoding UTF8
        if ($profile -match '(?m)^comp-type:\s*(\S+)') {
            $meta.CompType = $matches[1].Trim()
        }
        if ($profile -match '(?m)^submission-profile:\s*(\S+)') {
            $meta.SubmitProfile = $matches[1].Trim()
        }
    }

    $timelinePath = Join-Path $Root 'docs-ja\comp-timeline.md'
    if (Test-Path -LiteralPath $timelinePath) {
        $tl = Get-Content -LiteralPath $timelinePath -Raw -Encoding UTF8
        if ($tl -match '(?m)締切[：:]\s*(\d{4}[-/]\d{2}[-/]\d{2})') {
            $meta.CompDeadline = $matches[1].Trim()
        }
    }

    if ($TypeOverride -ne 'auto') {
        $meta.CompType = $TypeOverride
        if ($TypeOverride -eq 'simulation') {
            $meta.SubmitProfile = 'simulation'
        }
    }

    if ($meta.CompType -eq 'simulation' -and $meta.SubmitProfile -eq 'csv') {
        $meta.SubmitProfile = 'simulation'
    }

    return $meta
}

function Expand-Template {
    param(
        [string] $Content,
        [hashtable] $Meta
    )
    $out = $Content
    $out = $out -replace '\{\{COMP_NAME\}\}', $Meta.CompName
    $out = $out -replace '\{\{COMP_SLUG\}\}', $Meta.CompSlug
    $out = $out -replace '\{\{COMP_TYPE\}\}', $Meta.CompType
    $out = $out -replace '\{\{SUBMISSION_PROFILE\}\}', $Meta.SubmitProfile
    $out = $out -replace '\{\{COMP_URL\}\}', $Meta.CompUrl
    $out = $out -replace '\{\{COMP_DEADLINE\}\}', $Meta.CompDeadline
    $out = $out -replace '\{\{COMP_DATE\}\}', $Meta.CompDate
    $out = $out -replace '\{\{PARTICIPANT\}\}', $Meta.Participant
    return $out
}

function Install-FromTemplate {
    param(
        [string] $TemplateName,
        [string] $DestRelative,
        [hashtable] $Meta,
        [string] $TemplatesDir,
        [string] $Root
    )
    $src = Join-Path $TemplatesDir $TemplateName
    if (-not (Test-Path -LiteralPath $src)) {
        Write-Warning "Template missing: $TemplateName"
        return
    }
    $dest = Join-Path $Root $DestRelative
    $destDir = Split-Path -Parent $dest
    if (-not (Test-Path -LiteralPath $destDir)) {
        if ($PSCmdlet.ShouldProcess($destDir, 'Create directory')) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
    }
    if ((Test-Path -LiteralPath $dest) -and -not $Force) {
        Write-Host "Skip (exists): $DestRelative"
        return
    }
    $raw = Get-Content -LiteralPath $src -Raw -Encoding UTF8
    $text = Expand-Template -Content $raw -Meta $Meta
    if ($PSCmdlet.ShouldProcess($dest, 'Write template')) {
        [System.IO.File]::WriteAllText($dest, $text, [System.Text.UTF8Encoding]::new($false))
        Write-Host "OK: $DestRelative"
    }
}

function Ensure-Dir {
    param([string] $Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        if ($PSCmdlet.ShouldProcess($Path, 'Create directory')) {
            New-Item -ItemType Directory -Path $Path -Force | Out-Null
        }
    }
}

$compRootPath = Resolve-CompRootPath -InputPath $CompRoot
$templatesDir = Join-Path $PSScriptRoot 'templates'
$meta = Get-CompMeta -Root $compRootPath -TypeOverride $CompType

Write-Host "CompRoot: $compRootPath"
Write-Host "CompType: $($meta.CompType) · submission-profile: $($meta.SubmitProfile)"

# --- ディレクトリ ---
$dirs = @(
    'exp\protocol',
    'exp\latest',
    'exp\work',
    'exp\archive\history',
    'exp\archive\superseded',
    'exp\replay',
    'exp\local-eval',
    'my-notebook\planned',
    'my-local-eval-notebook',
    'my-ran-notebook',
    'my-submitted-notebook',
    'others-notebook',
    'docs-ja\pretrain-gates',
    'docs-ja\submission-validations'
)
if ($meta.CompType -eq 'simulation') {
    $dirs += @(
        'sim-track\snapshots\catalog',
        'sim-track\snapshots\deltas',
        'sim-track\leaderboard-csv'
    )
}
foreach ($d in $dirs) {
    Ensure-Dir -Path (Join-Path $compRootPath $d)
}

# --- テンプレ配置 ---
# submission-profile 別の提出ルール雛形（無ければ汎用 template）
$profileRules = @{
    'csv'             = 'submission-rules.csv.md.template'
    'simulation'      = 'submission-rules.simulation.md.template'
    'lora'            = 'submission-rules.lora.md.template'
    'notebook-output' = 'submission-rules.notebook-output.md.template'
}
$rulesTemplate = $profileRules[$meta.SubmitProfile]
if (-not $rulesTemplate) { $rulesTemplate = 'submission-rules.md.template' }
if (-not (Test-Path -LiteralPath (Join-Path $templatesDir $rulesTemplate))) {
    $rulesTemplate = 'submission-rules.notebook-output.md.template'
}
$files = @(
    @{ T = 'lifecycle-manifest.md.template'; D = 'lifecycle-manifest.md' },
    @{ T = 'folder-map.md.template'; D = 'docs-ja\folder-map.md' },
    @{ T = 'comp-start-checklist.md.template'; D = 'docs-ja\comp-start-checklist.md' },
    @{ T = $rulesTemplate; D = 'docs-ja\submission-rules.md' },
    @{ T = 'colab-cursor-runbook.md.template'; D = 'docs-ja\colab-cursor-runbook.md' },
    @{ T = 'exp-README.md.template'; D = 'exp\README.md' },
    @{ T = 'exp-latest-manifest.md.template'; D = 'exp\latest\manifest.md' },
    @{ T = 'improvement-loop-failures.json.template'; D = 'exp\improvement-loop-failures.json' },
    @{ T = 'improvement-loop-state.json.template'; D = 'exp\improvement-loop-state.json' },
    @{ T = 'improvement-loop-allowlist.json.template'; D = 'exp\improvement-loop-allowlist.json' },
    @{ T = 'work-protect.json.template'; D = 'exp\work-protect.json' },
    @{ T = 'artifact-routing.json.template'; D = 'exp\artifact-routing.json' },
    @{ T = 'pre-strategy-gate.md.template'; D = 'exp\pre-strategy-gate.md' },
    @{ T = 'my-notebook-README.md.template'; D = 'my-notebook\README.md' },
    @{ T = 'my-notebook-planned-README.md.template'; D = 'my-notebook\planned\README.md' },
    @{ T = 'my-local-eval-notebook-README.md.template'; D = 'my-local-eval-notebook\README.md' },
    @{ T = 'my-ran-notebook-README.md.template'; D = 'my-ran-notebook\README.md' },
    @{ T = 'my-submitted-notebook-README.md.template'; D = 'my-submitted-notebook\README.md' }
)
if ($meta.SubmitProfile -eq 'simulation') {
    $files += @{ T = 'strength-gate-profile.simulation.template.json'; D = 'docs-ja\strength-gate-profile.json' }
}
foreach ($f in $files) {
    Install-FromTemplate -TemplateName $f.T -DestRelative $f.D -Meta $meta -TemplatesDir $templatesDir -Root $compRootPath
}

$knowledgeScript = Join-Path $PSScriptRoot "run-kaggle-knowledge.ps1"
$repoRootForKnowledge = Split-Path -Parent $PSScriptRoot
$knowledgeDir = Join-Path $repoRootForKnowledge 'knowledge'
$knowledgeStoreJson = Join-Path $knowledgeDir 'store.json'
$knowledgeGitUrl = $env:KAGGLE_KNOWLEDGE_GIT_URL
if ([string]::IsNullOrWhiteSpace($knowledgeGitUrl)) {
    $knowledgeGitUrl = 'https://github.com/neko-rr/kaggle-knowledge-store.git'
}

if ((Test-Path -LiteralPath $knowledgeStoreJson)) {
    Write-Host "OK: knowledge/store.json already present (shared store — skip init)"
} elseif ($PSCmdlet.ShouldProcess($knowledgeDir, "Clone or init Kaggle knowledge store")) {
    $cloned = $false
    if (-not (Test-Path -LiteralPath $knowledgeDir)) {
        try {
            git clone --depth 1 $knowledgeGitUrl $knowledgeDir 2>&1 | Out-Host
            if ($LASTEXITCODE -eq 0 -and (Test-Path -LiteralPath $knowledgeStoreJson)) {
                Write-Host "OK: knowledge/ cloned from Private store ($knowledgeGitUrl)"
                $cloned = $true
            }
        } catch {
            Write-Warning "knowledge clone failed: $_"
        }
    }
    if (-not $cloned -and (Test-Path -LiteralPath $knowledgeScript)) {
        Write-Warning "No shared knowledge store found — local init (NEW store_id). Prefer: git clone $knowledgeGitUrl knowledge"
        & $knowledgeScript -Action init
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "Kaggle knowledge init failed; run scripts/run-kaggle-knowledge.ps1 -Action init later"
        }
    }
}

# 戦略前機械チェックのカタログを knowledge/ へ配置（既存なら保持）
$catalogTemplate = Join-Path $templatesDir 'mechanical-improvements.md.template'
$catalogDest = Join-Path (Split-Path -Parent $PSScriptRoot) 'knowledge\mechanical-improvements.md'
if ((Test-Path -LiteralPath $catalogTemplate) -and -not (Test-Path -LiteralPath $catalogDest)) {
    Ensure-Dir -Path (Split-Path -Parent $catalogDest)
    if ($PSCmdlet.ShouldProcess($catalogDest, 'Copy mechanical-improvements catalog')) {
        Copy-Item -LiteralPath $catalogTemplate -Destination $catalogDest
        Write-Host 'OK: knowledge\mechanical-improvements.md'
    }
}

if ($meta.CompType -eq 'simulation') {
    $simFiles = @(
        @{ T = 'sim-track-index.md.template'; D = 'sim-track\sim-track-index.md' },
        @{ T = 'sim-track-public-notebook-catalog.md.template'; D = 'sim-track\public-notebook-catalog.md' },
        @{ T = 'sim-track-notebook-score-history.md.template'; D = 'sim-track\notebook-score-history.md' },
        @{ T = 'sim-track-submitted-notebook-registry.md.template'; D = 'sim-track\submitted-notebook-registry.md' },
        @{ T = 'sim-track-leaderboard-log.md.template'; D = 'sim-track\leaderboard-log.md' }
    )
    foreach ($f in $simFiles) {
        Install-FromTemplate -TemplateName $f.T -DestRelative $f.D -Meta $meta -TemplatesDir $templatesDir -Root $compRootPath
    }
}

# archive README（空でも可）
$supersededReadme = Join-Path $compRootPath 'exp\archive\superseded\README.md'
if (-not (Test-Path -LiteralPath $supersededReadme) -or $Force) {
    $txt = @"
# archive/superseded/

方法論エラー・reject 確定の分析。再提出判断に使わない。

- 索引: [../../latest/manifest.md](../../latest/manifest.md)
"@
    if ($PSCmdlet.ShouldProcess($supersededReadme, 'Write README')) {
        [System.IO.File]::WriteAllText($supersededReadme, $txt, [System.Text.UTF8Encoding]::new($false))
        Write-Host 'OK: exp\archive\superseded\README.md'
    }
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$hooksJson = Join-Path $repoRoot '.cursor\hooks.json'
$needCursorInfra = $InstallCursorInfra -or -not (Test-Path -LiteralPath $hooksJson)
if ($needCursorInfra) {
    $infraScript = Join-Path $PSScriptRoot 'install-cursor-infra.ps1'
    if (Test-Path -LiteralPath $infraScript) {
        if ($PSCmdlet.ShouldProcess($repoRoot, 'Install Cursor hooks + agents')) {
            & $infraScript
        }
    }
    else {
        Write-Warning "install-cursor-infra.ps1 not found — run after sync-project-infra-from-template.ps1"
    }
}

Write-Host ''
Write-Host 'Next:'
Write-Host '  1. docs-ja/comp-start-checklist.md を上から [x] していく'
Write-Host '  2. docs-ja/folder-map.md を Agent 読み順の SSOT にする'
Write-Host '  3. comp-type が auto なら comp-profile.md を確定後 -CompType で再実行可'
Write-Host '  4. Cursor Reload Window（hooks 初回インストール後）'
