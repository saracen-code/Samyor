import gspread
from gspread.utils import ValueRenderOption

'''
MISC
'''
def convert_to_A1(row: int, col: int):
  column_letter = ''
  while col > 0:
      col -= 1
      column_letter = chr(col % 26 + 65) + column_letter
      col //= 26
  coord = column_letter + str(row)
  return coord


'''
ACCESSING  OPERATIONS
'''
def sheetaccess():
  gc = gspread.service_account(filename='/home/container/client_secret.json')
  return gc
def spreadsheet():
  return sheetaccess().open('SL_Economy')
def worksheet(name: str):
  if type(name) != str:
      raise TypeError("Incorrect name for the worksheet you're trying to access.")
  ws = spreadsheet().worksheet(name)
  return ws
  
'''
READING OPERATIONS
'''
# NON-BATCH OPERATIONS
def A1_get_valcell(cell: str, name: str): # using A1 format
  ws = worksheet(name)
  val = ws.acell(cell).value
  return val
def get_valcell(row: int, col: int, name: str): # using int
  ws = worksheet(name)
  val = ws.cell(row, col).value
  return val
def get_formula(row: int, col: int, name: str): #using int
  ws = worksheet(name)
  cell_form = ws.cell(row, col, value_render_option='FORMULA').value
  return cell_form
def raw_cellval(row: int, col: int, name: str):
  ws = worksheet(name)
  raw_val = ws.get(row, col, value_render_option=ValueRenderOption.unformatted)
  return raw_val
def get_row(row: int,  name: str):
  ws = worksheet(name)
  values_list = ws.row_values(row)
  return values_list
def get_col(col: int, name: str):
  ws = worksheet(name)
  values_list = ws.col_values(col)
  return values_list
# BATCH OPERATIONS
def matrix_allval(name: str):
  ws = worksheet(name)
  matrix = ws.get_all_values()
def dict_allval(name: str):
  ws = worksheet(name)
  ls_dict = ws.get_all_records()
def get_inrange(row1: int, col1: int, row2: int, col2: int, name: str):
  ws = worksheet(name)
  # convert to A1 format
  coord1 = convert_to_A1(row1, col1)
  coord2 = convert_to_A1(row2, col2)
  matrixrange = ws.get(coord1 + ":" + coord2)
  return matrixrange
'''
FINDING CELLS
'''
def find_cell(lookedval: str, name: str):
  ws = worksheet(name)
  cell = ws.find(lookedval)
  return cell
def unfilled_col(name: str, col: int):
  ws = worksheet(name)
  col = ws.find("", in_column=1)
  return

def unfilled_row(name: str, row: int):
  ws = worksheet(name)
  cells = ws.row_values(row)
  return len(cells) + 1

'''
WRITING IN CELLS
'''
def upd_country_col(col: int, values: list):
    ws = worksheet("Countries")  # Ensure worksheet() is correctly defined
    length = 0  # Initialize length
    for sublist in values:
        length += len(sublist)  # Calculate total number of rows needed
    cell_range = convert_to_A1(1, col) + ":" + convert_to_A1(length, col)  # Correct variable name
    # Flatten the values list if necessary
    flat_values = [item for sublist in values for item in sublist]
    ws.update(cell_range, [[value] for value in flat_values])  # Ensure correct data structure

def update_cell(cell, value, sheet_name):
    ws = client.open(sheet_name).worksheet(sheet_name)
    if not isinstance(value, (int, float, str)):  # Ensure value is valid
        raise ValueError(f"Invalid value type: {type(value)}")
    ws.update(cell, [[value]])  # Ensure value is wrapped correctly
