import React, { useEffect, useRef, useState } from 'react';
import { StyleSheet, View, Platform, StatusBar } from 'react-native';
import { WebView } from 'react-native-webview';
import { check, request, PERMISSIONS, RESULTS } from 'react-native-permissions';
import Geolocation from '@react-native-community/geolocation';

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
        const js = `if(window.receiveNativeLocation){window.receiveNativeLocation({latitude:${lat},longitude:${lon}});} if(window._injectedFetchByCoords){window._injectedFetchByCoords(${lat}, ${lon});} true;`;
        injectJS(js);
      },
      (err) => {
        console.warn('Geolocation error', err);
        injectJS(`if(window.__nativeLocationFailed){window.__nativeLocationFailed(${JSON.stringify(err)});} true;`);
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
  }

  function injectJS(code) {
    if (webViewRef.current) {
      webViewRef.current.injectJavaScript(code);
    }
  }

  function onMessage(event) {
    let data = null;
    try { data = JSON.parse(event.nativeEvent.data); } catch (e) { /* not JSON */ }
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
        injectedJavaScriptBeforeContentLoaded={`(function(){window.requestNativeLocation = function(){window.ReactNativeWebView.postMessage(JSON.stringify({type:'requestNativeLocation'}));};})(); true;`}
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