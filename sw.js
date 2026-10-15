// Offline support: app shell from cache, prices always fresh when online.
var CACHE = "pcil-v1";
var SHELL = ["./", "index.html", "manifest.webmanifest", "icons/icon.svg", "icons/icon-192.png"];
self.addEventListener("install", function(e){ e.waitUntil(caches.open(CACHE).then(function(c){ return c.addAll(SHELL); })); self.skipWaiting(); });
self.addEventListener("activate", function(e){ e.waitUntil(caches.keys().then(function(ks){ return Promise.all(ks.filter(function(k){ return k!==CACHE; }).map(function(k){ return caches.delete(k); })); })); self.clients.claim(); });
self.addEventListener("fetch", function(e){
  var u = new URL(e.request.url);
  if(e.request.method!=="GET" || u.origin!==location.origin) return;
  // network first for everything, so new prices and new versions show right away
  e.respondWith(fetch(e.request).then(function(r){ var cp=r.clone(); caches.open(CACHE).then(function(c){ c.put(e.request, cp); }); return r; }).catch(function(){ return caches.match(e.request).then(function(m){ return m || caches.match("index.html"); }); }));
});
