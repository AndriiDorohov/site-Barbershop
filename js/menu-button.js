// Single source of truth for the mobile navigation state.
// Keeps the visual classes, body scroll lock, and ARIA state in sync.
(() => {
  const button = document.querySelector("[data-menu-button]");
  const menu = document.querySelector("[data-menu]");

  if (!button || !menu) return;

  const isOpen = () => button.getAttribute("aria-expanded") === "true";

  const setOpen = (open) => {
    button.setAttribute("aria-expanded", String(open));
    button.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    button.classList.toggle("menu__button--open", open);
    menu.classList.toggle("navbar--open", open);
    document.body.classList.toggle("lock", open);
  };

  setOpen(false);

  button.addEventListener("click", () => {
    setOpen(!isOpen());
  });

  menu.addEventListener("click", (event) => {
    if (!(event.target instanceof Element)) return;

    const link = event.target.closest('a[href^="#"]');
    if (link && link.getAttribute("href") !== "#") {
      setOpen(false);
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape" || !isOpen()) return;

    setOpen(false);
    button.focus();
  });

  document.addEventListener("click", (event) => {
    if (!isOpen() || !(event.target instanceof Node)) return;

    if (!button.contains(event.target) && !menu.contains(event.target)) {
      setOpen(false);
    }
  });

  // The mobile toggle is hidden at this breakpoint.
  const desktop = window.matchMedia("(min-width: 768px)");
  desktop.addEventListener("change", (event) => {
    if (event.matches) setOpen(false);
  });
})();
