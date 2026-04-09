import pandas as pd
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
    
    # Smart Pathing
    current_folder = os.path.dirname(os.path.abspath(__file__))
    parent_folder = os.path.dirname(current_folder)
    output_path = os.path.join(parent_folder, 'include', 'food_prices_raw.csv')
    
    df.to_csv(output_path, index=False)
    print(f"✅ Success! Food prices extracted to {output_path}")

if __name__ == "__main__":
    extract_food_prices()