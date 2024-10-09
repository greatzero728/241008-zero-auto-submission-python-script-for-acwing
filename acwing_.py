import os
import traceback
import time
import pyperclip
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv

load_dotenv()
ACWING_USERNAME = os.getenv("ACWING_USERNAME")
ACWING_PASSWORD = os.getenv("ACWING_PASSWORD")
WAIT_TIME = int(os.getenv("WAIT_TIME"))

driver = None

def init_driver():
    """Initialize the Firefox WebDriver in incognito mode."""
    global driver
    if driver is None:
        options = Options()
        options.add_argument("--private")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("window-size=1200x600")

        driver = webdriver.Firefox(options=options)
        driver.maximize_window()

def login(acwingHandle=ACWING_USERNAME, acwingPassword=ACWING_PASSWORD):
    """Log in to acwing.com using the provided or default credentials."""
    init_driver()
    driver.get("https://www.acwing.com/problem/")

    try:
        login_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-target="#login-modal"]'))
        )
        login_button.click()

        WebDriverWait(driver, WAIT_TIME).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'modal-dialog'))
        )

        username_input = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        password_input = driver.find_element(By.NAME, 'password')

        username_input.send_keys(acwingHandle)
        password_input.send_keys(acwingPassword)
        password_input.send_keys(Keys.RETURN)

        time.sleep(5)
        print("Login successful.")
        return True
    except Exception as e:
        print(f"Error during login: {e}")
        return False

def load_valid_problems():
    """Load valid problems from a JSON file."""
    with open('validProblems.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def submit(problem, code):
    """Submit the code to a specific problem and return the submission ID."""
    try:
        submission_url = problem['url']
        driver.get(submission_url)
        print(f"Opened problem URL: {submission_url}")

        driver.refresh()
        time.sleep(2)

        # Scroll to the code input area
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Target the code editor div and paste the code into it
        code_input_area = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div[1]/div/div/div/div[4]/div[2]/div/div[3]'))
        )

        # Copy the code to the clipboard
        pyperclip.copy(code)

        # Move to the code input area, click it, and perform Ctrl+V
        actions = ActionChains(driver)
        actions.move_to_element(code_input_area).click().key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        time.sleep(1)
        print("Code input successful.")

        # Now click the submit button using CSS selector
        submit_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#submit_code_btn'))
        )
        submit_button.click()

        time.sleep(3)
        print("Code submitted successfully.")

        # Navigate to the submission page
        submission_url = submission_url.replace('/content/', '/content/submission/')
        driver.get(submission_url)
        print(f"Opened submission URL: {submission_url}")

        # Wait for the page to load and extract the submission ID
        submission_link = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)"))
        )

        href = submission_link.get_attribute("href")
        print(f"Found href: {href}")

        # Extract the submission_id from the href string
        submission_id = href.split('/')[-2]
        print(f"Submission ID: {submission_id}")

        return submission_id
    except Exception as e:
        print(f"Error while trying to submit the code: {e}")
        traceback.print_exc()  # Print full stack trace for better debugging
        return None

def get_status(submission_id):
    """Check the status of a specific submission using the submission_id."""
    try:
        # Construct the URL for the submission details page
        status_url = f"https://www.acwing.com/problem/content/submission/code_detail/{submission_id}/"
        driver.get(status_url)
        print(f"Opened status URL: {status_url}")

        # Wait for the page to load and find the result element by its ID: #submission-result
        result_element = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#submission-result"))
        )

        # Extract and return the submission result text (e.g., Pending, Accepted, Wrong Answer)
        submission_status = result_element.text
        print(f"Submission status: {submission_status}")
        return submission_status
    except Exception as e:
        print(f"Error while checking the submission status: {e}")
        traceback.print_exc()
        return None

class acwingSubmitter:
    def __init__(self):
        self.problems = load_valid_problems()
        login()

    def submit(self, problem_id, code):
        problem = next((p for p in self.problems if p['id'] == problem_id), None)
        if problem is None:
            print(f"Problem with ID {problem_id} not found.")
            raise
        return submit(problem, code)

    def get_result(self, problem_id, submission_id):
        return get_status(submission_id)
    
if __name__ == "__main__":
    a = acwingSubmitter()
    sid = a.submit(1, "#include<iostream>\nusing namespace std;\nint main() {\n    int x, y;\n    cin >> x >> y;\n    cout << x + y;\n}")
    print(sid)
    
    print(a.get_result(1, sid))
    time.sleep(5)
    print(a.get_result(1, sid))

    b = acwingSubmitter()
    sid = b.submit(5981, "#include<iostream>\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\n//I love acade\n//I want to work in acade project\nusing namespace std;\nint main() {\n    int x, y;\n    cin >> x >> y;\n    cout << x + y;\n}")
    print(sid)
    
    print(b.get_result(5981, sid))
    time.sleep(5)
    print(b.get_result(5981, sid))