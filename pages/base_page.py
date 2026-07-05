import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class BasePage:
    """Class induk untuk seluruh Page Object.

    Berisi method umum yang dipakai semua halaman: membuka url, mencari
    elemen dengan wait eksplisit, klik, ketik, cek visibilitas, dan
    menangani elemen pengganggu seperti popup cookie/consent.
    """

    DEFAULT_TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)

    # ---------------- Navigasi ----------------
    def open(self, url):
        self.logger.info(f"Membuka URL: {url}")
        try:
            self.driver.get(url)
        except TimeoutException:
            self.logger.warning(
                f"Timeout saat memuat {url}, menghentikan sisa pemuatan resource dan lanjut"
            )
            try:
                self.driver.execute_script("window.stop();")
            except Exception:
                pass

    # ---------------- Pencarian elemen (pakai WebDriverWait, BUKAN time.sleep) ----------------
    def find(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        """Sama seperti find(), tapi menunggu elemen benar-benar TAMPIL
        (bukan cuma ada di DOM). Wajib dipakai sebelum interaksi seperti
        clear()/send_keys(), karena elemen yang masih dalam proses animasi
        transisi (misal form multi-step) sudah 'present' tapi belum
        'interactable' -> menyebabkan ElementNotInteractableException."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def find_clickable(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def find_all(self, locator, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return self.driver.find_elements(*locator)

    # ---------------- Aksi ----------------
    def click(self, locator, max_attempts=3):
        """Klik elemen dengan penanganan dua jenis masalah umum di halaman
        dinamis seperti portal berita:

        1. StaleElementReferenceException - elemen 'basi' karena DOM berubah
           (misal iklan lazy-load menggeser layout) di antara pencarian dan
           klik. Solusinya: cari ulang elemennya dari awal.
        2. ElementClickInterceptedException - elemen tertutup elemen lain
           (banner/iklan/dropdown). Solusinya: fallback ke klik via JS.

        Kedua kasus ini bisa muncul di percobaan mana pun (termasuk saat
        mencari ulang elemen yang basi, elemen barunya bisa saja ternyata
        juga tertutup elemen lain) -- karena itu logic-nya digabung dalam
        satu loop retry, bukan blok except terpisah yang tidak saling
        menangani exception milik satu sama lain.
        """
        last_exception = None
        for attempt in range(1, max_attempts + 1):
            try:
                el = self.find_clickable(locator)
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", el
                )
                el.click()
                return
            except StaleElementReferenceException as exc:
                last_exception = exc
                self.logger.warning(
                    f"Elemen basi di {locator}, mencari ulang (percobaan {attempt}/{max_attempts})"
                )
                continue
            except ElementClickInterceptedException as exc:
                last_exception = exc
                self.logger.warning(
                    f"Klik normal terhalang elemen lain di {locator}, fallback ke klik JavaScript "
                    f"(percobaan {attempt}/{max_attempts})"
                )
                try:
                    el = self.find_clickable(locator)
                    self.driver.execute_script("arguments[0].click();", el)
                    return
                except StaleElementReferenceException as exc2:
                    # Elemen basi lagi tepat saat mau fallback JS-click -> lanjut retry loop
                    last_exception = exc2
                    continue

        # Semua percobaan habis, lempar exception terakhir yang tercatat
        raise last_exception

    def type(self, locator, text, clear_first=True, timeout=DEFAULT_TIMEOUT):
        """Ketik teks ke elemen. Menunggu elemen VISIBLE dulu (bukan cuma
        present di DOM) supaya tidak kena ElementNotInteractableException
        saat elemen masih dalam proses animasi/transisi tampil."""
        el = self.find_visible(locator, timeout=timeout)
        if clear_first:
            el.clear()
        el.send_keys(text)

    def get_text(self, locator, timeout=DEFAULT_TIMEOUT):
        return self.find(locator, timeout=timeout).text.strip()

    # ---------------- Pengecekan ----------------
    def is_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_present(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # ---------------- Elemen pengganggu ----------------
    def handle_cookie_popup(self):
        """Tutup banner cookie/consent yang sering muncul di portal berita."""
        try:
            close_btn = (
                By.CSS_SELECTOR,
                "[class*=cookie] button, [id*=consent] button, [class*=consent] button",
            )
            if self.is_visible(close_btn, timeout=3):
                self.click(close_btn)
                self.logger.info("Cookie popup ditutup")
        except Exception:
            pass  # popup tidak selalu muncul, aman diabaikan