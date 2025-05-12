# main.py

from scripts.fetch_utt import (
    clean_and_format_fund_data,
    create_utt_table,
    insert_utt_data
)
from scripts.generate_reports import generate_report
from scripts.config import (
    RAW_DATA_PATH,
    CLEANED_DATA_PATH,
    DATE_COLUMN,
    BIGINT_COLUMNS,
    DECIMAL_COLUMNS
)

import pandas as pd
import os

def main():
    print("🚀 Starting UTT Fund Performance Tracker")

    # Step 1: Load raw scraped data
    print("📥 Loading scraped data...")
    df = pd.read_csv(RAW_DATA_PATH)

    # Step 2: Clean and format data
    print("🧹 Cleaning data...")
    cleaned = clean_and_format_fund_data(
        df,
        date_column=DATE_COLUMN,
        bigint_columns=BIGINT_COLUMNS,
        decimal_columns=DECIMAL_COLUMNS
    )

    # Step 3: Save cleaned data to CSV
    cleaned.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"✅ Cleaned data saved to {CLEANED_DATA_PATH}")

    # Step 4: Insert into database
    print("🗄 Updating database...")
    create_utt_table()
    insert_utt_data(cleaned)

    # Step 5: Generate report (charts + PDF)
    print("📊 Generating charts and report...")
    generate_report()

    print("🎉 Report generation complete!")

if __name__ == "__main__":
    main()
