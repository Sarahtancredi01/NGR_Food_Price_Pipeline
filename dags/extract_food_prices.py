import pandas as pd  # type: ignore
import os

def extract_food_prices():
    data = {
        'item': ['Rice (local)', 'Tomato', 'Beans (brown)', 'Onion', 'Garri (white)'],
        'price_naira': [61000, 60000, 950, 450, 800],
        'unit': ['50kg bag', 'Big basket', '1kg', '1kg', '1kg'],
        'market': ['Mile 12', 'Mile 12', 'General', 'General', 'Mushin'],
        'date_recorded': ['2026-04-09', '2026-04-09', '2026-04-09', '2026-04-09', '2026-04-09']
    }
    
    df = pd.DataFrame(data)
    
    # Smart Pathing: Target include/ directory outside of dags/
    current_folder = os.path.dirname(os.path.abspath(__file__))
    parent_folder = os.path.dirname(current_folder)
    include_dir = os.path.join(parent_folder, 'include')
    
    # Ensure directory exists before saving
    os.makedirs(include_dir, exist_ok=True)
    output_path = os.path.join(include_dir, 'food_prices_raw.csv')
    
    df.to_csv(output_path, index=False)
    print(f"✅ Success! Extracted {len(df)} records to {output_path}")

if __name__ == "__main__":
    extract_food_prices()