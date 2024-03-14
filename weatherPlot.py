import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 

def load_and_prepare_data(file_paths):
    all_data = []

    for file_path in file_paths:
        group_number = int(file_path.split('_')[-1].split('.')[0])
        year = 2017 + (group_number - 1) // 4
        quarter = 'Q' + str(((group_number - 1) % 4) + 1)

        df = pd.read_csv(file_path)
        df['year'] = year
        df['quarter'] = quarter

        all_data.append(df)

    combined_data = pd.concat(all_data, ignore_index=True)

    return combined_data

file_paths = [f'data/training/quarterly-6-by-6/weather/group_{i}.csv' for i in range(1, 25)]
weather_data = load_and_prepare_data(file_paths)

def create_individual_plots(data, parameters):
    sns.set_style("whitegrid")
    
    for parameter in parameters:
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='quarter', y=parameter, hue='year', data=data, palette='pastel')
        plt.title(f'{parameter.replace("_", " ").capitalize()} vs Quarters', fontsize=16)
        plt.xlabel('Quarter', fontsize=14)
        plt.ylabel(parameter.replace("_", " ").capitalize(), fontsize=14)
        plt.legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
        plt.tight_layout()

        # Save each plot to a separate file
        plt.savefig(f'data/{parameter}_box_plot.png')
        plt.close()  # Close the plot to free up memory

parameters = ['precipitation', 'temperature', 'relative_humidity', 'wind_direction', 'wind_speed']

create_individual_plots(weather_data, parameters)