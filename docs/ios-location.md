# iOS Native Location Integration

## Overview

The React Native app now requests iOS location permissions and fetches the device's current location, then forwards it into the WebView so that web pages can access native GPS coordinates.

## Why This Change?

WebView pages inside React Native apps cannot directly access geolocation APIs due to permission restrictions. The native app must request location permission from iOS and then inject the coordinates into the WebView via JavaScript.

## Setup Instructions

### 1. Install Dependencies

Run the following command to install the required npm packages:

```bash
npm install
```

This will install:
- `react-native-permissions@^3.8.0` - for iOS permission management
- `@react-native-community/geolocation@^2.0.2` - for native location access

### 2. Configure Info.plist

See `ios/README_INFO_PLIST.md` for detailed instructions on adding the required `NSLocationWhenInUseUsageDescription` key to your iOS app's Info.plist.

### 3. Install iOS Pods

After updating dependencies and Info.plist, install the required CocoaPods:

```bash
cd ios
pod install
cd ..
```

### 4. Build the App

Build the app for iOS (requires a Mac with Xcode):

```bash
npm run ios
```

Or use Expo:

```bash
expo run:ios
```

### 5. Test on a Real Device

**Important:** Location services require a real iOS device. The iOS simulator does not provide GPS coordinates.

- Deploy the app to a physical iOS device
- When the app launches, it will prompt for location permission
- Accept the permission to allow location access
- The app will fetch the current location and inject it into the WebView

## How It Works

### Native Side (App.js)

1. On app launch, `requestLocationAndInject()` is called for iOS devices
2. The app checks for `PERMISSIONS.IOS.LOCATION_WHEN_IN_USE`
3. If not granted, it requests the permission
4. Once granted, `fetchAndInjectLocation()` calls `Geolocation.getCurrentPosition()`
5. The coordinates are injected into the WebView using `injectJavaScript()`

### WebView Bridge

The app injects JavaScript into the page that:
- Calls `window.receiveNativeLocation({latitude, longitude})` if it exists
- Calls `window._injectedFetchByCoords(lat, lon)` if it exists
- Provides a `window.requestNativeLocation()` function that web pages can call to re-request location

### Web Page Side

Web pages can trigger a location request by calling:

```javascript
if (window.requestNativeLocation) {
  window.requestNativeLocation();
}
```

Or define handlers to receive the location:

```javascript
window.receiveNativeLocation = function(coords) {
  console.log('Received location:', coords.latitude, coords.longitude);
};

window._injectedFetchByCoords = function(lat, lon) {
  console.log('Alternative handler:', lat, lon);
};
```

## Testing

1. Open the app on a real iOS device
2. Accept the location permission when prompted
3. Open the browser console in the WebView (if debugging)
4. Verify that location coordinates are being received
5. Test the `window.requestNativeLocation()` function from the web page

## Troubleshooting

- **Permission denied**: Check that Info.plist includes `NSLocationWhenInUseUsageDescription`
- **No location data**: Ensure you're testing on a real device, not the simulator
- **Build errors**: Run `pod install` in the ios directory after installing dependencies
- **Runtime errors**: Check that `react-native-permissions` and `@react-native-community/geolocation` are properly linked
