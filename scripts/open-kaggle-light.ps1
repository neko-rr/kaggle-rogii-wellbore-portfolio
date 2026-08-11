# Kaggle-Light Profile で Cursor を起動する（汎用スクリプト）
# 使い方: コンペフォルダ直下で .\scripts\open-kaggle-light.ps1

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$ProfileName = "Kaggle-Light"

$CursorCandidates = @(
    "${env:ProgramFiles}\cursor\Cursor.exe",
    "${env:LOCALAPPDATA}\Programs\cursor\Cursor.exe"
)

$CursorExe = $CursorCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $CursorExe) {
    Write-Error "Cursor.exe が見つかりません。Cursor のインストール先を確認してください。"
}

Write-Host "Profile: $ProfileName"
Write-Host "Folder : $ProjectRoot"
Write-Host "Cursor : $CursorExe"

Start-Process -FilePath $CursorExe -ArgumentList @("--new-window", "--profile", $ProfileName, $ProjectRoot)
