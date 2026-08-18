
import pandas as pd
import os
import random

def generate_dummy_forecast(model_name, num_quarters=20):
    # This function simulates sales forecasts for a given number of quarters.
    quarters = [f'Q{i}' for i in range(1, num_quarters + 1)]

    # Generate dummy sales data with some variation
    if model_name == 'naive':
        sales = [100 + i * 5 + random.randint(-10, 10) for i in range(num_quarters)]
    elif model_name == 'arima':
        sales = [150 + i * 8 + random.randint(-20, 20) for i in range(num_quarters)]
    elif model_name == 'analog_only':
        sales = [120 + i * 7 + random.randint(-15, 15) for i in range(num_quarters)]
    elif model_name == 'bass_only':
        # Simulate a Bass diffusion curve for dummy data
        # In a real scenario, you'd use a proper Bass diffusion model implementation.
        # This is a highly simplified dummy to show a different trend.
        M = 1000 # Market potential
        p, q = 0.03, 0.38 # Example Bass parameters
        sales = []
        cumulative_sales = 0
        for t in range(num_quarters):
            # A simplified Bass model formula for new adopters
            adopters = M * (p + q * (cumulative_sales / M)) * (1 - (cumulative_sales / M))
            sales.append(max(0, int(adopters + random.randint(-10, 10))))
            cumulative_sales += sales[-1]
            if cumulative_sales >= M * 0.95: # Cap cumulative sales near market potential
                sales[-1] = max(0, int(M - (cumulative_sales - sales[-1]) + random.randint(-5, 5)))
                cumulative_sales = M

    elif model_name == 'analog_bass_static':
        sales = [130 + i * 9 + random.randint(-25, 25) for i in range(num_quarters)]
    elif model_name == 'analog_bass_adaptive':
        sales = [140 + i * 10 + random.randint(-30, 30) for i in range(num_quarters)]
    else:
        sales = [100 + i * 6 + random.randint(-12, 12) for i in range(num_quarters)]

    df_forecast = pd.DataFrame({
        'quarter': quarters,
        'forecast_sales': sales
    })
    return df_forecast

def main():
    base_directory = 'GROUP21_BASELINE'
    new_member_name = 'kaviya'

    # Define paths for input engineered features
    features_input_path = os.path.join(base_directory, f'member_{new_member_name}', '03_features')

    # Define output path for forecasts
    models_output_path = os.path.join(base_directory, f'member_{new_member_name}', '04_models')
    os.makedirs(models_output_path, exist_ok=True)

    # Load engineered features (as dummy input for model training conceptualization)
    try:
        df_analog_engineered_features = pd.read_csv(os.path.join(features_input_path, 'analog_engineered_features.csv'))
        df_new_drug_engineered_features = pd.read_csv(os.path.join(features_input_path, 'new_drug_engineered_features.csv'))
        df_final_model_input = pd.read_csv(os.path.join(features_input_path, 'final_model_input.csv'))
    except FileNotFoundError as e:
        print(f"Error loading engineered features: {e}. Make sure 04_feature_engineering.py has been run.")
        return

    # List of models to simulate
    model_names = [
        'naive',
        'arima',
        'analog_only',
        'bass_only',
        'analog_bass_static',
        'analog_bass_adaptive'
    ]

    print("Generating and Saving Dummy Forecasts...")
    for model_name in model_names:
        # In a real scenario, input_data would be used for training specific models
        # For this dummy, we just pass df_final_model_input conceptually
        df_forecast = generate_dummy_forecast(model_name, input_data=df_final_model_input)

        file_path = os.path.join(models_output_path, f'forecast_{model_name}.csv')
        df_forecast.to_csv(file_path, index=False)
        print(f"  Forecast for {model_name} saved to: {file_path}")
        # print(df_forecast.head().to_markdown(index=False))

if __name__ == '__main__':
    main()
