import pandas as pd
import numpy as np
import os


def data_ingestion():
    print("Data Ingestion")
    
    # Idea: keep n be weather data and n+1 be burn data
    # Week 1: weather year x week 1, burn year x week 2
    # Week 52: weather year x week 52, burn year x+1 week 1
    
    for year in range(2017, 2023):
        year_burn_path = os.path.join('data/final-satellite-burn/', str(year))
        year_weather_path = os.path.join('data/final-weather/', str(year))
        for week in range(1, 53):
            year_week_burn_path = ""
            year_week_weather_path = os.path.join(year_weather_path, "week_" + str(week) + '.csv')
            # Normal case (week 1-51)
            if week <= 51:
                year_week_burn_path = os.path.join(year_burn_path, "week_" + str(week + 1) + '.csv')
            
            # Edge case (week 52)
            if week == 52 and year != 2022:
                new_year_path = os.path.join('data/final-satellite-burn/', str(year + 1))
                year_week_burn_path = os.path.join(new_year_path, "week_1.csv")
                
            
            print("Comparing burn data from: " + year_week_burn_path + " with weather data from: " + year_week_weather_path)
            
            # Sanity check for right files
            if year_week_burn_path != "":
                burn_data_df = pd.read_csv(year_week_burn_path)
                weather_data_df = pd.read_csv(year_week_weather_path)
                print("Burn data: " + burn_data_df.head(144).to_string())
                # print("Weather data: " + str(weather_data_df.shape)) incomplete weather data
            else:
                break

def main():
    data_ingestion()

if __name__ == "__main__":
    main()
