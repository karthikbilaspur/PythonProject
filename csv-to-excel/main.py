import pandas as pd

def csv_to_excel(csv_file: str, excel_file: str) -> None:
    """
    Converts a CSV file to an Excel file.

    Args:
        csv_file (str): The path to the CSV file.
        excel_file (str): The path to the Excel file.

    Returns:
        None
    """
    try:
        # Read CSV file
        csv_data = pd.read_csv(csv_file)
        
        # Write to Excel file
        csv_data.to_excel(excel_file, index=False)
        
        print(f"Successfully converted {csv_file} to {excel_file}")
    
    except FileNotFoundError:
        print(f"File {csv_file} not found.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    csv_file = input("Enter CSV file path: ")
    excel_file = input("Enter Excel file path: ")
    
    if not excel_file.endswith(".xlsx"):
        excel_file += ".xlsx"
    
    csv_to_excel(csv_file, excel_file)