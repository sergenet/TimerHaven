# inspect-index.ps1
# Usage:
#   cd "C:\TimerHavenWebsite"
#   powershell -ExecutionPolicy Bypass -File .\inspect-index.ps1
#
# This script:
# - prints the context around each occurrence of "page-title" in index.html
# - extracts the <head>...</head> content to index-head-index.txt and prints its first 200 lines

$path = ".\index.html"

if (-not (Test-Path $path)) {
  Write-Error "File not found: $path"
  exit 1
}

# Read lines for context printing
$lines = Get-Content -LiteralPath $path

# Find all matches of the string "page-title"
$matches = Select-String -Path $path -Pattern '"page-title"' -AllMatches

if ($matches.Count -eq 0) {
  Write-Output "No occurrences of ""page-title"" found in $path"
} else {
  foreach ($m in $matches) {
    $ln = $m.LineNumber
    $start = [math]::Max(1, $ln - 8)
    $end = [math]::Min($lines.Count, $ln + 12)
    Write-Output ("---- context around line {0} in {1} ----" -f $ln, $path)
    $n = $start
    for ($i = $start - 1; $i -le $end - 1; $i++) {
      "{0,4}: {1}" -f $n, $lines[$i]
      $n++
    }
    Write-Output ""
  }
}

# Extract <head> ... </head> content and write to a file for easier review
$content = Get-Content -Raw -LiteralPath $path
$headMatch = [regex]::Match($content, '(?is)<head\b[^>]*>(.*?)</head>')
if ($headMatch.Success) {
  $headText = $headMatch.Groups[1].Value
  $outFile = ".\index-head-index.txt"
  $headText | Out-File -FilePath $outFile -Encoding UTF8
  Write-Output ("Wrote head content to: " + $outFile)
  Write-Output "First 200 lines of head (or fewer):"
  Get-Content -LiteralPath $outFile -TotalCount 200 | ForEach-Object { $_ }
} else {
  Write-Warning "No <head>...</head> match found in $path"
}