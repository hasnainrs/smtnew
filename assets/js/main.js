/* Sports Medicine Training — main.js */
(function () {
  "use strict";

  /* mobile nav */
  var burger = document.querySelector(".burger"),
      nav = document.querySelector(".nav"),
      scrim = document.querySelector(".scrim");

  function closeNav() {
    if (!nav) return;
    nav.classList.remove("is-open");
    if (scrim) scrim.classList.remove("is-open");
    if (burger) burger.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  }
  function openNav() {
    if (!nav) return;
    nav.classList.add("is-open");
    if (scrim) scrim.classList.add("is-open");
    if (burger) burger.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
  }
  if (burger) burger.addEventListener("click", function () {
    burger.getAttribute("aria-expanded") === "true" ? closeNav() : openNav();
  });
  if (scrim) scrim.addEventListener("click", closeNav);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeNav(); });
  document.querySelectorAll(".nav a").forEach(function (a) { a.addEventListener("click", closeNav); });

  /* scroll reveal */
  var rev = document.querySelectorAll(".reveal");
  if (rev.length) {
    document.documentElement.classList.add("has-reveal");
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
        });
      }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
      rev.forEach(function (el) { io.observe(el); });
      setTimeout(function () { rev.forEach(function (el) { el.classList.add("in"); }); }, 2500);
    } else {
      rev.forEach(function (el) { el.classList.add("in"); });
    }
  }

  /* accordion */
  document.querySelectorAll(".acc-item > button").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.parentElement,
          panel = item.querySelector(".acc-panel"),
          open = item.getAttribute("data-open") === "true";
      item.parentElement.querySelectorAll(".acc-item").forEach(function (s) {
        if (s !== item) {
          s.setAttribute("data-open", "false");
          s.querySelector("button").setAttribute("aria-expanded", "false");
          s.querySelector(".acc-panel").style.maxHeight = null;
        }
      });
      item.setAttribute("data-open", String(!open));
      btn.setAttribute("aria-expanded", String(!open));
      panel.style.maxHeight = !open ? panel.scrollHeight + 24 + "px" : null;
    });
  });

  /* course category filter */
  var filters = document.querySelectorAll("[data-filter]");
  if (filters.length) {
    filters.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var want = btn.getAttribute("data-filter");
        filters.forEach(function (b) {
          b.classList.toggle("is-on", b === btn);
          b.setAttribute("aria-pressed", String(b === btn));
        });
        document.querySelectorAll("[data-cat]").forEach(function (band) {
          var show = want === "all" || band.getAttribute("data-cat") === want;
          band.classList.toggle("is-hidden", !show);
        });
      });
    });
  }

  /* forms — swap the setTimeout for your real backend */
  document.querySelectorAll("[data-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll("[required]").forEach(function (f) {
        var bad = f.type === "checkbox" ? !f.checked : !f.value.trim();
        f.style.borderColor = bad ? "#B4232A" : "";
        if (bad) ok = false;
      });
      var err = form.querySelector(".form-err");
      if (!ok) { if (err) err.style.display = "block"; return; }
      if (err) err.style.display = "none";

      var btn = form.querySelector('button[type="submit"]'),
          msg = form.querySelector(".form-ok") || form.parentElement.querySelector(".form-ok");
      if (btn) { btn.disabled = true; btn.dataset.t = btn.textContent; btn.textContent = "Sending…"; }
      setTimeout(function () {
        form.reset();
        if (btn) { btn.disabled = false; btn.textContent = btn.dataset.t; }
        if (msg) { msg.classList.add("show"); msg.setAttribute("role", "status"); msg.scrollIntoView({ behavior: "smooth", block: "center" }); }
      }, 650);
    });
  });

  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
