/* Offline cache for the optional hosted edition. Not used for file://. */
const CACHE_VERSION = '2';
const PREFIX = 'ai-academy:' + encodeURIComponent(self.registration.scope) + ':';
const CACHE = PREFIX + CACHE_VERSION;
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(async cache => { await cache.addAll(['./', './index.html']); await self.skipWaiting(); }));
});
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k.startsWith(PREFIX) && k !== CACHE).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET' || url.origin !== self.location.origin || event.request.mode !== 'navigate') return;
  // Network first keeps the hosted edition fresh; cached HTML includes all content.
  event.respondWith((async () => {
    try {
      const response = await fetch(event.request);
      if (response.ok) {
        const cache = await caches.open(CACHE);
        await cache.put('./index.html', response.clone());
      }
      return response;
    } catch (error) {
      const cached = await caches.match(new URL('./index.html', self.registration.scope));
      if (cached) return cached;
      throw error;
    }
  })());
});
