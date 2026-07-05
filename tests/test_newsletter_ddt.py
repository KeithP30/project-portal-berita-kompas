import time
from pages.home_page import HomePage
from pages.newsletter_page import NewsletterPage


class TestNewsletterDDT:
    def test_register_subscribes_newsletter(self, driver):
        home = HomePage(driver)
        home.navigate()
        home.go_to_newsletter()

        page = NewsletterPage(driver)
        page.go_to_register()

        page.fill_step1(
            fullname="QA Tester Otomatis",
            gender_value="l",
            tahun="2005",
            bulan_index=0,      
            tanggal="15",
            phone="081234567890",
        )
        page.fill_step2(email=f"qa.test.{int(time.time())}@mailinator.com")
        page.fill_password("Password123")

        assert page.is_recaptcha_visible(), (
            "Form pendaftaran harus terisi lengkap sampai reCAPTCHA muncul"
        )