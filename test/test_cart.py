import sys
import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage  

class TestCart(unittest.TestCase):

    def setUp(self):
        options = Options()
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False
        }
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.driver.maximize_window()
        
        self.wait = WebDriverWait(self.driver, 10)
        
        login_pg = LoginPage(self.driver)
        login_pg.open_page(Config.BASE_URL)
        login_pg.login(Config.CREDENTIALS['valid']['username'], Config.CREDENTIALS['valid']['password'])
        
        # ADD ITEM & MASUK KE CART PAGE
        inventory_pg = InventoryPage(self.driver)
        inventory_pg.add_backpack_to_cart() 
        inventory_pg.click_cart_icon()
        
        self.wait.until(EC.url_contains("cart.html"))

    def test_item_is_in_cart(self):
        """Memastikan barang yang ditambah benar-benar ada di keranjang"""
        cart_pg = CartPage(self.driver)
        
        # Validasi 1: Judul Halaman benar "Your Cart"
        self.assertEqual(cart_pg.get_page_title(), "Your Cart")
        
        # Validasi 2: Nama barangnya benar "Sauce Labs Backpack"
        item_name = cart_pg.get_item_name()
        self.assertEqual(item_name, "Sauce Labs Backpack")

    def test_proceed_to_checkout(self):
        """Memastikan tombol checkout berfungsi"""
        cart_pg = CartPage(self.driver)
        
        # Klik tombol Checkout
        cart_pg.click_checkout()
        
        self.wait.until(EC.url_contains("checkout-step-one"))
        self.assertIn("checkout-step-one", self.driver.current_url)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()