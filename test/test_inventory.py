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
        
    def _login_as(self, user_key):
        """Helper untuk login dinamis & membersihkan sesi sebelumnya"""
        
        self.driver.delete_all_cookies()
        
        login_pg = LoginPage(self.driver)
        login_pg.open_page(Config.BASE_URL)
        
        user = Config.CREDENTIALS[user_key]
        login_pg.login(user['username'], user['password'])
        
        self.wait.until(EC.url_contains("inventory.html"))
        
    def test_sort_z_to_a(self):
        """TC 4: Memastikan Sortir Z-A berfungsi untuk semua user"""
        
        users_to_test = ['valid', 'problem', 'glitch']
        
        for user in users_to_test:
            with self.subTest(user=user):
                self._login_as(user)
                
                inventory_pg = InventoryPage(self.driver)
                inventory_pg.select_sort_option("za")
                
                actual_names = inventory_pg.get_all_product_names()
                expected_names = sorted(actual_names, reverse=True)
                
                self.assertEqual(actual_names, expected_names, f"Sorting Z-A gagal pada user: {user}")

    def test_sort_low_to_high(self):
        """TC 6: Memastikan Sortir Harga Rendah-Tinggi berfungsi"""
        
        users_to_test = ['valid', 'problem', 'glitch']
        
        for user in users_to_test:
            with self.subTest(user=user):
                self._login_as(user)
                
                inventory_pg = InventoryPage(self.driver)
                inventory_pg.select_sort_option("lohi")
                
                actual_prices = inventory_pg.get_all_product_prices()
                expected_prices = sorted(actual_prices)
                
                self.assertEqual(actual_prices, expected_prices, f"Sorting Lo-Hi gagal pada user: {user}")

    def test_product_images_validity(self):
        """TC 8: Memastikan gambar produk tampil benar (kecuali problem_user)"""
        
        users_to_test = ['valid', 'problem', 'glitch']
        
        for user in users_to_test:
            with self.subTest(user=user):
                self._login_as(user)
                
                inventory_pg = InventoryPage(self.driver)
                images = inventory_pg.get_all_images()
                
                for img in images:
                    src = img.get_attribute("src")
                    
                    self.assertTrue(len(src) > 0, "Source gambar ditemukan kosong")
                    
                    
                    if user != 'problem':
                        self.assertNotIn("sl-404", src, f"Bug! Gambar rusak ditemukan pada user: {user}")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()