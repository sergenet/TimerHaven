$root = 'C:\TimerHavenWebsite'
Write-Output "Applying safe removal of '-en' before .html in files under $root"

foreach ($f in Get-ChildItem -Path $root -Recurse -Filter *.html -File) {
  $p = $f.FullName
  try {
    $t = Get-Content -Raw -LiteralPath $p -ErrorAction Stop
  } catch {
    Write-Output "SKIP (read error): $p"
    continue
  }

  if ($t -match '-en(?=\.html)') {
    $n = $t -replace '-en(?=\.html)','-'
    Copy-Item -LiteralPath $p -Destination ($p + '.bak') -Force
    Set-Content -LiteralPath $p -Value $n -Force
    Write-Output "Updated: $p (backup: $($p + '.bak'))"
  }
}

Write-Output "Done."