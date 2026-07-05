import pytest
from pages.home_page import HomePage
from pages.search_result_page import SearchResultPage
from tests.conftest import load_csv

SEARCH_DATA = [r for r in load_csv("search_and_newsletter_data.csv") if r["type"] == "search"]


class TestSearchDDT:
    @pytest.mark.parametrize(
        "row", SEARCH_DATA, ids=[r["description"] for r in SEARCH_DATA]
    )
    def test_search_article(self, driver, row):
        home = HomePage(driver)
        home.navigate()
        home.search_article(row["input_value"])

        result = SearchResultPage(driver)
        if row["expected"] == "FOUND":
            assert result.get_result_count() > 0, f"[{row['description']}] Harus ada hasil"
        else:
            assert result.has_no_result_message(), f"[{row['description']}] Harus tampil pesan kosong"
