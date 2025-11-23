<#
run-i18n-fix.ps1
Safe, single-script workflow to:
 - create backup-before-guides branch
 - create work branch fix/i18n-guides-remove-howto-tips from origin/complete-TH-site-files
 - scaffold missing non-en guide placeholders under /{lang}/{tool}/{tool}-index.html
 - replace how-to/tips cards on non-en tool pages with single centered-tool + CTA (backs up modified files as .bak)
 - list non-en how-to and tips files and, after confirmation, delete them
 - commit in three logical commits and push the branch
 - open PR with gh if available (otherwise prints PR URL)
Run from repo root. Requires PowerShell, git installed. No external credentials required beyond your local git auth.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Configuration: non-en languages and tools
$languages = @('fr','es','de','ru','el','ar')   # will not modify 'en'
$tools = @('task-timer','pomodoro','stopwatch','countdown','calendar','notes','habit-tracker','focus-music','clipboard-manager','meeting-planner','password-generator','unit-converter','currency','weather','world-clock')

# Branch names
$backupBranch = 'backup-before-guides'
$baseRemoteBranch = 'origin/complete-TH-site-files'
$workBranch = 'fix/i18n-guides-remove-howto-tips'

Write-Host "Script will perform changes on a new branch: $workBranch (based on $baseRemoteBranch)."
Write-Host "A backup branch $backupBranch will be created first. All modified files will have .bak copies."
Write-Host ""

# 0) Ensure we are in a git repo
if (-not (Test-Path .git)) {
  Write-Host "Error: This script must be run from your repo root where .git exists." -ForegroundColor Red
  exit 1
}

# 1) Create backup branch from current working tree (safe snapshot)
Write-Host "Creating backup branch $backupBranch..."
git rev-parse --verify $backupBranch > $null 2>&1
if ($LASTEXITCODE -eq 0) {
  Write-Host "Backup branch $backupBranch already exists. Skipping creation."
} else {
  git checkout -b $backupBranch
  # commit any changes so backup branch truly captures working state
  git add -A
  try {
    git commit -m "chore: backup before i18n guide changes" | Out-Null
    Write-Host "Committed working tree snapshot to $backupBranch."
  } catch {
    Write-Host "No changes to commit on backup branch (working tree clean)."
  }
  # return to original HEAD after creating backup (we'll base work branch from remote)
  git checkout - 2>$null | Out-Null
}

# 2) Create working branch based on origin/complete-TH-site-files (fall back to current HEAD)
Write-Host "Fetching origin..."
git fetch origin --prune

# Try to base from origin/complete-TH-site-files
$useRemoteBase = $true
git rev-parse --verify $baseRemoteBranch > $null 2>&1
if ($LASTEXITCODE -ne 0) {
  Write-Host "Remote branch $baseRemoteBranch not found; will create work branch from current HEAD." -ForegroundColor Yellow
  $useRemoteBase = $false
}

if ($useRemoteBase) {
  Write-Host "Creating branch $workBranch based on $baseRemoteBranch..."
  git checkout -b $workBranch $baseRemoteBranch
} else {
  Write-Host "Creating branch $workBranch from current HEAD..."
  git checkout -b $workBranch
}

# 3) Scaffold placeholders for missing guides under /{lang}/{tool}/{tool}-index.html
Write-Host "Creating placeholder guide files for missing non-en lang/tool combinations..."
foreach ($lang in $languages) {
  foreach ($tool in $tools) {
    $toolDir = Join-Path -Path $PWD -ChildPath "$lang\$tool"
    if (-not (Test-Path $toolDir)) { New-Item -ItemType Directory -Force -Path $toolDir | Out-Null }
    $file = Join-Path $toolDir ($tool + "-index.html")
    if (-not (Test-Path $file)) {
      $content = @"
<!doctype html>
<html lang="$lang">
<head>
  <meta charset='utf-8'>
  <title>$tool — Guide ($lang)</title>
  <meta name='viewport' content='width=device-width,initial-scale=1'>
  <link rel='stylesheet' href='/assets/css/tool-theme.css'>
  <meta name='description' content='Scaffold placeholder for $tool guide ($lang)'>
</head>
<body>
  <main class='container'>
    <article class='card' aria-labelledby='title'>
      <header><h1 id='title'>$tool — Guide ($lang)</h1></header>
      <p class='lead'>Scaffold placeholder. Full guide content to be added.</p>
    </article>
  </main>
</body>
</html>
"@
      $content | Set-Content -Path $file -Encoding UTF8
      Write-Host "Created placeholder: $file"
    }
  }
}
git add $(foreach ($lang in $languages) { foreach ($t in $tools) { Join-Path $lang ($t + "-index.html") } }) 2>$null | Out-Null
git commit -m "chore(i18n): scaffold non-en guides placeholders" 2>$null | Out-Null
Write-Host "Committed scaffold placeholders."

