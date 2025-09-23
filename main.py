#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from kaggle_interface import KaggleInterface

def create_accidents_per_year_dataset(data, date_col, new_index_name):
    """
    Creates a dataset of the number of accidents per year from the given data.

    Args:
        data (pd.DataFrame): The DataFrame containing accident data.
        date_col (str): The name of the column in `data` containing the date of the accidents.
        new_index_name (str): The name to assign to the new index column representing the year.

    Returns:
        pd.DataFrame: A DataFrame with two columns: 'Year' and 'Accidents', where 'Year' is the year of the accidents
                      and 'Accidents' is the number of accidents that occurred in that year.
    """
    # Convert the date column to datetime format
    data[date_col] = pd.to_datetime(data[date_col], errors='coerce')

    # Extract the year from the date column
    data['Year'] = data[date_col].dt.year

    # Group by year and count the number of accidents per year
    accidents_per_year = data.groupby('Year').size().reset_index(name=new_index_name)

    return accidents_per_year


def plot_combined_accidents(aviation_accidents_per_year, car_crashes_per_year):
    """
    Plots a comparison of aviation accidents and car crashes over time.

    Args:
        aviation_data (pd.DataFrame): The DataFrame containing aviation accident data.
        aviation_date_col (str): The name of the column in `aviation_data` containing the date of the accidents.
        car_crashes_data (pd.DataFrame): The DataFrame containing car crash data.
        car_crashes_date_col (str): The name of the column in `car_crashes_data` containing the date of the crashes.

    Returns:
        None: The function processes the data and prepares it for plotting but does not return a value.
    """

    # Merge the two datasets on the 'Year' column using an inner join
    combined_data = pd.merge(aviation_accidents_per_year, car_crashes_per_year, on='Year', how='inner')

    # Convert the number of accidents to thousands
    combined_data['Aviation Accidents'] /= 1000  # Convert to thousands
    combined_data['Car Crashes'] /= 1000         # Convert to thousands

    # Set the x-axis range to the years in the combined dataset
    x_min, x_max = combined_data['Year'].min(), combined_data['Year'].max()

    # Plot the data
    plt.figure(figsize=(12, 6))
    bar_width = 0.4  # Width of the bars

    # Create bar positions for each dataset
    years = combined_data['Year']
    aviation_positions = years - bar_width / 2
    car_crashes_positions = years + bar_width / 2

    # Plot bars for aviation accidents and car crashes
    plt.bar(aviation_positions, combined_data['Aviation Accidents'], width=bar_width, label='Aviation Accidents (Thousands)', color='skyblue')
    plt.bar(car_crashes_positions, combined_data['Car Crashes'], width=bar_width, label='Car Crashes (Thousands)', color='orange')

    # Add titles and labels
    plt.title('Accidents per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Accidents (Thousands)')  # Update the y-axis label
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlim(x_min - 1, x_max + 1)  # Extend x-axis limits slightly for better spacing
    plt.xticks(years, rotation=45)  # Set x-axis ticks to the years
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    kaggle_interface = KaggleInterface()
    '''
    Download the data.  For the aviation crash data, I download a single file befause the dataset is large
    and I only need one file.  For the car crashes data, I download the entire dataset but it takes a while
    because it needs to be unzipped.
    '''
    aviation_data_file = kaggle_interface.download_single_file_from_dataset("mirzaniazmorshed/ntsb-aviation-accidents", "events.xlsx")
    car_crashes_data_file = kaggle_interface.download_dataset("sobhanmoosavi/us-accidents")

    # Load each dataset into a pandas DataFrame
    aviation_data = kaggle_interface.load_excel_to_dataframe(aviation_data_file)
    car_crashes_data = kaggle_interface.load_csv_to_dataframe(car_crashes_data_file)

    aviation_accidents_per_year = create_accidents_per_year_dataset(aviation_data, "ev_date", 'Aviation Accidents')
    car_crashes_per_year = create_accidents_per_year_dataset(car_crashes_data, "Start_Time", 'Car Crashes')
    
    # Plot combined accidents
    plot_combined_accidents(aviation_accidents_per_year, car_crashes_per_year)