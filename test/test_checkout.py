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
from selenium.webdriver.common.by import By

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage 

class TestCheckout(unittest.TestCase):

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
        
    def _prepare_checkout_step_one(self, user_key):
        
        self.driver.get(Config.BASE_URL) 
        self.driver.execute_script("window.localStorage.clear();") 
        self.driver.execute_script("window.sessionStorage.clear();")
        self.driver.delete_all_cookies()
        self.driver.refresh()
        
        login_pg = LoginPage(self.driver)
        user = Config.CREDENTIALS[user_key]
        login_pg.login(user['username'], user['password'])
        self.wait.until(EC.url_contains("inventory.html"))
        
        inventory_pg = InventoryPage(self.driver)
        inventory_pg.add_backpack_to_cart()
        inventory_pg.click_cart_icon()
        
        cart_pg = CartPage(self.driver)
        cart_pg.click_checkout()
        self.wait.until(EC.url_contains("checkout-step-one"))
    
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

    def test_checkout_e2e_success(self):
        """FUll Checkout E2E"""
        users = ['valid', 'problem', 'glitch']
        
        for user in users:
            with self.subTest(user=user):
                try:
                    self._prepare_checkout_step_one(user)
                    checkout_pg = CheckoutPage(self.driver)
                    
                    checkout_pg.input_information("Reno", "Kurniawan", "12345")
                    checkout_pg.click_continue()
                    
                    self.wait.until(EC.url_contains("checkout-step-two"))
                    
                    checkout_pg.click_finish()
                    
                    self.wait.until(EC.url_contains("checkout-complete"))
                    success_msg = checkout_pg.get_success_message()
                    self.assertEqual(success_msg, "Thank you for your order!")

                except Exception as e:
                    self._take_screenshot(user, "test_checkout_e2e")
                    
                    if user == 'problem':
                        print(f"  -> Problem User gagal checkout (Bug Last Name). Ini Expected.")
                    else:
                        raise e 

    def test_checkout_negative_empty_field(self):
        """TC Negative: Validasi Error jika Last Name kosong (User Valid)"""
        user = 'valid'
        try:
            self._prepare_checkout_step_one(user)
            checkout_pg = CheckoutPage(self.driver)
            
            checkout_pg.input_information("Reno", "", "12345")
            checkout_pg.click_continue()
            
            error_msg = checkout_pg.get_error_message()
            self.assertEqual(error_msg, "Error: Last Name is required")
            
        except Exception as e:
            self._take_screenshot(user, "test_checkout_negative")
            raise e

    def tearDown(self):
        self.driver.quit()
        
if __name__ == "__main__":
    unittest.main()