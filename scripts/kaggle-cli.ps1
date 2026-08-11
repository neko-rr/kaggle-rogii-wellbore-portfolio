# Kaggle CLI wrapper - prefers .venv. Agent must use this script.
# Usage: .\scripts\kaggle-cli.ps1 competitions submissions orbit-wars -v
#
# NOTE: param() は使わない。PowerShell が -p / -v / -k / -f を共通パラメータに
# 部分マッチさせて kaggle へ渡らなくなる（毎回 --% が必要になる）ため、
# 生の $args をそのまま kaggle に転送する。これで -p <dir> 等が常に素通しされる。
$KaggleArgs = $args

$ErrorActionPreference = "Stop"

# 日本語 Windows の Python 既定 cp932 では kernels push / 一部出力が
# UnicodeDecodeError でクラッシュする。UTF-8 を必ず強制する。
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$CacheFile = Join-Path $RepoRoot ".cache\kaggle-cli-path.txt"
$VenvKaggle = Join-Path $RepoRoot ".venv\Scripts\kaggle.exe"
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"

function Write-KaggleCliMissing {
    Write-Error @"
kaggle CLI not found.

Bootstrap:
  .\scripts\setup-kaggle-venv.ps1
  .\scripts\check-kaggle-cli.ps1
  .\.venv\Scripts\kaggle.exe auth login

Then:
  .\scripts\kaggle-cli.ps1 --version

Do not: global pip install kaggle / raw kaggle command
See: .cursor/skills/kaggle-cli-ops/SKILL.md
"@
}

function Save-KaggleCliPath {
    param([string]$Path)
    $cacheDir = Split-Path $CacheFile -Parent
    if (-not (Test-Path $cacheDir)) {
        New-Item -ItemType Directory -Path $cacheDir -Force | Out-Null
    }
    $lockFile = "$CacheFile.lock"
    $maxWaitMs = 5000
    $waited = 0
    while (Test-Path -LiteralPath $lockFile) {
        Start-Sleep -Milliseconds 100
        $waited += 100
        if ($waited -ge $maxWaitMs) { break }
    }
    try {
        New-Item -ItemType File -Path $lockFile -Force | Out-Null
        Set-Content -Path $CacheFile -Value $Path -Encoding utf8 -NoNewline
    } finally {
        if (Test-Path -LiteralPath $lockFile) {
            Remove-Item -LiteralPath $lockFile -Force -ErrorAction SilentlyContinue
        }
    }
}

function Resolve-KaggleExe {
    $prevEap = $ErrorActionPreference
    $ErrorActionPreference = "SilentlyContinue"

    try {
        if ($env:KAGGLE_CLI_PATH -and (Test-Path -LiteralPath $env:KAGGLE_CLI_PATH)) {
            return (Resolve-Path -LiteralPath $env:KAGGLE_CLI_PATH).Path
        }

        if (Test-Path -LiteralPath $VenvKaggle) {
            return (Resolve-Path -LiteralPath $VenvKaggle).Path
        }

        if (Test-Path -LiteralPath $CacheFile) {
            $cached = (Get-Content -LiteralPath $CacheFile -Raw).Trim()
            if ($cached -and $cached -notmatch '^module:' -and (Test-Path -LiteralPath $cached)) {
                return (Resolve-Path -LiteralPath $cached).Path
            }
        }

        $cmd = Get-Command kaggle -ErrorAction SilentlyContinue
        if ($cmd -and $cmd.Source -and (Test-Path -LiteralPath $cmd.Source)) {
            return (Resolve-Path -LiteralPath $cmd.Source).Path
        }

        if ($IsWindows -or $env:OS -match "Windows") {
            $whereOut = & where.exe kaggle 2>$null
            if ($LASTEXITCODE -eq 0 -and $whereOut) {
                foreach ($line in @($whereOut)) {
                    $candidate = $line.Trim()
                    if ($candidate -and (Test-Path -LiteralPath $candidate)) {
                        return (Resolve-Path -LiteralPath $candidate).Path
                    }
                }
            }
        }

        return $null
    } finally {
        $ErrorActionPreference = $prevEap
    }
}

