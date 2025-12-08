# Preview: list what would be copied (no changes)
$root = 'C:\TimerHavenWebsite'
$src = Join-Path $root 'TH-Guides\en'
$languages = @('fr','es','de','ru','el','ar')

if (-not (Test-Path $src)) {
  Write-Error "Source guide folder not found: $src"
  exit 1
}

Write-Output "Source folder: $src"
Write-Output ""
foreach ($lang in $languages) {
  $destDir = Join-Path $root ("TH-Guides\" + $lang)
  Write-Output "=== Language: $lang ==="
  Write-Output "Destination folder: $destDir"
  # list files that would be copied
  Get-ChildItem -Path $src -File | ForEach-Object {
    $dest = Join-Path $destDir $_.Name
    if (Test-Path $dest) {
      Write-Output "Would OVERWRITE (backup: $($_.Name + '.bak')): $dest"
    } else {
      Write-Output "Would COPY: $dest"
    }
  }
  Write-Output ""
}
Write-Output "Preview complete. No files were changed."