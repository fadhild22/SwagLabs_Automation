from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    # LOCATORS
    PAGE_TITLE = (By.CLASS_NAME, "title")
    
    # Button add to cart for backpack product
    ADD_TO_CART_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    
    # Icon shopping cart
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ACTIONS
    
    def get_page_title(self):
        """Mengambil teks judul halaman untuk validasi"""
        return self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE)).text

    def add_backpack_to_cart(self):
        """Klik tombol Add to Cart produk Backpack"""
        self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BACKPACK)).click()

    def click_cart_icon(self):
        """Klik ikon keranjang untuk pindah ke halaman Cart"""
        self.wait.until(EC.element_to_be_clickable(self.CART_ICON)).click()