from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import pandas as pd # type: ignore
import os
from sqlalchemy import create_engine # type: ignore
from dotenv import load_dotenv # type: ignore

# 1. LOAD SECURE ENVIRONMENT VARIABLES
# This looks for your .env file and keeps your passwords hidden
load_dotenv()

# 2. Pipeline Configuration
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
    schedule='0 8 * * 1', 
    catchup=False,
    tags=['3MTT', 'Lagos_Markets']
) as dag:

    # 3. EXTRACTION TASK
    def extract_market_data():
        input_file = 'include/food_prices_raw.csv'
        staging_file = 'include/raw_staging.csv'
        
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Missing input file: {input_file}")
            
        df = pd.read_csv(input_file)
        df.to_csv(staging_file, index=False)
        print(f"Extraction Success: {len(df)} raw records moved to staging.")

    # 4. TRANSFORMATION TASK
    def transform_and_clean_data():
        staging_file = 'include/raw_staging.csv'
        final_file = 'include/food_prices_cleaned.csv'
        
        if not os.path.exists(staging_file):
            raise FileNotFoundError(f"Missing staging file: {staging_file}")

        df = pd.read_csv(staging_file)
        
        # Cleaning Logic
        df['market'] = df['market'].str.upper()
        df['price_naira'] = df['price_naira'].replace(r'[N,₦\s,]', '', regex=True).astype(float)
        
        # Update date to today
        df['date_recorded'] = datetime.now().strftime('%Y-%m-%d')
        
        df = df.dropna(subset=['price_naira'])
        df.to_csv(final_file, index=False)
        print(f"Transformation Success! Date updated to: {datetime.now().strftime('%Y-%m-%d')}")

    # 5. SECURED LOADING TASK
    def load_to_postgres():
        final_file = 'include/food_prices_cleaned.csv'
        
        # Pulling details from the hidden .env file (Sarah123 is now hidden)
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')
        
        # Building the connection string securely
        connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        engine = create_engine(connection_string)
        
        df = pd.read_csv(final_file)
        
        # Pushes data to the lagos_market_prices table
        df.to_sql('lagos_market_prices', engine, if_exists='replace', index=False)
        print(f"Success: Records successfully loaded into {db_name}!")

    # 6. Defining the Airflow Workflow
    task_1 = PythonOperator(
        task_id='extract_prices',
        python_callable=extract_market_data
    )

    task_2 = PythonOperator(
        task_id='transform_and_clean',
        python_callable=transform_and_clean_data
    )

    task_3 = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_to_postgres
    )

    # Workflow Order
    task_1 >> task_2 >> task_3

# 7. MANUAL TRIGGER BLOCK
if __name__ == "__main__":
    print("Starting the Sarah Retail Secured ETL Pipeline...")
    try:
        extract_market_data()
        transform_and_clean_data()
        load_to_postgres()
        print("Full ETL execution complete! Check pgAdmin 4.")
    except Exception as e:
        print(f"An error occurred during the run: {e}")
