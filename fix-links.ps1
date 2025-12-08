$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Output "Running in site root: $root"

$files = Get-ChildItem -Path $root -Recurse -Filter *.html -ErrorAction SilentlyContinue
if (-not $files) { Write-Output "No HTML files found. Exiting."; exit 0 }

$previewCount = 0
Write-Output ""
Write-Output "=== PREVIEW: Files and lines that match the bad pattern ==="
foreach ($f in $files) {
  $text = Get-Content -Raw -LiteralPath $f.FullName -ErrorAction SilentlyContinue
  if (-not $text) { continue }
  $dqMatches = [regex]::Matches($text, 'href="[^"]*-en-[a-z]{2}(\-[A-Z]{2})?\.html"')
  foreach ($m in $dqMatches) {
    Write-Output ("File: {0}" -f $f.FullName)
    Write-Output ("  ORIG: {0}" -f $m.Value.Trim())
    $previewCount++
  }
  $sqMatches = [regex]::Matches($text, "href='[^']*-en-[a-z]{2}(\-[A-Z]{2})?\.html'")
  foreach ($m in $sqMatches) {
    Write-Output ("File: {0}" -f $f.FullName)
    Write-Output ("  ORIG: {0}" -f $m.Value.Trim())
    $previewCount++
  }
}

if ($previewCount -eq 0) { Write-Output ""; Write-Output "No occurrences found. Exiting."; exit 0 }

Write-Output ""
Write-Output ("Total matches found: {0}" -f $previewCount)
Write-Output ""
Write-Output "Press Enter to proceed with replacements, or Ctrl+C to abort."
Read-Host | Out-Null

$updateCount = 0
foreach ($f in $files) {
  try {
    $path = $f.FullName
    $origText = Get-Content -Raw -LiteralPath $path -ErrorAction Stop
    $newText = $origText -replace 'href="([^"]+)-en-([a-z]{2}(\-[A-Z]{2})?\.html)"','href="$1-$2"'
    $newText = $newText -replace "href='([^']+)-en-([a-z]{2}(\-[A-Z]{2})?\.html)'","href='$1-$2'"
    if ($newText -ne $origText) {
      Copy-Item -LiteralPath $path -Destination ($path + '.bak') -Force
      Set-Content -LiteralPath $path -Value $newText -Force
      Write-Output ("Updated: {0}" -f $path)
      $updateCount++
    }
  } catch {
    Write-Output ("Error processing {0}: {1}" -f $f.FullName, $_.Exception.Message)
  }
}

Write-Output ""
Write-Output ("Replacement complete. Files updated: {0}" -f $updateCount)

$remaining = 0
foreach ($f in $files) {
  $text = Get-Content -Raw -LiteralPath $f.FullName -ErrorAction SilentlyContinue
  if (-not $text) { continue }
  $countDq = ([regex]::Matches($text, 'href="[^"]*-en-[a-z]{2}(\-[A-Z]{2})?\.html"')).Count
  $countSq = ([regex]::Matches($text, "href='[^']*-en-[a-z]{2}(\-[A-Z]{2})?\.html'")).Count
  $remaining += ($countDq + $countSq)
}

Write-Output ("Remaining bad href occurrences: {0}" -f $remaining)
if ($remaining -eq 0) { Write-Output "Done. No remaining bad hrefs." } else { Write-Output "Some occurrences remain. See .bak files for originals." }