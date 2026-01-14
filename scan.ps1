# scan.ps1
# Place this file in the root folder of your website files (where index.html lives).
# Run in PowerShell:
#   powershell -ExecutionPolicy Bypass -File .\scan.ps1
# Output: patch-scan.txt with a line per HTML file showing HAS or MISSING or ERROR.

$log = Join-Path (Get-Location) 'patch-scan.txt'
if (Test-Path $log) { Remove-Item $log -Force }

Get-ChildItem -Path . -Filter *.html -Recurse -File | ForEach-Object {
  $path = $_.FullName
  try {
    $content = Get-Content -LiteralPath $path -Raw -ErrorAction Stop
    if ($content -match 'pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js') {
      Add-Content -Path $log -Value ("HAS:     " + $path)
    } else {
      Add-Content -Path $log -Value ("MISSING: " + $path)
    }
  } catch {
    Add-Content -Path $log -Value ("ERROR:   " + $path + " -> " + $_.Exception.Message)
  }
}

Write-Output ("Scan complete. See " + $log)