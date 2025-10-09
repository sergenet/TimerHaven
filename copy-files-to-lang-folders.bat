@echo off
REM List all the files you want to copy (edit as needed)
set FILES=index.html calendar.html weather.html world-clock.html notes.html timer.html pomodoro.html stopwatch.html unit-converter.html meeting-planner.html password-generator.html habit-tracker.html focus-music.html countdown.html currency.html clipboard-manager.html

REM Loop over each language folder
for %%L in (fr es el de ru ar) do (
    REM Copy each file
    for %%F in (%FILES%) do (
        copy "en\%%F" "%%L\%%F"
    )
)
echo Files copied from /en/ to /fr/, /es/, /el/, /de/, /ru/, /ar/
pause