# My First QA Automation Project (Swag Labs) 🚀

![Python](https://img.shields.io/badge/Python-Learning-blue) ![Selenium](https://img.shields.io/badge/Selenium-4.0-green)

## 👋 About This Project
Hi! This repository represents **my very first step** into the world of QA Automation. 

I built this project to practice and understand the fundamentals of Automation Testing using **Python** and **Selenium**. The main goal was to move away from manual testing and learn how to create scripts that can run automatically.

I used the **Swag Labs (SauceDemo)** website as a playground to implement what I have learned.

## 🎯 Learning Objectives
In this project, I challenged myself to learn and apply these concepts:
* **Page Object Model (POM):** Learning how to separate test scripts from page locators to keep the code clean.
* **Explicit Waits:** Replacing `time.sleep` with `WebDriverWait` to make tests more stable.
* **Debugging:** Learning how to handle errors and take screenshots automatically when a test fails.
* **Code Structure:** Organizing files into folders like `pages` and `tests`.

## 📂 What I Have Automated
I created test scripts for the following flows:
1.  **Login:** Testing valid login, locked out user, and handling empty inputs.
2.  **Inventory:** Checking product sorting logic (Z-A, Low-High) and detecting broken images.
3.  **Cart:** Verifying adding/removing items.
4.  **Checkout:** Simulating the checkout process (End-to-End) and handling form validation.

## 🛠️ Tools I Used
* Python 3.x
* Selenium WebDriver
* Unittest (Standard Python Framework)
* Webdriver Manager (To manage browser drivers automatically)

## 🐛 Bug Reports (My Findings)
While practicing, I found some interesting bugs on the website (specifically for the `problem_user` account) and documented them.

* **My Bug Report & Test Cases:** [Click Here to View Google Spreadsheet](https://docs.google.com/spreadsheets/d/1ACtsSF-WBGNWV4-9-RjW_DWsdsCSFnK7x_0piC95tmQ/edit?usp=sharing)

## 📸 How to Run My Code

1.  **Clone this repository:**
    ```bash
    git clone [https://github.com/fadhild22/SwagLabs_Automation.git](https://github.com/fadhild22/SwagLabs_Automation.git)
    ```

2.  **Install requirements:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the tests:**
    ```bash
    python -m unittest discover tests -v
    ```

---
**Created by:** Fadhil
*A Junior QA Enthusiast looking for opportunities to learn and grow.*