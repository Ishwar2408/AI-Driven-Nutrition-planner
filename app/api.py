from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict
import pandas as pd

from .models.calorie_predictor import UserProfile, daily_calorie_target
from .utils.nutrients import macro_split
from .nutrition.data_sources import load_local_foods
from .nutrition.recommender import select_meals, summarize_plan
from .nutrition.chatbot import suggest_lunch

app = FastAPI(title="Nutrition Planner API")

class ProfileIn(BaseModel):
    age: int
    sex: str
    height_cm: float
    weight_kg: float
    activity: str
    goal: str

class LunchIn(BaseModel):
    remaining_cals: int
    preference: Optional[str] = ""

@app.post("/plan")
def create_plan(p: ProfileIn):
    user = UserProfile(**p.model_dump())
    calories = daily_calorie_target(user)
    targets = macro_split(calories).__dict__

    foods = load_local_foods()
    plan = select_meals(foods, {"calories": calories}, meals=3, snacks=1)
    totals = summarize_plan(plan)

    return {"calorie_target": calories, "macro_targets": targets, "plan": plan, "totals": totals}

@app.post("/lunch")
def lunch_suggestion(inp: LunchIn):
    foods = load_local_foods()
    picks = suggest_lunch(foods, inp.remaining_cals, inp.preference or "")
    return {"suggestions": picks}
