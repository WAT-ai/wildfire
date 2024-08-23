import pandas as pd 
import numpy as np
import os

# Function to calculate the fire vector for a specific week based on geographical splits
def get_fire_vector_for_week(kelowna_stations_df, burn_data_df, num_long_splits, num_lat_splits):
    # Initialize a result array with zeros to store fire sizes for each grid cell
    res = np.zeros(num_long_splits * num_lat_splits)

    # Determine the boundaries for the region covered by the stations
    longitude_max = kelowna_stations_df['Longitude'].max()
    longitude_min = kelowna_stations_df['Longitude'].min()
    latitude_max = kelowna_stations_df['Latitude'].max()
    latitude_min = kelowna_stations_df['Latitude'].min()

    # Calculate the total distance covered in both longitude and latitude
    longitude_distance = longitude_max - longitude_min
    latitude_distance = latitude_max - latitude_min
    
    # Calculate the size of each split in longitude and latitude
    long_split_distance = longitude_distance / num_long_splits
    lat_split_distance = latitude_distance / num_lat_splits
    
    # Iterate through each latitude split
    for i in range(num_lat_splits):
        lat_track = latitude_min + i * lat_split_distance  # Update latitude tracker
        # Iterate through each longitude split within the current latitude split
        for j in range(num_long_splits):
            long_track = longitude_min + j * long_split_distance  # Update longitude tracker
            
            # Create masks to filter burn data within the current grid cell
            latitude_mask_burn = (burn_data_df['LATITUDE'] < lat_track + lat_split_distance) & (burn_data_df['LATITUDE'] >= lat_track)
            longitude_mask_burn = (burn_data_df['LONGITUDE'] < long_track + long_split_distance) & (burn_data_df['LONGITUDE'] >= long_track)
            
            # Sum the fire sizes within the current grid cell and store it in the result array
            single_burn = burn_data_df[latitude_mask_burn & longitude_mask_burn]['FIRE_SIZE_HA'].sum(axis=0)
            res[j + i * num_long_splits] = single_burn
    
    return res

# Function to generate a DataFrame representing the fire vector for a specific week
def get_week_fire_df(file_path, kelowna_stations_df, num_long_splits, num_lat_splits):
    # Read the burn data for the week from the CSV file
    burn_data_df = pd.read_csv(file_path)
    
    # Calculate the fire vector based on the burn data and station data
    week_fire = get_fire_vector_for_week(kelowna_stations_df, burn_data_df, num_long_splits, num_lat_splits)
    
    # Convert the fire vector into a DataFrame and return it
    week_fire_df = pd.DataFrame(week_fire)
    return week_fire_df


def main():
    # Read the station data for Kelowna
    kelowna_stations_df = pd.read_csv('./data/processing/weather-stations/kelowna/kelowna_stations.csv')

    # Set the number of splits for longitude and latitude
    num_long_splits = 6
    num_lat_splits = 6

    # Base path for the satellite burn data
    base_path = './data/processing/satellite-burn'
    
    # Iterate through each year folder in the base directory
    for year_folder in os.listdir(base_path):
        weeks = [0] * 52  # Initialize a list to track the presence of weekly data
        
        year_path = os.path.join(base_path, year_folder)
        
        # Check if the path is a directory and if it represents a valid year between 2017 and 2023
        if not year_path.endswith('.csv') and year_folder.isdigit() and 2017 <= int(year_folder) <= 2023:
            if os.path.isdir(year_path):
                # Process each file in the year folder (each file represents a week)
                for file in os.listdir(year_path):
                    file_path = os.path.join(year_path, file)
                    print(f"Reading file: {file_path}")
                    
                    # Extract the week number from the filename
                    week_num = int(file.split('_')[1].split('.')[0])
                    weeks[week_num - 1] = 1  # Mark the week as present

                    # Generate the fire vector for the week and save it as a CSV
                    week_fire_df = get_week_fire_df(file_path, kelowna_stations_df, num_long_splits, num_lat_splits)
                    week_fire_df.to_csv(f'./data/processing/final-satellite-burn/{year_folder}/{file}', index=False, header=None)
        
        # Generate zeroed fire vector files for missing weeks
        for i in range(52):
            if weeks[i] == 0:
                print(f"Missing week: {i + 1}")
                zero_df = pd.DataFrame(np.zeros(num_long_splits * num_lat_splits))
                zero_df.to_csv(f'./data/processing/final-satellite-burn/{year_folder}/week_{i + 1}.csv', index=False, header=None)

if __name__ == "__main__":
    main()