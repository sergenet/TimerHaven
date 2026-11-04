import os
import re

directory = r'C:\TimerHavenWebsite'

updates = {
    'timer-en.html': {
        'title': 'Deep Work Timeboxing Session Timer Online | TimerHaven',
        'desc': 'Structure your workday with our deep work timeboxing session timer. A minimalist, privacy-first tool to enforce strict time blocks and prevent burnout.',
        'keys': 'timeboxing timer, deep work session timer, timebox tool online, adhd timeboxing, flow state timer',
        'h3_title': '<i class="fa fa-hourglass-half"></i> Deep Work Timeboxing Session Timer',
        'intro': 'Master your schedule with timeboxing. Allocate fixed time periods to specific tasks and use our visual timer to enforce boundaries, ensuring you stop when the time is up.',
        'overview_h4': 'The Timeboxing Method',
        'p1': 'Timeboxing forces you to prioritize. Instead of working on a task until it\'s "done," you work on it for a strict 30 or 60-minute block. When the timer rings, you stop. This prevents perfectionism and Parkinson\'s Law (work expanding to fill the time allotted).',
        'p2': 'Tip: Combine this timer with our Eisenhower Matrix guide. Pick your most urgent, important task and box out 90 minutes of deep work for it before checking any emails.'
    },
    'notes-en.html': {
        'title': 'Distraction-Free Auto-Saving Browser Notepad | TimerHaven',
        'desc': 'Capture thoughts instantly with our distraction-free, auto-saving browser notepad. No login required, everything stays local to your machine for ultimate privacy.',
        'keys': 'distraction free browser notepad, auto saving local notepad, privacy first text editor, quick online notes, adhd brain dump tool',
        'h3_title': '<i class="fa fa-note-sticky"></i> Distraction-Free Auto-Saving Browser Notepad',
        'intro': 'A perfectly blank canvas for your brain dumps. No formatting ribbons, no logins, and zero cloud syncing. Everything you type autosaves directly to your local browser.',
        'overview_h4': 'The Power of a Brain Dump',
        'p1': 'When you\'re trying to focus, stray thoughts ("Did I buy milk?", "Email Sarah") will derail you. A distraction-free notepad allows you to instantly capture these open loops without switching contexts or opening a heavy app like Notion.',
        'p2': 'Tip: Keep this notepad pinned in a browser tab. Treat it as your temporary inbox. At the end of the day, process these notes into your main calendar or task manager.'
    },
    'clipboard-manager-en.html': {
        'title': 'Privacy-First Local Browser Clipboard Manager | TimerHaven',
        'desc': 'Store and organize text snippets securely with our privacy-first local browser clipboard manager. No data leaves your device. 100% free and ad-free.',
        'keys': 'privacy first clipboard manager, local browser clipboard history, secure text snippet tool, offline clipboard manager online',
        'h3_title': '<i class="fa fa-clipboard-list"></i> Privacy-First Local Browser Clipboard Manager',
        'intro': 'Stop pasting passwords into shady cloud apps. Our clipboard manager saves your frequently used snippets entirely locally within your browser\'s storage. Your data never touches our servers.',
        'overview_h4': 'Secure Snippet Management',
        'p1': 'Whether you are doing repetitive data entry, coding, or managing customer support emails, a clipboard manager saves hours. By keeping it browser-based and local, you eliminate the security risks associated with third-party cloud tools.',
        'p2': 'Tip: Use this tool to hold email templates, hex color codes, or complex terminal commands. Since it runs offline, you can rely on it even when traveling or disconnected.'
    },
    'countdown-en.html': {
        'title': 'Aesthetic Full Screen Event Countdown Clock | TimerHaven',
        'desc': 'Create beautiful, customizable countdowns for any event. Our aesthetic full-screen countdown clock is perfect for classrooms, presentations, and product launches.',
        'keys': 'aesthetic full screen countdown clock, visual event countdown timer, classroom countdown online, minimalist presentation timer',
        'h3_title': '<i class="fa fa-stopwatch-20"></i> Aesthetic Full Screen Event Countdown Clock',
        'intro': 'Build anticipation or manage time beautifully. Set a target date or duration and project a clean, aesthetic countdown clock for your next presentation, sprint, or major life event.',
        'overview_h4': 'Visual Time Management',
        'p1': 'A full-screen countdown acts as a powerful psychological anchor. In a classroom or meeting room, displaying a large, clean timer keeps everyone aligned and creates a sense of urgency without anxiety.',
        'p2': 'Tip: Use the full-screen feature during workshops to limit Q&A sessions. The visual cue is often more effective than verbally interrupting a speaker.'
    },
    'password-generator-en.html': {
        'title': 'Memorable Secure Passphrase Generator | TimerHaven',
        'desc': 'Generate mathematically secure but highly memorable passphrases. Our local, offline generator creates strong word combinations that won\'t get hacked.',
        'keys': 'memorable secure passphrase generator, pronounceable password creator, correct horse battery staple generator, local offline password generator',
        'h3_title': '<i class="fa fa-key"></i> Memorable Secure Passphrase Generator',
        'intro': 'Stop using complex symbols you can\'t remember. A memorable passphrase (like "correct-horse-battery-staple") is mathematically stronger than a short complex password and infinitely easier for a human to type.',
        'overview_h4': 'The Math of Passphrases',
        'p1': 'A password like "Tr0ub4dor&3" is hard to remember but easy for a computer to guess. A passphrase like "purple-dinosaur-dancing-slowly" is extremely easy to remember but would take a supercomputer millions of years to crack.',
        'p2': 'Tip: Generate a 4-word or 5-word passphrase for your primary accounts (like your email or password manager master key). Never reuse passphrases across different sites.'
    },
    'currency-en.html': {
        'title': 'Digital Nomad Live Travel Currency Converter | TimerHaven',
        'desc': 'Instantly convert exchange rates with our ad-free, digital nomad live travel currency converter. Designed for speed, remote workers, and globetrotters.',
        'keys': 'digital nomad live travel currency converter, ad free exchange rate calculator, remote work currency tool, minimalist travel converter',
        'h3_title': '<i class="fa fa-dollar-sign"></i> Digital Nomad Live Travel Currency Converter',
        'intro': 'Fast, accurate, and completely ad-free. Quickly convert between global currencies using live market rates, designed specifically for the needs of remote workers and international travelers.',
        'overview_h4': 'Travel & Remote Income',
        'p1': 'When you live or work across borders, fluctuating exchange rates directly impact your bottom line. We built this tool to be incredibly lightweight so it loads instantly even on poor hotel Wi-Fi connections.',
        'p2': 'Tip: If you are invoicing international clients, always check the spot rate here before finalizing your quotes. Consider using a multi-currency account to minimize conversion fees.'
    },
    'calendar-en.html': {
        'title': 'Minimalist Visual Calendar Dashboard Online | TimerHaven',
        'desc': 'Plan your month without the clutter. Our minimalist visual calendar dashboard offers a distraction-free way to check dates and organize your upcoming schedule.',
        'keys': 'minimalist visual calendar dashboard online, ad free monthly calendar, simple browser calendar, aesthetic desk calendar web app',
        'h3_title': '<i class="fa fa-calendar-days"></i> Minimalist Visual Calendar Dashboard',
        'intro': 'Sometimes you just need to see the days of the month without being overwhelmed by meeting invites and notifications. Enjoy a clean, minimalist visual calendar right in your browser.',
        'overview_h4': 'The Value of Blank Space',
        'p1': 'Modern calendar apps are powerful, but they often induce anxiety by showing you every single obligation. A minimalist visual calendar provides a high-level view of the month, helping you grasp the passage of time without the stress.',
        'p2': 'Tip: Keep this calendar open on a secondary monitor to serve as a digital desk calendar. It\'s perfect for referencing dates quickly while on a phone call or writing an email.'
    },
    'stopwatch-en.html': {
        'title': 'Full Screen Split Time Lap Stopwatch | TimerHaven',
        'desc': 'Measure performance with our full-screen split time lap stopwatch. Ad-free, millisecond precision tracking ideal for coaches, presenters, and focus sessions.',
        'keys': 'full screen split time lap stopwatch, millisecond precision online stopwatch, coach presentation stopwatch, ad free lap timer',
        'h3_title': '<i class="fa fa-clock"></i> Full Screen Split Time Lap Stopwatch',
        'intro': 'Precision tracking without the ads. Use our millisecond-accurate stopwatch to record split times and laps. Features a full-screen mode perfect for coaches tracking athletes or speakers practicing presentations.',
        'overview_h4': 'Tracking Performance Metrics',
        'p1': 'Whether you are timing a sprint or rehearsing a TED talk, recording lap splits is crucial for analyzing performance. This stopwatch is built to handle multiple splits cleanly and export them easily.',
        'p2': 'Tip: When practicing a presentation, hit the "Lap" button at the end of each major section. Review the split times later to identify which parts of your speech are dragging and need trimming.'
    },
    'unit-converter-en.html': {
        'title': 'Quick Metric to Imperial Unit Converter | TimerHaven',
        'desc': 'Instantly convert length, weight, and temperature with our quick metric to imperial unit converter. Minimalist, ad-free, and designed for speed.',
        'keys': 'quick metric to imperial unit converter, ad free engineering conversion tool, simple browser metric converter, offline capable unit calculator',
        'h3_title': '<i class="fa fa-ruler-combined"></i> Quick Metric to Imperial Unit Converter',
        'intro': 'Eliminate the friction of switching systems. Our lightning-fast converter handles metric to imperial conversions instantly. Minimalist interface, zero ads, and offline capable.',
        'overview_h4': 'Frictionless Calculations',
        'p1': 'From following a foreign recipe to deciphering engineering specs, converting units should be instantaneous. We stripped away the bloat so you can get your conversion and get back to work.',
        'p2': 'Tip: The converter works completely offline. Bookmark this page, and you can use it on your laptop or phone even when you don\'t have cell service or Wi-Fi.'
    },
    'weather-en.html': {
        'title': 'Minimalist Ad-Free Global Weather Dashboard | TimerHaven',
        'desc': 'Check the forecast without the bloat. Our minimalist ad-free global weather dashboard provides accurate, instant weather data for any city in the world.',
        'keys': 'minimalist ad free global weather dashboard, simple current weather online, no ad weather forecast, aesthetic weather widget web app',
        'h3_title': '<i class="fa fa-cloud-sun"></i> Minimalist Ad-Free Global Weather Dashboard',
        'intro': 'Tired of weather sites packed with video ads and clickbait? Our minimalist dashboard gives you exactly what you need: accurate, instant global weather data with zero distractions.',
        'overview_h4': 'The Problem with Weather Sites',
        'p1': 'Most commercial weather sites have become unreadable, burying the actual forecast under auto-playing videos and intrusive ads. We built a weather dashboard that respects your time and your screen real estate.',
        'p2': 'Tip: Search for any city globally to check the conditions before a remote meeting. Knowing it\'s raining heavily at your client\'s location makes for excellent small talk before the agenda begins.'
    }
}

