from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import pandas as pd # type: ignore
import os

# 1. Pipeline Configuration
default_args = {
    'owner': 'Sarah_Ityav',
    'depends_on_past': False,
    'start_date': datetime(2026, 4, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='sarah_retail_dag',
    default_args=default_args,
    description='Weekly ETL for Lagos Food Prices',
    schedule='0 8 * * 1', # Runs every Monday at 8:00 AM
    catchup=False,
    tags=['3MTT', 'Lagos_Markets']
) as dag:

    # 2. EXTRACTION TASK
    def extract_market_data():
        input_file = 'include/food_prices_raw.csv'
        staging_file = 'include/raw_staging.csv'
        
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Missing input file: {input_file}")
            
        df = pd.read_csv(input_file)
        df.to_csv(staging_file, index=False)
        print(f"Extraction Success: {len(df)} raw records moved to staging.")

    # 3. TRANSFORMATION TASK
    def transform_and_clean_data():
        staging_file = 'include/raw_staging.csv'
        final_file = 'include/food_prices_cleaned.csv'
        
        if not os.path.exists(staging_file):
            raise FileNotFoundError(f"Missing staging file: {staging_file}")

        df = pd.read_csv(staging_file)
        
        # --- Cleaning Logic ---
        
        # 1. Capitalize market names (e.g., mile 12 -> MILE 12)
        df['market'] = df['market'].str.upper()
        
        # 2. Clean the price column (Removes N, commas, and spaces)
        df['price_naira'] = df['price_naira'].replace(r'[N,₦\s,]', '', regex=True).astype(float)
        
        # 3. UPDATE THE DATE TO TODAY'S DATE
        df['date_recorded'] = datetime.now().strftime('%Y-%m-%d')
        
        # 4. Remove rows with missing prices
        df = df.dropna(subset=['price_naira'])
        
        # Save the final clean file
        df.to_csv(final_file, index=False)
        print(f"Transformation Success! Clean records saved. Date updated to: {datetime.now().strftime('%Y-%m-%d')}")

    # 4. Defining the Airflow Workflow
    task_1 = PythonOperator(
        task_id='extract_prices',
        python_callable=extract_market_data
    )

    task_2 = PythonOperator(
        task_id='transform_and_clean',
        python_callable=transform_and_clean_data
    )

    task_1 >> task_2

# 5. MANUAL TRIGGER BLOCK
if __name__ == "__main__":
    print("Starting the Sarah Retail Pipeline...")
    try:
        extract_market_data()
        transform_and_clean_data()
        print("Pipeline execution complete! Check your include folder.")
    except Exception as e:
        print(f"An error occurred during the manual run: {e}")
