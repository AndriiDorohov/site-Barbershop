# Barbershop — Responsive Landing Page

A responsive, single-page website created as an HTML/CSS coursework project. The focus is frontend implementation: page structure, responsive layout, SCSS organization, and small JavaScript interactions.

**This is a fictional business demo, not a real barbershop or an active booking service.**

[View the GitHub Pages demo](https://andriidorohov.github.io/site-Barbershop/) · [View the source](https://github.com/AndriiDorohov/site-Barbershop)

![Barbershop landing page preview](images/preview_01.png)

## Highlights

- Semantic HTML structure for a single-page marketing website.
- Responsive styling with organized Sass partials and compiled CSS.
- Mobile navigation menu and in-page section links.
- Smooth scrolling for valid section anchors, with reduced-motion support.
- Back-to-top control and presentation sections for services, barbers, and contacts.

## Stack

- HTML5
- CSS3 and SCSS (Sass)
- Vanilla JavaScript for mobile navigation, section links, and the scroll-to-top control
- GitHub Pages for the static demo

## Run locally

No backend or install step is required to view the committed static website.

```bash
git clone https://github.com/AndriiDorohov/site-Barbershop.git
cd site-Barbershop
python3 -m http.server 8000
```

Open <http://localhost:8000> in your browser. Stop the local server with Ctrl+C.

The committed `css/main.css` is already compiled; it can be used without installing Sass. SCSS sources live under `sass/` and the entry point is `sass/main.scss`.

If you want to edit styles and have the Sass CLI available, compile them with:

```bash
sass sass/main.scss css/main.css
```

## Main files

```text
index.html             Page content and markup
css/main.css           CSS used by the page
sass/main.scss         SCSS entry point
sass/components/       Component-level styles
sass/utils/            Sass shared variables
js/menu-button.js      Mobile menu state, accessibility, and body scroll lock
js/id-scroll.js        Internal navigation / smooth scroll
js/totop.js            Back-to-top button
images/                Illustrations, icons, and project screenshot
```

## Demo limitations

- The booking area is a **disabled visual mockup**, not a working reservation service; its fields cannot accept data.
- The business address, contact details, opening hours, and social identities are fictional display content, not real contacts. Non-working external links are rendered as text rather than clickable anchors.
- Structured Organization schema was removed because this is not a genuine operating business.
- Mobile navigation uses only vanilla JavaScript. Clicking a section closes the menu; Escape, outside clicks, and desktop resizing also dismiss it.
- A lightweight Chromium smoke-test suite now covers viewport widths, mobile navigation, disabled booking, anchors, and keyboard activation. It is not a full accessibility audit or a production build test.
- This README documents source-code behavior; browser compatibility and the live GitHub Pages deployment still need to be rechecked.

## Browser checks

The repository includes Playwright/Chromium smoke tests that check the mobile menu, anchors, responsive overflow at five viewport widths, disabled booking fields, and the keyboard-operated back-to-top button.

```bash
python3 -m pip install playwright==1.56.0
python3 -m playwright install chromium
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

GitHub Actions also runs these checks for proposed changes and uploads mobile and desktop preview screenshots as temporary workflow artifacts. Passing smoke tests is not a substitute for manual visual and accessibility review.

## Planned improvements

1. Review the captured mobile and desktop screenshots and correct any remaining responsive issues.
2. Review remaining content accuracy, keyboard accessibility, and image descriptions.
3. Verify that compiled CSS remains in sync with the Sass source.
4. Revisit the published demo after testing and merging the revised site.

## Project context

This is a learning project. It demonstrates frontend fundamentals and is kept separate from larger backend, full-stack, and DevOps repositories. Features described as demonstrations should not be mistaken for real business functionality.