# 意図しないリーク防止: datasets create の Public 化を拒否（Rule: kaggle-private-assets）
if ($KaggleArgs.Count -ge 2 -and "$($KaggleArgs[0])" -eq "datasets" -and "$($KaggleArgs[1])" -eq "create") {
    foreach ($a in $KaggleArgs) {
        if ("$a" -eq "-u" -or "$a" -eq "--public") {
            Write-Error @"
REFUSED: datasets create --public / -u is forbidden.

Self-owned Kaggle Datasets / Notebooks / Models must stay Private.
See: .cursor/rules/kaggle-private-assets.mdc
Assert before push: .\scripts\assert-kaggle-private.ps1
"@
            exit 1
        }
    }
}

function Get-ExplicitPathArgument {
    param([object[]]$Arguments)
    for ($i = 0; $i -lt $Arguments.Count; $i++) {
        $value = "$($Arguments[$i])"
        if ($value -eq "-p" -or $value -eq "--path") {
            if ($i + 1 -lt $Arguments.Count) {
                return "$($Arguments[$i + 1])"
            }
            return $null
        }
    }
    return $null
}

# 書込 CLI は対象パスを明示し、Private/metadata 検査を自動で通す。
# ユーザー許可・実行指示の有無は Rule/Skill で確認し、本ガードは機械的事故を防ぐ。
$isKernelPush = $KaggleArgs.Count -ge 2 -and "$($KaggleArgs[0])" -eq "kernels" -and "$($KaggleArgs[1])" -eq "push"
$isDatasetWrite = $KaggleArgs.Count -ge 2 -and "$($KaggleArgs[0])" -eq "datasets" -and (@($KaggleArgs) -contains "create" -or @($KaggleArgs) -contains "version")
$isModelWrite = $KaggleArgs.Count -ge 2 -and "$($KaggleArgs[0])" -eq "models" -and (@($KaggleArgs) -contains "create" -or @($KaggleArgs) -contains "version")

if ($isKernelPush -or $isDatasetWrite -or $isModelWrite) {
    $targetPath = Get-ExplicitPathArgument -Arguments $KaggleArgs
    if (-not $targetPath) {
        Write-Error "REFUSED: write command requires explicit -p/--path to prevent target mistakes."
        exit 1
    }
    if (-not (Test-Path -LiteralPath $targetPath -PathType Container)) {
        Write-Error "REFUSED: target directory not found: $targetPath"
        exit 1
    }
    $assertScript = Join-Path $PSScriptRoot "assert-kaggle-private.ps1"
    if (-not (Test-Path -LiteralPath $assertScript -PathType Leaf)) {
        Write-Error "REFUSED: missing private preflight: $assertScript"
        exit 1
    }
    if ($isKernelPush) {
        & $assertScript -KernelDir $targetPath
    } elseif ($isDatasetWrite) {
        & $assertScript -DatasetDir $targetPath
    } else {
        & $assertScript -ModelDir $targetPath
    }
    if ($LASTEXITCODE -ne 0) {
        Write-Error "REFUSED: Private/metadata preflight failed for $targetPath"
        exit 1
    }
}

$exe = Resolve-KaggleExe
if ($exe) {
    Save-KaggleCliPath -Path $exe
    & $exe @KaggleArgs
    exit $LASTEXITCODE
}

if (Test-Path -LiteralPath $VenvPython) {
    & $VenvPython -m kaggle @KaggleArgs
    $exitCode = $LASTEXITCODE
    if ($exitCode -eq 0) {
        exit 0
    }
}

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
    & python -m kaggle @KaggleArgs
    $exitCode = $LASTEXITCODE
    if ($exitCode -eq 0) {
        exit 0
    }
}

Write-KaggleCliMissing
