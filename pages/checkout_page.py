import time

from selenium.webdriver.common.by import By

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

    # --- ACTIONS ---
    
    def input_information(self, first, last, postal):
        """Mengisi form data diri di Step 1"""
        self.driver.find_element(*self.FIRST_NAME).click()
        self.driver.find_element(*self.FIRST_NAME).clear()
        self.driver.find_element(*self.FIRST_NAME).send_keys(first)
        time.sleep(0.5)
        
        self.driver.find_element(*self.LAST_NAME).click()
        self.driver.find_element(*self.LAST_NAME).clear()
        self.driver.find_element(*self.LAST_NAME).send_keys(last)
        time.sleep(0.5)
        
        self.driver.find_element(*self.POSTAL_CODE).click()
        self.driver.find_element(*self.POSTAL_CODE).clear()
        self.driver.find_element(*self.POSTAL_CODE).send_keys(postal)
        time.sleep(0.5)

    def click_continue(self):
        """Klik tombol Continue untuk ke Step 2"""
        self.driver.find_element(*self.CONTINUE_BTN).click()

    def click_finish(self):
        """Klik tombol Finish di Step 2"""
        self.driver.find_element(*self.FINISH_BTN).click()

    def get_success_message(self):
        """Mengambil pesan sukses di Step 3"""
        return self.driver.find_element(*self.COMPLETE_HEADER).text