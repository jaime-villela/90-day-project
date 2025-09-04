import pandas as pd
import matplotlib.pyplot as plt
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
import os

def download_and_load_aviation_data():
    # Authenticate with Kaggle
    api = KaggleApi()
    api.authenticate()

    # Define the aviation dataset and file name
    aviation_dataset = "mirzaniazmorshed/ntsb-aviation-accidents"
    aviation_file_name = "events.xlsx"

    # Download the aviation dataset
    api.dataset_download_file(aviation_dataset, aviation_file_name, path="./")

    # If the file is compressed, extract it
    if aviation_file_name.endswith(".zip"):
        with zipfile.ZipFile(f"./{aviation_file_name}", "r") as zip_ref:
            zip_ref.extractall("./")
        aviation_file_name = zip_ref.namelist()[0]

    # Load the aviation data into a pandas DataFrame
    aviation_data = pd.read_excel(aviation_file_name)
    print(aviation_data.head())
    return aviation_data

def download_and_load_car_crashes_data():
    # Authenticate with Kaggle
    api = KaggleApi()
    api.authenticate()

    # Define the car crashes dataset
    car_crashes_dataset = "sobhanmoosavi/us-accidents"

    # Download the entire dataset as a .zip file
    dataset_zip_path = "./us-accidents.zip"
    api.dataset_download_files(car_crashes_dataset, path="./", unzip=False)

    # Unzip the dataset
    with zipfile.ZipFile(dataset_zip_path, "r") as zip_ref:
        zip_ref.extractall("./")
    
    # Find the CSV file in the extracted files
    extracted_files = os.listdir("./")
    csv_file = next((file for file in extracted_files if file.endswith(".csv")), None)

    if not csv_file:
        raise FileNotFoundError("No CSV file found in the extracted dataset.")

    # Load the CSV file into a pandas DataFrame
    dataframe = pd.read_csv(csv_file)
    print(dataframe.head())
    return dataframe

def plot_accidents_per_year(dataframe, date_column, title):
    # Ensure the date column is in datetime format
    dataframe['Date'] = pd.to_datetime(dataframe[date_column], errors='coerce')

    # Extract the year from the date column
    dataframe['Year'] = dataframe['Date'].dt.year

    # Group by year and count the number of accidents
    accidents_per_year = dataframe.groupby('Year').size()

    # Plot the data
    plt.figure(figsize=(10, 6))
    accidents_per_year.plot(kind='bar', color='skyblue')
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel('Number of Accidents')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_combined_accidents(aviation_data, aviation_date_col, car_crashes_data, car_crashes_date_col):
    # Process aviation data
    aviation_data[aviation_date_col] = pd.to_datetime(aviation_data[aviation_date_col], errors='coerce')
    aviation_data['Year'] = aviation_data[aviation_date_col].dt.year
    aviation_accidents_per_year = aviation_data.groupby('Year').size().reset_index(name='Aviation Accidents')

    # Process car crashes data
    car_crashes_data[car_crashes_date_col] = pd.to_datetime(car_crashes_data[car_crashes_date_col], errors='coerce')
    car_crashes_data['Year'] = car_crashes_data[car_crashes_date_col].dt.year
    car_crashes_per_year = car_crashes_data.groupby('Year').size().reset_index(name='Car Crashes')

    # Merge the two datasets on the 'Year' column
    combined_data = pd.merge(aviation_accidents_per_year, car_crashes_per_year, on='Year', how='outer').fillna(0)

    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.plot(combined_data['Year'], combined_data['Aviation Accidents'], label='Aviation Accidents', marker='o')
    plt.plot(combined_data['Year'], combined_data['Car Crashes'], label='Car Crashes', marker='o')
    plt.title('Accidents per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Accidents')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Download and load aviation data
    aviation_data = download_and_load_aviation_data()

    # Download and load car crashes data
    car_crashes_data = download_and_load_car_crashes_data()

    # Plot aviation accidents per year
    #plot_accidents_per_year(aviation_data, "ev_date", "Aviation Accidents per Year")

    # Plot car crashes per year
    #plot_accidents_per_year(car_crashes_data, "Start_Time", "Auto Accidents per Year")

    # Plot combined accidents
    plot_combined_accidents(aviation_data, "ev_date", car_crashes_data, "Start_Time")