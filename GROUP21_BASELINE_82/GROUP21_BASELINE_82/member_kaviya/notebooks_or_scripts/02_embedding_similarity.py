
import pandas as pd
import os
import random

def calculate_dummy_similarity(new_drug_features, analog_features):
    # Placeholder: In reality, you'd use cosine similarity, Euclidean distance, etc.
    # For demonstration, we'll create random similarities.
    num_analogs = len(analog_features)
    # Handle cases where analog_features might be empty to prevent division by zero or errors
    if num_analogs == 0:
        return pd.DataFrame({'drug_id': [], 'similarity_score': []})

    similarity_scores = pd.DataFrame({
        'drug_id': analog_features['drug_id'],
        'similarity_score': [1 - (i / num_analogs) * 0.7 for i in range(num_analogs)] # Dummy decreasing similarity
    })
    # Ensure the similarity scores are consistent for dummy example
    similarity_scores = similarity_scores.sort_values(by='similarity_score', ascending=False).reset_index(drop=True)
    return similarity_scores

def main():
    # Define the base directory and member name
    base_directory = 'GROUP21_BASELINE_82'
    new_member_name = 'kaviya'

    # Define paths for processed data (from 01_data_creation.py) and output
    processed_data_path = os.path.join(base_directory, f"member_{new_member_name}", '01_data', 'processed')
    embeddings_output_path = os.path.join(base_directory, f"member_{new_member_name}", '02_embeddings')
    os.makedirs(embeddings_output_path, exist_ok=True)

    # Define full paths for input feature files
    analog_features_clean_file = os.path.join(processed_data_path, 'analog_features_clean.csv')
    new_drug_features_clean_file = os.path.join(processed_data_path, 'new_drug_features_clean.csv')

    # Load processed feature data
    try:
        df_analog_features = pd.read_csv(analog_features_clean_file)
        df_new_drug_features = pd.read_csv(new_drug_features_clean_file)
    except FileNotFoundError as e:
        print(f"Error loading processed feature data: {e}. Make sure 01_data_creation.py has been run.")
        return

    # Calculate dummy similarity vectors
    df_similarity_vectors = calculate_dummy_similarity(df_new_drug_features, df_analog_features)
    print("Similarity Vectors (First 5 rows):")
    print(df_similarity_vectors.head().to_markdown(index=False))

    # Select top 5 analogs based on dummy similarity
    df_top5_analogs = df_similarity_vectors.head(5)
    print("
Top 5 Analogs Selected:")
    print(df_top5_analogs.to_markdown(index=False))

    # Define file paths for the output
    similarity_vectors_file = os.path.join(embeddings_output_path, 'similarity_vectors.csv')
    top5_analogs_file = os.path.join(embeddings_output_path, 'top5_analogs_selected.csv')

    # Save to CSV
    df_similarity_vectors.to_csv(similarity_vectors_file, index=False)
    df_top5_analogs.to_csv(top5_analogs_file, index=False)

    print(f"
Similarity vectors saved to: {similarity_vectors_file}")
    print(f"Top 5 analogs saved to: {top5_analogs_file}")

if __name__ == '__main__':
    main()
