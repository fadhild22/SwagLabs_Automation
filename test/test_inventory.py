import sys
import os
import unittest
import datetime

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
    
    def _take_screenshot(self, user_key, test_name):
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        filename = f"screenshots/{test_name}_{user_key}_{timestamp}.png"
        
        try:
            self.driver.save_screenshot(filename)
            print(f"\n Screenshot Error  '{user_key}' Saved IN: {filename}")
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
        
    def test_sort_z_to_a(self):
        """SL_TC_009: Sortir Z-A"""
        users_to_test = ['valid', 'problem', 'glitch']
        for user in users_to_test:
            with self.subTest(user=user):
                try:
                    self._login_as(user)
                    inventory_pg = InventoryPage(self.driver)
                    
                    # Pilih Z to A
                    inventory_pg.select_sort_option("za")
                    
                    actual = inventory_pg.get_all_product_names()
                    expected = sorted(actual, reverse=True) # Z-A
                    
                    self.assertEqual(actual, expected, f"Sorting Z-A gagal pada user: {user}")
                except Exception as e:
                    self._take_screenshot(user, "test_sort_z_to_a")
                    raise e

    def test_sort_a_to_z(self):
        """SL_TC_010: Sortir A-Z"""
        users_to_test = ['valid', 'problem', 'glitch']
        for user in users_to_test:
            with self.subTest(user=user):
                try:
                    self._login_as(user)
                    inventory_pg = InventoryPage(self.driver)
                    
                    # Trik: Pilih Z-A dulu, baru A-Z (biar kelihatan berubah)
                    inventory_pg.select_sort_option("za")
                    inventory_pg.select_sort_option("az")
                    
                    actual = inventory_pg.get_all_product_names()
                    expected = sorted(actual) # A-Z (Default)
                    
                    self.assertEqual(actual, expected, f"Sorting A-Z gagal pada user: {user}")
                except Exception as e:
                    self._take_screenshot(user, "test_sort_a_to_z")
                    raise e

    def test_sort_low_to_high(self):
        """SL_TC_011: Sortir Harga Rendah-Tinggi"""
        users_to_test = ['valid', 'problem', 'glitch']
        for user in users_to_test:
            with self.subTest(user=user):
                try:
                    self._login_as(user)
                    inventory_pg = InventoryPage(self.driver)
                    
                    # Pilih Low to High
                    inventory_pg.select_sort_option("lohi")
                    
                    actual = inventory_pg.get_all_product_prices()
                    expected = sorted(actual) # Kecil ke Besar
                    
                    self.assertEqual(actual, expected, f"Sorting Lo-Hi gagal pada user: {user}")
                except Exception as e:
                    self._take_screenshot(user, "test_sort_low_to_high")
                    raise e

    def test_sort_high_to_low(self):
        """SL_TC_012: Sortir Harga Tinggi-Rendah"""
        users_to_test = ['valid', 'problem', 'glitch']
        for user in users_to_test:
            with self.subTest(user=user):
                try:
                    self._login_as(user)
                    inventory_pg = InventoryPage(self.driver)
                    
                    # Pilih High to Low
                    inventory_pg.select_sort_option("hilo")
                    
                    actual = inventory_pg.get_all_product_prices()
                    expected = sorted(actual, reverse=True) # Besar ke Kecil
                    
                    self.assertEqual(actual, expected, f"Sorting Hi-Lo gagal pada user: {user}")
                except Exception as e:
                    self._take_screenshot(user, "test_sort_high_to_low")
                    raise e

    def test_product_images_validity(self):
        """SL_TC_013: Memastikan gambar produk tampil benar (kecuali problem_user)"""
        
        users_to_test = ['valid', 'problem', 'glitch']
        
        for user in users_to_test:
            with self.subTest(user=user):
                try:
                    self._login_as(user)
                    inventory_pg = InventoryPage(self.driver)
                    images = inventory_pg.get_all_images()
                    
                    for img in images:
                        src = img.get_attribute("src")
                        self.assertTrue(len(src) > 0, "Source kosong")
                        
                        if user != 'problem':
                            self.assertNotIn("sl-404", src, f"Gambar rusak pada {user}")
                            
                except Exception as e:
                    self._take_screenshot(user, "test_images")
                    raise e

    def tearDown(self):
        
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()