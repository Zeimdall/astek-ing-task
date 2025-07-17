import pytest
import os
from assertpy import assert_that
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from utils.analytics_cookies import ANALYTICS_COOKIES


def test_ing_cookies():
    errors = []
    with Stealth().use_sync(sync_playwright()) as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            try:
                browser = browser_type.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                page.goto("https://www.ing.pl")
                if not os.path.exists("artifacts"):
                    os.makedirs("artifacts")

                page.screenshot(path=f"artifacts/screen_no_1_{browser_type.name}.png")
                page.wait_for_load_state("load", timeout=60000)
                page.screenshot(path=f"artifacts/screen_no_2_{browser_type.name}.png")

                # Cookie dialog
                page.get_by_role("button", name="Dostosuj").wait_for(state="visible", timeout=60000)
                page.get_by_role("button", name="Dostosuj").click()
                page.get_by_label("analityczne").check()
                page.get_by_role("button", name="Zaakceptuj zaznaczone").click()

                page.get_by_role("button", name="Zaloguj").click()
                page.click('button[aria-label="Zamknij wyskakujące okno"]')
                page.click('a.small_teaser_tiles__anchor >> text="Pożyczka gotówkowa"')

                cookies = context.cookies()
                analytics_cookies = [c for c in cookies if c['name'] in ANALYTICS_COOKIES]

                assert_that(analytics_cookies).is_not_empty()
                for cookie in analytics_cookies:
                    cookie_name = cookie['name']
                    assert_that(any(cookie_name.startswith(name) for name in ANALYTICS_COOKIES)).is_true()

                browser.close()

            except Exception as e:
                errors.append(f"{browser_type.name}: {str(e)}")
                try:
                    page.screenshot(path=f"artifacts/failed_{browser_type.name}.png")
                except:
                    pass
                if 'browser' in locals():
                    browser.close()
    if errors:
        raise AssertionError("Some tests failed:\n".join(errors))
