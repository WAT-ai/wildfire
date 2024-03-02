import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize

def get_color_for_value(value, cmap, min_value, max_value):
    norm = Normalize(vmin=min_value, vmax=max_value)
    return cmap(norm(value))

def create_color_map(color_matrix, cmap=cm.coolwarm):
    norm = Normalize(vmin=np.min(color_matrix), vmax=np.max(color_matrix))
    cmap = cm.coolwarm  # You can choose a different colormap if desired
    norm = Normalize(vmin=min(map(min, color_matrix)), vmax=max(map(max, color_matrix)))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    return cmap, sm


def draw_grid(matrix, error_matrix, color_matrix, filename='output_plot.pdf'):  # Set the default filename
    # # Create a color map
    # norm = Normalize(vmin=np.min(color_matrix), vmax=np.max(color_matrix))
    # cmap = cm.coolwarm  # You can choose a different colormap if desired
    # norm = Normalize(vmin=min(map(min, color_matrix)), vmax=max(map(max, color_matrix)))
    # sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    # sm.set_array([])
    cmap, sm = create_color_map(color_matrix)

    rows, cols = len(matrix), len(matrix[0])

    fig, ax = plt.subplots()

    # Draw horizontal lines
    for i in range(rows + 1):
        ax.axhline(i, color='black')

    # Draw vertical lines
    for i in range(cols + 1):
        ax.axvline(i, color='black')

    # Display numbers in the grid with at most 3 digits and fill cells based on color_matrix
    for i in reversed(range(rows)):
        for j in reversed(range(cols)):
            number = matrix[i][j]
            formatted_number = '{:.3f}'.format(number)[:6]  # Ensure at most 3 digits before the decimal point
            
            error_value = error_matrix[i][j]
            color = get_color_for_value(error_value, cmap, np.min(color_matrix), np.max(color_matrix))

            ax.add_patch(plt.Rectangle((j, i), 1, 1, fill=True, color=color))
            ax.text(j + 0.5, i + 0.5, formatted_number, ha='center', va='center', fontsize=12, color='white')

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_xticks([])  # Remove x-axis ticks
    ax.set_yticks([])  # Remove y-axis ticks
    ax.invert_yaxis()

    # Add color bar
    cbar = plt.colorbar(sm, ax=ax, orientation='vertical', pad=0.02)
    cbar.set_label('Absolute Error', rotation=270, labelpad=15)
    cbar.set_ticks([np.min(color_matrix), np.max(color_matrix)])
    cbar.set_ticklabels(['{:.3f}'.format(np.min(color_matrix)), '{:.3f}'.format(np.max(color_matrix))])

    # Add label above the matrix (centered with the matrix)
    plt.text(cols / 2, rows + 0.5, 'Predicted Values', ha='center', va='center', fontsize=14)

    plt.grid(False)

    # Save the plot as a PDF file
    plt.savefig(filename, format='pdf')

    # Show the plot (if needed)
    # plt.show()

def main():
    ref_abs_error = None
    base_path = "./train-results/predicted-data-vis/"

    data_files = ["burn_6.csv", "burn_11.csv", "burn_16.csv", "burn_21.csv"]
    for file in data_files:
        df = pd.read_csv(base_path + file)
        df['absolute_error'] = abs(df['Actual'] - df['Predicted'])

        actual = np.array(df['Actual']).reshape(6, 6)
        predicted = np.array(df['Predicted']).reshape(6, 6)
        abs_error = np.array(df['absolute_error']).reshape(6, 6)

        # set the color scale to have the same range for all plots
        if file == "burn_6.csv":
            color_matrix = abs_error

        draw_grid(predicted, abs_error, color_matrix, filename=f'{base_path}{file.replace(".csv", "")}.pdf')

if __name__ == '__main__':
    main()