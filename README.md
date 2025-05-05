# FundFetch & Insights Tanzania - UTT AMIS Scheme Fund Tracker

This project focuses on scraping and analyzing investment fund data from the **UTT AMIS website**, a key platform for tracking the performance of various investment schemes in Tanzania. 
   - UTT AMIS provides valuable data on the performance of different investment funds, enabling investors to make informed decisions about where to allocate their resources. However, manually tracking these funds over time can be time-consuming and complex.

The goal of the **FundFetch & Insight Tanzania** tool is to automate the process of collecting, cleaning, and analyzing this data. 

   - The tool will track the performance of scheme funds over a period spanning from **Dec 31st, 2024, to Dec 31st, 2019**, offering a historical perspective on the growth patterns of these funds. 
   - It will also generate insightful visualizations to help users easily interpret fund trends and make better investment decisions.

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
FundFetch_and_Insight_Tanzania/
│
├── README.md                       # Project documentation
├── requirements.txt                # List of Python dependencies
├── fund_fetcher/                   # Folder containing the core functionality for fetching and processing data
│   ├── __init__.py                 # Marks the folder as a Python package
│   ├── fetch_utt.py                # Script for scraping data from the UTT AMIS website
│
├── data/                           # Directory for storing raw and cleaned data
│   ├── raw_data.csv                # Raw data fetched from UTT AMIS
│   └── cleaned_data.csv            # Cleaned and processed data ready for analysis
│
├── scripts/                        # Folder containing all scripts for different processes
│   ├── scrape_uttamis.py           # Web scraping script for fetching fund data
│   ├── clean_data.py               # Data cleaning and transformation script
│   ├── generate_reports.py         # Script to generate reports and visualizations
│   └── config.py                   # Configuration file (e.g., for scraping parameters)
│
├── outputs/                        # Directory for storing generated reports and visualizations
│   ├── daily_report.pdf            # Generated daily report with fund performance summary
│   ├── fund_performance_plot.png   # Visualization of fund performance over time
│
├── notebooks/ (Optional)           # Folder for Jupyter notebooks (for exploration and analysis)
│   ├── data_exploration.ipynb      # Jupyter notebook for interactive data exploration and analysis
│
├── main.py                         # Main script that runs the whole tool: fetches, cleans, and generates reports
├── .gitignore                      # Specifies files/folders to be ignored by Git
└── README.md                       # Project documentation (detailed above)

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
