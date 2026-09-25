/* prototype-space — small enhancements to the guide. Everything works
   without this file; it only makes the visitor's own track easier to find.

   - A track page remembers itself, so each step's per-track table can put
     that track first and mark it, and the front page can mark its card.
   - The Bonn page used to hold the city playbook; old links to its sections
     are forwarded to the directory page that holds them now.            */

(function () {
  "use strict";

  var KEY = "prototype-space:track";

  function recall() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }

  function remember(slug) {
    try { localStorage.setItem(KEY, slug); } catch (e) { /* private mode */ }
  }

  function markTrack() {
    var page = document.querySelector("[data-track-page]");
    if (page) remember(page.getAttribute("data-track-page"));

    var mine = recall();
    if (!mine) return;
    var found = document.querySelectorAll(
      '.track-table [data-track="' + mine + '"], .track-grid [data-track="' + mine + '"]');
    Array.prototype.forEach.call(found, function (el) {
      el.classList.add("is-mine");
      var list = el.parentNode;
      if (list.classList.contains("track-table") && list.firstChild !== el) {
        list.insertBefore(el, list.firstChild);
      }
    });
  }

  function forwardMovedAnchor() {
    var holder = document.querySelector("[data-moved]");
    if (!holder || !location.hash) return;
    var id = decodeURIComponent(location.hash.slice(1));
    if (document.getElementById(id)) return;
    try {
      var moved = JSON.parse(holder.getAttribute("data-moved"));
      if (moved[id]) location.replace(moved[id] + location.hash);
    } catch (e) { /* malformed map: stay on the page */ }
  }

  function init() {
    markTrack();
    forwardMovedAnchor();
  }

  // Material's instant navigation swaps the page body, so run on every page.
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(init);
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
