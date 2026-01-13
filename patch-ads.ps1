# patch-ads.ps1
# Place this file in the root folder of your website files (where index.html lives).
# Run from PowerShell:
#   powershell -ExecutionPolicy Bypass -File .\patch-ads.ps1
# The script creates .bak backups for any changed files.

$adsScript = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-0467059729557007" crossorigin="anonymous"></script>'

# Regex options: Singleline so .* matches newlines, IgnoreCase for case-insensitive
$regexOptions = [System.Text.RegularExpressions.RegexOptions]::Singleline -bor [System.Text.RegularExpressions.RegexOptions]::IgnoreCase

Get-ChildItem -Path . -Filter *.html -Recurse | ForEach-Object {
  $path = $_.FullName
  try {
    $content = Get-Content -LiteralPath $path -Raw -ErrorAction Stop
  } catch {
    Write-Warning ('Failed to read ' + $path + ' : ' + $_.Exception.Message)
    continue
  }

  if ($content -notmatch '(?i)</head>') {
    Write-Warning ('No </head> found in ' + $path + ' — skipped')
    continue
  }

  # Remove any existing adsbygoogle script tags (anywhere in file)
  $patternAds = '<script\b[^>]*pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^>]*>.*?</script>\s*'
  $contentClean = [regex]::Replace($content, $patternAds, '', $regexOptions)

  # Try to find an existing ca-pub id on the page; if present, preserve it
  $pubMatch = [regex]::Match($contentClean, 'ca-pub-\d+')
  if ($pubMatch.Success) { $firstId = $pubMatch.Value } else { $firstId = 'ca-pub-0467059729557007' }

  # Remove any existing window.__timerhaven_ad_client assignments
  $patternVar = 'window\.__timerhaven_ad_client[\s\S]*?;'
  $contentClean = [regex]::Replace($contentClean, $patternVar, '', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

  # Prepare the insertion block (var + newline-safe) using concatenation to avoid quoting issues
  $insertVar = '<script>' + "`r`n" + 'window.__timerhaven_ad_client = "' + $firstId + '";' + "`r`n" + '</script>'

  # Remove any accidental literal duplicates of the insertion block (defensive)
  $escapedInsert = [regex]::Escape($insertVar)
  $contentClean = [regex]::Replace($contentClean, $escapedInsert, '', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

  # Insert var + ads script before the first closing </head> only
  $regexHead = New-Object System.Text.RegularExpressions.Regex('</head>', $regexOptions)
  $newContent = $regexHead.Replace($contentClean, $insertVar + "`r`n" + $adsScript + "`r`n</head>", 1)

  if ($newContent -ne $content) {
    Copy-Item -LiteralPath $path -Destination ($path + '.bak') -Force
    Set-Content -LiteralPath $path -Value $newContent -Encoding UTF8
    Write-Output ('patched: ' + $path + ' (backup: ' + ($path + '.bak') + ')')
  } else {
    Write-Output ('no changes required: ' + $path)
  }
}