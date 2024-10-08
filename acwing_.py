import os
import traceback
import threading
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()
ACWING_USERNAME = os.getenv("ACWING_USERNAME")
ACWING_PASSWORD = os.getenv("ACWING_PASSWORD")

driver = None

def init_driver():
    """Initialize the Firefox WebDriver in incognito mode."""
    global driver
    if driver is None:
        options = Options()
        options.add_argument("--private")  # Firefox incognito mode
        # options.add_argument("--headless")  # Run in headless mode (optional, remove for debugging)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("window-size=1200x600")

        driver = webdriver.Firefox(options=options)
        driver.maximize_window()  # Maximize the browser window for better element visibility

def login(acwingHandle=ACWING_USERNAME, acwingPassword=ACWING_PASSWORD):
    """Log in to AcWing using the provided or default credentials."""
    init_driver()
    driver.get("https://www.acwing.com/problem/")

    try:
        # Wait for the login button to be clickable and click it
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-target="#login-modal"]'))
        )
        login_button.click()

        # Wait for the login modal to fully appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'login-modal'))
        )

        # Use provided CSS selectors to locate the input fields
        username_selector = 'html body#acwing_body.modal-open div#login-modal.modal.fade.in div.modal-dialog div.modal-content div#div-forms form#login-form.sign-form div.modal-body input#login_username.form-control'
        password_selector = 'html body#acwing_body.modal-open div#login-modal.modal.fade.in div.modal-dialog div.modal-content div#div-forms form#login-form.sign-form div.modal-body input#login_password.form-control'
        submit_selector = 'html body#acwing_body.modal-open div#login-modal.modal.fade.in div.modal-dialog div.modal-content div#div-forms form#login-form.sign-form div.modal-footer div button.btn.btn-primary.btn-lg.btn-block'

        # Wait for username input to be visible
        username_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, username_selector))
        )
        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, password_selector))
        )

        # Enter username and password
        username_input.send_keys(acwingHandle)
        password_input.send_keys(acwingPassword)

        # Wait until the submit button is clickable and click it
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, submit_selector))
        )

        # Use JavaScript to click the submit button
        driver.execute_script("arguments[0].click();", submit_button)

        print("Logged in successfully. The browser will remain open.")
        wait_for_exit()  # Wait for user input to close the browser

    except WebDriverException as we:
        print(f"Selenium WebDriverException occurred: {we}")
        traceback.print_exc()  # Print the full stack trace for more context

    except TimeoutException as te:
        print(f"TimeoutException: {te}")
        traceback.print_exc()  # Print the full stack trace for timeout errors

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()  # Print the full stack trace for general exceptions

def wait_for_exit():
    """Keep the browser open until the user inputs any text in the command line."""
    input("Type anything to close the browser...\n")
    if driver is not None:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    login()
