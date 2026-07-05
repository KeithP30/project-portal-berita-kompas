import time
import allure
from pages.home_page import HomePage
from pages.search_result_page import SearchResultPage
from pages.article_page import ArticlePage
from pages.newsletter_page import NewsletterPage


@allure.feature("Portal Berita Kompas.com")
@allure.story("End-to-End: Beranda - Cari - Artikel - Kembali - Register (Subscribe)")
class TestE2EPortalBerita:
    @allure.title("TC-PB-012: Alur Penuh Beranda -> Cari -> Artikel -> Kembali -> Subscribe")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_full_reader_flow(self, driver):
        with allure.step("1. Buka halaman beranda Kompas.com"):
            home = HomePage(driver)
            home.navigate()

        with allure.step('2. Cari artikel dengan kata kunci "kurs dollar"'):
            home.search_article_by_url("kurs dollar")
            result = SearchResultPage(driver)
            assert result.get_result_count() > 0

        with allure.step("3. Buka artikel pertama dari hasil pencarian"):
            result.open_first_result()
            article = ArticlePage(driver)
            assert article.get_title_text() != ""
            assert article.is_author_visible()
            assert article.is_date_visible()

        with allure.step("4. Kembali ke halaman beranda"):
            article.back_to_home()

        with allure.step(
            "5. Klik 'Daftarkan Email' lalu isi form Register sampai reCAPTCHA muncul"
        ):
            home.go_to_newsletter()
            newsletter = NewsletterPage(driver)
            newsletter.go_to_register()
            unique_email = f"qa.test.{int(time.time())}@mailinator.com"

            # --- Step 1: Data diri ---
            newsletter.fill_step1(
                fullname="QA Tester E2E",
                gender_value="l",      
                tahun="2005",
                bulan_index=0,         
                tanggal="15",
                phone="081234567890",
            )

            # --- Step 2: Email ---
            newsletter.fill_step2(email=unique_email)

            # --- Step 3: Password ---
            newsletter.fill_password("Password123")

            assert newsletter.is_recaptcha_visible(), (
                "Form pendaftaran harus terisi lengkap sampai reCAPTCHA muncul"
            )

        allure.attach(
            driver.get_screenshot_as_png(),
            name="e2e_final_state",
            attachment_type=allure.attachment_type.PNG,
        )