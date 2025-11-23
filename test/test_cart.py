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
        login_pg = LoginPage(self.driver)
        login_pg.open_page(Config.BASE_URL)
        self.driver.delete_all_cookies()
        self.driver.execute_script("window.localStorage.clear();") 
        self.driver.execute_script("window.sessionStorage.clear();")
        self.driver.refresh()
        user = Config.CREDENTIALS[user_key]
        login_pg.login(user['username'], user['password'])
        self.wait.until(EC.url_contains("inventory.html"))
    
    def test_inventory_interactions(self):
        """Test Inventory)"""
        users = ['valid', 'problem', 'glitch']
        
        for user in users:
            with self.subTest(user=user):
                self._login_as(user)
                inventory_pg = InventoryPage(self.driver)
                
                inventory_pg.add_backpack_to_cart()
                
                
                self.assertEqual(inventory_pg.get_cart_badge_number(), "1", f"Badge Error pada {user}")
                
                self.assertTrue(inventory_pg.is_remove_button_visible(), f"Tombol Remove Error pada {user}")
                
                inventory_pg.click_first_item_name()
                
                detail_pg = ItemDetailPage(self.driver)
                self.wait.until(EC.url_contains("inventory-item.html"))
                self.assertTrue(len(detail_pg.get_item_name()) > 0)
                
                detail_pg.click_back_to_products()
                self.wait.until(EC.url_contains("inventory.html"))

    def test_cart_page_operations(self):
        """Test Cart)"""
        users = ['valid', 'problem', 'glitch']
        
        for user in users:
            with self.subTest(user=user):
                self._login_as(user)
                inventory_pg = InventoryPage(self.driver)
                cart_pg = CartPage(self.driver)
                
                inventory_pg.add_backpack_to_cart()
                inventory_pg.click_cart_icon()
                self.wait.until(EC.url_contains("cart.html"))
                
                self.assertEqual(cart_pg.get_item_name(), "Sauce Labs Backpack")
                
                cart_pg.click_continue_shopping()
                self.wait.until(EC.url_contains("inventory.html"))
                
                inventory_pg.click_cart_icon()
                
                cart_pg.click_remove_item()
                self.assertFalse(cart_pg.is_item_displayed(), f"Remove gagal pada {user}")

    def tearDown(self):
        if hasattr(self, '_outcome'):
            result = self._outcome.result
            if result.errors or result.failures:
                all_problems = result.errors + result.failures
                if any(test == self for test, error_msg in all_problems):
                    if not os.path.exists("screenshots"):
                        os.makedirs("screenshots")
                    
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    test_name = self._testMethodName
                    filename = f"screenshots/{test_name}_{timestamp}.png"
                    
                    try:
                        self.driver.save_screenshot(filename)
                        print(f"\n Screenshot Error Saved IN: {filename}")
                    except Exception as e:
                        print(f"Failed to take screenshot: {e}")
        
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)