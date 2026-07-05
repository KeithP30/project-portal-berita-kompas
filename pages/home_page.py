from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object untuk halaman Beranda Kompas.com."""

    URL = "https://www.kompas.com"
    SEARCH_BASE_URL = "https://search.kompas.com/search?q="

    SEARCH_INPUT = (By.ID, "cSearch")
    SEARCH_SUBMIT = (By.CSS_SELECTOR, "input.header-search-button")
    NAV_CATEGORY = (By.LINK_TEXT, "Money")
    ARTICLE_LIST = (By.CSS_SELECTOR, "a[href*='/read/']")
    NEWSLETTER_LINK = (By.LINK_TEXT, "Daftarkan Email")

    def navigate(self):
        self.open(self.URL)
        self.handle_cookie_popup()

    def search_article(self, keyword):
        el = self.find(self.SEARCH_INPUT)
        el.clear()
        el.send_keys(keyword)
        el.send_keys(Keys.RETURN)

    def search_article_by_url(self, keyword):
        self.open(self.SEARCH_BASE_URL + keyword)

    def open_category(self, category_link_text):
        self.click((By.LINK_TEXT, category_link_text))

    def get_article_count(self):
        return len(self.driver.find_elements(*self.ARTICLE_LIST))

    def go_to_newsletter(self):
        self.click(self.NEWSLETTER_LINK)