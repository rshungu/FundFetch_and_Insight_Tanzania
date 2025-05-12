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
