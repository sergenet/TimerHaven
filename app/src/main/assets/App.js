import React from 'react';
import { StyleSheet, View, Platform, StatusBar } from 'react-native';
import { WebView } from 'react-native-webview';

export default function App() {
  const injectedJs = `
    (function() {
      // Hide navigation links for blog and guides
      var style = document.createElement('style');
      style.innerHTML = '.nav-link[href*="blog"], .nav-link[href*="guides"], .nav-link[href*="recommended"] { display: none !important; }';
      document.head.appendChild(style);
    })();
    true; // note: webview evaluateJavascript expects a return value
  `;

  return (
    <View style={styles.container}>
      <WebView
        source={{ uri: 'https://www.timerhaven.com' }}
        style={styles.webview}
        injectedJavaScript={injectedJs}
        startInLoadingState
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
  webview: {
    flex: 1,
  },
});