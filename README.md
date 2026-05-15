🇳🇬 Automated NGR Food Price ETL Pipeline
A Scalable Data Engineering Solution for Monitoring Food Price Trends Across Nigeria

📌 Project Overview

With food inflation continuing to affect households across Nigeria, access to current and reliable pricing data has become increasingly important. Manual data collection can be inconsistent and time-consuming, often leading to outdated information.

To address this, I built an automated ETL (Extract, Transform, Load) pipeline that tracks weekly food price trends across more than 125 food items.

The project initially focused on selected markets in Lagos but was later expanded to include markets in Abuja (Wuse, Garki, and Utako) and Ogun State (Akute and Arepo), providing a broader view of food prices across different regions.

🛠 Tech Stack
Python 3.11 – Core scripting and workflow orchestration
Pandas & SQLAlchemy – Data cleaning, transformation, and database integration
PostgreSQL – Structured storage and querying
Windows Task Scheduler – Automates weekly execution every Monday by 8:00 AM
python-dotenv – Secure management of database credentials and environment variables
🏗 ETL Workflow

The pipeline was designed in a modular structure to keep each stage independent and easier to maintain.

1. Extraction

The script checks the /include directory for the food_prices_raw.csv file before processing begins.

To avoid interruptions during testing or demonstrations, the pipeline generates a sample dataset when the source file is unavailable, ensuring execution continues without failure.

2. Transformation

This stage converts raw market data into a cleaner and more usable format.

Key transformations include:

Price formatting: Removes Naira symbols (₦), commas, and unnecessary spaces using regex
Data validation: Filters out repeated header rows and invalid values that may cause conversion errors
Standardization: Converts market names to uppercase for consistency across locations
Type conversion: Converts price values into numeric formats for future calculations and analysis

Additional safeguards such as errors='coerce' were implemented to prevent poor-quality data from stopping the pipeline.

3. Loading

After validation and cleaning, the transformed data is loaded into a PostgreSQL table named ngr_market_prices.

The pipeline uses if_exists='replace' so downstream reporting tools such as Power BI always display the most recent dataset.

🚀 Key Features

Scalable Design
Expanded from an initial dataset of 32 items to over 125 products, including fresh produce such as yam and tomatoes, as well as packaged household brands like Milo, McVitie's, and Golden Penny.

Multi-Region Coverage
Tracks pricing trends across Lagos, Abuja, and Ogun State markets.

Secure Configuration
Database credentials are stored in a protected .env file and excluded from version control.

Resilient Processing
Built to handle incomplete or inconsistent records without breaking the workflow.

📂 Project Structure

sarah_retail_dags.py – Main ETL script

/include – Stores raw, staging, and cleaned CSV files

.env (excluded from Git) – Contains database credentials

requirements.txt – Project dependencies for reproducibility

Sarah O. Ityav
Data Engineering Practitioner | 3MTT Fellow | Lagos, Nigeria