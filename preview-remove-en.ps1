$root = 'C:\TimerHavenWebsite'
Write-Output "Preview: scanning HTML files under $root"
$found = $false

foreach ($f in Get-ChildItem -Path $root -Recurse -Filter *.html -File) {
  $p = $f.FullName
  try {
    $t = Get-Content -Raw -LiteralPath $p -ErrorAction Stop
  } catch {
    Write-Output "SKIP (read error): $p"
    continue
  }

  if ($t -match '-en(?=\.html)') {
    if (-not $found) { $found = $true; Write-Output ""; Write-Output "Files that WOULD be changed:" }
    Write-Output $p
    # show the matching link fragments for that file
    [regex]::Matches($t,'([^\s"''>]*-en-[a-z]{2}(?:-[A-Z]{2})?\.html)') | ForEach-Object { Write-Output "  match: $($_.Value)" }
    Write-Output ""
  }
}

if (-not $found) { Write-Output "No files need changing." }