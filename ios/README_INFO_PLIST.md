# iOS Info.plist: Add location usage description

Edit your app's Info.plist (usually ios/<AppName>/Info.plist) and add the following entry inside the top-level `<dict>`:

```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>We need your location to show local weather and timezone information.</string>
```

After adding the Info.plist key, run:

```
cd ios
pod install
cd ..
```

Build and test on a real iOS device (simulator doesn't provide GPS).
