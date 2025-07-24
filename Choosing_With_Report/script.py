import pandas as pd

def generate_data_report(data_file_path, report_file_path):
    try:
        # Load data
        df = pd.read_csv(data_file_path)

        # Calculate summary statistics
        summary_statistics = df.describe()

        # Calculate column means, max, and min values
        column_means = df.mean(numeric_only=True)
        column_max_values = df.max(numeric_only=True)
        column_min_values = df.min(numeric_only=True)

        # Generate report
        with open(report_file_path, 'w') as report_file:
            report_file.write("# Data Report\n\n")
            report_file.write("## Summary Statistics:\n")
            report_file.write(summary_statistics.to_string() + "\n\n")
            report_file.write("## Column Means:\n")
            report_file.write(column_means.to_string() + "\n\n")
            report_file.write("## Column Maximum Values:\n")
            report_file.write(column_max_values.to_string() + "\n\n")
            report_file.write("## Column Minimum Values:\n")
            report_file.write(column_min_values.to_string())

        print("Data report generated successfully!")

    except FileNotFoundError:
        print("Error: Data file not found.")
    except pd.errors.EmptyDataError:
        print("Error: Data file is empty.")
    except pd.errors.ParserError:
        print("Error: Failed to parse data file.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    data_file_path = "path/to/your/data.csv"
    report_file_path = "path/to/your/report.txt"  # Changed to .txt for better readability

    generate_data_report(data_file_path, report_file_path)