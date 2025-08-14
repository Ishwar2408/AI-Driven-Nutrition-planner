from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class MacroTargets:
    calories: int
    protein_g: int
    fat_g: int
    carbs_g: int

def macro_split(calories: int, protein_ratio: float = 0.30, fat_ratio: float = 0.25) -> MacroTargets:
    """
    Compute macro targets from calories.
    Defaults: 30% protein, 25% fat, 45% carbs.
    """
    protein_cals = calories * protein_ratio
    fat_cals = calories * fat_ratio
    carbs_cals = calories - protein_cals - fat_cals

    protein_g = round(protein_cals / 4)
    fat_g = round(fat_cals / 9)
    carbs_g = round(carbs_cals / 4)
    return MacroTargets(calories=calories, protein_g=protein_g, fat_g=fat_g, carbs_g=carbs_g)

def deficiency_flags(day_intake: Dict[str, float]) -> Dict[str, bool]:
    """
    Super-light heuristic deficiency checks (daily). Adjust thresholds as needed.
    Keys expected in day_intake: protein_g, fiber_g, calcium_mg, iron_mg
    """
    thresholds = {
        "protein_g": 0.8 * 70,        # ~0.8g/kg for 70kg person baseline
        "fiber_g": 25,                # general adult baseline
        "calcium_mg": 1000,           # adult baseline
        "iron_mg": 8,                 # adult male baseline; vary by sex/age
    }
    return {k: (day_intake.get(k, 0) < v) for k, v in thresholds.items()}
