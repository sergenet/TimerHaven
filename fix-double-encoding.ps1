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

# Encodings
$utf8 = [System.Text.Encoding]::UTF8
$cp1252 = [System.Text.Encoding]::GetEncoding(1252)
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

# Read current file as UTF-8 (this yields the garbled characters like "Ã©")
$s = [System.IO.File]::ReadAllText($Path, $utf8)

# Interpret those characters as single-byte CP1252 values (get the bytes),
# then decode those bytes as UTF-8 to recover the original text.
$bytes = $cp1252.GetBytes($s)
$fixed = $utf8.GetString($bytes)

# Write fixed text back as UTF-8 (no BOM)
[System.IO.File]::WriteAllText($Path, $fixed, $utf8NoBom)

Write-Output "Fixed double-encoding and saved UTF-8 (no BOM): $Path"