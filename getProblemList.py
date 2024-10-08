from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

# Set up Firefox in incognito mode
def get_driver():
    options = Options()
    options.add_argument("-private")  # incognito mode
    driver = webdriver.Firefox(options=options)
    return driver

# Function to get the problems from a specific page
def get_problems_from_page(driver, page_number):
    url = f"https://www.acwing.com/problem/{page_number}/"
    driver.get(url)
    time.sleep(3)  # Wait for the page to load

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    problems = soup.find_all('a', {'id': lambda x: x and x.startswith('problem-title-')})
    
    problem_list = []
    for problem in problems:
        problem_title = problem.text.strip()
        problem_url = "https://www.acwing.com" + problem['href']
        formatted_problem = f"Please transcribe and solve problem <b>{problem_title}</b> from <b>acwing</b>. Problem statement is here: {problem_url}"
        problem_list.append((problem_url, formatted_problem))
    
    return problem_list

# Function to check the number of div elements within the "root" div
def check_problem_validity(driver, problem_url, formatted_problem, valid_problems, invalid_problems):
    driver.get(problem_url)
    time.sleep(1)  # Wait for the page to load
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find the "root" div using the CSS path provided
    root_div = soup.select_one('html body#acwing_body div#acwing_page div.base_body div.container div.panel.panel-default div.panel-body div#code_editor.ace_editor.ace-tm div.ace_gutter div.ace_layer.ace_gutter-layer.ace_folding-enabled')
    
    if root_div:
        # Count the number of child divs
        line_number = len(root_div.find_all('div'))
        
        # Add to appropriate set based on the line number
        if line_number == 1:
            valid_problems.add(formatted_problem)
        else:
            invalid_problems.add(formatted_problem)
    else:
        print(f"Skipping problem at {problem_url} as the root div was not found.")

# Main scraping function
def scrape_problems():
    driver = get_driver()
    page_num = 1  # Start from the first page

    valid_problems = set()
    invalid_problems = set()

    while True:  # Keep scraping until an empty page is found
        problems = get_problems_from_page(driver, page_num)  # Pass the driver as an argument
        if not problems:
            print(f"No problems found on page {page_num}. Stopping.")
            break  # Stop if no problems are found on a page
        
        for problem_url, formatted_problem in problems:
            check_problem_validity(driver, problem_url, formatted_problem, valid_problems, invalid_problems)
        
        print(f"Scraped page {page_num}...")
        page_num += 1

    driver.quit()

    # Sort and save problems to files
    with open('validProblem.txt', 'w', encoding='utf-8') as valid_file:
        for problem in sorted(valid_problems):
            valid_file.write(problem + '\n')
    
    with open('invalidProblem.txt', 'w', encoding='utf-8') as invalid_file:
        for problem in sorted(invalid_problems):
            invalid_file.write(problem + '\n')

    print("Problem scraping complete and saved to files.")

if __name__ == "__main__":
    scrape_problems()
