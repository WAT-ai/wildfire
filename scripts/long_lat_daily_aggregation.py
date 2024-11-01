import pandas as pd
import numpy as np
import os
from datetime import datetime

# change this to just use a pandas df, with rows
def meta_data(meta_data_path):
    meta_data_df = pd.read_csv(meta_data_path)
    meta_data_df = meta_data_df[["Network Name","Native ID","Longitude","Latitude","Elevation (m)"]]
    meta_data_df[["Longitude","Latitude","Elevation (m)"]] = meta_data_df[["Longitude","Latitude","Elevation (m)"]].apply(pd.to_numeric, errors='coerce')
    return meta_data_df

def aggregate_weather_data(weather_data_path, year_range, meta_data_df, output_path):
    all_dataframes = []

    for year_folder in os.listdir(weather_data_path):
        if year_range[0] <= year_folder <= year_range[1]:
            for network_folder in os.listdir(os.path.join(weather_data_path, year_folder)):
                if network_folder.startswith("week"):
                    continue
                # store network folder name
                network_name = network_folder
                print(f"Year: {year_folder} Network: {network_folder}")

                # iterate through weather stations
                for station_file in os.listdir(os.path.join(weather_data_path, year_folder, network_folder)):
                    if station_file.endswith('.csv') and station_file != 'variables.csv':
                        
                        native_id = station_file.removesuffix('.csv')
                        file_path = os.path.join(weather_data_path, year_folder, network_folder, station_file)

                        df = pd.read_csv(file_path, skiprows=1)
                        df.columns = df.columns.str.strip()

                        if 'time' not in df.columns:
                            print(f"Date column not found in file: {network_name} {station_file}")
                            continue

                        df['time'] = pd.to_datetime(df['time'], errors='coerce')

                        for col in df.columns:
                            if col != 'time':
                                df[col] = pd.to_numeric(df[col], errors='coerce')

                        df_daily_average = df.groupby(df['time'].dt.date).mean()
                        df_daily_average["Network Name"] = network_name
                        df_daily_average['Native ID'] = native_id
                                 
                        if df_daily_average is not None:
                            all_dataframes.append(df_daily_average)

    combined_df = pd.concat(all_dataframes, axis=0, ignore_index=True, sort=True)
    combined_df.replace("", None, inplace=True)
    
    meta_data_df['Native ID'] = meta_data_df['Native ID'].astype(str)
    combined_df['Native ID'] = combined_df['Native ID'].astype(str)

    meta_data_df['Network Name'] = meta_data_df['Network Name'].astype(str)
    combined_df['Network Name'] = combined_df['Network Name'].astype(str)
    print(combined_df)

    merged_df = pd.merge(meta_data_df, combined_df, on=['Network Name', 'Native ID'])

    merged_df.rename(columns = {'time':'Date'}, inplace = True)
    date_column = merged_df.pop('Date') 
    merged_df.insert(4, 'Date', date_column)    
    merged_df['Date'] = merged_df['Date'].dt.date 
    
    merged_df.to_csv(output_path, index=False)


def main():
    pd.set_option('display.max_columns', None)
    meta_data_path = './data/raw/weather_stations.csv'
    weather_data_path = './data/raw/weather'
    output_path = './data/daily_aggregated_data/daily_aggregated_data.csv'
    
    year_range=['2022','2022']

    meta_data_df = meta_data(meta_data_path)
    aggregate_weather_data(weather_data_path, year_range, meta_data_df, output_path)

if __name__ == '__main__':
    main()