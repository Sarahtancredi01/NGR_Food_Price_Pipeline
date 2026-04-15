# NGR Food Price Pipeline (Lagos)
Tracking weekly inflation trends across Lagos markets using Python and PostgreSQL.

## 📌 Why I Built This
Manual price tracking in Lagos is slow and full of errors. I built this pipeline to automate the collection of food prices from markets like Mile 12 and Oyingbo. Instead of manual entry, this script handles the heavy lifting—cleaning the currency formatting and pushing it straight to a database for analysis.

## 🛠 Tech I Used
* **Python 3.11** (The engine)
* **Pandas & CSV** (For cleaning up messy raw data)
* **PostgreSQL** (Where the clean data lives)
* **Windows Task Scheduler** (To handle the weekly 8:00 AM automation)
* **python-dotenv** (To keep my DB passwords off GitHub)

## 🏗 The Workflow
I broke the pipeline into three clear steps:

1. **Extraction**: My script scans the local directory for the latest `food_prices_raw.csv`. It runs a "pre-flight" check to make sure the file isn't empty or corrupted before starting.
2. **The "Clean-Up" (Transformation)**:
    * Raw prices often come as "N500" or "500.00". I wrote logic to strip the symbols and convert them into **floats** so I can actually run math on them later.
    * I standardized all market names to **UPPERCASE** to avoid having "Mile 12" and "mile 12" appearing as two different markets in my reports.
3. **The Load**: Clean data is sent to a table in my PostgreSQL database. I use `pgAdmin 4` to verify that all 32 items migrated correctly.

## 🚀 Key Features
* **Set and Forget**: It’s scheduled to run every Monday morning, so the data is always fresh for the new week.
* **Error Handling**: If the raw file is missing, the code doesn't just crash; it logs a validation error and stops safely.
* **Security**: I used a `.env` file to manage my credentials. If you're cloning this, you'll need to create your own `.env` file for the database connection.

## 📂 Folders
* `/data`: Raw and processed CSVs.
* `/scripts`: The Python ETL logic.
* `requirements.txt`: Everything you need to install to run this.

---
**Sarah O. Ityav** | 3MTT/DeepTech Data Engineering Fellow