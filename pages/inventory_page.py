from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class InventoryPage:
    # LOCATORS
    PAGE_TITLE = (By.CLASS_NAME, "title")
    ADD_TO_CART_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    REMOVE_BTN_BACKPACK = (By.ID, "remove-sauce-labs-backpack")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    ITEM_NAME_LINK = (By.CLASS_NAME, "inventory_item_name")
    
    BURGER_MENU_BTN = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ITEM_IMAGES = (By.CSS_SELECTOR, "img.inventory_item_img")

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
    
    def click_burger_menu(self):
        """Klik tombol menu di pojok kiri atas"""
        self.wait.until(EC.element_to_be_clickable(self.BURGER_MENU_BTN)).click()

    def click_logout(self):
        """Klik tombol Logout di sidebar"""
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK)).click()
    
    def select_sort_option(self, value):
        """
        Memilih opsi dropdown sortir.
        Value bisa: 'az', 'za', 'lohi', 'hilo'
        """
        
        dropdown_element = self.wait.until(EC.visibility_of_element_located(self.SORT_DROPDOWN))
        select = Select(dropdown_element)
        select.select_by_value(value)

    def get_all_product_names(self):
        """Mengembalikan LIST berisi semua nama produk (Teks)"""
        
        self.wait.until(EC.visibility_of_element_located(self.ITEM_NAMES))
        
        # Ambil semua elemen
        elements = self.driver.find_elements(*self.ITEM_NAMES)
        
        # Ekstrak teksnya saja -> ['Sauce Labs Backpack', 'Sauce Labs Bike Light', ...]
        return [el.text for el in elements]

    def get_all_product_prices(self):
        """Mengembalikan LIST berisi harga (Float)"""
        self.wait.until(EC.visibility_of_element_located(self.ITEM_PRICES))
        elements = self.driver.find_elements(*self.ITEM_PRICES)
        
        # Ekstrak teks, buang tanda '$', ubah ke float
        # Contoh: "$29.99" -> 29.99
        return [float(el.text.replace("$", "")) for el in elements]

    def get_all_images(self):
        """Mengembalikan LIST elemen gambar (untuk dicek src-nya di test)"""
        self.wait.until(EC.visibility_of_element_located(self.ITEM_IMAGES))
        return self.driver.find_elements(*self.ITEM_IMAGES)
    
    def get_cart_badge_number(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.SHOPPING_CART_BADGE)).text
        except:
            return "0"

    def is_remove_button_visible(self):
        return self.wait.until(EC.visibility_of_element_located(self.REMOVE_BTN_BACKPACK)).is_displayed()

    def click_first_item_name(self):
        # Klik produk pertama untuk masuk ke detail
        items = self.driver.find_elements(*self.ITEM_NAME_LINK)
        items[0].click()