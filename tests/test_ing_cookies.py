import pytest
from assertpy import assert_that
from playwright.sync_api import sync_playwright
from utils.analytics_cookies import ANALYTICS_COOKIES


def test_ing_cookies():
    with sync_playwright() as p:
        # 
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser = browser_type.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://www.ing.pl")

            # Wybranie odpowiednich cookies'ów
            page.get_by_role("button", name="Dostosuj").wait_for(state="visible", timeout=60000)
            page.get_by_role("button", name="Dostosuj").click()
            page.get_by_label("analityczne").check()
            page.get_by_role("button", name="Zaakceptuj zaznaczone").click()

            # Wykonanie paru akcji na stronie, aby odpowiednie ciasteczka się wygenerowały
            page.get_by_role("button", name="Zaloguj").click()
            page.click('button[aria-label="Zamknij wyskakujące okno"]')
            page.click('a.small_teaser_tiles__anchor >> text="Pożyczka gotówkowa"')

            cookies = context.cookies()

            # 9. Filtruj ciasteczka analityczne wg nazw
            analytics_cookies = [c for c in cookies if c['name'] in ANALYTICS_COOKIES]

            assert_that(analytics_cookies).is_not_empty().described_as("Brak ciasteczek analitycznych po akceptacji zgody.")
            for cookie in analytics_cookies:
                
                cookie_name = cookie['name']
                assert_that(any(cookie_name.startswith(name) for name in ANALYTICS_COOKIES)).is_true()

            browser.close()
