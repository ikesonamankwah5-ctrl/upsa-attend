const CACHE_NAME = 'upsa-attend-v3';

const APP_FILES = [
    '/static/pwa/manifest.json',
    '/static/pwa/icons/icon.svg',
    '/static/pwa/icons/icon-180.png',
    '/static/pwa/icons/icon-192.png',
    '/static/pwa/icons/icon-512.png'
];

// Install service worker and cache app resources
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(APP_FILES))
            .then(() => self.skipWaiting())
    );
});

// Activate and remove old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(
                keys
                    .filter(key => key !== CACHE_NAME)
                    .map(key => caches.delete(key))
            )
        ).then(() => self.clients.claim())
    );
});

// Cache only public PWA resources
self.addEventListener('fetch', event => {
    const request = event.request;
    const url = new URL(request.url);

    if (
        request.method === 'GET' &&
        url.origin === self.location.origin &&
        url.pathname.startsWith('/static/pwa/')
    ) {
        event.respondWith(
            caches.match(request).then(cached =>
                cached || fetch(request)
            )
        );
    }
});