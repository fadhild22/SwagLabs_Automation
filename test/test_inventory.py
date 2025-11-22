import sys
import os
import unittest
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from pages.login_page import LoginPage       # Kita butuh ini buat Login dulu
from pages.inventory_page import InventoryPage # Ini yang mau kita tes

class TestInventory(unittest.TestCase):

    def setUp(self):
        # 1. Open Browser
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        
        # 2. Pre-required steps using login function from LoginPage
        login_pg = LoginPage(self.driver)
        login_pg.open_page(Config.BASE_URL)
        
        login_pg.login(Config.CREDENTIALS['valid']['username'], Config.CREDENTIALS['valid']['password'])

    def test_ensure_on_inventory_page(self):
        """Memastikan user benar-benar ada di halaman Inventory"""
        inventory_pg = InventoryPage(self.driver)
        
        # Validasi Judul Halaman harus "Products"
        actual_title = inventory_pg.get_page_title()
        self.assertEqual(actual_title, "Products")
        time.sleep(5)

    def test_add_item_to_cart(self):
        """Memastikan bisa klik Add to Cart"""
        inventory_pg = InventoryPage(self.driver)
        
        # Klik Add to Cart
        inventory_pg.add_backpack_to_cart()
        time.sleep(5)
        

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()