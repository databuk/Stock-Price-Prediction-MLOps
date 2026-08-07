import os
from box.exceptions import BoxValueError
import yaml
from stock_prediction import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
from sklearn.base import BaseEstimator
import pandas as pd

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a yaml file and returns a ConfigBox object.
    Args:
        path_to_yaml (Path): Path to the yaml file.
    Returns:
        ConfigBox: A ConfigBox object containing the yaml data.
    """
    try:
        with open(path_to_yaml, "r") as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
        logger.info(f"YAML file: {path_to_yaml} loaded successfully.")
        return ConfigBox(yaml_data)
    except BoxValueError as e:
        logger.error(f"Error while converting YAML to ConfigBox: {e}")
    except Exception as e:
        raise e
    

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Creates a list of directories if they don't exist.
    Args:
        path_to_directories (list): List of directory paths to create.
        verbose (bool): If True, logs the creation of directories.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Directory created at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Saves a dictionary as a JSON file.
    Args:
        path (Path): Path to save the JSON file.
        data (dict): Dictionary to save as JSON.
    """
    try:
        with open(path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        logger.info(f"JSON file saved at: {path}")
    except Exception as e:
        logger.error(f"Error saving JSON file at {path}: {e}")
        raise e
    
@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Loads a JSON file and returns a ConfigBox object.
    Args:
        path (Path): Path to the JSON file.
    Returns:
        ConfigBox: A ConfigBox object containing the JSON data.
    """
    try:
        with open(path, "r") as json_file:
            data = json.load(json_file)
        logger.info(f"JSON file loaded from: {path}")
        return ConfigBox(data)
    except Exception as e:
        logger.error(f"Error loading JSON file from {path}: {e}")
        raise e
 
@ensure_annotations   
def save_csv(data: pd.DataFrame, file_path: Path):
    """Saves the DataFrame to a CSV file.

    Args:
        data (pd.DataFrame): The DataFrame to save.
        file_path (Path): The path where the CSV file will be saved.
    """
    try:
        data.to_csv(file_path, index=False)
        logger.info(f"Data saved to {file_path}")
    except Exception as e:
        logger.error(f"Error saving data to {file_path}: {e}")
        raise e
    

@ensure_annotations
def save_bin(data: object, path: Path):
    """
    Saves data as a binary file using joblib.
    Args:
        path (Path): Path to save the binary file.
        data (Any): Data to save as binary.
    """
    try:
        joblib.dump(value=data, filename=path)
        logger.info(f"Binary file saved at: {path}")
    except Exception as e:
        logger.error(f"Error saving binary file at {path}: {e}")
        raise e

@ensure_annotations
def load_bin(path: Path) -> BaseEstimator:
    """
    Loads a binary file using joblib and returns the data.
    Args:
        path (Path): Path to the binary file.
    Returns:
        Any: The data loaded from the binary file.
    """
    try:
        with open(path, "rb") as bin_file:
            data = joblib.load(bin_file)
        logger.info(f"Binary file loaded from: {path}")
        return data
    except Exception as e:
        logger.error(f"Error loading binary file from {path}: {e}")
        raise e

@ensure_annotations
def get_size(path: Path) -> str:
    """
    Returns the size of a file in kilobytes.
    Args:
        path (Path): Path to the file.
    Returns:
        str: The size of the file in kilobytes.
    """
    size = os.path.getsize(path)
    return f"{size / 1024:.2f} KB"