for filename, data in updates.items():
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filename}")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Title
    content = re.sub(r'<title>.*?</title>', f'<title>{data["title"]}</title>', content, flags=re.DOTALL)
    content = re.sub(r'<meta property="og:title" content="[^"]+">', f'<meta property="og:title" content="{data["title"]}">', content)
    content = re.sub(r'<meta name="twitter:title" content="[^"]+">', f'<meta name="twitter:title" content="{data["title"]}">', content)

    # 2. Update Description
    content = re.sub(r'<meta name="description"\s*content="[^"]+">', f'<meta name="description"\n    content="{data["desc"]}">', content)
    content = re.sub(r'<meta property="og:description" content="[^"]+">', f'<meta property="og:description" content="{data["desc"]}">', content)
    content = re.sub(r'<meta name="twitter:description" content="[^"]+">', f'<meta name="twitter:description" content="{data["desc"]}">', content)

    # 3. Update Keywords
    content = re.sub(r'<meta name="keywords" content="[^"]+">', f'<meta name="keywords" content="{data["keys"]}">', content)

    # 4. Update H3 Tool Title
    content = re.sub(r'<h3 id="tool-title" class="tool-title">.*?</h3>', f'<h3 id="tool-title" class="tool-title">{data["h3_title"]}</h3>', content, flags=re.DOTALL)

    # 5. Update Intro Paragraph
    content = re.sub(r'(<div class="tool-intro-in-card"[^>]*>\s*<p>).*?(</p>)', rf'\1{data["intro"]}\2', content, count=1, flags=re.DOTALL)

    # 6. Update Guide Excerpt H4
    content = re.sub(r'(<div class="guide-excerpt"[^>]*>\s*<h4>).*?(</h4>)', rf'\1{data["overview_h4"]}\2', content, count=1, flags=re.DOTALL)

    # 7. Update Excerpt Paragraphs
    def replace_excerpt(match):
        part1 = match.group(1)
        part2 = match.group(2)
        part3 = match.group(3)
        return f"{part1}{data['p1']}{part2}{data['p2']}{part3}"

    content = re.sub(
        r'(<div class="guide-excerpt"[^>]*>.*?<h4>.*?</h4>\s*<p>).*?(</p>\s*<p>).*?(</p>)', 
        replace_excerpt, 
        content, 
        count=1, 
        flags=re.DOTALL
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {filename}")

print("Batch 2 updates complete!")
