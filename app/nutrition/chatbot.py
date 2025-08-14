import re
from typing import Dict, List
import pandas as pd

def suggest_lunch(foods: pd.DataFrame, remaining_cals: int, preference: str = "") -> List[Dict]:
    """
    Very simple lunch suggester: filters by preference keywords and fits within remaining calories.
    """
    df = foods.copy()
    if preference:
        kw = preference.lower().split()
        mask = df["tags"].fillna("").str.lower().apply(lambda t: all(k in t for k in kw))
        df = df[mask] if mask.any() else foods

    df = df.sort_values(by=["protein_g", "fiber_g"], ascending=False)
    picks = []
    for _, row in df.iterrows():
        if remaining_cals <= 0 or len(picks) >= 3:
            break
        if row["calories"] <= remaining_cals + 150:  # allow a little wiggle room
            picks.append({
                "name": row["food"],
                "calories": int(row["calories"]),
                "protein_g": float(row["protein_g"]),
                "carbs_g": float(row["carbs_g"]),
                "fat_g": float(row["fat_g"]),
                "tags": row.get("tags", ""),
            })
            remaining_cals -= row["calories"]
    return picks
