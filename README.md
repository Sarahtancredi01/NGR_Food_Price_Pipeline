# 🇳🇬 NGR Food Price Pipeline (Lagos)

## 📊 Project Overview
This project is an automated Data Engineering pipeline designed to track the cost of food staples in Lagos, Nigeria. It automates the extraction and cleaning of market data for items like Rice and Tomatoes, providing a weekly snapshot of price trends in major markets like Mile 12, Mushin, and Oyingbo.

## 🛠️ The Tech Stack
* **Language:** Python 3.11+
* **Data Library:** Pandas (for cleaning and transformation)
* **Orchestration:** Apache Airflow (Logic) & Windows Task Scheduler (Execution)
* **Storage:** Local File System (CSV)

## 🏗️ How it Works
* **Extract:** The pipeline pulls raw market data (`food_prices_raw.csv`) from the `/include` folder.
* **Transform:** Using **Pandas**, the data is cleaned and standardized:
    * **Market Names:** Converted to UPPERCASE for consistency.
    * **Price Normalization:** Removes Naira symbols (N), commas, and spaces to convert values into floats.
    * **Data Quality:** Removes rows with missing prices and logs the total row count for verification.
* **Load:** The clean, analysis-ready data is saved as `food_prices_cleaned.csv` in the `/include` folder.

## 🚀 Key Features
* **Integrity Checks:** Includes built-in print statements to log "Total Rows Processed," ensuring no data is lost during transformation.
* **Automation:** Configured to run "hands-free" every Monday at 8:00 AM via Windows Task Scheduler.
* **Resilience:** Implements file-path validation to prevent code crashes if input files are moved or missing.

## 📂 Project Structure
* **`/dags`**: Contains `sarah_retail_dag.py` (the core pipeline logic).
* **`/include`**: Stores `food_prices_raw.csv` (input) and `food_prices_cleaned.csv` (output).
* **`requirements.txt`**: Lists all necessary libraries (`apache-airflow`, `pandas`).