"""
fund_fetcher Package
--------------------
Provides utilities to scrape, clean, and store fund data from the UTT AMIS website.

This package supports:
- Headless web scraping using Selenium
- Parsing data tables with BeautifulSoup
- Cleaning numeric and date fields using pandas
- Writing cleaned data to PostgreSQL

Main exposed functions:
- scrape_fund_data(): Scrape and save UTT AMIS data
- clean_and_format_fund_data(): Clean data and format for analysis or database
- insert_utt_data(): Insert cleaned data into PostgreSQL
"""

# Direct access to key functions
from .fetch_utt import (
    clean_fund_data_basic,
    clean_and_format_fund_data,
    process_fund_csv,
    create_utt_table,
    insert_utt_data,
)
