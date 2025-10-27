/**
 * Service Worker for Vani - Award-Level PWA
 * Hybrid approach: Try Workbox CDN, fallback to manual caching strategy
 */

const CACHE_VERSION = 'vani-v1';
const SHELL_CACHE = `${CACHE_VERSION}-shell`;
const RUNTIME_CACHE = `${CACHE_VERSION}-runtime`;
const MAP_CACHE = `${CACHE_VERSION}-maps`;
const API_CACHE = `${CACHE_VERSION}-api`;

// Precache assets
const SHELL_ASSETS = [
  '/',
  '/index.html',
  '/dashboard.html',
  '/login.html',
  '/mobile.css',
  '/mobile-nav.js',
  '/manifest.json',
];

/**
 * Install: Precache shell assets
 */
self.addEventListener('install', (event) => {
  console.log('[SW] Installing...');
  event.waitUntil(
    caches.open(SHELL_CACHE).then((cache) => {
      console.log('[SW] Precaching shell');
      return cache.addAll(SHELL_ASSETS).catch((err) => {
        console.warn('[SW] Some shell assets failed (offline?)', err);
      });
    }).then(() => self.skipWaiting())
  );
});

/**
 * Activate: Clean old caches
 */
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating...');
  event.waitUntil(
    caches.keys().then((names) => {
      return Promise.all(
        names
          .filter((n) => n.startsWith('vani-') && !n.includes(CACHE_VERSION))
          .map((n) => {
            console.log('[SW] Removing old cache:', n);
            return caches.delete(n);
          })
      );
    }).then(() => self.clients.claim())
  );
});

/**
 * Fetch: Smart caching strategy
 */
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  if (request.method !== 'GET') return;

  // Skip cross-origin (except CDN)
  const isCrossOrigin = url.origin !== location.origin;
  const isCDN = /unpkg|cdn\.jsdelivr|fonts\.googleapis|cartodb|tile/.test(url.host);
  if (isCrossOrigin && !isCDN) return;

  // Map tiles: Network first
  if (/tile|carto|openstreetmap|basemaps|arcgisonline/.test(url.pathname + url.host)) {
    event.respondWith(networkFirst(request, MAP_CACHE));
    return;
  }

  // API: Network first
  if (/api|\.netlify\/functions/.test(url.pathname)) {
    event.respondWith(networkFirst(request, API_CACHE));
    return;
  }

  // Fonts, images: Cache first
  if (/\.(woff|woff2|ttf|jpg|png|gif|svg)$/.test(url.pathname)) {
    event.respondWith(cacheFirst(request, RUNTIME_CACHE));
    return;
  }

  // HTML, JS, CSS: Network first
  if (['document', 'script', 'style'].includes(request.destination)) {
    event.respondWith(networkFirst(request, SHELL_CACHE));
    return;
  }

  // Default: Stale while revalidate
  event.respondWith(staleWhileRevalidate(request, RUNTIME_CACHE));
});

/**
 * Network first strategy
 */
function networkFirst(request, cacheName) {
  return fetch(request)
    .then((res) => {
      if (!res || res.status !== 200) return res;
      const clone = res.clone();
      caches.open(cacheName).then((c) => c.put(request, clone));
      return res;
    })
    .catch(() => caches.match(request).then((res) => res || offlineResponse()));
}

/**
 * Cache first strategy
 */
function cacheFirst(request, cacheName) {
  return caches.match(request).then((res) => {
    if (res) return res;
    return fetch(request).then((res) => {
      if (!res || res.status !== 200) return res;
      const clone = res.clone();
      caches.open(cacheName).then((c) => c.put(request, clone));
      return res;
    }).catch(() => offlineResponse());
  });
}

/**
 * Stale while revalidate
 */
function staleWhileRevalidate(request, cacheName) {
  return caches.match(request).then((cached) => {
    const fetched = fetch(request).then((res) => {
      if (!res || res.status !== 200) return res;
      const clone = res.clone();
      caches.open(cacheName).then((c) => c.put(request, clone));
      return res;
    }).catch(() => cached || offlineResponse());
    return cached || fetched;
  });
}

/**
 * Offline fallback
 */
function offlineResponse() {
  return new Response(
    `<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Offline</title><style>body{font-family:system-ui;background:#f5f7fa;color:#1e293b;padding:40px 20px;text-align:center}h1{font-size:32px;margin-bottom:16px}p{color:#64748b;margin-bottom:24px}button{background:#10b981;color:white;border:none;padding:12px 24px;border-radius:8px;cursor:pointer}button:hover{background:#0f5538}</style></head><body><h1>📡 Offline</h1><p>You're offline. Try refreshing when connected.</p><button onclick="location.reload()">Retry</button></body></html>`,
    { status: 503, headers: { 'Content-Type': 'text/html; charset=utf-8' } }
  );
}

console.log('[SW] Ready for offline support');
