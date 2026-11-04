import os
import re

directory = r'C:\TimerHavenWebsite'

updates = {
    'pomodoro-en.html': {
        'title': 'Aesthetic Pomodoro Timer for ADHD Focus Online | TimerHaven',
        'desc': 'Boost deep work with our aesthetic online Pomodoro timer designed for ADHD focus. Customizable 50/10 sessions, distraction-free visual timer. No login, 100% free.',
        'keys': 'aesthetic pomodoro timer, pomodoro timer for adhd, visual adhd timer, 50/10 pomodoro, adhd focus timer, distraction free pomodoro',
        'h3_title': '<span class="pomodoro-emoji" aria-hidden="true">🍅</span><i class="fa fa-stopwatch pomodoro-fa" aria-hidden="true"></i> Aesthetic Pomodoro Timer for ADHD Focus',
        'intro': 'Boost focus and manage time blindness with the Pomodoro technique. For ADHD brains, try starting with a custom 15-minute burst, or a 50/10 deep work cycle. Adjust work/break lengths and use the visual timer to maintain flow without distractions.',
        'overview_h4': 'Quick ADHD Focus Guide',
        'p1': 'Traditional 25-minute Pomodoros don\'t work for everyone. If you have ADHD or struggle with time blindness, our aesthetic timer provides a distraction-free visual cue to help you build momentum. Use the timer to reduce overwhelm and track exactly how long tasks take.',
        'p2': 'Tip: If a task feels too daunting, set the timer for just 10 minutes to break the barrier of starting. For deep hyperfocus sessions, switch to a 50/10 pattern. The full guide includes ADHD-friendly recipes and time-blocking variants.'
    },
    'meeting-planner-en.html': {
        'title': 'Remote Team Timezone Overlap Calculator & Planner | TimerHaven',
        'desc': 'Coordinate global meetings effortlessly with our remote team timezone overlap calculator. Find the perfect meeting time across multiple time zones instantly.',
        'keys': 'remote team timezone overlap calculator, global meeting scheduler, timezone overlap tool, digital nomad meeting planner, timezone converter',
        'h3_title': '<i class="fa fa-users"></i> Remote Team Timezone Overlap Calculator',
        'intro': 'Schedule global meetings without the timezone math. Visually compare time zones for your distributed team and find the perfect overlap window for everyone.',
        'overview_h4': 'Remote Scheduling Best Practices',
        'p1': 'Finding a meeting time for a globally distributed team can be a nightmare. Our timezone overlap calculator lets you add multiple locations and instantly see the intersecting business hours.',
        'p2': 'Tip: Try to rotate meeting times if your team spans across extreme time zones (like Tokyo and California) so the burden of early mornings or late nights is shared. Check our full guide for asynchronous communication strategies.'
    },
    'focus-music-en.html': {
        'title': 'Lofi Focus Music Timer for Deep Work & Studying | TimerHaven',
        'desc': 'Enhance your studying and deep work sessions with our Lofi focus music timer. Built-in productivity timer paired with curated ambient and lofi beats.',
        'keys': 'lofi focus music timer, deep work music, studying ambient music timer, lofi pomodoro, adhd focus music',
        'h3_title': '<i class="fa fa-music"></i> Lofi Focus Music Timer for Deep Work',
        'intro': 'Drown out distractions and enter a flow state. Pair our curated lofi and ambient focus music with a built-in timer to structure your deep work sessions.',
        'overview_h4': 'Music & Flow State',
        'p1': 'Music without lyrics, like lofi hip hop or ambient electronic, provides continuous acoustic stimulation that can help ADHD brains stay engaged and prevent the mind from wandering during complex tasks.',
        'p2': 'Tip: Use the built-in timer alongside the audio player to enforce structured work intervals. Read our deep work guide to learn how acoustic environments shape productivity.'
    },
    'habit-tracker-en.html': {
        'title': 'Visual "Don\'t Break The Chain" Habit Tracker Online | TimerHaven',
        'desc': 'Build lasting routines with our visual \'Don\'t Break The Chain\' habit tracker. A minimalist, privacy-first tool to track daily goals. No login required.',
        'keys': 'dont break the chain habit tracker, visual habit tracker online, seinfeld strategy tracker, minimalist habit tracker, atomic habits tool',
        'h3_title': '<i class="fa fa-check-double"></i> Visual "Don\'t Break The Chain" Habit Tracker',
        'intro': 'Apply the famous \'Don\'t Break The Chain\' strategy to your daily goals. Visually track your momentum and build lasting atomic habits without complex software.',
        'overview_h4': 'The Seinfeld Strategy',
        'p1': 'The most effective way to build a new habit is visual consistency. By marking a calendar every day you complete a task, you build a chain. Your only goal is to not break the chain.',
        'p2': 'Tip: Start with an incredibly small habit (e.g., read 1 page, do 1 pushup) to ensure you never break the chain on bad days. Read our Atomic Habits guide for more implementation strategies.'
    },
    'world-clock-en.html': {
        'title': 'Digital Nomad Dual Timezone Clock & Dashboard | TimerHaven',
        'desc': 'Track global time zones instantly with our digital nomad dual timezone clock. Build your own multi-city dashboard for remote work and travel.',
        'keys': 'digital nomad dual timezone clock, multi timezone dashboard, remote work clock, travel timezone tracker, global clock web app',
        'h3_title': '<i class="fa fa-globe"></i> Digital Nomad Dual Timezone Clock',
        'intro': 'Essential for digital nomads and remote workers. Build a custom dual or multi-timezone dashboard to keep track of clients, headquarters, and your local time.',
        'overview_h4': 'Managing Asynchronous Work',
        'p1': 'Working across borders requires constant awareness of your team\'s local time. Use this dashboard to instantly verify business hours before sending a Slack message or scheduling a sync.',
        'p2': 'Tip: Keep this tab pinned in your browser to avoid constantly Googling \'time in London\'. See our remote work guides for mastering asynchronous communication.'
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

    # 5. Update Intro Paragraph (the first p tag inside #tool-help)
    # The structure is: <div class="tool-intro-in-card" id="tool-help" ...> \n <p>OLD INTRO</p>
    content = re.sub(r'(<div class="tool-intro-in-card"[^>]*>\s*<p>).*?(</p>)', rf'\1{data["intro"]}\2', content, count=1, flags=re.DOTALL)

    # 6. Update Guide Excerpt H4
    content = re.sub(r'(<div class="guide-excerpt"[^>]*>\s*<h4>).*?(</h4>)', rf'\1{data["overview_h4"]}\2', content, count=1, flags=re.DOTALL)

    # 7. Update Excerpt Paragraphs
    # The structure is two <p> tags after the <h4>. We will match the first two <p> tags inside .guide-excerpt
    def replace_excerpt(match):
        # match.group(1) is everything before the first paragraph text
        # match.group(2) is the closing tag and everything up to the next <p>
        # match.group(3) is the closing tag
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

print("Batch 1 updates complete!")
