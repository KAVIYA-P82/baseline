import pandas as pd
import json
import os

def main():
    # Define the base directory and member name (these would ideally be passed as arguments or configured)
    base_directory = 'GROUP21_BASELINE_82' # Assuming this is set in the environment or a config
    new_member_name = 'kaviya' # Assuming this is set in the environment or a config

    # Define paths for the raw and processed data directories
    # The raw_data_path is still created for consistency with other scripts that might expect it,
    # but the raw data itself is embedded here.
    raw_data_path = os.path.join(base_directory, f'member_{new_member_name}', '01_data', 'raw')
    processed_data_path = os.path.join(base_directory, f'member_{new_member_name}', '01_data', 'processed')
    os.makedirs(processed_data_path, exist_ok=True)

    # In-built Raw Data (as requested by user)
    new_drug_raw = {
        'drug_id': 'NEW_001',
        'drug_name': 'New Drug X Calatinib',
        'mechanism_of_action': 'Proton pump inhibitor',
        'route_of_administration': 'Topical',
        'target_specialty': 'Hematology',
        'market_size': 1228526,
        'competitive_density': 3,
        'payer_restrictiveness': 5,
        'launch_quarter': 'Q1',
        'promotional_intensity': 3,
        'special_designation': False,
        'price_tier': 4,
        'early_rx': [
            {'week': 1, 'rx': 14502},
            {'week': 2, 'rx': 15234},
            {'week': 3, 'rx': 16128},
            {'week': 4, 'rx': 16890},
            {'week': 5, 'rx': 17562},
            {'week': 6, 'rx': 18123},
            {'week': 7, 'rx': 18765},
            {'week': 8, 'rx': 19345},
            {'week': 9, 'rx': 19987},
            {'week': 10, 'rx': 20567},
            {'week': 11, 'rx': 21123},
            {'week': 12, 'rx': 21678},
            {'week': 13, 'rx': 22234},
            {'week': 14, 'rx': 22789},
            {'week': 15, 'rx': 23345}
        ]
    }

    analog_drugs_raw = [
        {
            'drug_id': 'ANL_001',
            'drug_name': 'Ferropara',
            'mechanism_of_action': 'SGLT2 inhibitor',
            'route_of_administration': 'Intravenous',
            'target_specialty': 'Oncology',
            'market_size': 1294436,
            'competitive_density': 3,
            'payer_restrictiveness': 5,
            'launch_quarter': 'Q3',
            'promotional_intensity': 5,
            'special_designation': False,
            'price_tier': 5,
            'rx_curve': [
                {'month': 1, 'rx': 25903},
                {'month': 2, 'rx': 27198}
            ]
        }
    ]

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

    print('Analog Drug Features (First 5 rows):')
    print(df_analog_features.head().to_markdown(index=False))
    print('
New Drug Features (First 5 rows):')
    print(df_new_drug_features.head().to_markdown(index=False))

    # Save processed data to CSV files
    analog_features_clean_file = os.path.join(processed_data_path, 'analog_features_clean.csv')
    new_drug_features_clean_file = os.path.join(processed_data_path, 'new_drug_features_clean.csv')

    df_analog_features.to_csv(analog_features_clean_file, index=False)
    df_new_drug_features.to_csv(new_drug_features_clean_file, index=False)

    print(f'
Processed analog features saved to: {analog_features_clean_file}')
    print(f'Processed new drug features saved to: {new_drug_features_clean_file}')

if __name__ == '__main__':
    main()