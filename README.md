# FundFetch_and_Insight_Tanzania

A Python-based data scraping project that collects and structures fund performance data from top Tanzanian investment platforms. It’s built to automate the retrieval of key financial tables for analysis, reporting, or integration into dashboards and financial tools.

## Notes on Platform Coverage and Adaptability
This project currently extracts fund performance data from a few well-known Tanzania platforms such as:-
- [Zan Securities](https://zansec.co.tz)
- [Sanlam Tanzania](https://invest-tz.sanlameastafrica.com)
- [UTT AMIS](https://uttamis.co.tz/fund-performance)

> These were selected based on accessibilty and relevance, but the code can easily be adapted to other websites in Tanzania investment ecosystem or beyond. The scraping logic is modular and structured for extension.
>
> Some websites may use JavaScript-based loading with dynamic placeholders such as loading spinners or skeletons. In such cases, selenium is used to wait for the page to fully render before scraping.
>
> When working with the new site, consider the following
>   - Inspecting elements (right click - Inspect) to understand the structures and classes
>   - Viewing page source to understand if the content is dynamic or static
>   - Making minimal changes to the class names or selectors in the code depending on how the site's data is structured
>
> By adjusting wait conditions or selector paths, you can quickly repurpose this project for any fund data source that presents its information in an HTML table format.

## Use Case
This project is ideal for:

**Financial Analysts & Economists**
Professionals seeking up-to-date insights on Tanzania’s investment landscape can automate the retrieval of fund performance data from key platforms. This enables deeper analysis of trends, comparisons across fund managers, and data-driven decision-making without manual data collection.

**Data Scientists & BI Developers**
Those building dashboards or financial models for local markets can use this project as a clean data pipeline. It provides ready-to-use CSV datasets that can feed into tools like Power BI, Tableau, or Python-based analytics solutions for visualizing fund performance, ranking, and changes over time.

**Organizations Needing Automated Reporting**
Investment firms, research institutions, or consultancies who prepare recurring investment performance summaries can plug this scraper into their reporting systems. It removes the bottleneck of manual web scraping, reduces human error, and ensures timely data capture for scheduled reporting.

**Educators & Students in Finance/Data**
Academic environments can use this project to demonstrate real-world applications of Python web scraping, financial data pipelines, or Tanzanian market research. It also provides a base for learning data transformation, reporting, and workflow automation.

## Technologies Used
- `Python`
- `requests` & `BeautifulSoup` - Used for parsing and extracting data from static web pages (like Zan Securities). requests handles HTTP interactions, while BeautifulSoup parses and navigates the HTML tree for structured data extraction.
- `Selenium` - Essential for scraping JavaScript-heavy websites (e.g., Sanlam and UTT AMIS), where content is dynamically rendered. It allows full browser automation and interaction, including waiting for tables to load completely.
- `webdriver-manager` - Automatically handles ChromeDriver installation and management, making the Selenium setup smoother and more portable across environments.
- `pandas` - Powers the transformation and export of scraped HTML tables into clean, structured datasets. Enables CSV export, quick inspection, and future integration into data pipelines or visualizations

## Output
The project generates high-quality CSV files, each representing structured investment fund data from different platforms. These files are stored locally and named for easy reference

```
├── table_from_zansec.csv      # Data scraped from Zan Securities
├── table_from_sanlaam.csv     # Data scraped from Sanlam Tanzania
└── table_from_utt.csv         # Data scraped from UTT AMIS
```

### Example Use Cases for Output:
1. Direct integration into financial dashboards (e.g., Power BI, Tableau, Streamlit)
2. Feeding into automated reporting workflows
3. Enabling comparisons across fund managers and performance over time
4. Archiving data snapshots for future reference or backtesting strategies
   
## How to Run

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/FundFetch_and_Insight_Tanzania.git
    cd FundFetch_and_Insight_Tanzania
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the script:
    ```bash
    python fund_fetch.py
    ```

> Note: Ensure you have Chrome installed for Selenium to work properly with `webdriver-manager`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact
Feel free to connect on [LinkedIn](https://www.linkedin.com/in/rehema-shungu/) or fork and explore the repo.
