$p = 'app\src\main\res\values-fr\strings.xml' $bk = Join-Path $PWD ("strings_fr_backup_{0}.bak" -f (Get-Date -Format yyyyMMddHHmmss)) Copy-Item $p $bk -Force $txt = [System.IO.File]::ReadAllText($p)

remove backslashes that create \u style escapes
$txt = $txt -replace '\',''

normalize smart quotes/dashes (and common mojibake variants) to safe ASCII
$txt = $txt -replace '’', "'" $txt = $txt -replace '‘', "'" $txt = $txt -replace '“', '"' $txt = $txt -replace '”', '"' $txt = $txt -replace '–', '-' $txt = $txt -replace '—', '-' $txt = $txt -replace 'â€™', "'" # handle mojibake variants $txt = $txt -replace 'â€˜', "'" $txt = $txt -replace 'â€œ', '"' $txt = $txt -replace 'â€', '"' $txt = $txt -replace 'â€“', '-' $txt = $txt -replace 'â€”', '-'

remove control characters except newline/carriage/tab
$chars = $txt.ToCharArray() | ForEach-Object { if ([int]$_ -lt 32 -and $_ -ne "n" -and $_ -ne "r" -and $_ -ne "`t") { '' } else { $_ } } $txt = -join $chars

ensure there is a resources wrapper
if (-not $txt.TrimStart().StartsWith('<resources')) { $txt = "<resources>rn" + $txt + "rn</resources>" }

write UTF-8 without BOM
[System.IO.File]::WriteAllText($p, $txt, (New-Object System.Text.UTF8Encoding($false))) Write-Output "Sanitized file written; backup at $bk"