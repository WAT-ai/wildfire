import pandas as pd 
import numpy as np
import os
import csv

def read_csv_file(file_path, date_column_name):
    # Read the file, keeping rows even if the first column is empty
    data = pd.read_csv(file_path, skiprows=1, keep_default_na=False)

    # Strip whitespace from column names
    data.columns = data.columns.str.strip()

    return data

def get_fire_vector_for_week(kelowna_stations_df, burn_data_df, num_long_splits, num_lat_splits):
    res = np.zeros(num_long_splits * num_lat_splits)

    longitude_max = kelowna_stations_df['Longitude'].max()
    longitude_min = kelowna_stations_df['Longitude'].min()
    latitude_max = kelowna_stations_df['Latitude'].max()
    latitude_min = kelowna_stations_df['Latitude'].min()
    longitude_distance = longitude_max - longitude_min
    latitude_distance = latitude_max - latitude_min
    
    long_split_distance = longitude_distance / num_long_splits
    lat_split_distance = latitude_distance / num_lat_splits
    
    long_track = longitude_min
    lat_track = latitude_min
    print(f"min_long = {longitude_min}, min_lat = {latitude_min}, max_long = {longitude_max}, max_lat = {latitude_max}, long_split = {long_split_distance}, lat_split = {lat_split_distance}")
    
    for i in range(num_lat_splits):
        lat_track = latitude_min + i * lat_split_distance
        for j in range(num_long_splits):
            long_track = longitude_min + j * long_split_distance
            
            latitude_mask_burn = (burn_data_df['LATITUDE'] < lat_track + lat_split_distance) & (burn_data_df['LATITUDE'] >= lat_track)
            longitude_mask_burn = (burn_data_df['LONGITUDE'] < long_track + long_split_distance) & (burn_data_df['LONGITUDE'] >= long_track)
            
            single_burn = burn_data_df[latitude_mask_burn & longitude_mask_burn]['FIRE_SIZE_HA'].sum(axis=0)
            res[j + i * num_long_splits] = single_burn
            
        long_track = longitude_min
    
    return res

def numpy_array_to_csv_column_vector(numpy_array, output_file):
    # Reshape the numpy array to a column vector
    column_vector = numpy_array.reshape(-1, 1)

    # Save the column vector to a CSV file
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(column_vector)

def main():
    print("hi")
    kelowna_stations_df = pd.read_csv('./data/weather-stations/kelowna/kelowna_stations.csv')
    num_long_splits = 12
    num_lat_splits = 12

    base_path = 'data/satellite-burn'
    for year_folder in os.listdir(base_path):
        year_path = os.path.join(base_path, year_folder)
        if os.path.isdir(year_path):
            for file in os.listdir(year_path):
                week_num = 1
                
                file_path = os.path.join(year_path, file)
                burn_data_df = pd.read_csv(file_path)
                
                week_fire = get_fire_vector_for_week(kelowna_stations_df, burn_data_df, num_long_splits, num_lat_splits)
                week_fire_df = pd.DataFrame(week_fire)
                week_fire_df.to_csv(f'data/final-satellite-burn/{year_folder}/week_{week_num}.csv')

                week_num += 1

main()
        