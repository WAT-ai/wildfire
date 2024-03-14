import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 
import plotly.express as px

def load_and_prepare_burn_data(file_paths):
    all_data = []

    for file_path in file_paths:
        group_number = int(file_path.split('_')[-1].split('.')[0])

        year = 2017 + (group_number - 1) // 4
        quarter = 'Q' + str(((group_number - 1) % 4) + 1)

        df = pd.read_csv(file_path, header=None, names=['hectares_burned'])

        df['year'] = year
        df['quarter'] = quarter

        all_data.append(df)

    combined_data = pd.concat(all_data, ignore_index=True)

    return combined_data

burn_file_paths = [f'data/training/quarterly-6-by-6/satellite-burn/group_{i}.csv' for i in range(1, 29)]  # Files from group_1 to group_10
burn_data = load_and_prepare_burn_data(burn_file_paths)

def create_burn_box_plots(data):
    
    sns.set_style("whitegrid")
    
    plt.figure(figsize=(12, 6))
    
    sns.boxplot(x='quarter', y='hectares_burned', hue='year', data=data, palette='pastel', showfliers=False)

    plt.title('Hectares Burned vs Quarters', fontsize=16)
    plt.xlabel('Quarter', fontsize=14)
    plt.ylabel('Hectares Burned', fontsize=14)

    
    plt.legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

    
    plt.ylim(0, 5000)
    plt.tight_layout()
    plt.savefig('data/satellite_burn_box_plots_capped.png')

    # Show the plot
    plt.show()


def create_burn_box_plots_interactive(data):
    fig = px.box(data, x='quarter', y='hectares_burned', color='year',
                 labels={'hectares_burned': 'Hectares Burned', 'quarter': 'Quarter'},
                 title='Hectares Burned vs Quarters')
    fig.update_traces(quartilemethod="inclusive")  # Or "exclusive", depending on how you want to calculate quartiles
    fig.update_layout(yaxis=dict(range=[0, 25000]))
    fig.show()


#create_burn_box_plots_interactive(burn_data)
create_burn_box_plots(burn_data)