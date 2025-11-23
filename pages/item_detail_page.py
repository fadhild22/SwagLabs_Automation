from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ItemDetailPage:
    BACK_TO_PRODUCTS_BTN = (By.ID, "back-to-products")
    ITEM_NAME_LARGE = (By.CLASS_NAME, "inventory_details_name")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_item_name(self):
        """Ambil nama produk besar untuk Validasi"""
        return self.wait.until(EC.visibility_of_element_located(self.ITEM_NAME_LARGE)).text

    def click_back_to_products(self):
        """Klik tombol Back"""
        self.wait.until(EC.element_to_be_clickable(self.BACK_TO_PRODUCTS_BTN)).click()