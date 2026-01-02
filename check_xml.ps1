# save as check_xml.ps1 in the project root (the folder that contains the "app" folder)
$files = Get-ChildItem -Path ".\app\src\main\res" -Recurse -Filter *.xml -File
foreach ($f in $files) {
  try { $bytes = [System.IO.File]::ReadAllBytes($f.FullName) } catch { $bytes = @() }
  if ($bytes.Length -gt 0) {
    $len = [Math]::Min(7, $bytes.Length - 1)
    $hex = ($bytes[0..$len] | ForEach-Object { '{0:X2}' -f $_ }) -join ' '
  } else {
    $hex = "<empty>"
  }
  try { $firstLine = Get-Content -Path $f.FullName -TotalCount 1 -ErrorAction Stop } catch { $firstLine = "<cannot-read-as-text>" }

  $isProblem = $false
  if ($hex -match '^89 50 4E 47' -or $hex -match '^FF D8 FF' -or $hex -match '^FF FE' -or $hex -match '^FE FF' -or $hex -match '^00 3C' -or $hex -match '^EF BB BF') {
    $isProblem = $true
  }

  if ($isProblem) {
    Write-Output "PROBLEM: $hex  ->  $($f.FullName)"
    Write-Output "FirstVisible: $firstLine"
    Write-Output "-----"
  } else {
    Write-Output "OK: $hex  ->  $($f.FullName)"
  }
}