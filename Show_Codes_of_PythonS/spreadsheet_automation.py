import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
import pandas as pd
from datetime import datetime
from typing import Any

# Load the workbook
wb = openpyxl.load_workbook('example.xlsx')
sheet = wb['Sheet1']

# Define a function to format cells
def format_cells(cell_range: str, font_size: int, bold: bool=False, align: str='center'):
    for row in sheet[cell_range]:
        for cell in row:
            cell.font = Font(size=font_size, bold=bold)
            if align == 'center':
                cell.alignment = Alignment(horizontal='center')
            elif align == 'left':
                cell.alignment = Alignment(horizontal='left')
            elif align == 'right':
                cell.alignment = Alignment(horizontal='right')
# Define a function to add borders
def add_borders(cell_range: str, border_style: Any = 'thin'):
    """
    Add borders to the specified cell range. border_style is typed as Any to avoid
    mypy/LSP complaints about passing a non-literal string to Side(...).
    """
    border = Border(
        left=Side(style=border_style),
        right=Side(style=border_style),
        top=Side(style=border_style),
        bottom=Side(style=border_style)
    )
    for row in sheet[cell_range]:
        for cell in row:
            cell.border = border
            cell.border = border

# Define a function to fill data
def fill_data(data: list[list], start_row: int):
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            sheet.cell(row=start_row+i, column=j+1).value = value

# Sample data
data: list[list] = [
    ['John', 25, 'USA'],
    ['Alice', 30, 'UK'],
    ['Bob', 35, 'Canada']
]

# Format header row
format_cells('A1:C1', 12, bold=True)
add_borders('A1:C1')

# Fill data
fill_data(data, 2)

# Format data rows
format_cells('A2:C4', 10)
add_borders('A2:C4')

# Save the workbook
wb.save('example.xlsx')

# Use pandas to read and manipulate data
df = pd.read_excel('example.xlsx')
print(df)

# Use pandas to write data to a new Excel file
df.to_excel('output.xlsx', index=False)

# Add a timestamp to the output file
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
with open('output.xlsx', 'rb') as f:
    data = f.read()
with open(f'output_{timestamp}.xlsx', 'wb') as f:
    f.write(data)