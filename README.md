# 🇳🇬 NGR Food Price Pipeline (Lagos)

## 📊 Project Overview
This project is an automated Data Engineering pipeline designed to track the cost of food staples in Lagos, Nigeria. By capturing price data for items like Rice and Tomatoes, this tool provides a weekly snapshot of inflation trends during the April 2026 economic period.

## 🛠️ The Tech Stack
* **Language:** Python 3.11
* **Orchestration:** Apache Airflow (via Astronomer CLI)
* **Cloud Storage:** Amazon S3 (AWS)
* **Environment:** Docker Desktop

## 🏗️ How it Works
1. **Extract:** Python scripts pull price data from major Lagos markets (Mile 12, Oyingbo).
2. **Transform:** Data is cleaned and formatted into CSV files using Pandas.
3. **Load:** The final reports are automatically uploaded to an AWS S3 bucket for cloud storage and future analysis.

## 🚀 Key Features
- **Security:** Uses `.env` files to protect AWS credentials.
- **Automation:** Scheduled via Airflow DAGs to run without manual effort.
- **Real-World Impact:** Tracked the 46% surge in tomato prices following the April 2026 Easter holidays.

## 📂 Project Structure
- `/dags`: Contains the Airflow orchestration scripts.
- `/include`: Stores raw data files and helper scripts.
- `.env`: (Ignored via gitignore) Stores secret keys.