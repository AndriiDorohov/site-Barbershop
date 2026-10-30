const toTopButton = document.getElementById("to-top-btn");

if (toTopButton) {
  const prefersReducedMotion = () =>
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const updateVisibility = () => {
    const visible = window.scrollY > window.innerHeight / 2;
    toTopButton.style.display = visible ? "block" : "none";
  };

  toTopButton.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: prefersReducedMotion() ? "auto" : "smooth",
    });
  });

  window.addEventListener("scroll", updateVisibility, { passive: true });
  window.addEventListener("resize", updateVisibility);
  updateVisibility();
}
