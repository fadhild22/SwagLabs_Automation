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
from pages.item_detail_page import ItemDetailPage  

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
        
    def _login_as(self, user_key):
        self.driver.delete_all_cookies()
        login_pg = LoginPage(self.driver)
        login_pg.open_page(Config.BASE_URL)
        user = Config.CREDENTIALS[user_key]
        login_pg.login(user['username'], user['password'])
        self.wait.until(EC.url_contains("inventory.html"))
    
    def test_inventory_interactions(self):
        """Test TC 1, 2, 3, 6 (Interaksi sebelum masuk Cart)"""
        users = ['valid', 'problem', 'glitch']
        
        for user in users:
            with self.subTest(user=user):
                self._login_as(user)
                inventory_pg = InventoryPage(self.driver)
                
                # TC 1 & 2: Add Item & Cek Tampilan
                inventory_pg.add_backpack_to_cart()
                
                # Validasi Badge (TC 1)
                self.assertEqual(inventory_pg.get_cart_badge_number(), "1", f"Badge Error pada {user}")
                # Validasi Tombol Remove (TC 2)
                self.assertTrue(inventory_pg.is_remove_button_visible(), f"Tombol Remove Error pada {user}")
                
                # TC 3: Full Product View
                inventory_pg.click_first_item_name()
                
                # Validasi Masuk Detail (TC 3)
                detail_pg = ItemDetailPage(self.driver)
                self.wait.until(EC.url_contains("inventory-item.html"))
                self.assertTrue(len(detail_pg.get_item_name()) > 0)
                
                # TC 6: Back to Products
                detail_pg.click_back_to_products()
                self.wait.until(EC.url_contains("inventory.html"))

    def test_cart_page_operations(self):
        """Test TC 4, 5, 7 (Operasi di dalam Cart)"""
        users = ['valid', 'problem', 'glitch']
        
        for user in users:
            with self.subTest(user=user):
                self._login_as(user)
                inventory_pg = InventoryPage(self.driver)
                cart_pg = CartPage(self.driver)
                
                # Pre-condition: Beli barang dulu
                inventory_pg.add_backpack_to_cart()
                inventory_pg.click_cart_icon()
                self.wait.until(EC.url_contains("cart.html"))
                
                # TC 4: Cek Item Tampil
                self.assertEqual(cart_pg.get_item_name(), "Sauce Labs Backpack")
                
                # TC 7: Continue Shopping
                cart_pg.click_continue_shopping()
                self.wait.until(EC.url_contains("inventory.html"))
                
                # Balik lagi ke Cart untuk tes Remove
                inventory_pg.click_cart_icon()
                
                # TC 5: Remove Item
                cart_pg.click_remove_item()
                self.assertFalse(cart_pg.is_item_displayed(), f"Remove gagal pada {user}")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)