import pandas as pd
import os
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def download_and_load_data():
    # Authenticate with Kaggle
    api = KaggleApi()
    api.authenticate()

    # Define the dataset and file name
    dataset = "atharvakoshti/aeroplane-crash-data-from-1919-to-2025"  # Replace with your dataset identifier
    file_name = "Airplane_Crashes_and_Fatalities_Since_1908.csv"  # Replace with the specific file name in the dataset

    # Download the dataset
    api.dataset_download_file(dataset, file_name, path="./")

    # Extract the file if it's a zip
    if file_name.endswith(".zip"):
        with zipfile.ZipFile(f"./{file_name}", "r") as zip_ref:
            zip_ref.extractall("./")

    # Detect the file encoding
    encoding = detect_encoding(file_name)
    print(f"Detected encoding: {encoding}")

    # Load the dataset into a pandas DataFrame
    dataframe = pd.read_csv(file_name, encoding=encoding)
    print(dataframe.head())
    return dataframe

if __name__ == "__main__":
    dataframe = download_and_load_data()