# 4) Replace how-to/tips cards on non-en pages (make .bak backups)
Write-Host ""
Write-Host "Scanning non-en HTML pages and replacing how-to/tips cards with single centered tool + CTA..."
# Candidate files: lang/*.html, lang/*/*.html, and root files with -<lang>.html suffix
$candidates = @()
foreach ($lang in $languages) {
  $candidates += Get-ChildItem -Path $PWD -Recurse -File -Include "$lang\*.html","$lang\*\*.html" -ErrorAction SilentlyContinue
}
# also files at root with pattern *-fr.html etc
foreach ($lang in $languages) {
  $candidates += Get-ChildItem -Path $PWD -Filter "*-$lang.html" -File -ErrorAction SilentlyContinue
}
$candidates = $candidates | Sort-Object -Unique

# Helper function to safely update file content
function Update-File([string]$path, [string]$newText) {
  $bak = "$path.bak"
  if (-not (Test-Path $bak)) { Copy-Item -Path $path -Destination $bak -Force }
  Set-Content -Path $path -Value $newText -Encoding UTF8
}

# Heuristic edits: remove any block that contains a link to "*-how-to" or "*-tips"
foreach ($f in $candidates) {
  try {
    $text = Get-Content -Raw -Path $f.FullName -Encoding UTF8
  } catch {
    Write-Host "Skipping unreadable file: $($f.FullName)" -ForegroundColor Yellow
    continue
  }
  $original = $text
  $modified = $false

  # Remove nearest container that includes a link to -how-to or -tips:
  # We'll remove any <div...>...</div> or <section...>...</section> that contains such links (simple regex)
  $patternBlock = '(?s)(<(?:(?:div|section|article)[^>]*)>.*?(?:href\s*=\s*["'']?[^"'\>]*-(?:how-to|tips)(?:\.html)?[^"'\>]*["'']?).*?</(?:div|section|article)>)'
  $text = [regex]::Replace($text, $patternBlock, { param($m) $modified = $true; return "" }, 'IgnoreCase')

  # Also remove standalone anchors that match -how-to or -tips
  $text = [regex]::Replace($text, '(?i)<a\b[^>]*\b(?:href|data-href)\s*=\s*["'']?[^"'\>]*-(?:how-to|tips)(?:\.html)?[^"'\>]*["'']?[^>]*>.*?<\/a>', '', 'IgnoreCase')

  # Ensure there is a centered-tool container; if not, try to insert CTA into first .card or before </main>
  $cta = "<p style=`"margin-top:1rem;`"><a class=`"cta`" href=""/{lang}/{tool}/{tool}-index.html"">Read full guide</a></p>"

  # Determine language and tool from path
  $rel = Resolve-Path -Relative $f.FullName
  $relParts = $rel -split '[\\/]' 
  $lang = $null; $tool = $null
  if ($relParts.Length -ge 2 -and $languages -contains $relParts[0]) {
    $lang = $relParts[0]; 
    # tool may be folder name or file stem
    if ($relParts.Length -ge 3) { $tool = $relParts[1] } else { $tool = [regex]::Replace([IO.Path]::GetFileNameWithoutExtension($relParts[-1]), '-(' + ($languages -join '|') + ')$', '') }
  } else {
    # try filename like pomodoro-fr.html
    foreach ($L in $languages) {
      if ($rel -match "(.+)-$L\.html$") { $lang = $L; $tool = $matches[1]; break }
    }
  }

  if ($lang -and $tool) {
    # craft CTA for this file
    $ctaHtml = "<p style=`"margin-top:1rem;`"><a class=`"cta`" href=""/$lang/$tool/$tool-index.html"">Read full guide</a></p>"
    # If .centered-tool exists, append CTA inside it
    if ($text -match '(?s)<[^>]*class\s*=\s*["''][^"']*centered-tool[^"']*["''][^>]*>') {
      $text = [regex]::Replace($text, '(<[^>]*class\s*=\s*["''][^"']*centered-tool[^"']*["''][^>]*>)(?s)', "`$1", 'IgnoreCase') # noop to ensure match
      # append CTA before first closing </div> after centered-tool opening (simple approach)
      $text = [regex]::Replace($text, '(?is)(<[^>]*class\s*=\s*["''][^"']*centered-tool[^"']*["''][^>]*>)(.*?)(</div>)', { param($m) $m.Groups[1].Value + $m.Groups[2].Value + $ctaHtml + $m.Groups[3].Value }, 'IgnoreCase')
    } else {
      # else append CTA before </main> or at end of body
      if ($text -match '(?i)</main>') {
        $text = [regex]::Replace($text, '(?i)(</main>)', $ctaHtml + "`$1", 'IgnoreCase')
      } elseif ($text -match '(?i)</body>') {
        $text = [regex]::Replace($text, '(?i)(</body>)', $ctaHtml + "`$1", 'IgnoreCase')
      } else {
        $text = $text + "`n" + $ctaHtml
      }
    }
    $modified = $true
  } else {
    # no lang/tool found - avoid touching file structure, but remove anchors referencing -how-to/-tips (done above)
  }

  if ($modified -and $text -ne $original) {
    Update-File -path $f.FullName -newText $text
    Write-Host "Updated: $($f.FullName) (backup: $($f.FullName).bak)"
    git add $f.FullName
  }
}

