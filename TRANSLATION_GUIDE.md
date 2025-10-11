# TimerHaven Translation Implementation Guide

## Overview
This guide documents the translation system implementation for TimerHaven, supporting 7 languages: English (en), French (fr), Spanish (es), German (de), Russian (ru), Greek (el), and Arabic (ar).

## Current Status

### ✅ Completed
1. **Pomodoro Timer** - Fully implemented with all 7 languages
   - Translation dictionaries for all UI elements
   - Dynamic language switching
   - LocalStorage persistence
   - All buttons, labels, status messages, FAQs, tips, and how-to sections

2. **All 15 Tools** - Basic framework in place
   - Language selector dropdown UI
   - CSS styling for language selector
   - Google notranslate meta tag
   - Ready for full translation implementation

### 🔄 In Progress
- Full translation dictionaries for remaining 14 tools
- Translation logic and updateLanguage() functions
- ID assignments to all translatable elements

## Implementation Pattern

### 1. HTML Structure

#### Language Selector (Already Added to All Tools)
```html
<div class="language-select">
  <label for="lang-select"><strong id="language-label">Language:</strong></label>
  <select id="lang-select">
    <option value="en">English</option>
    <option value="fr">Français</option>
    <option value="es">Español</option>
    <option value="de">Deutsch</option>
    <option value="ru">Русский</option>
    <option value="el">Ελληνικά</option>
    <option value="ar">العربية</option>
  </select>
</div>
```

#### Meta Tags (Already Added)
```html
<meta name="google" content="notranslate">
```

#### CSS (Already Added)
```css
.language-select { 
  text-align: right; 
  padding: 10px 18px 0 0; 
  margin-bottom: 0.5em; 
}
```

### 2. Adding IDs to HTML Elements

Every translatable element needs an ID. Example from Pomodoro:

```html
<!-- Titles -->
<h2 id="howto-title">...</h2>
<h3 id="tool-title">...</h3>
<h4 id="tips-mobile-title">...</h4>

<!-- Lists -->
<ol id="howto-steps">...</ol>
<ul id="tips-list">...</ul>
<ul id="faq-list">...</ul>

<!-- Buttons and Labels -->
<label id="work-label">...</label>
<span id="start-text">Start</span>
<span id="pause-text">Pause</span>

<!-- Links -->
<a id="back-link">...</a>
<a id="howto-article-btn">...</a>
```

### 3. Translation Dictionary Structure

```javascript
const translations = {
  en: {
    "language-label": "Language:",
    "back-link": "Back to Main Menu",
    "tool-title": "Tool Name",
    "start-text": "Start",
    // ... all other translatable strings
  },
  fr: {
    "language-label": "Langue :",
    "back-link": "Retour au menu principal",
    "tool-title": "Nom de l'outil",
    "start-text": "Démarrer",
    // ... French translations
  },
  // ... other languages (es, de, ru, el, ar)
};
```

### 4. Update Language Function

```javascript
function updateLanguage() {
  const lang = document.getElementById("lang-select").value;
  const t = translations[lang];
  
  // Update all elements with IDs
  document.getElementById("language-label").textContent = t["language-label"];
  document.getElementById("back-link").innerHTML = '<i class="fa fa-arrow-left"></i> ' + t["back-link"];
  document.getElementById("tool-title").innerHTML = t["tool-title"];
  document.getElementById("start-text").textContent = t["start-text"];
  
  // Update lists (use innerHTML for HTML content)
  if (document.getElementById("howto-steps")) {
    document.getElementById("howto-steps").innerHTML = t["howto-steps"];
  }
  if (document.getElementById("faq-list")) {
    document.getElementById("faq-list").innerHTML = t["faq-list"];
  }
  
  // Update article links
  if (document.getElementById("howto-article-btn")) {
    document.getElementById("howto-article-btn").textContent = t["howto-article-btn"];
    document.getElementById("howto-article-btn").href = t["howto-article-link"];
  }
  
  // Preserve input field values when updating labels
  const inputValue = document.getElementById('someInput').value;
  document.getElementById('some-label').innerHTML = t["some-label"] + 
    ' <input type="number" id="someInput" value="' + inputValue + '" ... />';
  // Re-attach event listeners after updating innerHTML
  document.getElementById('someInput').addEventListener('change', someFunction);
}
```

### 5. Event Listeners and Persistence

