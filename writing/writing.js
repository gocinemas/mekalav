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


// Search and topic filter on the /writing/ list. Works on the page's own
// markup, so there is no index file to keep in step with the posts.
(function () {
  const input = document.getElementById("writing-q");
  if (!input) return;
  const items = Array.from(document.querySelectorAll(".post-item"));
  const buttons = Array.from(document.querySelectorAll(".tag-filter"));
  const status = document.querySelector(".search-status");
  const empty = document.querySelector(".no-results");
  const params = new URLSearchParams(location.search);
  let tag = (params.get("tag") || "").toLowerCase();
  input.value = params.get("q") || "";

  function apply() {
    const words = input.value.toLowerCase().split(/\s+/).filter(Boolean);
    let shown = 0;
    items.forEach(item => {
      const tags = item.dataset.tags.split("|");
      const text = item.dataset.search;
      const ok = (!tag || tags.includes(tag)) && words.every(w => text.includes(w));
      item.hidden = !ok;
      if (ok) shown++;
    });
    buttons.forEach(b => b.classList.toggle("active", b.dataset.tag === tag));
    empty.hidden = shown > 0;
    status.textContent = (words.length || tag) ? shown + " of " + items.length + " posts" : "";
    const next = new URLSearchParams();
    if (input.value.trim()) next.set("q", input.value.trim());
    if (tag) next.set("tag", tag);
    const qs = next.toString();
    history.replaceState(null, "", location.pathname + (qs ? "?" + qs : ""));
  }

  input.addEventListener("input", apply);
  buttons.forEach(b => b.addEventListener("click", () => { tag = b.dataset.tag; apply(); }));
  document.addEventListener("keydown", e => {
    if (e.key === "/" && document.activeElement !== input) { e.preventDefault(); input.focus(); }
  });
  apply();
})();
