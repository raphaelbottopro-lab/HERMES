/* HERMÈS · service worker
   - appli (index.html) : réseau d’abord, copie de secours en cache
   - données (data/*.json) : réseau d’abord, dernière version en cache pour lire hors connexion
   - icônes et manifeste : cache d’abord */
const VERSION = '1.0.1';
const SHELL = 'hermes-shell-' + VERSION;
const DATA = 'hermes-data';
const SHELL_FILES = ['./', './index.html', './manifest.webmanifest', './icons/logo.png', './icons/icon-192.png', './icons/icon-512.png', './icons/apple-touch-icon.png'];

const DATA_FILES = ['index', 'fils', 'personnes', 'glossaire', 'plf', 'sondages', 'chiffres'];

// Met les données du jour en cache dès l’installation, pour que la première lecture hors connexion fonctionne
async function prechargerDonnees() {
  const base = new URL('./data/', self.registration.scope);
  const cache = await caches.open(DATA);
  const garder = async (chemin) => {
    const url = new URL(chemin, base);
    try { const res = await fetch(url, { cache: 'no-store' }); if (res.ok) { await cache.put(url.origin + url.pathname, res.clone()); return res; } } catch (err) {}
    return null;
  };
  const [ix] = await Promise.all(DATA_FILES.map((f) => garder(f + '.json')));
  if (!ix) return;
  try {
    const index = await ix.json();
    const dates = (index.editions || []).map((x) => x.date).sort().reverse().slice(0, 7);
    await Promise.all(dates.map((d) => garder('editions/' + d + '.json')));
  } catch (err) {}
}

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(SHELL).then((c) => c.addAll(SHELL_FILES))
      .then(() => prechargerDonnees())
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((ks) => Promise.all(ks.filter((k) => k.startsWith('hermes-shell-') && k !== SHELL).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

function cleData(url) { return url.origin + url.pathname; }

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  if (url.pathname.includes('/data/')) {
    e.respondWith(
      fetch(req).then((res) => {
        if (res.ok) { const copie = res.clone(); caches.open(DATA).then((c) => c.put(cleData(url), copie)); }
        return res;
      }).catch(() => caches.open(DATA).then((c) => c.match(cleData(url))).then((r) => r || new Response('{"erreur":"hors connexion"}', { status: 503, headers: { 'Content-Type': 'application/json' } })))
    );
    return;
  }

  if (req.mode === 'navigate') {
    const page = new URL('./index.html', self.registration.scope).href;
    e.respondWith(
      fetch(req).then((res) => {
        if (res.ok) { const copie = res.clone(); caches.open(SHELL).then((c) => c.put(page, copie)); }
        return res;
      }).catch(() => caches.match(page))
    );
    return;
  }

  e.respondWith(caches.match(req, { ignoreSearch: true }).then((r) => r || fetch(req)));
});
