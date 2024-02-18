import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime

def train(model, X, y, X_test, y_test, n_estimators, learning_rate, early_stopping_rounds):
    if(model == None):
        model = XGBRegressor(n_estimators=n_estimators, learning_rate=learning_rate, early_stopping_rounds=early_stopping_rounds)
    
    model.fit(X, y, eval_set=[(X_test, y_test)], verbose=False)
    predictions = model.predict(X_test)

    # Calculate MAE
    mae = mean_absolute_error(y_test, predictions)
    print('Mean Absolute Error:', mae)

    # Calculate MSE
    mse = mean_squared_error(y_test, predictions)
    print('Mean Squared Error:', mse)

    # Calculate RMSE
    rmse = mean_squared_error(y_test, predictions, squared=False)
    print('Root Mean Squared Error:', rmse)

    return model, mae, mse, rmse

def xgboost_trainer():
    model = None
    
    mae_array = []
    mse_array = []
    rmse_array = []

    # TODO: read in the final weather and satellite data
    for i in range(0, 10):
        X = pd.read_csv("./dummy-data/2016_weather_filtered.csv")
        X = X.values
        X

        y = np.genfromtxt("./dummy-data/2017_burn_filtered.csv", delimiter=',', skip_header=1)
        y

        X_test = pd.read_csv("./dummy-data/2017_weather_filtered.csv")
        X_test = X_test.values
        X_test

        y_test = np.genfromtxt("./dummy-data/2018_burn_filtered.csv", delimiter=',', skip_header=1)
        y_test

        model, mae, mse, rmse = train(model, X, y, X_test, y_test, 1000, 0.01, 50)
        mae_array.append(mae)
        mse_array.append(mse)
        rmse_array.append(rmse)

    save_results(mae_array, mse_array, rmse_array)

def get_run_notes():
    time_step = "time-step-"
    time_step += input("Enter the time step: ")
    fine_areas = "fine-areas-"
    fine_areas += input("Enter the number of fine areas: ")
    return time_step, fine_areas

def save_results(mae_array, mse_array, rmse_array):
    # Get information about this run 
    time_step, fine_areas = get_run_notes()

    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create a folder with the current time as the name
    base_folder_name = "train-results"
    folder_name = f"{base_folder_name}/{current_time}_{time_step}_{fine_areas}"
    try:
        os.mkdir(folder_name)
        print(f"Folder '{folder_name}' created successfully.")
    except FileExistsError:
        print(f"Folder '{folder_name}' already exists.")

    # Mean Absolute Errors Plot
    sns.lineplot(x=range(len(mae_array)), y=mae_array, marker='o')
    plt.xlabel('Index')
    plt.ylabel('Mean Absolute Error')
    plt.title('Mean Absolute Errors Plot')
    plt.savefig(f'{folder_name}/mean_absolute_errors.pdf')
    plt.close()

    # Mean Squared Errors Plot
    sns.lineplot(x=range(len(mse_array)), y=mse_array, marker='o')
    plt.xlabel('Index')
    plt.ylabel('Mean Squared Error')
    plt.title('Mean Squared Errors Plot')
    plt.savefig(f'{folder_name}/mean_squared_errors.pdf')
    plt.close()

    # Root Mean Absolute Errors Plot
    sns.lineplot(x=range(len(rmse_array)), y=rmse_array, marker='o')
    plt.xlabel('Index')
    plt.ylabel('Root Mean Squared Error')
    plt.title('Root Mean Squared Errors Plot')
    plt.savefig(f'{folder_name}/root_mean_squared_errors.pdf')
    plt.close()
    
if __name__ == "__main__":
    xgboost_trainer()
