import pandas as pd
import os
from datetime import datetime
from pathlib import Path

def get_weekly_averaged_df(week_path):
    file_list = Path(week_path).glob('*')

    # Read CSV files and calculate averages
    dfs = []
    for file in file_list:
        df = pd.read_csv(file, skipinitialspace=True)  # skipinitialspace to remove extra spaces in column names
        # Convert columns to numeric, handling errors with coerce to replace invalid values with NaN
        df = df.apply(pd.to_numeric, errors='coerce')
        # Calculate average of each column
        averaged_row = df.mean(axis=0)
        dfs.append(averaged_row)

    # Concatenate averaged values into one DataFrame
    averaged_df = pd.concat(dfs, axis=1).transpose()
    print(averaged_df)

def group_and_interpolate():
    # TODO: replace rows and cols with the long and lat splits 
    rows = 6
    cols = 6
    num_fine_areas = rows * cols
    
    base_path = 'data/final-weather'

    for year_folder in os.listdir(base_path):
        year_path = os.path.join(base_path, year_folder)

        for week_num in range(1, 53):
            week_path = os.path.join(year_path, f'week_{week_num}')
            # get_weekly_averaged_df(week_path)

            if not os.path.exists(week_path):
                print(f"Path {week_path} does not exist")
                continue

            ## TODO: use aryan's code to push values into the df and threshold
            # use a set to keep track of the indices that are empty
            # put the threshold filtered df into the matrix
            # perform interpolation 
            # grab everything back into a df

        # for week_folder in os.listdir(year_path):
        #     matrix = [[0 for _ in range(cols)] for _ in range(rows)]
        #     week_path = os.path.join(year_path, week_folder)
        #     get_weekly_averaged_df(week_path)

if __name__ == "__main__":
    group_and_interpolate()