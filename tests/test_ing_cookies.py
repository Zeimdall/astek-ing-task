import os
import pytest
import asyncio
from assertpy import assert_that
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from utils.analytics_cookies import ANALYTICS_COOKIES


@pytest.mark.asyncio
async def test_ing_cookies():
    errors = []
    async with Stealth().use_async(async_playwright()) as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser_name = browser_type.name
            browser = None
            try:
                browser = await browser_type.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                
                Stealth().apply_stealth_async(page)

                await page.goto("https://www.ing.pl", timeout=60000)

                os.makedirs("artifacts", exist_ok=True)
                await page.screenshot(path=f"artifacts/screen_no_1_{browser_name}.png")
                await page.wait_for_load_state("load", timeout=60000)
                await page.screenshot(path=f"artifacts/screen_no_2_{browser_name}.png")

                # Cookie dialog
                await page.get_by_role("button", name="Dostosuj").wait_for(state="visible", timeout=60000)
                await page.get_by_role("button", name="Dostosuj").click()
                await page.get_by_label("analityczne").check()
                await page.get_by_role("button", name="Zaakceptuj zaznaczone").click()

                await page.get_by_role("button", name="Zaloguj").click()
                await page.click('button[aria-label="Zamknij wyskakujące okno"]')
                await page.click('a.small_teaser_tiles__anchor >> text="Pożyczka gotówkowa"')

                cookies = await context.cookies()
                analytics_cookies = [c for c in cookies if c['name'] in ANALYTICS_COOKIES]

                assert_that(analytics_cookies).is_not_empty()
                for cookie in analytics_cookies:
                    cookie_name = cookie['name']
                    assert_that(any(cookie_name.startswith(name) for name in ANALYTICS_COOKIES)).is_true()

                await browser.close()

            except Exception as e:
                errors.append(f"{browser_name}: {e}")
                try:
                    await page.screenshot(path=f"artifacts/failed_{browser_name}.png")
                except:
                    pass
                if browser:
                    await browser.close()

    if errors:
        raise AssertionError("Some browsers failed:\n" + "\n".join(errors))


asyncio.run(test_ing_cookies())
