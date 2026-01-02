# remove_bom.ps1
# Safe: makes .bak backups before changing files.
$root = Join-Path $PWD 'app\src\main\res'
$files = Get-ChildItem -Path $root -Recurse -Filter *.xml -File
foreach ($f in $files) {
  $path = $f.FullName
  try {
    $bytes = [System.IO.File]::ReadAllBytes($path)
  } catch {
    Write-Output "ERROR reading: $path"
    continue
  }
  if ($bytes.Length -lt 1) { Write-Output "EMPTY: $path"; continue }

  $changed = $false

  # Remove one or more leading UTF-8 BOM sequences (EF BB BF)
  while ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    $bytes = $bytes[3..($bytes.Length - 1)]
    $changed = $true
  }

  # Convert UTF-16 LE/BE to UTF-8 if present
  if (-not $changed -and $bytes.Length -ge 2) {
    if ($bytes[0] -eq 0xFF -and $bytes[1] -eq 0xFE) {
      # UTF-16 little-endian
      $str = [System.Text.Encoding]::Unicode.GetString($bytes)
      $bytes = [System.Text.Encoding]::UTF8.GetBytes($str)
      $changed = $true
    } elseif ($bytes[0] -eq 0xFE -and $bytes[1] -eq 0xFF) {
      # UTF-16 big-endian
      $str = [System.Text.Encoding]::BigEndianUnicode.GetString($bytes)
      $bytes = [System.Text.Encoding]::UTF8.GetBytes($str)
      $changed = $true
    }
  }

  if ($changed) {
    Copy-Item -LiteralPath $path -Destination "$path.bak" -Force
    try {
      [System.IO.File]::WriteAllBytes($path, $bytes)
      Write-Output "FIXED: $path  (backup -> $path.bak)"
    } catch {
      Write-Output "ERROR writing: $path"
    }
  } else {
    Write-Output "OK: $path"
  }
}