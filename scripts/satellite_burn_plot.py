import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 
import plotly.express as px

# Function to load and prepare burn data from multiple CSV files
def load_and_prepare_burn_data(file_paths):
    all_data = []

    # Process each file in the list of file paths
    for file_path in file_paths:
        # Extract group number from the file name
        group_number = int(file_path.split('_')[-1].split('.')[0])

        # Calculate the corresponding year and quarter based on group number
        year = 2017 + (group_number - 1) // 4
        quarter = 'Q' + str(((group_number - 1) % 4) + 1)

        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path, header=None, names=['hectares_burned'])

        # Add year and quarter information to the DataFrame
        df['year'] = year
        df['quarter'] = quarter

        # Append the DataFrame to the list of all data
        all_data.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_data = pd.concat(all_data, ignore_index=True)

    return combined_data

# Function to create static box plots of burn data by quarter
def create_burn_box_plots(data):
    # Set the style of the plot
    sns.set_style("whitegrid")
    
    # Create a figure with specified size
    plt.figure(figsize=(12, 6))
    
    # Create a box plot showing hectares burned by quarter and year
    sns.boxplot(x='quarter', y='hectares_burned', hue='year', data=data, palette='pastel', showfliers=False)

    # Add titles and labels
    plt.title('Hectares Burned vs Quarters', fontsize=16)
    plt.xlabel('Quarter', fontsize=14)
    plt.ylabel('Hectares Burned', fontsize=14)

    # Adjust legend position
    plt.legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

    # Set the y-axis limit and adjust layout
    plt.ylim(0, 5000)
    plt.tight_layout()
    
    # Save the plot as an image
    plt.savefig('data/satellite_burn_box_plots_capped.png')

    # Show the plot
    plt.show()

# Function to create interactive box plots using Plotly
def create_burn_box_plots_interactive(data):
    # Create an interactive box plot with Plotly
    fig = px.box(data, x='quarter', y='hectares_burned', color='year',
                 labels={'hectares_burned': 'Hectares Burned', 'quarter': 'Quarter'},
                 title='Hectares Burned vs Quarters')
    
    # Update the method for calculating quartiles
    fig.update_traces(quartilemethod="inclusive")
    
    # Set the y-axis range
    fig.update_layout(yaxis=dict(range=[0, 25000]))
    
    # Display the interactive plot
    fig.show()

def main():
    # List of file paths to be loaded and processed
    burn_file_paths = [f'data/training/quarterly-6-by-6/satellite-burn/group_{i}.csv' for i in range(1, 29)]
    
    # Load and prepare the burn data
    burn_data = load_and_prepare_burn_data(burn_file_paths)
    
    # Create static box plots
    create_burn_box_plots(burn_data)

if __name__ == "__main__":
    main()