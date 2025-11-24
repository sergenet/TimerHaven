param(
  [string]$Path = 'C:\timerhavenwebsite'
)

Get-ChildItem -Path $Path -Recurse -Filter *.html | ForEach-Object {
  $f = $_.FullName
  try {
    $t = Get-Content -Raw -Encoding UTF8 $f
  } catch {
    Write-Host "ERR READ: $f"
    return
  }
  if ($t -match '(?i)/tool-toolbar\.js') {
    Write-Host "SKIP (has script): $f"
  } elseif ($t -match '(?i)tool-card') {
    Write-Host "DRY-RUN: WOULD MODIFY $f"
  } else {
    Write-Host "SKIP (no tool-card): $f"
  }
}