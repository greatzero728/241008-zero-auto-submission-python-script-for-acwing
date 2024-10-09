from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import json

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
        problem_url = "https://www.acwing.com" + problem['href']
        problem_list.append(problem_url)

    return problem_list

# Function to check problem validity and extract required information
def check_problem_validity(driver, problem_url, valid_problems, invalid_problems):
    driver.get(problem_url)
    time.sleep(1)  # Wait for the page to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the title element
    title_element = soup.select_one('div.nice_font.problem-content-title')
    if title_element:
        full_title = title_element.text.strip()  # Extract the full title, e.g. "11. 背包问题求方案数"
        # Split the title into problem_id and problem_name
        problem_id, problem_name = full_title.split('. ', 1)  # Split on ". " to get both parts
        problem_id = int(problem_id.strip())  # Convert problem_id to an integer
        problem_name = problem_name.strip()   # Clean up problem_name
    else:
        print(f"Problem title not found at {problem_url}")
        return  # Skip if the title is not found

    # Use the specific CSS path to get the tbody
    tbody = soup.select_one('html body#acwing_body div#acwing_page div.base_body div.container div.panel.panel-default div.panel-body div.row div.col-sm-3.hidden-xs div.table-responsive table.table.table-striped.table-responsive tbody')

    if tbody:
        # Find the 3rd <tr> (index 2 in 0-based index)
        tr_elements = tbody.find_all('tr')
        if len(tr_elements) >= 3:
            third_tr = tr_elements[2]  # Select the third <tr>
            
            # Now find the <span> inside the third <tr> with the right float style
            accepted_element = third_tr.find('span', style="float:right;")
            if accepted_element:
                accepted_text = accepted_element.text.strip()
                try:
                    accepted_count = int(accepted_text)  # Convert to integer
                except ValueError:
                    print(f"Non-numeric accepted count ('{accepted_text}') found at {problem_url}, skipping.")
                    return  # Skip this problem if the accepted count is not numeric
            else:
                print(f"Accepted submissions span not found at {problem_url}")
                return  # Skip if the span is not found
        else:
            print(f"Third <tr> not found at {problem_url}, skipping.")
            return
    else:
        print(f"<tbody> not found at {problem_url}, skipping.")
        return  # Skip if the tbody is not found

    # Create the problem JSON object
    problem_data = {
        "id": problem_id,
        "name": problem_name,
        "url": problem_url,
        "accepted": accepted_count
    }

    # Now check the number of div elements within the "root" div for validity
    root_div = soup.select_one('html body#acwing_body div#acwing_page div.base_body div.container div.panel.panel-default div.panel-body div#code_editor.ace_editor.ace-tm div.ace_gutter div.ace_layer.ace_gutter-layer.ace_folding-enabled')

    if root_div:
        line_number = len(root_div.find_all('div'))

        if line_number == 1:
            valid_problems.append(problem_data)  # Add valid problem JSON to list
        else:
            invalid_problems.append(problem_data)  # Add invalid problem JSON to list
    else:
        print(f"Skipping problem at {problem_url} as the root div was not found.")

def scrape_problems():
    driver = get_driver()
    page_num = 1  # Start from the first page

    valid_problems = []
    invalid_problems = []

    while True:  # Keep scraping until an empty page is found
        problems = get_problems_from_page(driver, page_num)  # Pass the driver as an argument
        if not problems:
            print(f"No problems found on page {page_num}. Stopping.")
            break  # Stop if no problems are found on a page

        for problem_url in problems:
            check_problem_validity(driver, problem_url, valid_problems, invalid_problems)
        
        print(f"Scraped page {page_num}...")
        page_num += 1

    driver.quit()

    # Save valid and invalid problems to JSON files
    with open('validProblems.json', 'w', encoding='utf-8') as valid_file:
        json.dump(valid_problems, valid_file, ensure_ascii=False, indent=4)
    
    with open('invalidProblems.json', 'w', encoding='utf-8') as invalid_file:
        json.dump(invalid_problems, invalid_file, ensure_ascii=False, indent=4)

    print("Problem scraping complete and saved to files.")

if __name__ == "__main__":
    scrape_problems()
