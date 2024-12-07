from pathlib import Path

import pandas as pd
import yaml


def find_skiprows(filename: Path, target_cols: set) -> int:
    target_cols = {col.replace(' ', '') for col in target_cols}
    if filename.suffix != ".xlsx":
        raise ValueError("Filename must have .xlsx extension")
    sample_df = pd.read_excel(filename)

    for i in range(len(sample_df)):
        row = [str(val).strip() for val in sample_df.iloc[i]]
        current_cols = {col.replace(' ', '') for col in row}
        if target_cols.issubset(current_cols):
            return i + 1
    raise ValueError(f"Could not find header row with columns {target_cols}")


def find_currency(filename: Path) -> str | None:
    read_method = pd.read_excel if filename.suffix == ".xlsx" else pd.read_csv
    data = read_method(filename)

    for i in range(data.shape[0]):
        row = {str(val).strip().replace(' ', '').lower() for val in data.iloc[i]}
        for currency in {"eur", "gel"}:
            if currency in row:
                return currency.upper()
    return None


def load_logging_config(config_path, variables: dict = None) -> dict:
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    if variables:
        for key, value in variables.items():
            config_str = yaml.dump(config)
            config_str = config_str.replace(f"${{{key}}}", value)
            config = yaml.safe_load(config_str)

    return config

def has_csv_or_xlsx_files(directory: Path) -> bool:
    return any(f.suffix in ('.csv', '.xlsx') for f in directory.iterdir() if f.is_file())
