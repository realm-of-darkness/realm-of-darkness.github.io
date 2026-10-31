/* Realm of Darkness — small shared helpers. */
(function () {
  "use strict";

  // Deterministic string hash (FNV-1a, 32 bit)
  function hash(str) {
    var h = 2166136261;
    for (var i = 0; i < str.length; i++) {
      h ^= str.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return h >>> 0;
  }

  // Seeded RNG (mulberry32). Returns a function producing floats in [0, 1).
  function rng(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function pick(list, rand) {
    return list[Math.floor((rand || Math.random)() * list.length)];
  }

  function params() {
    return new URLSearchParams(window.location.search);
  }

  // localStorage that never throws (private mode, blocked storage, ...)
  var store = {
    get: function (key, fallback) {
      try {
        var v = window.localStorage.getItem(key);
        return v === null ? fallback : JSON.parse(v);
      } catch (e) { return fallback; }
    },
    set: function (key, value) {
      try { window.localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* the void accepts no deposits */ }
    }
  };

  // Crypt: remember which deaths were discovered and show the counter.
  function cryptCounter() {
    var el = document.querySelector("[data-death-counter]");
    if (!el) return;
    var total = parseInt(el.getAttribute("data-total"), 10);
    var found = store.get("rod-deaths", []);
    var death = document.body.getAttribute("data-death");
    if (death && found.indexOf(death) === -1) {
      found.push(death);
      store.set("rod-deaths", found);
    }
    if (!found.length) return;
    el.textContent = "Deaths discovered: " + found.length + " / " + total +
      (found.length >= total ? " — a true connoisseur of demise." : "");
    el.hidden = false;
  }

  window.ROD = { hash: hash, rng: rng, pick: pick, params: params, store: store };
  document.addEventListener("DOMContentLoaded", cryptCounter);
})();
