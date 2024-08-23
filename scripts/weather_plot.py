import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 

# Function to load and prepare weather data from multiple CSV files
def load_and_prepare_data(file_paths):
    all_data = []

    # Process each file in the list of file paths
    for file_path in file_paths:
        # Extract the group number from the file name
        group_number = int(file_path.split('_')[-1].split('.')[0])
        
        # Calculate the corresponding year and quarter based on the group number
        year = 2017 + (group_number - 1) // 4
        quarter = 'Q' + str(((group_number - 1) % 4) + 1)

        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Add year and quarter information to the DataFrame
        df['year'] = year
        df['quarter'] = quarter

        # Append the DataFrame to the list of all data
        all_data.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_data = pd.concat(all_data, ignore_index=True)

    return combined_data

# Function to create individual box plots for specified weather parameters
def create_individual_plots(data, parameters):
    # Set the style for the plots
    sns.set_style("whitegrid")
    
    # Create a box plot for each parameter
    for parameter in parameters:
        plt.figure(figsize=(12, 6))
        
        # Create the box plot
        sns.boxplot(x='quarter', y=parameter, hue='year', data=data, palette='pastel')
        
        # Set titles and labels
        plt.title(f'{parameter.replace("_", " ").capitalize()} vs Quarters', fontsize=16)
        plt.xlabel('Quarter', fontsize=14)
        plt.ylabel(parameter.replace("_", " ").capitalize(), fontsize=14)
        
        # Adjust legend position
        plt.legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
        plt.tight_layout()

        # Save each plot to a separate file
        plt.savefig(f'data/{parameter}_box_plot.png')
        plt.close()  # Close the plot to free up memory

def main():
    # Define the file paths for the weather data files
    file_paths = [f'data/training/quarterly-6-by-6/weather/group_{i}.csv' for i in range(1, 25)]
    
    # Load and prepare the weather data
    weather_data = load_and_prepare_data(file_paths)

    # List of weather parameters to plot
    parameters = ['precipitation', 'temperature', 'relative_humidity', 'wind_direction', 'wind_speed']

    # Create and save the plots
    create_individual_plots(weather_data, parameters)


if __name__ == "__main__":
    main()