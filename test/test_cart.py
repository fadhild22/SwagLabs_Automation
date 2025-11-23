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
        
        self.driver.get(Config.BASE_URL) 
        self.driver.execute_script("window.localStorage.clear();") 
        self.driver.execute_script("window.sessionStorage.clear();")
        self.driver.delete_all_cookies()
        self.driver.refresh()
        
        login_pg = LoginPage(self.driver)
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


    def test_inventory_interactions(self):
        """SL_TC_018 - SL_TC_020 & SL_TC_023: Interaksi Inventory & Detail"""
        users = ['valid', 'problem', 'glitch']
        
        for user in users:
            with self.subTest(user=user):
                try:
                    self._login_as(user)
                    inventory_pg = InventoryPage(self.driver)
                    
                    # TC 18 & 19
                    inventory_pg.add_backpack_to_cart()
                    self.assertEqual(inventory_pg.get_cart_badge_number(), "1", f"Badge Error pada {user}")
                    self.assertTrue(inventory_pg.is_remove_button_visible(), f"Tombol Remove Error pada {user}")
                    
                    # TC 20 & 23
                    inventory_pg.click_first_item_name()
                    detail_pg = ItemDetailPage(self.driver)
                    self.wait.until(EC.url_contains("inventory-item.html"))
                    
                    
                    item_name = detail_pg.get_item_name()
                    self.assertTrue(len(item_name) > 0)
                    
                    detail_pg.click_back_to_products()
                    self.wait.until(EC.url_contains("inventory.html"))

                except Exception as e:
                    self._take_screenshot(user, "test_inventory_interactions")
                    raise e

    def test_cart_page_operations(self):
        """SL_TC_021 - SL_TC_022 & SL_TC_024 - SL_TC_025: Operasi Cart"""
        users = ['valid', 'problem', 'glitch']
        
        for user in users:
            with self.subTest(user=user):
                try:
                    self._login_as(user)
                    inventory_pg = InventoryPage(self.driver)
                    cart_pg = CartPage(self.driver)
                    
                    inventory_pg.add_backpack_to_cart()
                    inventory_pg.click_cart_icon()
                    self.wait.until(EC.url_contains("cart.html"))
                    
                    # TC 21
                    self.assertEqual(cart_pg.get_item_name(), "Sauce Labs Backpack")
                    
                    # TC 24 (Continue Shopping)
                    cart_pg.click_continue_shopping()
                    self.wait.until(EC.url_contains("inventory.html"))
                    inventory_pg.click_cart_icon() 
                    
                    # TC 25 cuma cek visible
                    
                    # TC 22 (Remove Item)
                    cart_pg.click_remove_item()
                    # Validasi item hilang
                    self.assertFalse(cart_pg.is_item_displayed(), f"Remove gagal pada {user}")

                except Exception as e:
                    self._take_screenshot(user, "test_cart_page_operations")
                    raise e

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)