from pages.home_page import HomePage
from pages.search_result_page import SearchResultPage


class TestBeranda:
    def test_beranda_terbuka(self, driver):
        """TC-PB-001: Verifikasi halaman beranda terbuka & title mengandung nama situs."""
        home = HomePage(driver)
        home.navigate()
        assert "kompas" in driver.title.lower(), "Title halaman harus mengandung 'kompas'"


class TestKategori:
    def test_kategori_dapat_diklik(self, driver):
        """TC-PB-004: Verifikasi menu kategori dapat diklik dan memuat artikel."""
        home = HomePage(driver)
        home.navigate()
        home.open_category("Money")
        assert home.get_article_count() >= 1, "Halaman kategori harus memuat minimal 1 artikel"

    def test_jumlah_artikel_kategori(self, driver):
        """TC-PB-005: Verifikasi jumlah artikel yang tampil di halaman kategori >= 1."""
        home = HomePage(driver)
        home.navigate()
        home.open_category("Money")
        assert home.get_article_count() >= 1
        @allure.title("TC-PB-013: Verifikasi kategori Tekno dapat diklik dan memuat artikel")
def test_kategori_tekno_dapat_diklik(self, driver):
    home = HomePage(driver)
    home.navigate()
    home.open_category("Tekno")
    assert home.get_article_count() >= 1, "Halaman kategori Tekno harus memuat minimal 1 artikel"


class TestNavigasi:
    def test_kembali_ke_beranda(self, driver):
        home = HomePage(driver)
        home.navigate()
        home.search_article_by_url("pemilu")

        result = SearchResultPage(driver)
        assert result.get_result_count() > 0, "Harus ada hasil pencarian untuk 'pemilu'"
        result.open_first_result()

        from pages.article_page import ArticlePage
        article = ArticlePage(driver)
        article.back_to_home()
        assert "kompas" in driver.title.lower()
