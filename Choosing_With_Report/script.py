import pandas as pd

def load_data(data_file_path):
    try:
        # Load data
        df = pd.read_csv(data_file_path)
        return df
    except FileNotFoundError:
        print("Error: Data file not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: Data file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: Failed to parse data file.")
        return None

def calculate_summary_statistics(df):
    # Calculate summary statistics
    summary_statistics = df.describe()
    return summary_statistics

def calculate_column_statistics(df):
    # Calculate column means, max, and min values
    column_means = df.mean(numeric_only=True)
    column_max_values = df.max(numeric_only=True)
    column_min_values = df.min(numeric_only=True)
    column_median = df.median(numeric_only=True)
    column_std_dev = df.std(numeric_only=True)
    return column_means, column_max_values, column_min_values, column_median, column_std_dev

def generate_data_report(df, report_file_path):
    try:
        summary_statistics = calculate_summary_statistics(df)
        column_means, column_max_values, column_min_values, column_median, column_std_dev = calculate_column_statistics(df)

        # Generate report
        with open(report_file_path, 'w') as report_file:
            report_file.write("# Data Report\n\n")
            report_file.write("## Summary Statistics:\n")
            report_file.write(summary_statistics.to_string() + "\n\n")
            report_file.write("## Column Statistics:\n")
            report_file.write("### Column Means:\n")
            report_file.write(column_means.to_string() + "\n\n")
            report_file.write("### Column Maximum Values:\n")
            report_file.write(column_max_values.to_string() + "\n\n")
            report_file.write("\n### Column Minimum Values:\n")
            report_file.write(column_min_values.to_string() + "\n\n")
            report_file.write("### Column Median Values:\n")
            report_file.write(column_median.to_string() + "\n\n")
            report_file.write("### Column Standard Deviation:\n")
            report_file.write(column_std_dev.to_string())

        print("Data report generated successfully!")

    except Exception as e:
        print(f"An error occurred while generating the report: {e}")


def main():
    data_file_path = "path/to/your/data.csv"
    report_file_path = "path/to/your/report.txt"

    df = load_data(data_file_path)
    if df is not None:
        generate_data_report(df, report_file_path)


if __name__ == "__main__":
    main()