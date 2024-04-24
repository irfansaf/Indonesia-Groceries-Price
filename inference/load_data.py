# Load data from the given path
import os
import pandas as pd


def load_data(path):
    """
    Load data from the given path
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path)


def load_data_from_dir(path):
    """
    Load data from the given directory
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Directory not found: {path}")
    data = []
    for file in os.listdir(path):
        if file.endswith(".csv"):
            data.append(pd.read_csv(os.path.join(path, file)))
    return data
