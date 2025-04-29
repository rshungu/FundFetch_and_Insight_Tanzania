
#### `fetch_zansec.py`

```python
import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_zansec_data():
    url = 'https://zansec.co.tz/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', class_='table')
    if table:
        headers = [th.text.strip() for th in table.select('thead th')]
        rows = [[td.text.strip() for td in tr.select('td')] for tr in table.select('tbody tr')]
        df = pd.DataFrame(rows, columns=headers)
        df.to_csv('data/table_from_zansec.csv', index=False)
        print("ZANSEC data saved to 'table_from_zansec.csv'")
