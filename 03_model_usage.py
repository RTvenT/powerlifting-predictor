from src.config import *

import os

import numpy as np 
import pandas as pd

from joblib import dump, load


model = load(os.path.join(MODELS_PATH, "LR_v1.joblib"))


age = int(input("Возраст (полных лет): "))
bwt = float(input("Собственный вес (кг): "))
squat = float(input("Присед 1ПМ: "))
deadlift = float(input("Становая 1ПМ: "))

person_stats = pd.DataFrame(data=[[age, bwt, squat, deadlift]], columns=['Age', 'Bwt', 'Best Squat', 'Best Deadlift'])

bench_pred = model.predict(person_stats)

print("Ваш возможный жим 1ПМ:", bench_pred[0])