import os
import pandas as pd
import boto3
from dotenv import load_dotenv 

load_dotenv() 

def transform_and_upload():
    # --- SMART PATH SETUP ---
    current_folder = os.path.dirname(os.path.abspath(__file__))
    parent_folder = os.path.dirname(current_folder)
    input_path = os.path.join(parent_folder, 'include', 'food_prices_raw.csv')
    output_path = os.path.join(parent_folder, 'include', 'food_prices_cleaned.csv')

    bucket_name = 'global-tech-news-bucket-882856017211' 
    
    try:
        # Load and Transform
        df = pd.read_csv(input_path)
        df['currency'] = 'NGN'
        df['market'] = df['market'].str.upper()
        df.to_csv(output_path, index=False)
        
        s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
        # Upload
        s3.upload_file(output_path, bucket_name, 'food_prices_april_2026.csv')
        
        print(f"🚀 Success! Data uploaded to S3 bucket: {bucket_name}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    transform_and_upload()