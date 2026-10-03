import csv
import json

# Load the address.json file
with open('address.json') as f:
    address_schema = json.load(f)

# Define a function to convert CSV to JSON
def csv_to_json(csv_file: str, json_file: str) -> None:
    try:
        # Read the CSV file
        with open(csv_file, 'r') as csv_f:
            csv_reader = csv.DictReader(csv_f)
            data = list(csv_reader)

        # Convert data types based on the address schema
        for row in data:
            for field, field_type in address_schema['fields'].items():
                if field_type == 'integer' and row[field]:
                    row[field] = int(row[field])

        # Write the JSON file
        with open(json_file, 'w') as json_f:
            json.dump(data, json_f, indent=4)

        print(f"Successfully converted {csv_file} to {json_file}")

    except FileNotFoundError:
        print(f"File {csv_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
csv_file = 'input.csv'
json_file = 'output.json'
csv_to_json(csv_file, json_file)