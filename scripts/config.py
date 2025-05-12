# ======================
# Configuration Settings
# ======================

# Data file paths
RAW_DATA_PATH = "data/raw_data.csv"
CLEANED_DATA_PATH = "data/cleaned_data.csv"

# Output directories
REPORT_OUTPUT_DIR = "outputs/"
CHART_OUTPUT_DIR = "outputs/visuals/"

# PostgreSQL Database credentials
DB_NAME = "(yourdatabasename)"
DB_USER = "postgres"
DB_PASSWORD = "(writeyourpassword)"
DB_HOST = "localhost"
DB_PORT = "5432"

# Column names for UTT fund data (adjust if needed)
DATE_COLUMN = "Date Valued"
BIGINT_COLUMNS = ["Net Asset Value", "Outstanding Number of Units"]
DECIMAL_COLUMNS = ["Nav Per Unit", "Sale Price per Unit", "Repurchase Price/Unit"]

# Chart display options
DEFAULT_SAMPLE_FUND = "Wekeza Maisha"  # fallback fund name for combo chart
