import React, { useEffect, useRef } from 'react';
import { StyleSheet, View, Platform, StatusBar } from 'react-native';
import { WebView } from 'react-native-webview';
import { check, request, PERMISSIONS, RESULTS } from 'react-native-permissions';
import Geolocation from '@react-native-community/geolocation';

// Injected script that provides window.requestNativeLocation() function for web pages
const INJECTED_BRIDGE_SCRIPT = `
  (function(){
    window.requestNativeLocation = function(){
      window.ReactNativeWebView.postMessage(JSON.stringify({type:'requestNativeLocation'}));
    };
  })(); 
  true;
`;

// Geolocation configuration
const GEOLOCATION_OPTIONS = {
  enableHighAccuracy: true,
  timeout: 10000, // 10 seconds
  maximumAge: 0   // No caching
};

export default function App() {
  const webViewRef = useRef(null);

  useEffect(() => {
    if (Platform.OS === 'ios') {
      requestLocationAndInject();
    }
  }, []);

  async function requestLocationAndInject() {
    try {
      const perm = PERMISSIONS.IOS.LOCATION_WHEN_IN_USE;
      const status = await check(perm);
      if (status === RESULTS.GRANTED) {
        fetchAndInjectLocation();
        return;
      }
      const req = await request(perm);
      if (req === RESULTS.GRANTED) {
        fetchAndInjectLocation();
      } else {
        injectJS(`window.__nativeLocationPermission = "denied"; true;`);
      }
    } catch (e) {
      console.warn('Permission request error', e);
    }
  }

  function fetchAndInjectLocation() {
    Geolocation.getCurrentPosition(
      (pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;
        const js = `if(window.receiveNativeLocation){window.receiveNativeLocation({latitude:${JSON.stringify(lat)},longitude:${JSON.stringify(lon)}});} if(window._injectedFetchByCoords){window._injectedFetchByCoords(${JSON.stringify(lat)}, ${JSON.stringify(lon)});} true;`;
        injectJS(js);
      },
      (err) => {
        console.warn('Geolocation error', err);
        injectJS(`if(window.__nativeLocationFailed){window.__nativeLocationFailed(${JSON.stringify(err)});} true;`);
      },
      GEOLOCATION_OPTIONS
    );
  }

  function injectJS(code) {
    if (webViewRef.current) {
      webViewRef.current.injectJavaScript(code);
    }
  }

  function onMessage(event) {
    let data = null;
    try { 
      data = JSON.parse(event.nativeEvent.data); 
    } catch (e) { 
      // Ignore non-JSON messages - WebView may send other message types
      return;
    }
    if (data && data.type === 'requestNativeLocation') {
      requestLocationAndInject();
      return;
    }
  }

  return (
    <View style={styles.container}>
      <WebView
        ref={webViewRef}
        source={{ uri: 'https://www.timerhaven.com' }}
        style={styles.webview}
        startInLoadingState
        onMessage={onMessage}
        injectedJavaScriptBeforeContentLoaded={INJECTED_BRIDGE_SCRIPT}
      />
      {Platform.OS === 'android' && <StatusBar barStyle="dark-content" />}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: Platform.OS === 'android' ? StatusBar.currentHeight : 0,
  },
  webview: { flex: 1 },
});