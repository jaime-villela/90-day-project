import pandas as pd
import matplotlib.pyplot as plt
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
    return dataframe

def plot_accidents_per_year(dataframe):
    # Ensure the date column is in datetime format
    dataframe['Date'] = pd.to_datetime(dataframe['ev_date'], errors='coerce')

    # Extract the year from the date column
    dataframe['Year'] = dataframe['ev_date'].dt.year

    # Group by year and count the number of accidents
    accidents_per_year = dataframe.groupby('Year').size()

    # Plot the data
    plt.figure(figsize=(10, 6))
    accidents_per_year.plot(kind='bar', color='skyblue')
    plt.title('Number of Accidents per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Accidents')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    dataframe = download_and_load_data()
    plot_accidents_per_year(dataframe)