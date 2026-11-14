/* TimerHaven service worker: installable app + offline fallback. */
// Bump this whenever a precached file changes. With the cache name unchanged,
// a changed file never reaches anyone who already has the worker: the fetch
// handler below prefers the cache, and the browser only reinstalls when this
// file's bytes change. That is what hid the Play Store link - install.js was
// updated on the server while every returning visitor kept the old copy.
const CACHE = "timerhaven-v4";
const OFFLINE_URL = "/offline.html";
const PRECACHE = [
  "/",
  OFFLINE_URL,
  "/assets/css/install.css",
  "/assets/js/install.js",
  "/assets/js/app-interface.js",
  "/assets/icons/app-192.png",
  "/assets/icons/app-512.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) =>
      Promise.all(
        PRECACHE.map((url) =>
          cache.add(new Request(url, { cache: "reload" })).catch(() => null)
        )
      )
    )
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("message", (event) => {
  if (event.data === "skip-waiting") self.skipWaiting();
});

function isCacheable(request) {
  if (request.method !== "GET") return false;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return false;
  return /\.(?:css|js|png|jpe?g|webp|svg|gif|woff2?|ico|json)$/i.test(url.pathname);
}

// The install sheet is the only thing on the site that can carry a store link,
// so a stale copy silently removes a path into the app. These two files are
// fetched from the network first and fall back to the cache only when offline;
// every other asset stays cache-first for speed. Without this, each change to
// the sheet needed a CACHE bump to be seen at all.
function isAlwaysFresh(request) {
  const path = new URL(request.url).pathname;
  return /\/assets\/(?:js\/install\.js|css\/install\.css)$/.test(path);
}

self.addEventListener("fetch", (event) => {
  const request = event.request;

  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE).then((cache) => cache.put(request, copy)).catch(() => {});
          return response;
        })
        .catch(() =>
          caches
            .match(request)
            .then((cached) => cached || caches.match(OFFLINE_URL))
            .then((cached) => cached || new Response("Offline", { status: 503 }))
        )
    );
    return;
  }

  if (!isCacheable(request)) return;

  if (isAlwaysFresh(request)) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response.ok) {
            const copy = response.clone();
            caches.open(CACHE).then((cache) => cache.put(request, copy)).catch(() => {});
          }
          return response;
        })
        .catch(() => caches.match(request).then((cached) => cached || Response.error()))
    );
    return;
  }

  event.respondWith(
    caches.match(request).then((cached) => {
      const network = fetch(request)
        .then((response) => {
          if (response.ok) {
            const copy = response.clone();
            caches.open(CACHE).then((cache) => cache.put(request, copy)).catch(() => {});
          }
          return response;
        })
        .catch(() => cached);
      return cached || network;
    })
  );
});
