readme = """
# AI-Driven Personal Nutrition Planner 

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
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Launch the Streamlit app
streamlit run app/main.py

# (Optional) Run API server in another terminal
uvicorn app.api:app --reload --port 8000
