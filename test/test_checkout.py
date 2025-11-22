import sys
import os
import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

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
        
        
        login_pg = LoginPage(self.driver)
        login_pg.open_page(Config.BASE_URL)
        login_pg.login(Config.CREDENTIALS['valid']['username'], Config.CREDENTIALS['valid']['password'])
        
        inventory_pg = InventoryPage(self.driver)
        inventory_pg.add_backpack_to_cart()
        inventory_pg.click_cart_icon()
        
        # CLICK CHECKOUT (Masuk ke halaman pengisian data)
        cart_pg = CartPage(self.driver)
        cart_pg.click_checkout()
        time.sleep(3)

    def test_checkout_success(self):
        """Test Full Flow Checkout sampai sukses"""
        time.sleep(5)
        checkout_pg = CheckoutPage(self.driver)
        
        # Isi Form (Step One)
        checkout_pg.input_information("Reno", "Kurniawan", "23231")
        time.sleep(2)
        checkout_pg.click_continue()
        
        # Validasi URL pindah ke step-two
        time.sleep(3)
        self.assertIn("checkout-step-two", self.driver.current_url)
        
        checkout_pg.click_finish()
        
        # 3. Validation
        actual_msg = checkout_pg.get_success_message()
        self.assertEqual(actual_msg, "Thank you for your order!")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()