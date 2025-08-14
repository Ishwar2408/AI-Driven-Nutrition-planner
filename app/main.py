import streamlit as st
import pandas as pd

from nutrition.data_sources import load_local_foods
from models.calorie_predictor import UserProfile, daily_calorie_target
from utils.nutrients import macro_split, deficiency_flags
from nutrition.recommender import select_meals, summarize_plan
from nutrition.chatbot import suggest_lunch

st.set_page_config(page_title="AI-Driven Personal Nutrition Planner", page_icon="🍎", layout="wide")
st.title("🍎 AI-Driven Personal Nutrition Planner")

with st.sidebar:
    st.header("Your Profile")
    age = st.number_input("Age", 16, 90, 24)
    sex = st.selectbox("Sex", ["male", "female"])
    height_cm = st.number_input("Height (cm)", 120, 220, 175)
    weight_kg = st.number_input("Weight (kg)", 40.0, 180.0, 70.0)
    activity = st.selectbox("Activity Level", ["sedentary","light","moderate","active","very_active"])
    goal = st.selectbox("Goal", ["lose","maintain","gain"])

    if st.button("Compute Targets"):
        user = UserProfile(age=age, sex=sex, height_cm=height_cm, weight_kg=weight_kg, activity=activity, goal=goal)
        cals = daily_calorie_target(user)
        targets = macro_split(cals)
        st.session_state["targets"] = targets
        st.success(f"Daily calorie target: {targets.calories} kcal — P:{targets.protein_g}g F:{targets.fat_g}g C:{targets.carbs_g}g")

foods = load_local_foods()

st.subheader("📊 Meal Plan")
if "targets" in st.session_state:
    plan = select_meals(foods, {"calories": st.session_state["targets"].calories}, meals=3, snacks=1)
    totals = summarize_plan(plan)
    col1, col2 = st.columns([2,1])
    with col1:
        for section in ["breakfast","lunch","dinner","snacks"]:
            st.markdown(f"### {section.capitalize()}")
            df = pd.DataFrame(plan[section])
            st.dataframe(df, use_container_width=True, hide_index=True)
    with col2:
        st.markdown("### Daily Totals")
        st.metric("Calories", f"{int(totals['calories'])} kcal")
        st.metric("Protein", f"{totals['protein_g']} g")
        st.metric("Carbs", f"{totals['carbs_g']} g")
        st.metric("Fat", f"{totals['fat_g']} g")
        st.metric("Fiber", f"{totals['fiber_g']} g")
        st.metric("Calcium", f"{totals['calcium_mg']} mg")
        st.metric("Iron", f"{totals['iron_mg']} mg")

        flags = deficiency_flags(totals)
        st.markdown("### ⚠️ Potential Deficiencies (heuristic)")
        for k, v in flags.items():
            st.write(f"- {k}: {'low' if v else 'ok'}")

st.subheader("🤖 Chatbot: What should I eat for lunch?")
pref = st.text_input("Optional preference keywords (e.g., 'veg high-protein')", "")
remaining = st.number_input("Remaining calories for lunch", 200, 1500, 650)
if st.button("Suggest Lunch"):
    picks = suggest_lunch(foods, remaining, pref)
    st.write(picks if picks else "No suggestions matched; try different preferences.")
