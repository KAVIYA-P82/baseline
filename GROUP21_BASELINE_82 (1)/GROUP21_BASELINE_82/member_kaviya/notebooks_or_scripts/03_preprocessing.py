
import pandas as pd
import os

def main():
    # Define the base directory and member name
    base_directory = 'GROUP21_BASELINE'
    new_member_name = 'kaviya'

    # Define paths for input data from previous steps
    processed_data_path = os.path.join(base_directory, f'member_{new_member_name}', '01_data', 'processed')
    embeddings_output_path = os.path.join(base_directory, f'member_{new_member_name}', '02_embeddings')

    # Define output path for preprocessed features (will be consumed by 04_feature_engineering.py)
    preprocessed_output_path = os.path.join(base_directory, f'member_{new_member_name}', '03_features')
    os.makedirs(preprocessed_output_path, exist_ok=True)

    # Load processed feature data
    try:
        df_analog_features = pd.read_csv(os.path.join(processed_data_path, 'analog_features_clean.csv'))
        df_new_drug_features = pd.read_csv(os.path.join(processed_data_path, 'new_drug_features_clean.csv'))
    except FileNotFoundError as e:
        print(f"Error loading cleaned features: {e}. Make sure 01_data_creation.py has been run.")
        return

    # Load similarity vectors
    try:
        df_similarity_vectors = pd.read_csv(os.path.join(embeddings_output_path, 'similarity_vectors.csv'))
    except FileNotFoundError as e:
        print(f"Error loading similarity vectors: {e}. Make sure 02_embedding_similarity.py has been run.")
        return

    # Preprocessing Step 1: Merge analog features with similarity scores
    # This prepares the data for more complex feature engineering in the next step.
    df_analog_preprocessed = df_analog_features.merge(df_similarity_vectors, on='drug_id', how='left')
    print("Analog Features Preprocessed (first 5 rows with similarity scores):")
    print(df_analog_preprocessed.head().to_markdown(index=False))

    print("
New Drug Features (ready for engineering - first 5 rows):")
    print(df_new_drug_features.head().to_markdown(index=False))

    # Define file paths for the output
    analog_preprocessed_file = os.path.join(preprocessed_output_path, 'analog_preprocessed_for_fe.csv')
    new_drug_preprocessed_file = os.path.join(preprocessed_output_path, 'new_drug_preprocessed_for_fe.csv')

    # Save to CSV
    df_analog_preprocessed.to_csv(analog_preprocessed_file, index=False)
    df_new_drug_features.to_csv(new_drug_preprocessed_file, index=False) # New drug features might not need merging here, but saved for consistency

    print(f"
Preprocessed analog features saved to: {analog_preprocessed_file}")
    print(f"New drug features saved for FE to: {new_drug_preprocessed_file}")

if __name__ == '__main__':
    main()
