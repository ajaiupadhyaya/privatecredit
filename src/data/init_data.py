from src.data.fetchers import fetch_bdc_data, fetch_macro_data
from src.data.db_manager import save_dataframe
import time

def initialize_database():
    print("Fetching BDC proxy data via yFinance...")
    prices, returns = fetch_bdc_data(start_date="2018-01-01")
    
    if not prices.empty:
        # Reset index to make 'Date' a column for SQLite
        save_dataframe(prices.reset_index(), "bdc_prices", if_exists="replace")
        save_dataframe(returns.reset_index(), "bdc_returns", if_exists="replace")
        print(f"Saved BDC data: {len(prices)} rows.")
    
    time.sleep(1) # Prevent rate limiting
    
    print("Fetching Macroeconomic data via FRED...")
    macro = fetch_macro_data(start_date="2018-01-01")
    if not macro.empty:
        save_dataframe(macro.reset_index(), "macro_data", if_exists="replace")
        print(f"Saved Macro data: {len(macro)} rows.")
        
    print("Database initialization complete.")

if __name__ == "__main__":
    initialize_database()
