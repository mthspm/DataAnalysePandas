import re
from typing import Tuple, Dict
import numpy as np
from pathlib import Path
import os


def load_files(path=Path(os.getcwd()) / 'formula-one-data-2000-2024') -> Tuple[Dict[str,Path], Dict[str,Path]]:
    """
    Load all paths from csv and db files from the formula-one-data-2000-2024 directory.

    Args:
    path (Path): The path to the formula-one-data-2000-2024 directory. if path is not provided, it will use the current working directory.

    Returns:
    Tuple[Dict[str,Path], Dict[str,Path]]: A tuple of dictionaries containing the csv and db files.
    """
    csvs = {}
    dbs = {}
    for file in os.listdir(path):
        if file.endswith('.csv'):
            csvs[file[:-4]] = path / file
        if file.endswith('.db'):
            dbs[file[:-3]] = path / file
    return csvs, dbs


def convert_to_seconds(time_str: str) -> float:
    if not isinstance(time_str, str):
        return np.nan
    match = re.match(r'^(\d+):(\d{2})\.(\d+)$', time_str)
    if match:
        mins = int(match.group(1))
        secs = int(match.group(2))
        ms = int(match.group(3))
        total_secs = mins * 60 + secs + ms / 1000
        return total_secs
    return np.nan

def convert_to_time_components(time_in_seconds: float) -> Tuple[int, int, int]:
    if not isinstance(time_in_seconds, (int, float)) or np.isnan(time_in_seconds):
        return np.nan
    minutes = int(time_in_seconds // 60)
    seconds = int(time_in_seconds % 60)
    milliseconds = int((time_in_seconds - minutes * 60 - seconds) * 1000)
    return f"{minutes}:{seconds}.{milliseconds}"