# AI-Driven Personal Nutrition Planner 🍎

A practical end-to-end project that analyzes dietary habits, wearable data (steps, heart rate, sleep),
and food nutrition databases to recommend personalized meal plans and answer natural-language queries
like “What should I eat for lunch?”

## Features
- TDEE & macro target calculation (Mifflin–St Jeor + activity level)
- Lightweight nutrient deficiency heuristics (iron, calcium, fiber, protein)
- Greedy meal planner to meet daily calories & macros from a sample foods database
- Simple chatbot that suggests a meal given your goals & remaining calories
- Streamlit UI for interaction
- FastAPI endpoints for programmatic access
- Pluggable data source layer with USDA/Fitbit/Apple Health placeholders

> This repo includes a **sample dataset** and works **offline** out of the box. You can later plug in real APIs.

## Quickstart
```bash
# 1) Create & activate a virtualenv (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Launch the Streamlit app
streamlit run app/main.py

# (Optional) Run API server in another terminal
uvicorn app.api:app --reload --port 8000
```

## Project Structure
```
app/
  main.py            # Streamlit app (UI)
  api.py             # FastAPI endpoints
  nutrition/
    recommender.py   # meal planning & suggestions
    data_sources.py  # connectors to USDA / wearables (stubs + local fallback)
    chatbot.py       # simple nutrition chatbot
  models/
    calorie_predictor.py # TDEE + goal adjustments
  utils/
    nutrients.py     # macro & micronutrient helpers
  data/
    foods.csv        # sample food database
requirements.txt
README.md
```

## Notes on Real Integrations
- **USDA FoodData Central**: add your key in env `USDA_API_KEY`. Implement the TODOs in `data_sources.py`.
- **Fitbit / Apple Health**: export CSVs or connect via their APIs (OAuth). See `data_sources.py` for loaders.

## Educational Use Only
This tool is not medical advice. Consult a healthcare professional for personalized recommendations.
