from selenium.webdriver.common.by import By

class CartPage:
    # LOCATORS
    PAGE_TITLE = (By.CLASS_NAME, "title")
    
    # Itemn namenya yg title di keranjang
    INVENTORY_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    
    # Tombol Checkout
    CHECKOUT_BTN = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver

    # --- ACTIONS ---
    def get_page_title(self):
        return self.driver.find_element(*self.PAGE_TITLE).text

    def get_item_name(self):
        """Mengambil teks nama barang pertama di keranjang"""
        return self.driver.find_element(*self.INVENTORY_ITEM_NAME).text

    def click_checkout(self):
        self.driver.find_element(*self.CHECKOUT_BTN).click()