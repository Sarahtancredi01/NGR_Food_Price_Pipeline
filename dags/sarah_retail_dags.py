# from airflow import DAG # type: ignore
# from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import pandas as pd # type: ignore
import os
from sqlalchemy import create_engine # type: ignore
from dotenv import load_dotenv # type: ignore

# 1. LOAD SECURE ENVIRONMENT VARIABLES
load_dotenv()

# 2. Pipeline Configuration
# These settings help the system know who is running the pipeline
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
    input_file = 'include/food_prices_raw.csv'
    staging_file = 'include/raw_staging.csv'
    
    if not os.path.exists(input_file):
        print(f"Warning: {input_file} not found. Creating a sample folder...")
        os.makedirs('include', exist_ok=True)
        # Dummy data to prevent crash if file is missing
        df_dummy = pd.DataFrame([{
            'item': 'Rice (local)', 
            'price_naira': '61000', 
            'unit': '50kg bag', 
            'market': 'Mile 12', 
            'date_recorded': '2026-04-13'
        }])
        df_dummy.to_csv(input_file, index=False)
        
    df = pd.read_csv(input_file)
    df.to_csv(staging_file, index=False)
    print(f"Extraction Success: {len(df)} raw records moved to staging.")

# 4. TRANSFORMATION TASK 
# This handles cleaning and national standardization
def transform_and_clean_data():
    staging_file = 'include/raw_staging.csv'
    final_file = 'include/food_prices_cleaned.csv'
    
    if not os.path.exists(staging_file):
        raise FileNotFoundError(f"Missing staging file: {staging_file}")

    df = pd.read_csv(staging_file)
    
    # --- DATA INTEGRITY: REMOVE HEADER REPETITIONS ---
    # This prevents the 'could not convert string to float' error
    df = df[df['price_naira'].astype(str) != 'price_naira']
    
    # --- STANDARDIZATION ---
    # Converts market names to UPPERCASE (e.g., 'wuse' becomes 'WUSE')
    # This is vital for cross-state data consistency
    df['market'] = df['market'].str.upper()
    
    # --- NUMERIC CONVERSION ---
    # Removes Naira symbols, commas, and spaces. 
    # errors='coerce' turns bad data into 'NaN' (empty) so the script doesn't stop.
    df['price_naira'] = pd.to_numeric(
        df['price_naira'].astype(str).replace(r'[N,₦\s,]', '', regex=True), 
        errors='coerce'
    )
    
    # Remove any rows where the price was invalid or empty
    df = df.dropna(subset=['price_naira'])
    
    # Update date to the current run date
    df['date_recorded'] = datetime.now().strftime('%Y-%m-%d')
    
    df.to_csv(final_file, index=False)
    print(f"Transformation Success! {len(df)} records standardized and validated.")

# 5. SECURED LOADING TASK
def load_to_postgres():
    final_file = 'include/food_prices_cleaned.csv'
    
    # Pulling credentials from your hidden .env file
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    
    # Connection string construction
    connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(connection_string)
    
    df = pd.read_csv(final_file)
    
    # LOAD INTO DATABASE
    # Renamed to 'ngr_market_prices' to reflect the national expansion
    df.to_sql('ngr_market_prices', engine, if_exists='replace', index=False)
    print(f"Success: Records loaded into database table: ngr_market_prices!")

# 6. MANUAL TRIGGER BLOCK (The "Play" Button)
if __name__ == "__main__":
    print("--- Starting the Sarah Retail Secured ETL Pipeline ---")
    try:
        extract_market_data()
        transform_and_clean_data()
        load_to_postgres()
        print("--- Full ETL execution complete! Check pgAdmin 4 for ngr_market_prices. ---")
    except Exception as e:
        print(f"An error occurred during the run: {e}")
