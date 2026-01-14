# convert-and-zip.ps1
# Safe conversion of common web files to UTF-8 (no BOM), keep .enc.bak backups, then build a filtered zip.
# Run from C:\TimerHavenWebsite

Set-StrictMode -Version Latest

# File types to convert
$exts = @('*.html','*.htm','*.js','*.css','*.txt','*.json','*.xml')

# Convert files to UTF-8 (no BOM) if needed, keep backups as .enc.bak
Get-ChildItem -Recurse -File -Include $exts | ForEach-Object {
    $path = $_.FullName
    try {
        $bytes = [IO.File]::ReadAllBytes($path)
        if ($bytes.Length -eq 0) { continue }

        # detect BOMs / encodings
        if ($bytes.Length -ge 2 -and $bytes[0] -eq 0xFF -and $bytes[1] -eq 0xFE) {
            $enc = [System.Text.Encoding]::Unicode        # UTF-16 LE
        } elseif ($bytes.Length -ge 2 -and $bytes[0] -eq 0xFE -and $bytes[1] -eq 0xFF) {
            $enc = [System.Text.Encoding]::BigEndianUnicode
        } elseif ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
            $enc = [System.Text.Encoding]::UTF8           # UTF-8 with BOM
        } else {
            # conservative UTF-8 roundtrip test
            try {
                $s = [System.Text.Encoding]::UTF8.GetString($bytes)
                $re = [System.Text.Encoding]::UTF8.GetBytes($s)
                if ($re.Length -eq $bytes.Length) {
                    $enc = [System.Text.Encoding]::UTF8
                } else {
                    $enc = [System.Text.Encoding]::GetEncoding(1252)  # fallback ANSI/Windows-1252
                }
            } catch {
                $enc = [System.Text.Encoding]::GetEncoding(1252)
            }
        }

        # If not utf-8 without BOM, convert
        if ($enc.WebName -ne 'utf-8' -or ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF)) {
            # backup
            $bak = "$path.enc.bak"
            Copy-Item -LiteralPath $path -Destination $bak -Force

            # decode and re-encode as UTF8 without BOM
            $text = $enc.GetString($bytes)
            $utf8bytes = [System.Text.Encoding]::UTF8.GetBytes($text)
            [IO.File]::WriteAllBytes($path, $utf8bytes)

            Write-Output "Converted: $path (from $($enc.WebName) -> utf-8 no-bom) -> backup: $bak"
        } else {
            # already utf-8 without BOM (nothing to do)
        }
    } catch {
        Write-Warning "Skipped (error): $path - $_"
    }
}

# Build a temporary copy for zipping (exclude node_modules and .enc.bak and scripts and existing zips)
$tmp = Join-Path $env:TEMP "timerhaven_upload_utf8_tmp"
if (Test-Path $tmp) { Remove-Item -Recurse -Force $tmp }
New-Item -ItemType Directory -Path $tmp | Out-Null

# Use robocopy for a fast copy while excluding common bundles/backups
$exclDirs = @('node_modules')
$exclFiles = @('*.enc.bak','*.ps1','timerhaven_upload*.zip')
$xd = $exclDirs -join ' '
$xf = $exclFiles -join ' '
robocopy . $tmp /MIR /XD $exclDirs /XF $exclFiles /NFL /NDL /NP | Out-Null

# Create zip in current folder
$zipName = Join-Path (Get-Location) 'timerhaven_upload_utf8.zip'
if (Test-Path $zipName) { Remove-Item $zipName -Force }
Compress-Archive -Path (Join-Path $tmp '*') -DestinationPath $zipName -Force

# Summary
Write-Output "Created ZIP: $zipName"
$z = Get-Item $zipName
Write-Output "Size: $($z.Length) bytes"

# Clean up temp
Remove-Item -Recurse -Force $tmp

Write-Output "Done. Backups: *.enc.bak created beside original files."