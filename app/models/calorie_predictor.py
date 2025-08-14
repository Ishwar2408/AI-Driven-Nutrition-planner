from dataclasses import dataclass

@dataclass
class UserProfile:
    age: int
    sex: str          # "male" or "female"
    height_cm: float
    weight_kg: float
    activity: str     # "sedentary", "light", "moderate", "active", "very_active"
    goal: str         # "lose", "maintain", "gain"

def mifflin_st_jeor_bmr(sex: str, age: int, height_cm: float, weight_kg: float) -> float:
    if sex.lower() == "male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

def activity_multiplier(level: str) -> float:
    return {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
    }.get(level.lower(), 1.2)

def goal_adjustment(calories: float, goal: str) -> int:
    if goal == "lose":
        return int(calories - 400)  # modest deficit
    elif goal == "gain":
        return int(calories + 300)  # modest surplus
    return int(calories)

def daily_calorie_target(user: UserProfile) -> int:
    bmr = mifflin_st_jeor_bmr(user.sex, user.age, user.height_cm, user.weight_kg)
    tdee = bmr * activity_multiplier(user.activity)
    target = goal_adjustment(tdee, user.goal)
    # clamp to sensible bounds
    return max(1200, min(int(target), 3800))
