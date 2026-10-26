// Theme toggle for the writing pages. Uses the same storage key as the homepage,
// so a choice made on one page carries over to the others.
function setTheme(t) {
  document.documentElement.setAttribute("data-theme", t);
  try { localStorage.setItem("mekalav_theme", t); } catch (e) {}
  document.querySelectorAll(".theme-btn").forEach(b => b.classList.toggle("active", b.dataset.t === t));
}
(function () {
  let saved = "system";
  try { saved = localStorage.getItem("mekalav_theme") || "system"; } catch (e) {}
  setTheme(saved);
})();

