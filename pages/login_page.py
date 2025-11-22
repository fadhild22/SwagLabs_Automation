from selenium.webdriver.common.by import By

class LoginPage:
    # LOCATE BY ID
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    
    # Locator error message
    ERROR_MSG = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        self.driver = driver

    # ACTIONS (What user can do)
    
    def open_page(self, url):
        self.driver.get(url)

    def input_username(self, username):
        self.driver.find_element(*self.USERNAME_FIELD).send_keys(username)

    def input_password(self, password):
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BTN).click()

    # Fungsi gabungan test case
    def login(self, username, password):
        self.input_username(username)
        self.input_password(password)
        self.click_login()

    def get_error_message(self):
        return self.driver.find_element(*self.ERROR_MSG).text