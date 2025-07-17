import os
import pytest
from assertpy import assert_that
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from utils.analytics_cookies import ANALYTICS_COOKIES


@pytest.mark.asyncio
async def test_ing_cookies():
    errors = []

    selected_browser = os.getenv("BROWSER")  # np. "chromium", "firefox", "webkit"

    async with Stealth().use_async(async_playwright()) as p:
        browser_map = {
            "chromium": p.chromium,
            "firefox": p.firefox,
            "webkit": p.webkit,
        }

        # Jeśli nie podano konkretnej przeglądarki – testuj wszystkie
        browsers_to_test = (
            [selected_browser] if selected_browser in browser_map else browser_map.keys()
        )

        for browser_name in browsers_to_test:
            browser_type = browser_map[browser_name]
            browser = None
            try:
                browser = await browser_type.launch(headless=True)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                    locale="pl-PL",
                    timezone_id="Europe/Warsaw",
                    permissions=["geolocation"],
                    geolocation={"latitude": 52.2297, "longitude": 21.0122},
                    viewport={"width": 1600, "height": 900}
                )
                
                page = await context.new_page()

                await Stealth().apply_stealth_async(page)

                await page.goto("https://www.ing.pl")
                await page.wait_for_load_state("load", timeout=60000)

                os.makedirs("artifacts", exist_ok=True)
                await page.screenshot(path=f"artifacts/screen_no_1_{browser_name}.png")

                # Akceptacja cookies
                await page.get_by_role("button", name="Dostosuj").wait_for(state="visible", timeout=60000)

                await page.screenshot(path=f"artifacts/screen_no_1_{browser_name}.png")
                await page.get_by_role("button", name="Dostosuj").click()
                await page.get_by_label("analityczne").check()
                await page.get_by_role("button", name="Zaakceptuj zaznaczone").click()

                # Akcje na stronie
                await page.get_by_role("button", name="Zaloguj").click()
                await page.click('button[aria-label="Zamknij wyskakujące okno"]')
                await page.click('a.small_teaser_tiles__anchor >> text="Pożyczka gotówkowa"')

                # Sprawdzenie cookies
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
