from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    # --- LOCATORS ---
    # Step 1: Form Input
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")

    # Step 2: Halaman Overview
    FINISH_BTN = (By.ID, "finish")

    # Step 3: Halaman Complete (Sukses)
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header") # Tulisannya: "Thank you for your order!"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- ACTIONS ---
    
    def input_information(self, first, last, postal):
        """Mengisi form data diri di Step 1"""
        first_name_field = self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME))
        first_name_field.clear()
        first_name_field.send_keys(first)
        
        last_name_field = self.wait.until(EC.visibility_of_element_located(self.LAST_NAME))
        last_name_field.clear()
        last_name_field.send_keys(last)
        
        postal_code_field = self.wait.until(EC.visibility_of_element_located(self.POSTAL_CODE))
        postal_code_field.clear()
        postal_code_field.send_keys(postal)
        

    def click_continue(self):
        """Klik tombol Continue untuk ke Step 2"""
        self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BTN)).click()

    def click_finish(self):
        """Klik tombol Finish di Step 2"""
        self.wait.until(EC.element_to_be_clickable(self.FINISH_BTN)).click()

    def get_success_message(self):
        """Mengambil pesan sukses di Step 3"""
        return self.wait.until(EC.visibility_of_element_located(self.COMPLETE_HEADER)).text