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
        
        login_pg = LoginPage(self.driver)
        login_pg.open_page(Config.BASE_URL)
        login_pg.login(Config.CREDENTIALS['valid']['username'], Config.CREDENTIALS['valid']['password'])
        
        inventory_pg = InventoryPage(self.driver)
        inventory_pg.add_backpack_to_cart()
        inventory_pg.click_cart_icon()
        
        # CLICK CHECKOUT (Masuk ke halaman pengisian data)
        cart_pg = CartPage(self.driver)
        cart_pg.click_checkout()

    def test_checkout_success(self):
        """Test Full Flow Checkout sampai sukses"""
        checkout_pg = CheckoutPage(self.driver)
        
        self.wait.until(EC.visibility_of_element_located((By.ID, "first-name")))
        # Isi Form (Step One)
        checkout_pg.input_information("Reno", "Kurniawan", "23231")
        checkout_pg.click_continue()
        
        self.wait.until(EC.url_contains("checkout-step-two"))
        # Validasi URL pindah ke step-two
        self.assertIn("checkout-step-two", self.driver.current_url)
        
        checkout_pg.click_finish()
        
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "complete-header")))
        # 3. Validation
        actual_msg = checkout_pg.get_success_message()
        self.assertEqual(actual_msg, "Thank you for your order!")

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
    unittest.main()