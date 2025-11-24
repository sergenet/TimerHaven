# fix-i18n-filenames.ps1
# Dry-run script to normalize filenames like "pomodoro-en-fr.html" -> "pomodoro-fr.html"
# Usage: run from repository root. This script is SAFE by default ($dryRun = $true).
# To apply changes: set $dryRun = $false and re-run the script (after reviewing the report).

# === Configuration ===
$langs = @('en','fr','es','de','ru','el','ar')
$dryRun = $true   # Set to $false to APPLY changes after reviewing report
$report = "i18n-filename-fix-report.txt"

if (Test-Path $report) { Remove-Item $report -Force }

Write-Host "Scanning for candidate files..."
$candidates = Get-ChildItem -Recurse -File -Filter '*.html' |
  Where-Object {
    $parts = $_.BaseName -split '-'
    ($parts.Length -ge 3) -and ($langs -contains $parts[-1])
  }

"`nFound $($candidates.Count) candidate files to examine`n" | Tee-Object -FilePath $report -Append

$plans = @()
foreach ($f in $candidates) {
  $parts = $f.BaseName -split '-'
  if ($parts.Length -lt 3) { continue }
  $baseParts = $parts[0..($parts.Length - 3)]
  if ($baseParts.Count -eq 0) { continue }
  $base = ($baseParts -join '-')
  $lang = $parts[-1]
  if ($langs -notcontains $lang) { continue }
  $oldName = $f.Name
  $newName = "$base-$lang$($f.Extension)"
  $plans += [pscustomobject]@{ Old=$f.FullName; OldName=$oldName; NewName=$newName; Dir=$f.DirectoryName }
}

if ($plans.Count -eq 0) {
  "No multi-language filename issues found." | Tee-Object -FilePath $report -Append
  Write-Host "No candidate files found."
  return
}

"Planned renames (old -> new):" | Tee-Object -FilePath $report -Append
$plans | ForEach-Object { "$($_.OldName) -> $($_.NewName)" | Tee-Object -FilePath $report -Append }

Write-Host "Planned renames written to $report"
Write-Host "Sample (first 10):"
$plans[0..([math]::Min(9,$plans.Count-1))] | ForEach-Object { Write-Host "$($_.OldName) -> $($_.NewName)" }

if ($dryRun) {
  Write-Host "`nDRY RUN: No files changed. Inspect $report. To apply changes, set `$dryRun = $false` in this script and re-run."
  return
}

# ---------- APPLY CHANGES ----------
Write-Host "`nApplying changes..."
git fetch origin

# Create branch based on complete-TH-site-files if it exists, otherwise from current HEAD
$remoteBranch = "origin/complete-TH-site-files"
$branchName = "fix/i18n-filenames"
try {
  git rev-parse --verify $remoteBranch > $null 2>&1
  git checkout -b $branchName $remoteBranch
} catch {
  Write-Host "Remote branch origin/complete-TH-site-files not found; creating $branchName from current HEAD"
  git checkout -b $branchName
}

foreach ($p in $plans) {
  $oldPath = $p.Old
  $newPath = Join-Path $p.Dir $p.NewName
  Write-Host "Renaming $($p.OldName) -> $($p.NewName)"
  Rename-Item -Path $oldPath -NewName $p.NewName -Force
}

# Update references in HTML/JS/JSON files
Get-ChildItem -Recurse -File -Include *.html,*.js,*.json | ForEach-Object {
  $file = $_.FullName
  $text = Get-Content -Raw -Path $file
  $changed = $false
  foreach ($p in $plans) {
    $oldName = [regex]::Escape($p.OldName)
    $newName = $p.NewName
    if ($text -match $oldName) {
      $text = $text -replace $oldName, $newName
      $changed = $true
    }
  }
  if ($changed) {
    Set-Content -Path $file -Value $text
    Write-Host "Updated references in: $file"
  }
}

git add -A
git commit -m "fix(i18n): normalize localized filenames (e.g. pomodoro-fr) and update internal links"
git push -u origin $branchName
Write-Host "Pushed branch $branchName"
Write-Host "Open a PR: https://github.com/sergenet/TimerHaven/pull/new/$branchName"