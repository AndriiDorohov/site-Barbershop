"""Browser smoke tests for the static Barbershop portfolio demo.

Run with:
  python -m pip install playwright
  python -m playwright install chromium
  python -m unittest discover -s tests -p "test_*.py" -v
"""

from pathlib import Path
import unittest

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent.parent
URL = (ROOT / "index.html").as_uri()
SCREENSHOTS = ROOT / "screenshots"


class BarbershopBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def open_page(self, width=375, height=812):
        page = self.browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=1,
            reduced_motion="reduce",
        )
        page.goto(URL, wait_until="domcontentloaded")
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
                    self.assertLessEqual(
                        actual_width,
                        width + 1,
                        f"Horizontal overflow: viewport={width}, document={actual_width}",
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
