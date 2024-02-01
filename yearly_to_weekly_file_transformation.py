import pandas as pd
import os
from datetime import datetime

def get_week_of_year(day):
    if pd.isna(day):
        return None
    return (day - 1) // 7 + 1

def read_csv_file(file_path, date_column_name):
    # Read the file, keeping rows even if the first column is empty
    data = pd.read_csv(file_path, skiprows=1, keep_default_na=False)

    # Strip whitespace from column names
    data.columns = data.columns.str.strip()

    return data

def parse_dates(data, date_column_name):
    # Convert non-empty strings to datetime, keep empty strings as is
    data[date_column_name] = pd.to_datetime(data[date_column_name], errors='coerce')
    return data

def group_data(data, date_column_name):
    # Calculate "week of year", handling missing values
    data['week_of_year'] = data[date_column_name].dt.dayofyear.apply(get_week_of_year)
    return data.groupby([data[date_column_name].dt.year, 'week_of_year'], dropna=False)

def process_file(file_path, base_path, date_column_name, year_folder, network_folder):
    try:
        data = read_csv_file(file_path, date_column_name)
        if date_column_name not in data.columns:
            print(f"Date column '{date_column_name}' not found in {file_path}. Columns found: {data.columns}")
            return

        data = parse_dates(data, date_column_name)
        for (year, week_of_year), group in group_data(data, date_column_name):
            if pd.isna(year) or pd.isna(week_of_year):
                # Handle rows with missing date values
                week_folder = os.path.join(base_path, 'missing_dates', network_folder)
            else:
                week_folder = os.path.join(base_path, str(int(year)), f'week_{int(week_of_year)}', network_folder)
            os.makedirs(week_folder, exist_ok=True)
            group.to_csv(os.path.join(week_folder, os.path.basename(file_path)), index=False)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def read_and_group_data(base_path, date_column_name='time'):
    for year_folder in os.listdir(base_path):
        year_path = os.path.join(base_path, year_folder)

        # Skip data before the year 2017 and files named 'variables.csv'
        if not year_path.endswith('.csvfile') and int(year_folder) >= 2017:
            if os.path.isdir(year_path):
                for network_folder in os.listdir(year_path):
                    network_path = os.path.join(year_path, network_folder)
                    if os.path.isdir(network_path):
                        for file in os.listdir(network_path):
                            if file == 'variables.csv':  # Skip 'variables.csv'
                                continue
                            file_path = os.path.join(network_path, file)
                            process_file(file_path, base_path, date_column_name, year_folder, network_folder)

base_path = 'data/weather' 
read_and_group_data(base_path, date_column_name='time')
