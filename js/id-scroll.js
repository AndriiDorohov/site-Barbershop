// Smooth-scroll only for existing on-page section links.
// Do not intercept external, mailto:, tel:, or placeholder links.
document.addEventListener("click", (event) => {
  if (!(event.target instanceof Element)) return;

  const link = event.target.closest('a[href^="#"]');
  if (!link) return;

  const hash = link.getAttribute("href");
  if (!hash || hash === "#") return;

  const section = document.getElementById(hash.slice(1));
  if (!section) return;

  event.preventDefault();

  const reduceMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  section.scrollIntoView({
    behavior: reduceMotion ? "auto" : "smooth",
    block: "start",
  });

  window.history.replaceState(null, "", hash);
});
