(function () {
  "use strict";

  var KEY = "theme"; // "light" | "dark" | "auto"
  var root = document.documentElement;
  var darkQuery = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

  function stored() {
    try { return localStorage.getItem(KEY) || "auto"; } catch (e) { return "auto"; }
  }

  function resolve(pref) {
    if (pref === "light" || pref === "dark") return pref;
    return darkQuery && darkQuery.matches ? "dark" : "light";
  }

  function syncButtons(theme) {
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", String(theme === "dark"));
      btn.title = theme === "dark" ? "Switch to light theme" : "Switch to dark theme";
    });
  }

  function apply(pref) {
    var theme = resolve(pref);
    root.setAttribute("data-theme", theme);
    syncButtons(theme);
    document.dispatchEvent(new Event("themechange"));
  }

  function set(pref) {
    try { localStorage.setItem(KEY, pref); } catch (e) { /* storage blocked: the theme still changes on this page */ }
    apply(pref);
  }

  apply(stored()); // runs in <head>, before first paint, so there is no flash

  // One delegated listener: works for any toggle button, whenever it appears.
  document.addEventListener("click", function (event) {
    var button = event.target.closest ? event.target.closest("[data-theme-toggle]") : null;
    if (!button) return;
    set(root.getAttribute("data-theme") === "dark" ? "light" : "dark");
  });

  if (darkQuery && darkQuery.addEventListener) {
    darkQuery.addEventListener("change", function () { if (stored() === "auto") apply("auto"); });
  }

  document.addEventListener("DOMContentLoaded", function () { syncButtons(root.getAttribute("data-theme")); });

  window.setTheme = set;
})();