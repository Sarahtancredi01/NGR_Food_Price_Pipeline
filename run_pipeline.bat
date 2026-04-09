@echo off
cd /d C:\Users\SARAH\Desktop\NGR_Food_Price_Pipeline
python dags/extract_food_prices.py
python dags/transform_food_prices.py
pause