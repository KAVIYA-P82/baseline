
import pandas as pd
import json
import os

def main():
    # Define the base directory and member name (these would ideally be passed as arguments or configured)
    base_directory = 'GROUP21_BASELINE' # Assuming this is set in the environment or a config
    new_member_name = 'kaviya' # Assuming this is set in the environment or a config

    # Define paths for the raw and processed data directories
    raw_data_path = os.path.join(base_directory, f'member_{new_member_name}', '01_data', 'raw')
    processed_data_path = os.path.join(base_directory, f'member_{new_member_name}', '01_data', 'processed')
    os.makedirs(processed_data_path, exist_ok=True)

    # Define full paths for raw input files
    anlog_drugs_path = os.path.join(raw_data_path, 'analog_drugs.json')
    new_drug_path = os.path.join(raw_data_path, 'new_drug.json')

    # Load raw drug data
    try:
        with open(anlog_drugs_path, 'r') as f:
            analog_drugs_raw = json.load(f)
        with open(new_drug_path, 'r') as f:
            new_drug_raw = json.load(f)
    except FileNotFoundError as e:
        print(f"Error loading raw data: {e}. Make sure the files exist at {raw_data_path}")
        return

    # Convert to DataFrame for easier manipulation
    df_analog_drugs_raw = pd.DataFrame(analog_drugs_raw)
    df_new_drug_raw = pd.DataFrame([new_drug_raw])

    # Feature Extraction Function
    def extract_dummy_features(df):
        # This is a placeholder for actual feature engineering
        # In a real application, you would convert categorical data, create interaction terms, etc.
        # For now, let's just use some existing numerical columns and create a dummy one.
        df['dummy_feature_1'] = df['market_size'] / 1000000
        df['dummy_feature_2'] = df['competitive_density'] * df['payer_restrictiveness']
        return df[['drug_id', 'dummy_feature_1', 'dummy_feature_2']]

    # Apply feature extraction
    df_analog_features = extract_dummy_features(df_analog_drugs_raw)
    df_new_drug_features = extract_dummy_features(df_new_drug_raw)

    print("Analog Drug Features (First 5 rows):")
    print(df_analog_features.head().to_markdown(index=False))
    print("
New Drug Features (First 5 rows):")
    print(df_new_drug_features.head().to_markdown(index=False))

    # Save processed data to CSV files
    analog_features_clean_file = os.path.join(processed_data_path, 'analog_features_clean.csv')
    new_drug_features_clean_file = os.path.join(processed_data_path, 'new_drug_features_clean.csv')

    df_analog_features.to_csv(analog_features_clean_file, index=False)
    df_new_drug_features.to_csv(new_drug_features_clean_file, index=False)

    print(f"
Processed analog features saved to: {analog_features_clean_file}")
    print(f"Processed new drug features saved to: {new_drug_features_clean_file}")

if __name__ == '__main__':
    main()
