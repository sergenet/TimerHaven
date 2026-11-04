const CACHE_NAME = 'timerhaven-cache-v1';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
  // A simple fetch handler is enough to satisfy the PWA requirements.
  // We'll just perform a network-first strategy, falling back to cache, or just pass it through.
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});
