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
        problem_list.append(formatted_problem)
    
    return problem_list

# Main scraping function
def scrape_problems():
    driver = get_driver()
    all_problems = []
    page_num = 1  # Start from the first page

    while True:  # Keep scraping until an empty page is found
        problems = get_problems_from_page(driver, page_num)  # Pass the driver as an argument
        if not problems:
            print(f"No problems found on page {page_num}. Stopping.")
            break  # Stop if no problems are found on a page
        all_problems.extend(problems)
        print(f"Scraped page {page_num}...")
        page_num += 1

    driver.quit()
    
    # Save problems to file
    with open('problemList.txt', 'w', encoding='utf-8') as file:
        for problem in all_problems:
            file.write(problem + '\n')
    
    print("Problem list saved to problemList.txt.")

if __name__ == "__main__":
    scrape_problems()
