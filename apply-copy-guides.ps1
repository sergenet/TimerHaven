# Apply: copy TH-Guides/en -> TH-Guides/<lang> for languages list
# Creates .bak for any overwritten files.
param(
  [switch]$ForceOverwrite  # use -ForceOverwrite to overwrite existing files without prompting
)

$root = 'C:\TimerHavenWebsite'
$src = Join-Path $root 'TH-Guides\en'
$languages = @('fr','es','de','ru','el','ar')

if (-not (Test-Path $src)) {
  Write-Error "Source guide folder not found: $src"
  exit 1
}

$files = Get-ChildItem -Path $src -File
if ($files.Count -eq 0) {
  Write-Output "No files found in source folder: $src"
  exit 0
}

foreach ($lang in $languages) {
  $destDir = Join-Path $root ("TH-Guides\" + $lang)
  if (-not (Test-Path $destDir)) {
    New-Item -Path $destDir -ItemType Directory -Force | Out-Null
    Write-Output "Created folder: $destDir"
  } else {
    Write-Output "Using existing folder: $destDir"
  }

  foreach ($f in $files) {
    $srcPath = $f.FullName
    $destPath = Join-Path $destDir $f.Name

    if (Test-Path $destPath) {
      if ($ForceOverwrite) {
        $bak = $destPath + '.bak'
        Copy-Item -LiteralPath $destPath -Destination $bak -Force
        Copy-Item -LiteralPath $srcPath -Destination $destPath -Force
        Write-Output "Overwrote: $destPath (backup: $bak)"
      } else {
        Write-Output "Skipped existing: $destPath (use -ForceOverwrite to overwrite)"
      }
    } else {
      Copy-Item -LiteralPath $srcPath -Destination $destPath -Force
      Write-Output "Copied: $destPath"
    }
  }
  Write-Output ""
}

Write-Output "Copy complete. If any files were overwritten, backups have .bak appended to the original filenames."