from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    # LOCATORS
    PAGE_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BTN = (By.ID, "checkout")
    
    REMOVE_BTN = (By.ID, "remove-sauce-labs-backpack")
    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")
    CART_ITEM_CONTAINER = (By.CLASS_NAME, "cart_item")

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
    
    def click_remove_item(self):
        self.wait.until(EC.element_to_be_clickable(self.REMOVE_BTN)).click()

    def click_continue_shopping(self):
        self.wait.until(EC.element_to_be_clickable(self.CONTINUE_SHOPPING_BTN)).click()

    def is_item_displayed(self):
        items = self.driver.find_elements(*self.CART_ITEM_CONTAINER)
        return len(items) > 0