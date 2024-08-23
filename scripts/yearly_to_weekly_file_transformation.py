import pandas as pd
import os
from datetime import datetime

# Function to calculate the week of the year from a day number
def get_week_of_year(day):
    if pd.isna(day):
        return None
    return (day - 1) // 7 + 1

# Function to read a CSV file while keeping rows even if the first column is empty
def read_csv_file(file_path, date_column_name):
    data = pd.read_csv(file_path, skiprows=1, keep_default_na=False)
    # Strip any whitespace from column names
    data.columns = data.columns.str.strip()
    return data

# Function to parse dates in a specified column
def parse_dates(data, date_column_name):
    # Convert non-empty strings to datetime, keep empty strings as is
    data[date_column_name] = pd.to_datetime(data[date_column_name], errors='coerce')
    return data

# Function to group data by year and week of year, handling missing date values
def group_data(data, date_column_name):
    # Calculate "week of year" for each date, handling missing values
    data['week_of_year'] = data[date_column_name].dt.dayofyear.apply(get_week_of_year)
    return data.groupby([data[date_column_name].dt.year, 'week_of_year'], dropna=False)

# Function to process each file, group data by week, and save grouped data into separate folders
def process_file(file_path, base_path, date_column_name, year_folder, network_folder):
    try:
        data = read_csv_file(file_path, date_column_name)
        if date_column_name not in data.columns:
            print(f"Date column '{date_column_name}' not found in {file_path}. Columns found: {data.columns}")
            return

        data = parse_dates(data, date_column_name)
        grouped_data = group_data(data, date_column_name)

        for (year, week_of_year), group in grouped_data:
            if pd.isna(year) or pd.isna(week_of_year):
                # Handle rows with missing date values
                week_folder = os.path.join(base_path, 'missing_dates', network_folder)
            else:
                week_folder = os.path.join(base_path, str(int(year)), f'week_{int(week_of_year)}', network_folder)
            
            os.makedirs(week_folder, exist_ok=True)
            output_file_path = os.path.join(week_folder, os.path.basename(file_path))
            group.to_csv(output_file_path, index=False)

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Function to iterate over directories, read and group data by week
def read_and_group_data(base_path, date_column_name='time'):
    for year_folder in os.listdir(base_path):
        year_path = os.path.join(base_path, year_folder)

        # Skip files before 2016 and any file named 'variables.csv'
        if not year_path.endswith('.csvfile') and 2016 <= int(year_folder) <= 2023:
            if os.path.isdir(year_path):
                for network_folder in os.listdir(year_path):
                    network_path = os.path.join(year_path, network_folder)
                    if os.path.isdir(network_path):
                        for file in os.listdir(network_path):
                            if file == 'variables.csv':  # Skip 'variables.csv'
                                continue
                            file_path = os.path.join(network_path, file)
                            process_file(file_path, base_path, date_column_name, year_folder, network_folder)

# Main function to set up paths and initiate the processing
def main():
    # Set the base path for the raw weather data
    base_path = './data/raw/weather'
    
    # Call the function to read and group data by week
    read_and_group_data(base_path, date_column_name='time')

# Entry point of the script
if __name__ == "__main__":
    main()