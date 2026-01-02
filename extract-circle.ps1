$src = '.\app\src\main\res\drawable\ic_launcher_foreground.xml'
$backup = '.\app\src\main\res\drawable\ic_launcher_foreground.backup.xml'
$tmp = '.\app\src\main\res\drawable\circle_only.xml'

if (-not (Test-Path $src)) {
    Write-Error "Source file not found: $src"
    exit
}

if (-not (Test-Path $backup)) {
    Copy-Item $src $backup -Force
    Write-Host "Backup created: $backup"
} else {
    Write-Host "Backup already exists: $backup"
}

$content = Get-Content $src -Raw
$openTag = [regex]::Match($content,'<vector[^>]*>').Value

# search case-insensitively for the blue color hex used by the circle
$lower = $content.ToLower()
$match = [regex]::Match($lower,'<path[^>]*#0d6efd[^>]*/>')
if (-not $match.Success) {
    Write-Error "Blue circle path not found (searched for #0d6efd). Run: Get-Content $src -TotalCount 80 and paste output here."
    exit
}

$pathMatch = $content.Substring($match.Index, $match.Length)

$xml = $openTag + "`r`n    " + $pathMatch + "`r`n</vector>"
Set-Content -Path $tmp -Value $xml -Encoding UTF8
Write-Host "Temporary circle-only drawable written to: $tmp"