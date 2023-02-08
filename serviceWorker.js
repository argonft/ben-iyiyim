const staticDev = 'beniyiyim-v1';
const assets = ['/', '/index.html', '/images/icons/favicon.jpg'];

self.addEventListener('install', (installEvent) => {
  installEvent.waitUntil(
    caches.open(staticDev).then((cache) => {
      cache.addAll(assets);
    })
  );
});

self.addEventListener('fetch', (fetchEvent) => {
  fetchEvent.respondWith(
    caches.match(fetchEvent.request).then((res) => {
      return res || fetch(fetchEvent.request);
    })
  );
});
