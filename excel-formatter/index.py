
import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
import pandas as pd
from datetime import datetime
import os
from collections.abc import Sequence
from typing import Any, Literal, cast
from openpyxl.utils import get_column_letter

HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
HEADER_FONT = Font(size=12, bold=True, color="FFFFFF")
DATA_FONT = Font(size=11)
THIN = Border(left=Side('thin'), right=Side('thin'), top=Side('thin'), bottom=Side('thin'))

def format_cells(
    sheet: Worksheet,
    cell_range: str,
    font_size: int = 11,
    bold: bool = False,
    align: str = 'center',
    fill: PatternFill | None = None,
    font_color: str | None = None,
):
    for row in sheet[cell_range]:
        for cell in row:
            cell.font = Font(size=font_size, bold=bold, color=font_color) if font_color else Font(size=font_size, bold=bold)
            cell.alignment = Alignment(horizontal=align, vertical='center')
            if fill: cell.fill = fill

def add_borders(
    sheet: Worksheet,
    cell_range: str,
    style: Literal[
        'dashDot', 'dashDotDot', 'dashed', 'dotted', 'double', 'hair', 'medium',
        'mediumDashDot', 'mediumDashDotDot', 'mediumDashed', 'mediumDotted',
        'slantDashDot', 'thick', 'thin', 'none',
    ] = 'thin',
):
    side = Side(cast(Any, style))
    border = Border(left=side, right=side, top=side, bottom=side)
    for row in sheet[cell_range]:
        for cell in row: cell.border = border  # FIXED: was assigned twice

def fill_data(
    sheet: Worksheet,
    data: Sequence[Sequence[Any]],
    start_row: int = 2,
    start_col: int = 1,
):
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            cast(Any, sheet.cell(row=start_row + i, column=start_col + j)).value = v

def auto_width(sheet: Worksheet, min_w: int = 12, max_w: int = 30):
    for column_index, col in enumerate(sheet.columns, start=1):
        letter = get_column_letter(column_index)
        longest = max((len(str(c.value)) if c.value is not None else 0) for c in col)
        sheet.column_dimensions[letter].width = min(max(longest+2, min_w), max_w)

def create_sample(path: str = 'example.xlsx'):
    wb = openpyxl.Workbook()
    sheet = wb.active
    if not isinstance(sheet, Worksheet):
        raise RuntimeError('Workbook does not contain an active worksheet')
    sheet.title = 'Sheet1'
    headers = ['Name','Age','Country']
    fill_data(sheet, [headers], start_row=1)
    format_cells(sheet, 'A1:C1', 12, bold=True, align='center', fill=HEADER_FILL, font_color="FFFFFF")
    add_borders(sheet, 'A1:C1')
    data: list[list[str | int]] = [['John',25,'USA'],['Alice',30,'UK'],['Bob',35,'Canada'],['Priya',28,'India']]
    fill_data(sheet, data, start_row=2)
    format_cells(sheet, 'A2:C5', 11, align='center')
    add_borders(sheet, 'A2:C5')
    sheet.freeze_panes = 'A2'
    sheet.auto_filter.ref = 'A1:C5'
    auto_width(sheet)
    wb.save(path); print(f"Created {path}"); return path

def main():
    src = 'example.xlsx'
    if not os.path.exists(src):
        print(f"{src} not found - creating sample...")
        create_sample(src)
    else:
        wb = openpyxl.load_workbook(src); sheet = wb['Sheet1']
        # Re-apply formatting idempotently
        format_cells(sheet, 'A1:C1', 12, bold=True, fill=HEADER_FILL, font_color="FFFFFF")
        add_borders(sheet, 'A1:C1')
        max_row = sheet.max_row
        format_cells(sheet, f'A2:C{max_row}', 11)
        add_borders(sheet, f'A2:C{max_row}')
        sheet.freeze_panes='A2'; auto_width(sheet); wb.save(src)
        print(f"Formatted {src}")
    df: pd.DataFrame = cast(Any, pd).read_excel(src)
    print("\nData:\n", df)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    out = f'output_{ts}.xlsx'
    cast(Any, df).to_excel(out, index=False)
    print(f"Saved timestamped copy: {out}")

if __name__=="__main__": main()
