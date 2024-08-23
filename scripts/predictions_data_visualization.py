import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize

# Function to get a color from a colormap based on a value
def get_color_for_value(value, cmap, min_value, max_value):
    norm = Normalize(vmin=min_value, vmax=max_value)
    return cmap(norm(value))

# Function to create a colormap and ScalarMappable object for the color bar
def create_color_map(color_matrix, cmap=cm.coolwarm):
    # Normalize the color matrix to determine the range of the colormap
    norm = Normalize(vmin=np.min(color_matrix), vmax=np.max(color_matrix))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # Set the array to empty for color bar usage
    return cmap, sm

# Function to draw the grid with the predicted values, errors, and color mapping
def draw_grid(matrix, error_matrix, color_matrix, filename='output_plot.pdf'):
    # Create a colormap and a ScalarMappable for the color bar
    cmap, sm = create_color_map(color_matrix)

    rows, cols = len(matrix), len(matrix[0])

    # Initialize the plot
    fig, ax = plt.subplots()

    # Draw grid lines for the cells
    for i in range(rows + 1):
        ax.axhline(i, color='black')
    for i in range(cols + 1):
        ax.axvline(i, color='black')

    # Fill each cell with color and display the predicted values
    for i in reversed(range(rows)):
        for j in reversed(range(cols)):
            # Format the predicted number to 3 decimal places
            number = matrix[i][j]
            formatted_number = '{:.3f}'.format(number)[:6]
            
            # Get the error value and corresponding color for the cell
            error_value = error_matrix[i][j]
            color = get_color_for_value(error_value, cmap, np.min(color_matrix), np.max(color_matrix))

            # Draw the cell with the appropriate color and add the text
            ax.add_patch(plt.Rectangle((j, i), 1, 1, fill=True, color=color))
            ax.text(j + 0.5, i + 0.5, formatted_number, ha='center', va='center', fontsize=12, color='white')

    # Set limits and remove ticks
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_xticks([])  # Remove x-axis ticks
    ax.set_yticks([])  # Remove y-axis ticks
    ax.invert_yaxis()  # Invert y-axis to match typical matrix layout

    # Add a color bar to the right of the plot
    cbar = plt.colorbar(sm, ax=ax, orientation='vertical', pad=0.02)
    cbar.set_label('Absolute Error', rotation=270, labelpad=15)
    cbar.set_ticks([np.min(color_matrix), np.max(color_matrix)])
    cbar.set_ticklabels(['{:.3f}'.format(np.min(color_matrix)), '{:.3f}'.format(np.max(color_matrix))])

    # Add a label above the grid
    plt.text(cols / 2, rows + 0.5, 'Predicted Values', ha='center', va='center', fontsize=14)

    plt.grid(False)

    # Save the plot as a PDF file
    plt.savefig(filename, format='pdf')

# Main function to read data, calculate errors, and draw the grids
def main():
    color_matrix = None
    base_path = "./train-results/predicted-data-vis/"

    # List of CSV files to process
    data_files = ["burn_6.csv", "burn_11.csv", "burn_16.csv", "burn_21.csv"]

    for file in data_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(base_path + file)
        
        # Calculate the absolute error between the actual and predicted values
        df['absolute_error'] = abs(df['Actual'] - df['Predicted'])

        # Reshape the data into 6x6 matrices for visualization
        actual = np.array(df['Actual']).reshape(6, 6)
        predicted = np.array(df['Predicted']).reshape(6, 6)
        abs_error = np.array(df['absolute_error']).reshape(6, 6)

        # Set the color scale based on the first file's error matrix
        if file == "burn_6.csv":
            color_matrix = abs_error

        # Draw the grid and save the output as a PDF
        draw_grid(predicted, abs_error, color_matrix, filename=f'{base_path}{file.replace(".csv", "")}.pdf')

if __name__ == '__main__':
    main()