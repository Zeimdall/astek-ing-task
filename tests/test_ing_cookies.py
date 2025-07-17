import pytest
import os
import asyncio
from assertpy import assert_that
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from utils.analytics_cookies import ANALYTICS_COOKIES


@pytest.mark.asyncio
async def test_ing_cookies():
    async with async_playwright() as p:
        # 
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser = await browser_type.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await Stealth().apply_stealth_async(page)

            await page.goto("https://www.ing.pl")

            # Dynamiczny wait, który pozwala, aby wszystko poprawnie wczytało się na stronie
            await page.wait_for_load_state("networkidle")

            # Wybranie odpowiednich cookies'ów
            await page.get_by_role("button", name="Dostosuj").wait_for(state="visible", timeout=60000)
            await page.get_by_role("button", name="Dostosuj").click()
            await page.get_by_label("analityczne").check()
            await page.get_by_role("button", name="Zaakceptuj zaznaczone").click()

            # Wykonanie paru akcji na stronie, aby odpowiednie ciasteczka się wygenerowały
            await page.get_by_role("button", name="Zaloguj").click()
            await page.click('button[aria-label="Zamknij wyskakujące okno"]')
            await page.click('a.small_teaser_tiles__anchor >> text="Pożyczka gotówkowa"')

            # Pobranie ciasteczek po wykonanych czynnościach
            cookies = await context.cookies()

            # Filtruj ciasteczka analityczne wg nazw
            analytics_cookies = [c for c in cookies if c['name'] in ANALYTICS_COOKIES]

            assert_that(analytics_cookies).is_not_empty()
            for cookie in analytics_cookies:
                
                cookie_name = cookie['name']
                assert_that(any(cookie_name.startswith(name) for name in ANALYTICS_COOKIES)).is_true()

            await browser.close()

asyncio.run(test_ing_cookies())
