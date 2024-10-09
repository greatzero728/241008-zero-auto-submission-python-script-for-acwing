# Auto Submission Script for Acwing

This repository contains Python scripts that automate the process of scraping problem lists and submitting solutions to problems on acwing.

## GIF Demonstrations

Here are some demonstration GIFs showing the functionality of the scripts:

1. ![Auto Submission to acwing - 1](https://github.com/greatzero728/241008-zero-auto-submission-python-script-for-acwing/blob/main/Final%20Result/gif/Auto%20Submission%20to%20acwing%20-%201%2000_00_00-00_00_30.gif)
2. ![Auto Submission to acwing - 2](https://github.com/greatzero728/241008-zero-auto-submission-python-script-for-acwing/blob/main/Final%20Result/gif/Auto%20Submission%20to%20acwing%20-%202%2000_00_00-00_00_30.gif)
3. ![Scraping the Problem List of acwing - 1](https://github.com/greatzero728/241008-zero-auto-submission-python-script-for-acwing/blob/main/Final%20Result/gif/Scarping%20the%20problem%20list%20of%20acwing%201%20-%201%2000_00_00-00_00_30.gif)
4. ![Scraping the Problem List of acwing - 2](https://github.com/greatzero728/241008-zero-auto-submission-python-script-for-acwing/blob/main/Final%20Result/gif/Scarping%20the%20problem%20list%20of%20acwing%201%20-%202%2000_00_00-00_00_30.gif)
5. ![Scraping the Problem List of acwing - 3](https://github.com/greatzero728/241008-zero-auto-submission-python-script-for-acwing/blob/main/Final%20Result/gif/Scarping%20the%20problem%20list%20of%20acwing%202%2000_00_00-00_00_30.gif)

## Overview of the Code

The repository contains two main scripts:

1. **`getProblemList.py`**: 
   - This script scrapes all problem details from acwing and saves them in a JSON file. It retrieves the problem ID, name, URL, and the number of accepted submissions. The script uses Selenium and BeautifulSoup for web scraping.

2. **`acwing.py`**: 
   - This script handles user login, code submission, and checking the status of submissions on acwing. It uses Selenium to automate browser actions and interact with the acwing platform.

## Environment Setup

To run the scripts, you need to set up your environment as follows:

1. **Install Required Packages**:
   Make sure you have Python installed, then install the required packages using pip:
   ```bash
   pip install selenium beautifulsoup4 python-dotenv pyperclip
   ```

2. **Set Up WebDriver**:
   - Ensure you have the Firefox browser installed.
   - Download the appropriate version of the [GeckoDriver](https://github.com/mozilla/geckodriver/releases) and make sure it's in your system's PATH.

3. **Environment Variables**:
   - Create a `.env` file in the same directory as your scripts and add your acwing credentials and wait time:
   ```
   ACWING_USERNAME=your_username
   ACWING_PASSWORD=your_password
   WAIT_TIME=10  # Adjust as necessary
   ```

4. **Run the Scripts**:
   - To scrape problems, run:
   ```bash
   python getProblemList.py
   ```
   - To submit code, run:
   ```bash
   python acwing.py
   ```

## Conclusion

This repository provides a complete solution for automating the process of scraping problem lists and submitting solutions on acwing. Feel free to explore and modify the scripts according to your needs!