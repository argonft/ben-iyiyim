const staticDev = 'beniyiyim-v1';
const assets = [
  '/',
  '/deprem.html',
  '/images/icons/beniyiyim72.jpg',
  '/images/icons/beniyiyim96.jpg',
  '/images/icons/beniyiyim128.jpg',
  '/images/icons/beniyiyim144.jpg',
  '/images/icons/beniyiyim152.jpg',
  '/images/icons/beniyiyim192.jpg',
  '/images/icons/beniyiyim384.jpg',
  '/images/icons/beniyiyim512.jpg',
];

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
