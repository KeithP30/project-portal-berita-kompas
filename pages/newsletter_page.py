from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class NewsletterPage(BasePage):
    SUCCESS_URL_PART = "newsletter/pendaftaran-berhasil"
    SUCCESS_TITLE = (By.XPATH, "//*[contains(text(),'berhasil didaftarkan')]")
    REGISTER_LINK = (By.PARTIAL_LINK_TEXT, "Daftar Akun KG Media ID")
    ERROR_MSG = (By.CSS_SELECTOR, ".form-email.form-error")

    # ---- Step 1: Data diri ----
    FULLNAME_INPUT = (By.CSS_SELECTOR, "input#fullname")
    GENDER_SELECT = (By.CSS_SELECTOR, "select#gender")
    BIRTHDATE_INPUT = (By.CSS_SELECTOR, "input#birthdate")
    PHONE_INPUT = (By.CSS_SELECTOR, "input#phone_2")
    NEXT_STEP1_BUTTON = (By.CSS_SELECTOR, "input#next1")

    # ---- Step 2: Email ----
    EMAIL_INPUT = (By.CSS_SELECTOR, "input#email")
    CONSENT_CHECKBOX = (By.CSS_SELECTOR, "div.form-checkbox input[type='checkbox']")
    NEXT_STEP2_BUTTON = (By.CSS_SELECTOR, "input#next2")

    # ---- Step 3: Password ----
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input#password")
    PASSWORD_CONFIRM_INPUT = (By.CSS_SELECTOR, "input#password_confirmation")
    RECAPTCHA_IFRAME = (By.CSS_SELECTOR, "iframe[title*='recaptcha'], iframe[src*='recaptcha']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "input#next3")

    def go_to_register(self):
        try:
            self.click(self.REGISTER_LINK)
        except TimeoutException as e:
            raise TimeoutException(
                f"Link '{self.REGISTER_LINK}' tidak ditemukan/tidak bisa diklik di {self.driver.current_url}. "
                f"Cek ulang locator lewat Inspect Element."
            ) from e

    # ---------------- Step 1 ----------------
    def fill_fullname(self, fullname):
        self.type(self.FULLNAME_INPUT, fullname)

    def select_gender(self, value):
        el = self.find(self.GENDER_SELECT)
        Select(el).select_by_value(value)

    def _click_datepicker_cell(self, css_scope, attr, value):
        locator = (By.CSS_SELECTOR, f"{css_scope}[{attr}='{value}']")
        self.click(locator)

    def pilih_tanggal_lahir(self, tahun, bulan_index, tanggal):
        self.click(self.BIRTHDATE_INPUT)
        self._click_datepicker_cell("span.datepicker-cell.year", "data-year", tahun)
        self._click_datepicker_cell("span.datepicker-cell.month", "data-month", bulan_index)
        day_locator = (
            By.XPATH,
            f"//span[contains(concat(' ', normalize-space(@class), ' '), ' datepicker-cell day ')]"
            f"[not(contains(@class, 'prev')) and not(contains(@class, 'next'))]"
            f"[normalize-space(text())='{tanggal}']",
        )
        self.click(day_locator)

    def fill_phone(self, phone):
        self.type(self.PHONE_INPUT, phone)

    def go_to_step2(self):
        self.click(self.NEXT_STEP1_BUTTON)

    def fill_step1(self, fullname, gender_value, tahun, bulan_index, tanggal, phone):
        self.fill_fullname(fullname)
        self.select_gender(gender_value)
        self.pilih_tanggal_lahir(tahun, bulan_index, tanggal)
        self.fill_phone(phone)
        self.go_to_step2()

    # ---------------- Step 2 ----------------
    def fill_email(self, email):
        self.type(self.EMAIL_INPUT, email)

    def ensure_consent_checked(self):
        checkbox = self.find(self.CONSENT_CHECKBOX)
        if not checkbox.is_selected():
            self.click(self.CONSENT_CHECKBOX)

    def go_to_step3(self):
        self.click(self.NEXT_STEP2_BUTTON)

    def fill_step2(self, email):
        self.fill_email(email)
        self.ensure_consent_checked()
        self.go_to_step3()

    # ---------------- Step 3 ----------------
    def fill_password(self, password):
        self.type(self.PASSWORD_INPUT, password)
        self.type(self.PASSWORD_CONFIRM_INPUT, password)

    def is_recaptcha_visible(self):
        return self.is_visible(self.RECAPTCHA_IFRAME, timeout=10)

    def is_subscribe_success(self):
        return self.SUCCESS_URL_PART in self.driver.current_url and \
            self.is_visible(self.SUCCESS_TITLE)

    def get_registered_email_text(self):
        return self.get_text(self.SUCCESS_TITLE)

    def is_email_format_error_shown(self):
        return self.is_visible(self.ERROR_MSG)