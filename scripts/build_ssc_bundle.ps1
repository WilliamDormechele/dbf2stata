param(
    [string]$ProjectDir = (Split-Path -Parent $PSScriptRoot)
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Set-Location $ProjectDir

$required = @(
    "stata\dbf2stata.ado",
    "stata\dbf2stata.sthlp",
    "docs\SSC_SUBMISSION_EMAIL.md"
)

foreach ($file in $required) {
    if (-not (Test-Path $file)) {
        throw "Required SSC submission file not found: $file"
    }
}

$outDir = Join-Path $ProjectDir "dist\ssc"
$stageDir = Join-Path $outDir "dbf2stata-ssc-submission"
$zipPath = Join-Path $outDir "dbf2stata-ssc-submission.zip"

Remove-Item $stageDir -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $zipPath -Force -ErrorAction SilentlyContinue

New-Item -ItemType Directory -Force $stageDir | Out-Null

Copy-Item "stata\dbf2stata.ado" $stageDir
Copy-Item "stata\dbf2stata.sthlp" $stageDir

$emailText = Get-Content "docs\SSC_SUBMISSION_EMAIL.md" -Raw
Set-Content `
    (Join-Path $stageDir "SUBMISSION_EMAIL.txt") `
    $emailText `
    -Encoding UTF8

Compress-Archive `
    -Path "$stageDir\*" `
    -DestinationPath $zipPath `
    -Force

Write-Host ""
Write-Host "SSC submission-preparation bundle created:"
Write-Host $zipPath
Write-Host ""

Get-ChildItem $stageDir |
    Format-Table Name, Length -AutoSize