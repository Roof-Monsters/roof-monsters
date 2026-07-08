$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$html = (Resolve-Path (Join-Path $root 'GROWTH-ROADMAP-PROPOSAL.html')).Path
$pdf = Join-Path $root 'GROWTH-ROADMAP-PROPOSAL.pdf'
$chrome = "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe"
if (-not (Test-Path $chrome)) { throw 'Chrome not found' }
if (Test-Path $pdf) { Remove-Item $pdf -Force }
$fileUri = 'file:///' + ($html -replace '\\', '/')
& $chrome --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$pdf" $fileUri
Start-Sleep -Seconds 3
Get-Item $pdf | Format-List Name, Length, LastWriteTime
