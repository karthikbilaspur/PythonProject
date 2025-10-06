import pandas as pd
import argparse
import os

def convert_file(input_file, input_format, output_file, output_format):
    """
    Convert a file from one format to another.

    Args:
        input_file (str): Path to the input file.
        input_format (str): Format of the input file (csv, excel, json).
        output_file (str): Path to the output file.
        output_format (str): Format of the output file (csv, excel, json).
    """
    # Read the input file
    if input_format == 'csv':
        df = pd.read_csv(input_file)
    elif input_format == 'excel':
        df = pd.read_excel(input_file)
    elif input_format == 'json':
        df = pd.read_json(input_file)
    else:
        raise ValueError(f"Unsupported input format: {input_format}")

    # Write the output file
    if output_format == 'csv':
        df.to_csv(output_file, index=False)
    elif output_format == 'excel':
        df.to_excel(output_file, index=False)
    elif output_format == 'json':
        df.to_json(output_file, orient='records')
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File format converter')
    parser.add_argument('-i', '--input_file', required=True, help='Path to the input file')
    parser.add_argument('-f', '--input_format', required=True, choices=['csv', 'excel', 'json'], help='Format of the input file')
    parser.add_argument('-o', '--output_file', required=True, help='Path to the output file')
    parser.add_argument('-t', '--output_format', required=True, choices=['csv', 'excel', 'json'], help='Format of the output file')

    args = parser.parse_args()
    convert_file(args.input_file, args.input_format, args.output_file, args.output_format)

    print(f"File converted successfully: {args.input_file} ({args.input_format}) -> {args.output_file} ({args.output_format})")
    