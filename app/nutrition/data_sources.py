import os
import pandas as pd
from typing import Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LOCAL_FOODS = os.path.join(DATA_DIR, "foods.csv")

def load_local_foods() -> pd.DataFrame:
    df = pd.read_csv(LOCAL_FOODS)
    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]
    return df

# ---- Placeholders for real integrations ----

def load_fitbit_csv(path: str) -> Optional[pd.DataFrame]:
    """Load a sample exported CSV from Fitbit (steps, heart rate, sleep)."""
    try:
        df = pd.read_csv(path)
        return df
    except Exception:
        return None

def load_apple_health_export(path: str) -> Optional[pd.DataFrame]:
    """Load parsed Apple Health export (pre-parsed to CSV externally)."""
    try:
        df = pd.read_csv(path)
        return df
    except Exception:
        return None

def usda_search_foods(query: str, api_key: Optional[str] = None):
    """
    TODO: Implement real USDA FoodData Central API search & nutrients lookup.
    For now, return None and rely on local foods.
    """
    _ = (query, api_key)  # unused
    return None
