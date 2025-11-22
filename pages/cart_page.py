from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    # LOCATORS
    PAGE_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BTN = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- ACTIONS ---
    def get_page_title(self):
        return self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE)).text

    def get_item_name(self):
        """Mengambil teks nama barang pertama di keranjang"""
        return self.wait.until(EC.visibility_of_element_located(self.INVENTORY_ITEM_NAME)).text

    def click_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BTN)).click()