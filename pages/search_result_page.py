import re
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SearchResultPage(BasePage):

    RESULT_COUNT_TEXT = (By.XPATH, "//*[contains(text(),'hasil dari pencarian')]")
    NO_RESULT_BOX = (By.CSS_SELECTOR, "[class*='emptyAlart']")
    RESULT_ITEMS = (By.CSS_SELECTOR, "a.article-link")
    RESULT_TITLES = (By.CSS_SELECTOR, "a[href*='/read/']")

    def get_result_count_text(self):
        return self.get_text(self.RESULT_COUNT_TEXT)

    def get_result_count(self):
    try:
        text = self.get_result_count_text()
        match = re.search(r"Ditemukan\s+(\d+)\s+hasil", text)
        if match:
            return int(match.group(1))
    except Exception:
        pass
    try:
        return len(self.find_all(self.RESULT_ITEMS, timeout=15))
    except Exception:
        return 0

    def has_no_result_message(self):
        return self.is_visible(self.NO_RESULT_BOX)

    def open_first_result(self):
       handles_before = self.driver.window_handles
       self.click(self.RESULT_TITLES)

       handles_after = self.driver.window_handles
       if len(handles_after) > len(handles_before):
            self.driver.switch_to.window(handles_after[-1])
