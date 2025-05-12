# UTT AMIS Scheme Fund Tracker - FundFetch & Insights Tanzania 

 UTT AMIS Scheme Fund Tracker is a tool designed to automate the scraping, cleaning, and analysis of investment fund data from the [UTT AMIS website](https://uttamis.co.tz/fund-performance) — a key platform for monitoring unit trust scheme performance in Tanzania.

While UTT AMIS provides valuable insights, manually tracking fund data over time can be tedious and inefficient. This project streamlines that process by automatically collecting and processing daily fund performance data, enabling users to explore historical trends with ease.

The tool covers fund performance from December 31st, 2021 to December 31st, 2024, and produces visual reports that help investors, analysts, and enthusiasts make informed financial decisions based on reliable and timely data.

## Key Features
1. Automated Data Scraping: The tool fetches daily data from the UTT AMIS website, ensuring that the information is always up-to-date.
  
2. Data Cleaning: It automatically cleans the scraped data to eliminate inconsistencies and make it ready for analysis.
  
3. Performance Tracking: It tracks the performance of various scheme funds, providing a clear view of how each fund has changed over time.
   
4. Reporting & Visualizations: The tool generates reports with visualizations, such as line charts and bar charts, to highlight trends and insights into the performance of the funds.

> This tool streamlines the process for investors, analysts, and financial professionals by allowing them to easily track and compare the performance of various investment funds over time. It automates the generation of reports, saving time and ensuring consistency in data analysis.
> 
> Additionally, the tool is valuable for data enthusiasts who are interested in exploring financial data sets, gaining insights into fund performance trends, and creating data visualizations to better understand the dynamics of investment schemes.

## Repo Structure
```
UTT AMIS Fund Tracker/
│
├── README.md                       # Project documentation
├── requirements.txt                # Python dependencies
├── fund_fetcher/                   # Core functions for data scraping and processing
│   ├── __init__.py                 # Marks it as a package
│   ├── fetch_utt.py                # Main scraper for UTT AMIS
│
├── data/                           # Stores both raw and cleaned data
│   ├── raw_data.csv                # Raw HTML table data
│   └── cleaned_data.csv            # Processed dataset ready for analysis
│
├── scripts/                        # Utility scripts
│   ├── scrape_uttamis.py           # Web scraping logic
│   ├── clean_data.py               # Data cleaning script
│   ├── generate_reports.py         # Creates visual summaries and reports
│   └── config.py                   # Configuration settings
│
├── outputs/                        # Reports and plots output folder
│   ├── daily_report.pdf            # Summary of fund performance
│   ├── fund_performance_plot.png   # Line/bar plots of fund trends
│
├── notebooks/ (optional)          # Jupyter notebooks for exploration
│   ├── data_exploration.ipynb      # Interactive data exploration
│
├── main.py                         # Main automation runner script
├── .gitignore                      # Files to be excluded from Git
└── README.md                       # Project description (this file)

```
> The scraping logic is modular, allowing for extension to other data sources with similar structures. Some websites may use JavaScript-based loading with dynamic content, such as loading spinners or skeleton screens. In such cases, Selenium can be used to ensure that the page is fully rendered before scraping.
> 
> When adapting this project to other sites, consider the following:
>
> 1. Inspecting elements (right-click - Inspect) to understand the structure and classes of the data.
> 2. Viewing the page source to check if the content is dynamic (loaded by JavaScript) or static.
> 3. Making necessary adjustments to class names or selectors in the code based on how the site's data is structured.
>
> By adjusting wait conditions or modifying selector paths, this project can be repurposed for any fund data source that presents its information in an HTML table format.

## Technologies Used
- `Python`
- `requests` & `BeautifulSoup` - Used for parsing and extracting data from static web pages (like Zan Securities). requests handles HTTP interactions, while BeautifulSoup parses and navigates the HTML tree for structured data extraction.
- `Selenium` - Essential for scraping JavaScript-heavy websites (e.g., Sanlam and UTT AMIS), where content is dynamically rendered. It allows full browser automation and interaction, including waiting for tables to load completely.
- `webdriver-manager` - Automatically handles ChromeDriver installation and management, making the Selenium setup smoother and more portable across environments.
- `pandas` - Powers the transformation and export of scraped HTML tables into clean, structured datasets. Enables CSV export, quick inspection, and future integration into data pipelines or visualizations

## How to Run
1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/FundFetch-and-Insight-Tanzania.git
    cd FundFetch-and-Insight-Tanzania
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the script:
    ```bash
    python scripts/scrape_uttamis.py
    ```

4. Clean the fetch data
   ```bash
    python scripts/clean_data.py
    ```
5. Generate reports and visualizations
   ```bash
    python scripts/generate_reports.py
    ```
## Example output
After running the generate_reports.py scripts, you will get:
   - daily_report.pdf containing the summary of fund performance

## Contributions
Contributions are welcome! If you find any bugs or have suggestions for improvements, feel free to create a pull request or open an issue.
