# Import all necessary libraries and modules
# These include Selenium components for browser automation,
# BeautifulSoup for HTML parsing, and pandas for data manipulation.

from selenium import webdriver
from selenium.webdriver.common.by import By  # Used to specify how we locate elements (e.g., by name, ID, class, etc.)
from selenium.webdriver.support.ui import WebDriverWait, Select  # WebDriverWait allows us to wait for certain conditions. Select is for handling dropdowns.
from selenium.webdriver.support import expected_conditions as EC  # Contains expected conditions to wait for (e.g., element to be present)
from selenium.webdriver.chrome.options import Options  # Used to set browser options (like headless mode)
from selenium.webdriver.chrome.service import Service  # Used to configure the ChromeDriver service
from webdriver_manager.chrome import ChromeDriverManager  # Automatically manages ChromeDriver installation
from bs4 import BeautifulSoup  # For parsing HTML and extracting data from it
import pandas as pd  # For handling tabular data and saving it to CSV
import time  # Used for delays in execution (though WebDriverWait is usually preferred)
import psycopg2
from sqlalchemy import create_engine
import os


# The URL of the webpage containing the fund performance table
url = "https://uttamis.co.tz/fund-performance"

# Set up Chrome browser options for automated use
options = Options()
options.add_argument("--headless")  # Run browser in headless mode (no UI). Useful for automation and running on servers.
options.add_argument("--no-sandbox")  # Disable sandboxing for Chrome (commonly needed for running in containers or CI/CD)
options.add_argument("--disable-dev-shm-usage")  # Prevents issues related to limited shared memory space in container environments

# Initialize a Chrome browser session using WebDriverManager to auto-handle driver setup
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),  # Automatically install and use the correct ChromeDriver version
    options=options  # Use the browser options defined above
)

try:
    # Navigate to the fund performance page
    driver.get(url)

    # Wait up to 30 seconds for the dropdown element that controls how many table entries are shown
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "data_table_length"))
    )

    # Locate the dropdown menu by its HTML 'name' attribute and create a Select object to interact with it
    dropdown = Select(driver.find_element(By.NAME, "data_table_length"))

    # Print all available dropdown options (e.g., 50, 100, 200, Max 5000) for debugging purposes
    print("Dropdown options:")
    for option in dropdown.options:
        print(f"- {option.text} (value: {option.get_attribute('value')})")

    # Select the dropdown option that has value "5000", which corresponds to "Max (5000)" entries
    dropdown.select_by_value("5000")
    print("Selected 'Max (5000)' option...")

    # Pause execution for 5 seconds to allow the table to start loading the large number of entries
    # (5000 entries can take significant time to fully load; this buffer prevents premature scraping)
    time.sleep(5)

    # Wait until the table has been updated and contains rows inside the <tbody> section
    # This is done using an anonymous lambda function that tries to find <tr> elements inside the <tbody> of the table with ID "data_table"
    WebDriverWait(driver, 30).until(
        lambda d: d.find_element(By.ID, "data_table")
                 .find_element(By.TAG_NAME, "tbody")
                 .find_elements(By.TAG_NAME, "tr")  # Will return True when at least one row is present
    )

    # Parse the current page's HTML using BeautifulSoup to allow easier navigation and extraction of the table
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the main table on the page that has the class "table"
    table = soup.find("table", class_="table")

    # If the table exists and was successfully found:
    if table:
        # Extract the column headers by selecting all <th> elements inside the <thead>
        headers = [th.text.strip() for th in table.select("thead th")]

        # Extract each row of data by selecting <tr> elements inside the <tbody>
        # For each row, extract the text from each <td> (cell), strip whitespace, and store it as a list of lists
        rows = [
            [td.text.strip() for td in tr.select("td")]
            for tr in table.select("tbody tr")
        ]

        # Create a pandas DataFrame from the extracted rows and headers
        df = pd.DataFrame(rows, columns=headers)

        # Display the first 5 rows of the resulting DataFrame in the terminal for verification
        print(df.head())
    else:
        # If the table could not be found on the page, print an error message
        print("Table not found.")

finally:
    # Close and terminate the browser session to free up resources (regardless of whether success or failure)
    driver.quit()

# Save the DataFrame as a CSV file named 'utt_fund_data_max.csv'
# This allows future analysis or processing without needing to re-scrape
df.to_csv("raw_data.csv", index=False)

# Confirm to the user via console that the file was saved successfully
print("Saved to 'raw_data.csv'")
