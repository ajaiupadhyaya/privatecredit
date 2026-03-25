import sqlite3
import pandas as pd
from pathlib import Path

# Setup database path
DB_DIR = Path(__file__).parent.parent.parent / "data" / "db"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "privatecredit.db"

def get_connection():
    """Returns a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

def save_dataframe(df: pd.DataFrame, table_name: str, if_exists: str = "replace"):
    """Saves a pandas DataFrame to the SQLite database."""
    with get_connection() as conn:
        df.to_sql(table_name, conn, if_exists=if_exists)

def load_dataframe(table_name: str, index_col: str = None, parse_dates: list = None) -> pd.DataFrame:
    """Loads a pandas DataFrame from the SQLite database."""
    with get_connection() as conn:
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        
    if index_col and index_col in df.columns:
        df = df.set_index(index_col)
        
    if parse_dates:
        for col in parse_dates:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
            elif col == index_col or (isinstance(index_col, list) and col in index_col):
                 if df.index.name == col:
                     df.index = pd.to_datetime(df.index)
                    
    return df

def execute_query(query: str):
    """Executes a raw SQL query."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()

def query_to_dataframe(query: str, parse_dates: list = None) -> pd.DataFrame:
    """Runs a SELECT query and returns a DataFrame."""
    with get_connection() as conn:
        df = pd.read_sql(query, conn)
        
    if parse_dates:
        for col in parse_dates:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
                
    return df