```javascript
// Save language preference on change
document.getElementById("lang-select").addEventListener("change", function() {
  localStorage.setItem('timerhavenLang', this.value);
  updateLanguage();
});

// Load saved language on page load
document.addEventListener("DOMContentLoaded", function() {
  const savedLang = localStorage.getItem('timerhavenLang') || 'en';
  document.getElementById('lang-select').value = savedLang;
  updateLanguage();
});
```

## Tool-Specific Considerations

### Dynamic Content
Some tools display dynamic content (e.g., timer status, countdown messages). These need to reference the translation dictionary:

```javascript
function updateDisplay() {
  const lang = document.getElementById("lang-select")?.value || 'en';
  const t = translations[lang] || translations['en'];
  
  document.getElementById('status').textContent = 
    isActive ? t["status-active"] : t["status-inactive"];
}
```

### Input Fields
When updating labels that contain input fields, preserve the input values:

```javascript
const currentValue = document.getElementById('inputField').value;
document.getElementById('label').innerHTML = 
  t["label-text"] + ' <input id="inputField" value="' + currentValue + '" ... />';
// Re-attach event listeners
document.getElementById('inputField').addEventListener('change', handler);
```

## Translation Guidelines

### Text Content
- Keep translations concise and user-friendly
- Maintain consistent terminology across the interface
- Consider cultural context for each language
- Use native speakers or professional translation services for accuracy

### HTML Content in Translations
- Use escaped quotes: `\\"` for HTML attributes within JavaScript strings
- Use template literals (backticks) for multi-line HTML
- Preserve HTML structure and classes

Example:
```javascript
"tips-list": `<li><b>Don't skip breaks:</b> Regular rests keep you energized.</li>
    <li><b>Track sessions:</b> See how many Pomodoros you complete daily.</li>`,
```

### Article Links
- Each tool should link to language-specific article pages
- Use the pattern: `tool-how-to.html` for English, `tool-how-to-fr.html` for French, etc.
- Ensure article pages exist for all languages

## Complete Example: Pomodoro Timer

See `/en/pomodoro.html` for a fully implemented example with:
- ✅ All 7 languages
- ✅ Complete translation dictionaries
- ✅ Dynamic UI updates
- ✅ Language persistence
- ✅ All UI elements translated (buttons, labels, FAQs, tips, how-to)

## Step-by-Step Implementation for New Tools

1. **Add IDs to HTML elements**
   - Use descriptive IDs like `tool-title`, `start-text`, `faq-list`
   - Add IDs to all headings, buttons, labels, lists, and links

2. **Create translation dictionaries**
   - Start with English (`en`)
   - Translate all strings for 6 other languages
   - Include both text content and HTML content with proper escaping

3. **Implement updateLanguage() function**
   - Update all elements by ID
   - Handle special cases (input fields, dynamic content)
   - Use `.textContent` for plain text, `.innerHTML` for HTML

4. **Add event listeners**
   - Language selector change event
   - DOMContentLoaded event for initial load
   - Re-attach listeners after innerHTML updates

5. **Test thoroughly**
   - Switch between all 7 languages
   - Verify all UI elements update correctly
   - Check that language preference persists
   - Test on mobile and desktop views

## Files Modified

### Fully Implemented
- `/en/pomodoro.html` - Complete 7-language implementation

### Framework Added
- `/en/timer.html`
- `/en/countdown.html`
- `/en/stopwatch.html`
- `/en/calendar.html`
- `/en/notes.html`
- `/en/password-generator.html`
- `/en/weather.html`
- `/en/world-clock.html`
- `/en/unit-converter.html`
- `/en/currency.html`
- `/en/clipboard-manager.html`
- `/en/habit-tracker.html`
- `/en/meeting-planner.html`
- `/en/focus-music.html`

## Next Steps

1. Complete full translation implementation for remaining 14 tools
2. Create/translate article pages for all tools in all languages
3. Update index.html with language selector
4. Test language switching across all pages
5. Verify all links point to correct language versions

## Resources

- **Reference Implementation**: `/en/pomodoro.html`
- **Translation Script**: `/tmp/add_language_selector.py` (for adding framework)
- **Issue**: #5 - Translate entire TimerHaven site

## Notes

- All tools now have the language selector framework in place
- The Pomodoro Timer demonstrates the complete implementation
- Following this pattern ensures consistency across all tools
- Translation dictionaries can be incrementally improved
- Consider using professional translation services for final production versions
