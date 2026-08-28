import os
import glob
import pandas as pd  # type: ignore

# Set project paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INCLUDE_DIR = os.path.join(BASE_DIR, 'include')

def merge_all_csvs():
    # Search for all .csv files in the include directory
    csv_pattern = os.path.join(INCLUDE_DIR, '*.csv')
    csv_files = glob.glob(csv_pattern)
    
    if not csv_files:
        print(f"No CSV files found in {INCLUDE_DIR}")
        return

    print(f"Found {len(csv_files)} CSV file(s) to process...")
    
    df_list = []
    for file in csv_files:
        try:
            temp_df = pd.read_csv(file)
            df_list.append(temp_df)
            print(f"Loaded {len(temp_df)} rows from {os.path.basename(file)}")
        except Exception as e:
            print(f"Error reading {file}: {e}")

    if not df_list:
        return

    # Combine all DataFrames into one
    combined_df = pd.concat(df_list, ignore_index=True)
    initial_total = len(combined_df)

    # Remove exact duplicate records across all columns
    cleaned_df = combined_df.drop_duplicates()
    duplicates_removed = initial_total - len(cleaned_df)

    # Overwrite raw dataset with deduplicated output
    output_file = os.path.join(INCLUDE_DIR, 'food_prices_raw.csv')
    cleaned_df.to_csv(output_file, index=False)

    print("\n--- Consolidation Complete ---")
    print(f"Total raw rows gathered: {initial_total}")
    print(f"Duplicate rows removed: {duplicates_removed}")
    print(f"Final unique records saved: {len(cleaned_df)} -> {output_file}")

if __name__ == "__main__":
    merge_all_csvs()