from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

import pandas as pd

from src.config import MODELS_PATH
from src.utils import load_models


BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"


class Athlet(BaseModel):
    """
    Input features validation for the ML model
    """
    
    age: int
    body_weight: float
    squat: float
    deadlift: float
    
    
def get_predictions(models, features):
    predictions = dict()

    for model_name, model in models.items():
        predictions[model_name] = model.predict(features).round(1)[0]

    return predictions


app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name='static')
models = load_models(MODELS_PATH)
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/")   
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name = "index.html"
    )
    

@app.get("/form")
def form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="predict.html"
    )


@app.post("/predict")
def predict(athlet: Athlet):
    """
    :param athlet: input data about athlet from the POST request
    :return predicted Max Bench Press
    """
    
    athlet_features = pd.DataFrame(
        data=[[
            athlet.age,
            athlet.body_weight,
            athlet.squat,
            athlet.deadlift
        ]],
        columns=['Age', 'Bwt', 'Best Squat', 'Best Deadlift']
    )
    
    predictions = get_predictions(models, athlet_features)
    
    return {"predictions": predictions}