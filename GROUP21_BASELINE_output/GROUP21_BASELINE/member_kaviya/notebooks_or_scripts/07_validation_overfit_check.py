
import pandas as pd
import os

def main():
    base_directory = 'GROUP21_BASELINE'
    new_member_name = 'kaviya'

    # Define paths for input evaluation results
    evaluation_input_path = os.path.join(base_directory, f'member_{new_member_name}', '05_evaluation')

    # Define output path for the final report (if any, for this dummy, we just print)
    # report_output_path = os.path.join(base_directory, f'member_{new_member_name}', '06_reports')
    # os.makedirs(report_output_path, exist_ok=True)

    # Load evaluation results
    try:
        df_model_comparison_metrics = pd.read_csv(os.path.join(evaluation_input_path, 'model_comparison_metrics.csv'))
        df_loo_validation_results = pd.read_csv(os.path.join(evaluation_input_path, 'loo_validation_results.csv'))
        df_backtest_results = pd.read_csv(os.path.join(evaluation_input_path, 'backtest_results.csv'))

        with open(os.path.join(evaluation_input_path, 'overfit_check_notes.md'), 'r') as f:
            overfit_check_notes = f.read()

    except FileNotFoundError as e:
        print(f"Error loading evaluation results: {e}. Make sure 06_evaluate_models.py has been run.")
        return

    print("
--- Final Validation and Overfit Check Summary ---
")

    print("1. Model Comparison Metrics:")
    print(df_model_comparison_metrics.to_markdown(index=False))

    print("
2. Leave-One-Out (LOO) Validation Results:")
    print(df_loo_validation_results.to_markdown(index=False))

    print("
3. Backtest Validation Results:")
    print(df_backtest_results.to_markdown(index=False))

    print("
4. Overfitting Check Notes:")
    print(overfit_check_notes)

    print("
--- End of Summary ---
")

    # In a real scenario, you might generate a comprehensive report (PDF, HTML) here.
    # For this dummy, we'll just print to console.

if __name__ == '__main__':
    main()
