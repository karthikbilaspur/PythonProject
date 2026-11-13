"""
Excel Merger - Single File
==========================
Merge all .xlsx files in a folder into one unified workbook.

Two methods:
  1. openpyxl  - fast, keeps raw values, no pandas needed
  2. pandas    - keeps headers, handles different column orders

Run:
  python excel_merge.py
"""

import os
from typing import Any
from openpyxl import load_workbook, Workbook

try:
    import pandas as pd
    has_pandas = True
except ImportError:
    pd: Any | None = None
    has_pandas = False


# Helpers
def get_excel_files(path: str) -> list[str]:
    """Return only .xlsx files (skip temp / hidden files like ~$...)."""
    return sorted([
        f for f in os.listdir(path)
        if f.lower().endswith(".xlsx") and not f.startswith("~$")
    ])


def reader(file: str, path: str) -> list[list[object | None]]:
    """Read all rows except header (row 1) from one file."""
    abs_file = os.path.join(path, file)
    workbook = load_workbook(abs_file, data_only=True)
    wb_sheet = workbook.active
    if wb_sheet is None:
        raise ValueError(f"No active worksheet found in: {abs_file}")

    rows: list[list[object | None]] = []
    for row in wb_sheet.iter_rows(min_row=2, values_only=True):
        rows.append(list(row))
    return rows


def read_header(file: str, path: str) -> list[object | None]:
    abs_file = os.path.join(path, file)
    workbook = load_workbook(abs_file, data_only=True)
    wb_sheet = workbook.active
    if wb_sheet is None:
        raise ValueError(f"No active worksheet found in: {abs_file}")

    return [cell.value for cell in next(wb_sheet.iter_rows(min_row=1, max_row=1))]


# Method 1: openpyxl
def merge_excel_files(path: str, output_file: str):
    files = get_excel_files(path)
    if not files:
        print(f"No .xlsx files found in: {path}")
        return

    book = Workbook()
    sheet = book.active
    if sheet is None:
        sheet = book.create_sheet()
    sheet.title = "Merged"

    # Keep header from first file (original code dropped it)
    sheet.append(read_header(files[0], path))

    total = 0
    for file in files:
        rows = reader(file, path)
        for row in rows:
            sheet.append(row)
        total += len(rows)
        print(f"  + {file}: {len(rows)} rows")

    book.save(filename=output_file)
    print(f"\nDone! {total} rows merged -> {output_file}")


# Method 2: pandas
def merge_excel_files_pandas(file_paths: list[str], output_file: str):
    if pd is None:
        print("pandas not installed. Run: pip install pandas openpyxl")
        return

    dfs = []
    for file_path in file_paths:
        df = pd.read_excel(file_path)
        df["_source_file"] = os.path.basename(file_path)  # track where each row came from
        dfs.append(df) # pyright: ignore[reportUnknownMemberType]
        print(f"  + {os.path.basename(file_path)}: {len(df)} rows")

    if not dfs:
        print(f"No .xlsx files found in: {os.path.dirname(file_paths[0]) if file_paths else '.'}")
        return

    merged_df = pd.concat(dfs, ignore_index=True)
    merged_df.to_excel(output_file, index=False)
    print(f"\nDone! {len(merged_df)} rows merged -> {output_file}")


def main():
    path = input("Folder path containing Excel files: ").strip().strip('"')
    output_file = input("Unified workbook name (e.g. merged.xlsx): ").strip()
    if not output_file.lower().endswith((".xlsx", ".xls")):
        output_file += ".xlsx"

    if not os.path.isdir(path):
        print(f"Folder not found: {path}")
        return

    print("\nChoose method:")
    print("1. openpyxl  (fast, raw values)")
    print("2. pandas   (keeps headers, adds _source_file column)")
    choice = input("Choose 1 or 2: ").strip()

    if choice == "2":
        file_paths = [os.path.join(path, f) for f in get_excel_files(path)]
        merge_excel_files_pandas(file_paths, output_file)
    else:
        merge_excel_files(path, output_file)


if __name__ == "__main__":
    main()
