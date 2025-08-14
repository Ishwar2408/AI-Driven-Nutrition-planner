from typing import Dict, List, Tuple
import pandas as pd
import math

NUTRIENT_COLS = [
    "calories", "protein_g", "fat_g", "carbs_g", "fiber_g", "calcium_mg", "iron_mg"
]

def select_meals(df: pd.DataFrame, targets: Dict[str, int], meals: int = 3, snacks: int = 1) -> Dict[str, List[Dict]]:
    """
    Greedy meal builder: picks items to approach macro targets.
    Each item represents one serving. You can scale servings using 'serving' multiplier.
    """
    df = df.copy()
    df = df.sort_values(by=["protein_g", "fiber_g"], ascending=False)

    total_targets = targets.copy()
    plan: Dict[str, List[Dict]] = {"breakfast": [], "lunch": [], "dinner": [], "snacks": []}

    meal_names = ["breakfast", "lunch", "dinner"]
    per_meal_cals = total_targets["calories"] * 0.28  # ~28% each meal
    snack_cals = total_targets["calories"] * 0.16     # ~16% snacks

    def add_item(bucket: str, row: pd.Series, servings: float = 1.0):
        item = {
            "name": row["food"],
            "serving": round(servings, 2),
            "calories": round(row["calories"] * servings),
            "protein_g": round(row["protein_g"] * servings, 1),
            "fat_g": round(row["fat_g"] * servings, 1),
            "carbs_g": round(row["carbs_g"] * servings, 1),
            "fiber_g": round(row["fiber_g"] * servings, 1),
            "calcium_mg": round(row["calcium_mg"] * servings),
            "iron_mg": round(row["iron_mg"] * servings, 1),
        }
        plan[bucket].append(item)

    # Simple greedy fill for meals
    for i, meal in enumerate(meal_names[:meals]):
        remaining = per_meal_cals
        for _, row in df.iterrows():
            if remaining <= 120:
                break
            c = row["calories"]
            # pick 0.5 to 1.5 servings based on remaining
            mult = max(0.5, min(1.5, remaining / max(c, 1)))
            mult = round(mult * 2) / 2  # step of 0.5
            if mult <= 0:
                continue
            add_item(meal, row, mult)
            remaining -= row["calories"] * mult

    # Snacks: favor high-protein, high-fiber smaller items
    snack_df = df.sort_values(by=["protein_g"], ascending=False).head(15)
    remaining = snack_cals
    for _, row in snack_df.iterrows():
        if remaining <= 80 or len(plan["snacks"]) >= snacks * 2:
            break
        mult = 1.0 if row["calories"] < 250 else 0.5
        add_item("snacks", row, mult)
        remaining -= row["calories"] * mult

    return plan

def summarize_plan(plan: Dict[str, List[Dict]]) -> Dict[str, float]:
    totals = {k: 0.0 for k in ["calories", "protein_g", "fat_g", "carbs_g", "fiber_g", "calcium_mg", "iron_mg"]}
    for items in plan.values():
        for it in items:
            for k in totals:
                totals[k] += it[k]
    return {k: round(v, 1) for k, v in totals.items()}
