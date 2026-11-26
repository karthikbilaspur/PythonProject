# Excel Formatter - Improved

index Run
bash
pip install -r requirements.txt
python excel_formatter.py

index What Was Fixed
| Original Bug | Fix |

|---|---|
| Crashed if `example.xlsx` missing | Auto-creates sample file |
| `cell.border = border` twice | Once |
| Functions used global `sheet` | All take `sheet` param - reusable |
| Timestamp copy via manual read/write | Direct `df.to_excel(f'output_{ts}.xlsx')` |
| No column widths / freeze / filter | `auto_width()`, freeze A2, auto-filter |
| Header had no colour | Dark blue header + white bold text |

index Features

- Header styling, borders, alignment, auto-width
- Freeze panes + auto-filter
- pandas read -> timestamped output file
- Re-runnable: formatting is idempotent

index Requirements
`openpyxl`, `pandas`
