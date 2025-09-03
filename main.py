import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile

def download_and_load_data():
    # Authenticate with Kaggle
    api = KaggleApi()
    api.authenticate()

    # Define the dataset and file name
    dataset = "mirzaniazmorshed/ntsb-aviation-accidents"  # Dataset identifier
    file_name = "events.xlsx"  # Specific file to download

    # Download the specific file
    api.dataset_download_file(dataset, file_name, path="./")

    # If the file is compressed (e.g., .zip), extract it
    if file_name.endswith(".zip"):
        with zipfile.ZipFile(f"./{file_name}", "r") as zip_ref:
            zip_ref.extractall("./")
        file_name = zip_ref.namelist()[0]  # Update to the extracted file name

    # Load the Excel file into a pandas DataFrame
    dataframe = pd.read_excel(file_name)
    print(dataframe.head())
    return dataframe

if __name__ == "__main__":
    dataframe = download_and_load_data()