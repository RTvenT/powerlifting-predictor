from .config import *

import io
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


def log_dfs(dfs: dict, file_name: str):
    with open(os.path.join(LOGS_PATH, f"{file_name}.log"), "w", encoding="utf-8") as log:
        for name, df in dfs.items():
            buf = io.StringIO()
            df.info(buf=buf)
            info_str = buf.getvalue()
            log.write(f"{name}:\n{info_str}\n")