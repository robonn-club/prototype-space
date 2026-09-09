/* prototype-space — the filter view.
   Reads the resources.json that build.py derives from the markdown, so the
   markdown stays the thing anyone edits. Filters combine as OR inside a facet
   and AND across facets, which is what people expect from "free" + "bonn".   */

(function () {
  "use strict";

  var FACETS = ["page", "cost", "place", "licence", "access"];

  function base() {
    try {
      return JSON.parse(document.getElementById("__config").textContent).base;
    } catch (e) {
      return "..";
    }
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function highlight(text, query) {
    if (!query) return escapeHtml(text);
    var i = text.toLowerCase().indexOf(query);
    if (i < 0) return escapeHtml(text);
    return escapeHtml(text.slice(0, i)) + "<mark>" +
      escapeHtml(text.slice(i, i + query.length)) + "</mark>" +
      escapeHtml(text.slice(i + query.length));
  }

  function init() {
    var root = document.querySelector(".browse");
    if (!root || root.dataset.ready) return;
    root.dataset.ready = "1";

    var input = root.querySelector("#q");
    var results = root.querySelector("#results");
    var countEl = root.querySelector("#count");
    var resetEl = root.querySelector("#reset");
    var emptyEl = root.querySelector("#empty");
    var chips = Array.prototype.slice.call(root.querySelectorAll(".chip"));
    var active = {};
    var data = [];
    var prefix = base().replace(/\/$/, "");

    FACETS.forEach(function (f) { active[f] = []; });
    chips.forEach(function (c) { c.setAttribute("aria-pressed", "false"); });

    function matches(entry, query) {
      for (var i = 0; i < FACETS.length; i++) {
        var facet = FACETS[i];
        var chosen = active[facet];
        if (!chosen.length) continue;
        var values = facet === "page" ? [entry.page] : entry[facet] || [];
        var hit = chosen.some(function (v) { return values.indexOf(v) !== -1; });
        if (!hit) return false;
      }
      if (!query) return true;
      return entry.haystack.indexOf(query) !== -1;
    }

    // Same markup the category pages emit, so both surfaces look identical.
    function row(entry, query) {
      var tags = entry.tags.map(function (t) {
        return "<span>" + escapeHtml(t) + "</span>";
      }).join("");
      return '<div class="row">' +
        '<a class="row-name" href="' + escapeHtml(entry.url) + '" rel="noopener">' +
        highlight(entry.name, query) + "</a>" +
        '<div class="row-desc">' + entry.desc + "</div>" +
        '<div class="row-tags">' + tags +
        '<span class="row-from"><a href="' + prefix + "/" + entry.anchor + '">' +
        escapeHtml(entry.page_nav) + "</a></span></div></div>";
    }

    function render() {
      var query = input.value.trim().toLowerCase();
      var shown = data.filter(function (e) { return matches(e, query); });
      results.innerHTML = shown.map(function (e) { return row(e, query); }).join("");
      countEl.textContent = shown.length === data.length
        ? data.length + " resources"
        : shown.length + " of " + data.length;
      emptyEl.hidden = shown.length !== 0;
      var filtering = query !== "" || FACETS.some(function (f) { return active[f].length; });
      resetEl.hidden = !filtering;
      sync(query);
    }

    function sync(query) {
      var params = new URLSearchParams();
      if (query) params.set("q", query);
      FACETS.forEach(function (f) {
        if (active[f].length) params.set(f, active[f].join(","));
      });
      var qs = params.toString();
      history.replaceState(null, "", qs ? "?" + qs : location.pathname);
    }

    function restore() {
      var params = new URLSearchParams(location.search);
      input.value = params.get("q") || "";
      FACETS.forEach(function (f) {
        var raw = params.get(f);
        if (!raw) return;
        active[f] = raw.split(",");
        chips.forEach(function (c) {
          if (c.dataset.facet === f && active[f].indexOf(c.dataset.value) !== -1) {
            c.setAttribute("aria-pressed", "true");
          }
        });
      });
    }

    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        var facet = chip.dataset.facet, value = chip.dataset.value;
        var i = active[facet].indexOf(value);
        if (i === -1) { active[facet].push(value); } else { active[facet].splice(i, 1); }
        chip.setAttribute("aria-pressed", i === -1 ? "true" : "false");
        render();
      });
    });

    resetEl.addEventListener("click", function () {
      input.value = "";
      FACETS.forEach(function (f) { active[f] = []; });
      chips.forEach(function (c) { c.setAttribute("aria-pressed", "false"); });
      render();
      input.focus();
    });

    input.addEventListener("input", render);

    fetch(prefix + "/assets/resources.json")
      .then(function (r) { return r.json(); })
      .then(function (json) {
        data = json.map(function (e) {
          e.haystack = (e.name + " " + e.desc + " " + e.tags.join(" ") + " " +
            e.section + " " + e.page_nav).toLowerCase();
          return e;
        });
        restore();
        render();
      })
      .catch(function () {
        countEl.textContent = "Could not load the resource list.";
      });
  }

  // Material's instant navigation replaces the body, so re-run on each page.
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(init);
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
