from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ArticlePage(BasePage):
    """Page Object untuk halaman detail artikel Kompas.com."""
    TITLE = (By.CSS_SELECTOR, "h1.read_title, h1")
    AUTHOR = (By.CSS_SELECTOR, ".credit-title-name")
    DATE = (By.CSS_SELECTOR, ".read_date")

    HOME_BUTTON = (By.CSS_SELECTOR, "a[href='https://www.kompas.com']")

    def get_title_text(self):
        return self.get_text(self.TITLE)

    def is_author_visible(self):
        return self.is_visible(self.AUTHOR)

    def is_date_visible(self):
        return self.is_visible(self.DATE)

    def back_to_home(self):
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.click(self.HOME_BUTTON)
