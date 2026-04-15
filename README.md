# 🇳🇬 NGR Food Price Pipeline (Lagos)

## 📊 Project Overview
This project is an automated Data Engineering pipeline designed to track the cost of food staples in Lagos, Nigeria. It automates the extraction, cleaning, and migration of market data for 32 essential items, providing a weekly snapshot of price trends in major markets like Mile 12, Mushin, and Oyingbo.

## 🛠️ The Tech Stack
* **Language:** Python 3.11+
* **Data Processing:** Pandas & CSV (for cleaning and transformation)
* **Database:** PostgreSQL (Relational storage for longitudinal analysis)
* **Orchestration:** Windows Task Scheduler (Automated weekly execution)
* **Security:** python-dotenv (Credential Management)

## 🏗️ How it Works
1. **Extract:** The pipeline systematically pulls raw market data from the designated local directory using Python's `os` and `csv` modules.
2. **Transform:** Using **Pandas**, the data is standardized for analysis:
    * **Market Names:** Converted to UPPERCASE for unified reporting across all market locations.
    * **Price Normalization:** Removes Naira symbols (₦), commas, and spaces to convert currency strings into precise numerical (float) formats.
    * **Data Quality:** Implements "pre-flight" validation to handle missing values and verify schema integrity before loading.
3. **Load:** The clean, high-integrity data is migrated into a **PostgreSQL** database environment, verified and managed via **pgAdmin 4**.



## 🚀 Key Features
* **Automated Scheduling:** Configured to run "hands-free" every Monday at 8:00 AM via Windows Task Scheduler.
* **Security First:** Sensitive database credentials (host, user, password) are kept out of the source code using `.env` files and secured via `.gitignore`.
* **Scalability:** Built with a modular logic, allowing for the easy addition of new markets or food commodities without changing the core engine.

## 📂 Project Structure
* **`/data`**: Stores the raw input market files and intermediate processing logs.
* **`/scripts`**: Contains the core Python ETL logic and database connection functions.
* **`.env`**: (Hidden) Stores secure environment variables for database access.
* **`requirements.txt`**: Lists all necessary libraries (`pandas`, `sqlalchemy`, `psycopg2-binary`, `python-dotenv`).

---
© 2026 Sarah O. Ityav | 3MTT Data Engineering Fellow