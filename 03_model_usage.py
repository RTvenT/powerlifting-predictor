from src.config import *
from src.utils import load_models

import os

import numpy as np 
import pandas as pd

from joblib import dump, load


def get_predictions(models_dir, x):
    models = load_models(models_dir)

    predictions = dict()

    for model_name, model in models.items():
        predictions[model_name] = model.predict(x).round(1)[0]

    return predictions


age = int(input("Возраст (полных лет): "))
bwt = float(input("Собственный вес (кг): "))
squat = float(input("Присед 1ПМ: "))
deadlift = float(input("Становая 1ПМ: "))

person_stats = pd.DataFrame(data=[[age, bwt, squat, deadlift]], columns=['Age', 'Bwt', 'Best Squat', 'Best Deadlift'])

bench_predictions = get_predictions(MODELS_PATH, person_stats)


print("Ваш возможный максимальный жим по оценкам разных моделей):")

for model_name, predicted_bench in bench_predictions.items():
    print(f"{model_name}: {predicted_bench}")