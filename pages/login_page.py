from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    # LOCATE BY ID
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    
    # Locator error message
    ERROR_MSG = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ACTIONS (What user can do)
    def open_page(self, url):
        self.driver.get(url)

    def input_username(self, username):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_FIELD)).send_keys(username)

    def input_password(self, password):
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD)).send_keys(password)

    def click_login(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BTN)).click()

    # Fungsi gabungan test case
    def login(self, username, password):
        self.input_username(username)
        self.input_password(password)
        self.click_login()

    def get_error_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.ERROR_MSG)).text