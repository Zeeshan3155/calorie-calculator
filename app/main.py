from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import joblib
from fastapi import Request
import os
import pandas as pd
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

model_path = os.path.join(os.path.dirname(__file__), "model/model.pkl")
model = joblib.load(model_path)

app = FastAPI()

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


class CalorieInput(BaseModel):
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    duration_minutes: int
    activity_type: str
    intensity: str


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
def predict(data: CalorieInput):
    try:
        df = pd.DataFrame([data.model_dump()])
        prediction = model.predict(df)[0]
        calories_burned = prediction * df["duration_minutes"][0]
        return {"calories_burned": calories_burned}
    except Exception as e:
        return {"error": str(e)}