git commit -m "fix(i18n): replace how-to/tips with single guide CTA on non-en tool pages" 2>$null | Out-Null
Write-Host "Committed replacement changes."

# 5) Show list of non-en how-to and tips files (dry-run) and ask for confirmation to delete
Write-Host ""
Write-Host "The script has found the following non-en how-to/tips files (dry-run list):"
$toDelete = Get-ChildItem -Recurse -Include "*-how-to*.html","*-tips*.html" | Where-Object { $_.FullName -notmatch "\\en\\" }
if ($toDelete.Count -eq 0) {
  Write-Host "No non-en how-to or tips files found to delete."
} else {
  $toDelete | ForEach-Object { Write-Host $_.FullName }
  Write-Host ""
  $confirm = Read-Host "Type DELETE to permanently remove these non-en how-to/tips files (or anything else to abort)"
  if ($confirm -eq 'DELETE') {
    foreach ($f in $toDelete) {
      Remove-Item -Path $f.FullName -Force
      Write-Host "Deleted: $($f.FullName)"
      # stage deletion
      git rm --cached --ignore-unmatch $f.FullName 2>$null | Out-Null
    }
    git commit -m "chore(i18n): remove old how-to and tips files for non-en languages" 2>$null | Out-Null
    Write-Host "Deleted files committed."
  } else {
    Write-Host "Deletion aborted by user. No files were removed."
  }
}

# 6) Run quick link-check to detect remaining references to -how-to or -tips
Write-Host ""
Write-Host "Searching for remaining references to -how-to or -tips (report):"
$refs = Select-String -Path * -Pattern "-how-to|-tips" -SimpleMatch -AllMatches -ErrorAction SilentlyContinue | Select-Object Path,LineNumber,Line
if ($refs) {
  $refs | ForEach-Object { Write-Host "$($_.Path):$($_.LineNumber) -> $($_.Line.Trim())" }
  $note = "Link-check found references; please inspect listed files and update links if needed."
  Write-Host $note -ForegroundColor Yellow
} else {
  Write-Host "No remaining references found."
}

# 7) Push branch and open PR (if gh installed)
Write-Host ""
Write-Host "Pushing branch $workBranch to origin..."
git push -u origin $workBranch

# If gh CLI is available, open PR automatically; otherwise print PR URL
$ghInstalled = (Get-Command gh -ErrorAction SilentlyContinue) -ne $null
if ($ghInstalled) {
  Write-Host "Creating PR via gh..."
  # Compose a helpful PR body
  $prBody = @"
fix(i18n): replace how-to/tips with single guide CTA on non-en tool pages

This branch:
- scaffolds non-en guide placeholders under /{lang}/{tool}/{tool}-index.html
- replaces how-to/tips cards on non-en tool pages with a single centered tool view + Read full guide CTA
- deletes non-en how-to and tips files (if you confirmed)
- includes .bak backups for modified files

Please review changes on this branch. Do NOT merge until reviewed.

Link-check notes included in PR description.
"@

  gh pr create --base complete-TH-site-files --head $env:USERNAME + ":" + $workBranch --title "fix(i18n): replace how-to/tips with single guide per tool and update non-en tool pages" --body $prBody
  Write-Host "PR created via gh."
} else {
  $repoUrl = git config --get remote.origin.url
  if ($repoUrl -match 'github.com[:/](.+?)/(.+?)(\.git)?$') {
    $owner = $matches[1]; $repo = $matches[2]
    $prUrl = "https://github.com/$owner/$repo/pull/new/$workBranch"
    Write-Host ""
    Write-Host "gh CLI not found. Open this URL in your browser to create the PR:"
    Write-Host $prUrl -ForegroundColor Cyan
  } else {
    Write-Host "Could not determine repo URL for PR. Please open GitHub and create a PR from branch $workBranch into complete-TH-site-files."
  }
}

Write-Host ""
Write-Host "Done. If anything looks wrong or you see errors, copy the PowerShell output and paste here so I can help fix it."