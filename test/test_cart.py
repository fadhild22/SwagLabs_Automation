import sys
import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage  

class TestCart(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        
        login_pg = LoginPage(self.driver)
        login_pg.open_page(Config.BASE_URL)
        login_pg.login(Config.CREDENTIALS['valid']['username'], Config.CREDENTIALS['valid']['password'])
        
        # ADD ITEM & MASUK KE CART PAGE
        inventory_pg = InventoryPage(self.driver)
        inventory_pg.add_backpack_to_cart() 
        inventory_pg.click_cart_icon()      

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
        
        self.assertIn("checkout-step-one", self.driver.current_url)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()