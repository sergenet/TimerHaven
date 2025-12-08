param(
  [Parameter(Mandatory=$true)]
  [string]$Path
)

if (-not (Test-Path $Path)) {
  Write-Error "File not found: $Path"
  exit 1
}

$bak = "$Path.bak.$((Get-Date).ToString('yyyyMMddHHmmss'))"
Copy-Item -LiteralPath $Path -Destination $bak -Force
Write-Output "Backup written to: $bak"

# Read bytes and decode as CP1252 (Windows-1252)
$bytes = [System.IO.File]::ReadAllBytes($Path)
$text = [System.Text.Encoding]::GetEncoding(1252).GetString($bytes)

# Create UTF8 encoding without BOM and write file
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($Path, $text, $utf8NoBom)

Write-Output "Converted and saved as UTF-8 (no BOM): $Path"