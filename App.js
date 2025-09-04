import React from 'react';
import { StyleSheet, View, Platform, StatusBar } from 'react-native';
import { WebView } from 'react-native-webview';

export default function App() {
  return (
    <View style={styles.container}>
      <WebView 
        source={{ uri: 'https://www.timerhaven.com' }}
        style={styles.webview}
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