
import pandas as pd
import os

def main():
    # Define the base directory and member name
    base_directory = 'GROUP21_BASELINE'
    new_member_name = 'kaviya'

    # Define paths for input data from previous steps
    preprocessed_output_path = os.path.join(base_directory, f'member_{new_member_name}', '03_features')

    # Load preprocessed feature data
    try:
        df_analog_preprocessed = pd.read_csv(os.path.join(preprocessed_output_path, 'analog_preprocessed_for_fe.csv'))
        df_new_drug_preprocessed = pd.read_csv(os.path.join(preprocessed_output_path, 'new_drug_preprocessed_for_fe.csv'))
    except FileNotFoundError as e:
        print(f"Error loading preprocessed features: {e}. Make sure 03_preprocessing.py has been run.")
        return

    # Feature Engineering for Analog Drugs
    def engineer_analog_features(df):
        # For demonstration purposes, creating more dummy features based on existing ones.
        df['engineered_feature_analog_1'] = df['dummy_feature_1'] * df['similarity_score']
        df['engineered_feature_analog_2'] = df['dummy_feature_2'] / (df['similarity_score'] + 1e-6) # Avoid division by zero
        # Add a categorical feature from launch quarter for example (assuming it was encoded)
        # For this dummy, let's create a simple interaction
        df['engineered_feature_analog_3'] = df['engineered_feature_analog_1'] * df['engineered_feature_analog_2']
        return df

    df_analog_engineered_features = engineer_analog_features(df_analog_preprocessed.copy())
    print("Analog Engineered Features (first 5 rows):")
    print(df_analog_engineered_features.head().to_markdown(index=False))

    # Feature Engineering for New Drug
    def engineer_new_drug_features(df):
        # Similar engineering for the new drug, using its features
        df['engineered_feature_new_1'] = df['dummy_feature_1'] * 2 # Just a dummy transformation
        df['engineered_feature_new_2'] = df['dummy_feature_2'] + 5 # Another dummy transformation
        df['engineered_feature_new_3'] = df['engineered_feature_new_1'] / df['engineered_feature_new_2']
        return df

    df_new_drug_engineered_features = engineer_new_drug_features(df_new_drug_preprocessed.copy())
    print("
New Drug Engineered Features (first 5 rows):")
    print(df_new_drug_engineered_features.head().to_markdown(index=False))

    # Output path for engineered features
    engineered_output_path = os.path.join(base_directory, f'member_{new_member_name}', '03_features')
    os.makedirs(engineered_output_path, exist_ok=True) # Ensure directory exists

    # Define file paths for the output
    analog_engineered_file = os.path.join(engineered_output_path, 'analog_engineered_features.csv')
    new_drug_engineered_file = os.path.join(engineered_output_path, 'new_drug_engineered_features.csv')

    # Save to CSV
    df_analog_engineered_features.to_csv(analog_engineered_file, index=False)
    df_new_drug_engineered_features.to_csv(new_drug_engineered_file, index=False)

    print(f"
Engineered analog features saved to: {analog_engineered_file}")
    print(f"Engineered new drug features saved to: {new_drug_engineered_file}")

if __name__ == '__main__':
    main()
