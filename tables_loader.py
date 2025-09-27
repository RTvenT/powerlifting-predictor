from config import (CLEAN_PATH, COMPETITIONS_NAMES)

import os

import numpy as np
import pandas as pd
import openpyxl


def load_tables():
    competitions_results = dict()

    for comp_name in COMPETITIONS_NAMES:
        table_path = os.path.join(CLEAN_PATH, f"{comp_name}_2024.xlsx")

        if os.path.exists(table_path):
            sheets = pd.read_excel(table_path, sheet_name=None)

            if isinstance(sheets, dict):
                df = pd.concat(sheets.values(), axis=0)
            else:
                df = sheets

            competitions_results[comp_name] = df
        else:
            print("Incorrect clean table path:", table_path)

    return competitions_results