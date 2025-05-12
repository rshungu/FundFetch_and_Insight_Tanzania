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
df.to_csv("utt_fund_data_max.csv", index=False)

# Confirm to the user via console that the file was saved successfully
print("Saved to 'utt_fund_data_max.csv'")


# Clean the basic columns (BIGINT and numeric columns)
def clean_fund_data_basic(df, bigint_columns, decimal_columns=None):
    """
    This function takes a DataFrame and lists of column names representing numeric values.
    - `bigint_columns`: typically large integer-like values such as 'Net Asset Value' or 'Outstanding Units'.
    - `decimal_columns`: columns containing decimal values like prices or ratios.

    Purpose:
    - Many scraped values are in string format with commas (e.g., "1,234,567").
    - This function removes commas and converts the values into numeric `float` types for further analysis.
    - It ensures that all such columns are ready for computations or storage into a numeric-compatible database.
    """
    for col in bigint_columns:
        df[col] = df[col].replace({',': ''}, regex=True).astype(float)  # Remove commas and convert to float
    if decimal_columns:
        for col in decimal_columns:
            df[col] = df[col].replace({',': ''}, regex=True).astype(float)  # Handle decimals similarly
    return df  # Return cleaned DataFrame

# Clean and format date
def clean_and_format_fund_data(df, date_column, bigint_columns, decimal_columns=None, date_format="%b %d, %Y"):
    """
    This function extends `clean_fund_data_basic` by also converting date columns to a uniform format.
    
    Parameters:
    - `df`: DataFrame containing the fund data
    - `date_column`: Name of the date column to clean and reformat
    - `bigint_columns`, `decimal_columns`: Passed to the basic cleaner
    - `date_format`: Optional format string if the original dates need specific parsing

    Key Steps:
    - Clean numeric columns first
    - Parse dates from strings to datetime objects
    - Reformat all dates to 'YYYY-MM-DD' which is standard for databases and analysis
    """
    df = clean_fund_data_basic(df, bigint_columns, decimal_columns)
    df[date_column] = pd.to_datetime(df[date_column], dayfirst=True).dt.strftime('%Y-%m-%d')
    return df  # Return fully cleaned and formatted DataFrame

# === Dispatcher Function ===
def process_fund_csv(file_path):
    """
    This function serves as a central dispatcher to clean different types of fund CSVs based on the filename.

    It does the following:
    1. Reads the CSV from the specified `file_path`.
    2. Checks the filename to determine which institution (zansec, sanlam, utt) the data belongs to.
    3. Calls the appropriate cleaning logic based on the structure and format typical to that institution's data.
    4. Outputs a cleaned CSV file with a modified name (prefix `cleaned_table_` instead of `table_`).

    This approach ensures flexibility and reuse across different datasets that have slightly different formats.
    """
    filename = os.path.basename(file_path)  # Extract only the filename from full path
    df = pd.read_csv(file_path)  # Load the data into a DataFrame

    if "zansec" in filename:
        # ZANSEC files typically only need bigint columns cleaned (no decimals or dates)
        cleaned = clean_fund_data_basic(df, bigint_columns=["Net Asset Value", "Outstanding number of units"])
    
    elif "sanlaam" in filename:
        # Sanlam files have both bigint and date columns that need parsing
        cleaned = clean_and_format_fund_data(
            df,
            date_column="Date",
            bigint_columns=["Net Asset Value", "Outstanding Number of Units"]
        )

    elif "utt" in filename:
        # UTT files include both bigint and decimal columns, no dates
        cleaned = clean_fund_data_basic(
            df,
            bigint_columns=["Net Asset Value", "Outstanding Number of Units"],
            decimal_columns=["Nav Per Unit", "Sale Price per Unit", "Repurchase Price/Unit"]
        )

    else:
        # If file doesn't match any known patterns, skip and notify
        print(f"Unknown file type: {filename}")
        return

    # Replace "table_" with "cleaned_table_" in filename and save to that new path
    output_path = file_path.replace("_max", "_cleaned_table_")
    cleaned.to_csv(output_path, index=False)
    print(f"✅ Cleaned file saved to: {output_path}")
    
# Define file path of the data to process (can be updated if called dynamically)
file_path = r"C:\Users\rshun\Downloads\CML_2025\Scripts\Personal projects\1. Web Scraping\UTT_schemes\utt_fund_data_max.csv"

# === DATABASE CONNECTION ===
# === CLEAN CSV ===
file_path = "utt_fund_data_max.csv"
df = pd.read_csv(file_path)

# Clean UTT-specific format
cleaned = clean_and_format_fund_data(
    df,
    date_column="Date Valued",
    bigint_columns=["Net Asset Value", "Outstanding Number of Units"],
    decimal_columns=["Nav Per Unit", "Sale Price per Unit", "Repurchase Price/Unit"]
)

cleaned_file_path = file_path.replace("_max", "_cleaned_table")
cleaned.to_csv(cleaned_file_path, index=False)
print(f"✅ Cleaned file saved to: {cleaned_file_path}")

# === DATABASE CONFIG ===
DB_NAME = "fundfetch_analytics"
DB_USER = "postgres"
DB_PASSWORD = "tanzania08"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_engine():
    return create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# === TABLE CREATION ===
def create_utt_table():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utt_data (
            "#" INT,
            "Scheme Name" TEXT,
            "Net Asset Value" FLOAT,
            "Outstanding Number of Units" FLOAT,
            "Nav Per Unit" FLOAT,
            "Sale Price per Unit" FLOAT,
            "Repurchase Price/Unit" FLOAT,
            "Date Valued" DATE
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

# === DATA INSERTION ===
def insert_utt_data(df):
    engine = get_engine()
    df.to_sql("utt_data", con=engine, if_exists="append", index=False)
    print("✅ Data inserted into 'utt_data' table.")

# === EXECUTION FLOW ===
create_utt_table()
insert_utt_data(cleaned)
