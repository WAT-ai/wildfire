import pandas as pd 
import numpy as np
import os

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
    # print(f"min_long = {longitude_min}, min_lat = {latitude_min}, max_long = {longitude_max}, max_lat = {latitude_max}, long_split = {long_split_distance}, lat_split = {lat_split_distance}")
    
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

def get_week_fire_df(file_path, kelowna_stations_df, num_long_splits, num_lat_splits):
    burn_data_df = pd.read_csv(file_path)
    week_fire = get_fire_vector_for_week(kelowna_stations_df, burn_data_df, num_long_splits, num_lat_splits)
    week_fire_df = pd.DataFrame(week_fire)
    return week_fire_df

def main():
    kelowna_stations_df = pd.read_csv('./data/weather-stations/kelowna/kelowna_stations.csv')
    num_long_splits = 12
    num_lat_splits = 12

    base_path = 'data/satellite-burn'
    # For every year
    for year_folder in os.listdir(base_path):
        # Make a 52 long array
        weeks = [0] * 52
        
        year_path = os.path.join(base_path, year_folder)
        # Check if it is a directory and it is a year
        if not year_path.endswith('.csv') and year_folder.isdigit() and 2017 <= int(year_folder) <= 2023:
            if os.path.isdir(year_path):
                # For every file in the year (every week)
                for file in os.listdir(year_path):
                    file_path = os.path.join(year_path, file)
                    print(f"Reading file: {file_path}")
                    print(f"File: {file}")
                    week_num = int(file.split('_')[1].split('.')[0])
                    weeks[week_num - 1] = 1

                    week_fire_df = get_week_fire_df(file_path, kelowna_stations_df, num_long_splits, num_lat_splits)
                    week_fire_df.to_csv(f'data/final-satellite-burn/{year_folder}/{file}', index=False, header=None)
        
        for i in range(52):
            if weeks[i] == 0 and year_folder.isdigit() and 2017 <= int(year_folder) <= 2023:
                print(f"Missing week: {i + 1}")
                zero_df = pd.DataFrame(np.zeros(num_long_splits * num_lat_splits))
                zero_df.to_csv(f'data/final-satellite-burn/{year_folder}/week_{i + 1}.csv', index=False, header=None)

main()
        