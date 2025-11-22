import sys 
import os

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Import file diluar folder test/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Config & Page Object
from config import Config
from pages.login_page import LoginPage

class TestLogin(unittest.TestCase):

    def setUp(self):
        # Seting up ChromeDriver
        options = Options()
        options.add_experimental_option("detach", True) 
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()

    def test_login_success(self):
        
        login_page = LoginPage(self.driver)

        login_page.open_page(Config.BASE_URL)

        # 3. Login based on config library
        login_page.login(Config.CREDENTIALS['valid']['username'], Config.CREDENTIALS['valid']['password'])

        # 4. Validation
        # if login success, user will be directed to inventory page
        self.assertIn("inventory.html", self.driver.current_url)

    def test_login_failed_locked_user(self):
        login_page = LoginPage(self.driver)
        login_page.open_page(Config.BASE_URL)
        
        # Login as locked user
        login_page.login(Config.CREDENTIALS['locked']['username'], Config.CREDENTIALS['locked']['password'])
        
        # Validation Error Message
        expected_error = "Epic sadface: Sorry, this user has been locked out."
        self.assertEqual(login_page.get_error_message(), expected_error)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()