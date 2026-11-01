"""Browser smoke tests for the static Barbershop portfolio demo.

Run with:
  python -m pip install playwright
  python -m playwright install chromium
  python -m unittest discover -s tests -p "test_*.py" -v
"""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import unittest

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent.parent
SCREENSHOTS = ROOT / "screenshots"


class QuietStaticHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, *args):
        pass


class BarbershopBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Serve over HTTP rather than file://: external SVG <use> references
        # are blocked on file:// in Chromium even though GitHub Pages serves them.
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), QuietStaticHandler)
        cls.server_thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.site_url = f"http://127.0.0.1:{cls.server.server_port}/index.html"
        cls.asset_url = f"http://127.0.0.1:{cls.server.server_port}"

        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join(timeout=5)

    def open_page(self, width=375, height=812):
        page = self.browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=1,
            reduced_motion="reduce",
        )
        response = page.goto(self.site_url, wait_until="load")
        self.assertEqual(response.status, 200)
        return page

    def test_mobile_navigation(self):
        page = self.open_page()
        try:
            button = page.locator("[data-menu-button]")
            menu = page.locator("[data-menu]")
            self.assertTrue(button.is_visible())
            self.assertEqual(button.get_attribute("aria-expanded"), "false")

            button.click()
            self.assertEqual(button.get_attribute("aria-expanded"), "true")
            self.assertIn("navbar--open", menu.get_attribute("class"))
            self.assertIn("lock", page.locator("body").get_attribute("class"))

            page.keyboard.press("Escape")
            self.assertEqual(button.get_attribute("aria-expanded"), "false")
            self.assertNotIn("lock", page.locator("body").get_attribute("class"))

            button.click()
            menu.get_by_role("link", name="About us").click()
            self.assertEqual(button.get_attribute("aria-expanded"), "false")

            button.click()
            page.set_viewport_size({"width": 1024, "height": 768})
            page.wait_for_function(
                """() => document.querySelector('[data-menu-button]')
                    .getAttribute('aria-expanded') === 'false'""",
                timeout=2000,
            )
            self.assertEqual(button.get_attribute("aria-expanded"), "false")
            self.assertNotIn("lock", page.locator("body").get_attribute("class"))
        finally:
            page.close()

    def test_booking_is_not_submittable(self):
        page = self.open_page()
        try:
            self.assertEqual(page.locator("form").count(), 0)
            self.assertTrue(page.get_by_text("Portfolio demonstration only", exact=False).is_visible())
            inputs = page.locator(".form-online-appointment input")
            self.assertGreater(inputs.count(), 0)
            self.assertTrue(all(inputs.nth(i).is_disabled() for i in range(inputs.count())))
            self.assertTrue(page.locator(".form-online-appointment textarea").is_disabled())
            self.assertTrue(page.get_by_role("button", name="Unavailable").is_disabled())
        finally:
            page.close()

    def test_anchors_and_contact_placeholders(self):
        page = self.open_page()
        try:
            broken = page.evaluate(
                """() => [...document.querySelectorAll('a[href^="#"]')]
                  .filter(a => !a.hash || !document.getElementById(a.hash.slice(1)))
                  .map(a => a.outerHTML)"""
            )
            self.assertEqual(broken, [])
            self.assertEqual(page.locator('a[href=""]').count(), 0)
            self.assertEqual(page.locator('a[href="#"]').count(), 0)
            self.assertEqual(page.locator('a[href^="tel:"]').count(), 0)
            self.assertEqual(page.locator('a[href^="mailto:"]').count(), 0)
        finally:
            page.close()

    def test_responsive_widths(self):
        for width in (320, 375, 768, 1024, 1440):
            with self.subTest(width=width):
                page = self.open_page(width, 800)
                try:
                    actual_width = page.evaluate(
                        "() => document.documentElement.scrollWidth"
                    )
                    offenders = page.evaluate(
                        """() => [...document.querySelectorAll('body *')]
                            .filter(el => {
                                const rect = el.getBoundingClientRect();
                                return rect.right > innerWidth + 1
                                    && rect.width > 0
                                    && getComputedStyle(el).display !== 'none';
                            })
                            .map(el => ({
                                tag: el.tagName.toLowerCase(),
                                className: typeof el.className === 'string'
                                    ? el.className.slice(0, 85) : 'svg',
                                right: Math.round(el.getBoundingClientRect().right),
                                width: Math.round(el.getBoundingClientRect().width)
                            }))
                            .slice(0, 12)"""
                    )
                    scroll_children = page.evaluate(
                        """() => [...document.querySelectorAll('body, body *')]
                          .filter(el => el.scrollWidth > el.clientWidth + 2
                                  && el.scrollWidth > innerWidth)
                          .map(el => ({
                            tag: el.tagName.toLowerCase(),
                            cls: typeof el.className === 'string'
                                ? el.className.slice(0, 70) : 'svg',
                            client: el.clientWidth,
                            scroll: el.scrollWidth
                          }))
                          .slice(0, 25)"""
                    )
                    self.assertLessEqual(
                        actual_width,
                        width + 1,
                        f"Horizontal overflow: viewport={width}, document={actual_width}; "
                        f"outlying-boxes={offenders}; overflowing-containers={scroll_children}",
                    )
                finally:
                    page.close()

    def test_back_to_top_keyboard(self):
        page = self.open_page(width=1024, height=768)
        try:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            button = page.get_by_role("button", name="Back to top")
            button.wait_for(state="visible")
            button.focus()
            page.keyboard.press("Enter")
            page.wait_for_function("window.scrollY < 5")
        finally:
            page.close()

    def test_svg_assets_available_over_http(self):
        page = self.open_page()
        try:
            self.assertEqual(page.locator("svg.logo-img use").count(), 1)
            svg = page.request.get(self.asset_url + "/images/icons/sprite.svg")
            self.assertEqual(svg.status, 200)
            self.assertIn("image/svg+xml", svg.headers.get("content-type", ""))
        finally:
            page.close()

    def test_visual_snapshots(self):
        SCREENSHOTS.mkdir(exist_ok=True)
        for name, width, height in (
            ("mobile", 375, 812),
            ("desktop", 1365, 900),
        ):
            page = self.open_page(width, height)
            try:
                page.screenshot(
                    path=str(SCREENSHOTS / f"barbershop-{name}.png"),
                    full_page=True,
                    animations="disabled",
                    timeout=30000,
                )
            finally:
                page.close()


if __name__ == "__main__":
    unittest.main()
