#!/usr/bin/env python3
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
import os
import pandas as pd

class KaggleInterface:
    def __init__(self):
        self.api = KaggleApi()
        self.api.authenticate()
        self.download_path = "./"

    def download_dataset(self, dataset_name):
        zip_file_path = f"./{dataset_name.split('/')[-1]}.zip"
        if not os.path.exists(zip_file_path):  # Ensure this line exists
            # Download the entire dataset as a .zip file
            self.api.dataset_download_files(dataset_name, path=self.download_path, unzip=False)

        # Unzip the dataset
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall("./")
        
        # Find the CSV file in the extracted files
        extracted_files = os.listdir("./")
        csv_file_name = next((file for file in extracted_files if file.endswith(".csv")), None)

        if not csv_file_name:
            raise FileNotFoundError("No CSV file found in the extracted dataset.")

        return csv_file_name
    
    def download_single_file_from_dataset(self, dataset_name, file_name):
        # Download a specific file from the dataset
        self.api.dataset_download_file(dataset_name, file_name, path=self.download_path, unzip=False)
        
        # If the file is compressed, extract it
        if file_name.endswith(".zip"):
            with zipfile.ZipFile(f"./{file_name}", "r") as zip_ref:
                zip_ref.extractall("./")
            file_name = zip_ref.namelist()[0]

        return file_name
    
    def load_csv_to_dataframe(self, csv_file):
        return pd.read_csv(csv_file)
    
    def load_excel_to_dataframe(self, excel_file):
        return pd.read_excel(excel_file)