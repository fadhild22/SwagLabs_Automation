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

class TestInventory(unittest.TestCase):

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
        
        # 2. Pre-required steps using login function from LoginPage
        login_pg = LoginPage(self.driver)
        login_pg.open_page(Config.BASE_URL)
        login_pg.login(Config.CREDENTIALS['valid']['username'], Config.CREDENTIALS['valid']['password'])
        
        self.wait.until(EC.url_contains("inventory.html"))

    def test_ensure_on_inventory_page(self):
        """Memastikan user benar-benar ada di halaman Inventory"""
        inventory_pg = InventoryPage(self.driver)
        
        # Validasi Judul Halaman harus "Products"
        actual_title = inventory_pg.get_page_title()
        self.assertEqual(actual_title, "Products")

    def test_add_item_to_cart(self):
        """Memastikan bisa klik Add to Cart"""
        inventory_pg = InventoryPage(self.driver)
        
        # Klik Add to Cart
        inventory_pg.add_backpack_to_cart()
        

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()