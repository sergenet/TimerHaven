
$tools = @{
    "calendar" = "free online calendar, localized calendar, productivity calendar, schedule planner"
    "habit-tracker" = "free habit tracker no account, daily routine tracker, habitify alternative, simple habit tracking"
    "timer" = "online timer, countdown timer, simple timer, digital timer"
    "unit-converter" = "online unit converter, metric to imperial converter, unit conversion tool"
    "notes" = "online notepad, privacy-first notes, quick notes app, minimalist writer"
    "world-clock" = "world clock, global time zones, current time world, city time converter"
    "focus-music" = "focus music online, lofi study music, deep work music, concentration sounds"
    "clipboard-manager" = "online clipboard, clipboard history manager, copy paste tool"
    "password-generator" = "secure password generator, random password tool, strong password creator"
    "countdown" = "event countdown timer, online countdown, days until counter"
    "currency" = "currency converter online, exchange rate tool, money converter"
    "weather" = "local weather, world weather forecast, current temperature"
}

$files = Get-ChildItem -Path "c:\TimerHavenWebsite" -Filter "*.html" -Exclude "index*.html", "pomodoro*.html", "meeting-planner*.html"

foreach ($file in $files) {
    try {
        $content = Get-Content $file.FullName -Raw
        $toolName = ""
        
        foreach ($key in $tools.Keys) {
            if ($file.Name -like "*$key*") {
                $toolName = $key
                break
            }
        }
        
        if ($toolName) {
            $keywords = $tools[$toolName]
            $updated = $false
            
            # 1. Update/Add Meta Keywords
            if ($content -notmatch '<meta name="keywords"') {
                $content = $content -replace '</head>', "`n  <meta name=`"keywords`" content=`"$keywords, productivity tools, privacy-first, no login`">`n</head>"
                $updated = $true
            }
            
            # 2. Add SEO Footer using Regex for robustness
            if ($content -notlike "*TimerHaven is your go-to destination*") {
                $footerRegex = '(?s)<footer.*?>.*?&copy; 2025 TimerHaven.*?</footer>'
                if ($content -match $footerRegex) {
                    $originalFooter = $matches[0]
                    # Extract internal links from original footer if possible, or just build a new one.
                    # For simplicity, we'll keep it consistent with the tool's keywords.
                    $seoParagraph = "<div style=`"font-size: 0.85em; color: #6b7c89; margin-bottom: 1em; max-width: 600px; margin-left: auto; margin-right: auto; text-align: center;`">" +
                                    "TimerHaven is your go-to destination for <strong>$($keywords.Split(',')[0])</strong> and other <strong>privacy-first productivity tools</strong>." +
                                    "</div>"
                    
                    # Inject SEO paragraph BEFORE the copyright text or just inside the footer
                    $newFooterContent = $originalFooter -replace '(&copy; 2025 TimerHaven\.)', "$seoParagraph`n    $1"
                    $content = $content -replace [regex]::Escape($originalFooter), $newFooterContent
                    $updated = $true
                }
            }
            
            if ($updated) {
                Write-Host "Updated SEO for $($file.Name)"
                Set-Content $file.FullName $content -NoNewline
            }
        }
    } catch {
        Write-Host "Error processing $($file.Name): $($_.Exception.Message)"
    }
}
