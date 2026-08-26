from datetime import datetime, timedelta
import os
import pandas as pd  # type: ignore
from sqlalchemy import create_engine  # type: ignore
from dotenv import load_dotenv  # type: ignore

# 1. LOAD SECURE ENVIRONMENT VARIABLES
load_dotenv()

# Navigate up one directory level from 'dags/' to project root
DAGS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(DAGS_DIR)
INCLUDE_DIR = os.path.join(PROJECT_ROOT, 'include')

# 2. Pipeline Configuration
default_args = {
    'owner': 'Sarah_Ityav',
    'depends_on_past': False,
    'start_date': datetime(2026, 4, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 3. EXTRACTION TASK
def extract_market_data():
    input_file = os.path.join(INCLUDE_DIR, 'food_prices_raw.csv')
    staging_file = os.path.join(INCLUDE_DIR, 'raw_staging.csv')
    
    os.makedirs(INCLUDE_DIR, exist_ok=True)
    
    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"Extraction Failed: '{input_file}' was not found. "
            f"Ensure the 125-row raw CSV is placed inside '{INCLUDE_DIR}'."
        )
        
    df = pd.read_csv(input_file)
    df.to_csv(staging_file, index=False)
    print(f"Extraction Success: {len(df)} raw records staged.")

# 4. TRANSFORMATION TASK 
def transform_and_clean_data():
    staging_file = os.path.join(INCLUDE_DIR, 'raw_staging.csv')
    final_file = os.path.join(INCLUDE_DIR, 'food_prices_cleaned.csv')
    
    if not os.path.exists(staging_file):
        raise FileNotFoundError(f"Missing staging file: {staging_file}")

    df = pd.read_csv(staging_file)
    initial_count = len(df)
    
    # Remove header repetitions
    df = df[df['price_naira'].astype(str).str.strip().str.lower() != 'price_naira']
    
    # Standardize text columns
    df['market'] = df['market'].astype(str).str.upper()
    
    # Clean currency symbols (N, ₦, NGN, spaces, commas)
    cleaned_price_series = df['price_naira'].astype(str).replace(r'[N₦\s,]|NGN', '', regex=True)
    df['price_naira'] = pd.to_numeric(cleaned_price_series, errors='coerce')
    
    # Audit dropped rows before discarding
    invalid_rows = df[df['price_naira'].isna()]
    if not invalid_rows.empty:
        print(f"Warning: {len(invalid_rows)} records dropped due to unparseable price values.")
    
    df = df.dropna(subset=['price_naira'])
    df['date_recorded'] = datetime.now().strftime('%Y-%m-%d')
    
    df.to_csv(final_file, index=False)
    print(f"Transformation Success! Output saved with {len(df)} / {initial_count} valid records.")

# 5. SECURED LOADING TASK
def load_to_postgres():
    final_file = os.path.join(INCLUDE_DIR, 'food_prices_cleaned.csv')
    
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    
    connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(connection_string)
    
    df = pd.read_csv(final_file)
    df.to_sql('ngr_market_prices', engine, if_exists='append', index=False)
    print(f"Success: {len(df)} records loaded into table 'ngr_market_prices'.")

# 6. MANUAL TRIGGER BLOCK
if __name__ == "__main__":
    print("--- Starting Secured ETL Pipeline ---")
    try:
        extract_market_data()
        transform_and_clean_data()
        load_to_postgres()
        print("--- Full ETL execution complete! ---")
    except Exception as e:
        print(f"Pipeline error: {e}")
