#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from kaggle_interface import KaggleInterface

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

    # Find the overlapping years
    overlapping_years = combined_data['Year'][
        (combined_data['Aviation Accidents'] > 0) & (combined_data['Car Crashes'] > 0)
    ]

    # Set the x-axis range to the overlapping years
    x_min, x_max = overlapping_years.min(), overlapping_years.max()

    # Convert the number of accidents to thousands
    combined_data['Aviation Accidents'] /= 1000  # Convert to thousands
    combined_data['Car Crashes'] /= 1000         # Convert to thousands

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

    # Plot combined accidents
    plot_combined_accidents(aviation_data, "ev_date", car_crashes_data, "Start_Time")