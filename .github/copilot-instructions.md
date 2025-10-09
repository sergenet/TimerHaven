# TimerHaven - Copilot Instructions

## Project Overview

TimerHaven is a free online suite of time management tools with two components:
1. **Web App**: A static HTML website (`index.html`) with embedded JavaScript
2. **Mobile App**: A React Native/Expo wrapper app that displays the website in a WebView

## Technology Stack

### Web App (Primary)
- Pure HTML, CSS, and vanilla JavaScript
- Bootstrap 5.3.3 for UI components
- Luxon 3.4.3 for date/time handling
- Font Awesome 6.4.2 for icons
- External APIs: WeatherAPI, currency exchange rates

### Mobile App (Wrapper)
- React Native with Expo (~53.0.22)
- React 19.0.0
- react-native-webview for displaying the website

## Code Style & Guidelines

### HTML/CSS/JavaScript
- Use vanilla JavaScript - no frameworks or build tools for the web app
- Keep all JavaScript inline in `index.html` for simplicity
- Use Bootstrap classes for styling consistency
- Maintain the existing color scheme: primary blue (#1558b0), accent cyan (#26c6da), and orange (#ff9800)
- Follow the existing naming conventions for CSS classes and JavaScript functions

### React Native/Expo
- Keep the mobile app minimal - it's just a WebView wrapper
- Use functional components with hooks
- Follow React best practices for state management

## Project Structure

- `index.html` - Main web application (all HTML, CSS, and JavaScript)
- `App.js` - React Native app component
- `index.js` - React Native entry point
- `package.json` - Mobile app dependencies
- `README.md` - Project documentation
- `LICENSE` - MIT License

## Features

The web app includes these tools:
- 🌎 World Clock - Display time across major cities
- ⏳ Countdown Timer - Custom countdowns with buzzer
- ⏰ Alarm - Date/time alarms with repeat and sound
- 🕒 Stopwatch - Elapsed time tracking with laps
- 🍅 Pomodoro Timer - Focus/break cycles (25/5 min)
- ☀️ Weather - Current weather by city
- 💱 Currency Converter - Live exchange rates

## Development Guidelines

### Making Changes to the Web App
1. All changes to `index.html` should maintain backward compatibility
2. Test thoroughly in multiple browsers (Chrome, Firefox, Safari, Edge)
3. Ensure mobile responsiveness (the site is mobile-first)
4. Do not add build tools or frameworks - keep it simple and static
5. External API keys are embedded (WeatherAPI key is in the code)

### Making Changes to the Mobile App
1. The mobile app is just a WebView pointing to https://www.timerhaven.com
2. Only modify if fixing WebView-specific issues
3. Test on both iOS and Android when possible
4. Use Expo Go for testing during development

### Testing
- Web app: Open `index.html` directly in a browser
- Mobile app: Use `npm start` to launch Expo
- No automated tests currently exist - manual testing is required

### Dependencies
- Web app: No dependencies (uses CDN links)
- Mobile app: Run `npm install` after modifying `package.json`

## Important Notes

### APIs and Services
- **WeatherAPI**: Key is embedded in code (WEATHER_API_KEY = '63cbee1756fd4002802201248250109')
- **Currency API**: Uses exchangerate-api.com with free tier limits
- **Google Analytics**: Tracking ID G-R1F6Y45MW2
- **AdSense**: Publisher ID ca-pub-0467059729557007
- **Amazon Affiliate**: Tag sergenet20-20

### Privacy & Compliance
- Cookie consent banner implemented (Osano)
- Google Analytics configured
- Affiliate links properly disclosed
- Privacy policy referenced in cookie banner

### Deployment
- Web app: Static hosting (GitHub Pages, Netlify, Vercel)
- Mobile app: Expo build for iOS/Android stores

## Common Tasks

### Adding a New Tool Feature
1. Add HTML structure in the tools section of `index.html`
2. Add corresponding JavaScript functions (use `window.functionName`)
3. Update navigation and hero section if needed
4. Follow Bootstrap grid layout patterns
5. Test on mobile devices

### Updating Styling
1. Modify the `<style>` section in `index.html`
2. Maintain consistency with existing color palette
3. Ensure responsive design with media queries
4. Use Bootstrap utility classes when possible

### Fixing Bugs
1. Check browser console for JavaScript errors
2. Test across different browsers and devices
3. Verify API calls and responses
4. Check for timing issues with async operations

## Do Not
- Add build tools, bundlers, or frameworks to the web app
- Break the single-file structure of `index.html`
- Remove or modify affiliate/ad code without approval
- Change the simple static nature of the web app
- Add authentication or backend dependencies

## Support
- Repository: https://github.com/sergenet/TimerHaven
- License: MIT
- Maintainer: sergenet
