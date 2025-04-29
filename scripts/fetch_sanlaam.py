from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup

def fetch_sanlaam_data():
    url = "https://invest-tz.sanlameastafrica.com"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get(url)
    WebDriverWait(driver, 30).until_not(EC.presence_of_element_located((By.CLASS_NAME, "spinner-border")))
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "thead th")))

    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", class_="table")

    if table:
        headers = [th.text.strip() for th in table.select("thead th")]
        rows = [[td.text.strip() for td in tr.select("td")] for tr in table.select("tbody tr")]
        df = pd.DataFrame(rows, columns=headers)
        df.to_csv('data/table_from_sanlaam.csv', index=False)
        print("Sanlam data saved to 'table_from_sanlaam.csv'")

    driver.quit()
