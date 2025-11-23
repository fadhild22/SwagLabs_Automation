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

# Import Config & Page Object
from config import Config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

class TestLogin(unittest.TestCase):

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

    #Scenario Positive
    def test_01_login_standard_user(self):
        """Login menggunakan Standard User (Valid)"""
        login_page = LoginPage(self.driver)
        login_page.open_page(Config.BASE_URL)

        user = Config.CREDENTIALS['valid']
        login_page.login(user['username'], user['password'])

        self.wait.until(EC.url_contains("inventory.html"))
        self.assertIn("inventory.html", self.driver.current_url)
    
    def test_02_login_problem_user(self):
        """
        Login menggunakan Problem User.
        User ini loginnya sukses, tapi tampilan di dalamnya rusak.
        """
        login_page = LoginPage(self.driver)
        login_page.open_page(Config.BASE_URL)

        user = Config.CREDENTIALS['problem']
        login_page.login(user['username'], user['password'])

        self.wait.until(EC.url_contains("inventory.html"))
        self.assertIn("inventory.html", self.driver.current_url)
    
    def test_03_login_performance_glitch_user(self):
        """
        Login menggunakan Performance Glitch User.
        """
        login_page = LoginPage(self.driver)
        login_page.open_page(Config.BASE_URL)

        user = Config.CREDENTIALS['glitch']
        login_page.login(user['username'], user['password'])

        self.wait.until(EC.url_contains("inventory.html"))
        self.assertIn("inventory.html", self.driver.current_url)
    
    #Scenario Negative
    def test_04_login_locked_out_user(self):
        """Login menggunakan User Terkunci"""
        login_page = LoginPage(self.driver)
        login_page.open_page(Config.BASE_URL)

        user = Config.CREDENTIALS['locked']
        login_page.login(user['username'], user['password'])

        expected_error = "Epic sadface: Sorry, this user has been locked out."
        self.assertEqual(login_page.get_error_message(), expected_error)
    
    def test_05_login_empty_username(self):
        """
        Login dengan Username Kosong.
        """
        login_page = LoginPage(self.driver)
        login_page.open_page(Config.BASE_URL)

        user = Config.CREDENTIALS['invalid_user']
        login_page.login(user['username'], user['password'])

        expected_error = "Epic sadface: Username is required"
        self.assertEqual(login_page.get_error_message(), expected_error)
    
    def test_06_login_empty_password(self):
        """
        Login dengan Password Kosong.
        """
        login_page = LoginPage(self.driver)
        login_page.open_page(Config.BASE_URL)

        user = Config.CREDENTIALS['invalid_pass']
        login_page.login(user['username'], user['password'])

        expected_error = "Epic sadface: Password is required"
        self.assertEqual(login_page.get_error_message(), expected_error)
    
    def test_07_login_empty_user(self):
        """
        Login dengan Username & Password Kosong.
        """
        login_page = LoginPage(self.driver)
        login_page.open_page(Config.BASE_URL)

        user = Config.CREDENTIALS['empty_user']
        login_page.login(user['username'], user['password'])

        expected_error = "Epic sadface: Username is required"
        self.assertEqual(login_page.get_error_message(), expected_error)
    
    #Fungsi Logout
    def test_08_logout_success(self):
        """
        Cek fitur Logout untuk tipe user valid (Standard, Problem, Glitch).
        """
        
        valid_users = ['valid', 'problem', 'glitch']
        
        for user_key in valid_users:
            
            with self.subTest(user=user_key):
                
                login_page = LoginPage(self.driver)
                login_page.open_page(Config.BASE_URL)
                
                current_user = Config.CREDENTIALS[user_key]
                login_page.login(current_user['username'], current_user['password'])
                
                self.wait.until(EC.url_contains("inventory.html"))
                
                inventory_page = InventoryPage(self.driver)
                inventory_page.click_burger_menu()
                inventory_page.click_logout()
                
                self.wait.until(EC.url_to_be(Config.BASE_URL))
                
                self.assertEqual(self.driver.current_url, Config.BASE_URL)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()