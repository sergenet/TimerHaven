#!/usr/bin/env python3
from pathlib import Path

ROOT = Path.cwd()
languages = ['fr','es','de','ru','el','ar']
tools = ['task-timer','pomodoro','stopwatch','countdown','calendar','notes','habit-tracker','focus-music','clipboard-manager','meeting-planner','password-generator','unit-converter','currency','weather','world-clock']

for lang in languages:
    for tool in tools:
        folder = ROOT / lang / tool
        folder.mkdir(parents=True, exist_ok=True)
        file = folder / f"{tool}-index.html"
        if not file.exists():
            content = f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <title>{tool} — Guide ({lang})</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="/assets/css/tool-theme.css">
  <meta name="description" content="Scaffold placeholder for {tool} guide ({lang})">
</head>
<body>
  <main class="container">
    <article class="card" aria-labelledby="title">
      <header><h1 id="title">{tool} — Guide ({lang})</h1></header>
      <p class="lead">Scaffold placeholder. Full guide content to be added.</p>
    </article>
  </main>
</body>
</html>"""
            file.write_text(content, encoding='utf-8')
            print(f'Created placeholder: {file}')
        else:
            print(f'Exists: {file}')