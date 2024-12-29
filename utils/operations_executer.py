import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.sheetoperations as so
import json
import time

# PARSE TEXT FILE AND EXECUTE OPERATIONS
def read_operations(file_path: str):
    operations = []
    with open(file_path, 'r') as file:
        print ("succesfully opened")
        for line in file:
            print("reading operations by line")
            operation = json.loads(line.strip())  # Assuming each line contains a JSON operation
            operations.append(operation)
    print(operations)
    print(type(operations))
    return operations

# Execute batch operations
def execute_operations(operations):
    for operation in operations:
        print(operation)
        print(type(operation))
        op_type = operation["type"]  # Get the operation type
        if op_type == "update":
            cell_range = operation["range"]
            values = operation["values"]
            name = operation["file"]
            ws = so.worksheet(name)
            print(f"Updating range {cell_range} with values: {values}")
            ws.update(cell_range, values)

        elif op_type == "append":
            cell_range = operation["range"]
            values = operation["values"]
            name = operation["file"]
            ws = so.worksheet(name)
            ws.append_rows(values)
            print(f"Appended values: {values} to range {cell_range}")

        elif op_type == "read":
            cell_range = operation["range"]
            print(cell_range)
            value = ws.acell(cell_range).value  # Read value from the given range
            name = operation["file"]
            ws = so.worksheet(name)
            print(f"Value at {cell_range}: {value}")
            return value

        elif op_type == "A1_get_valcell":
            cell = operation["cell"]
            name = operation["file"]
            result = so.A1_get_valcell(cell, name)
            print(f"Value at {cell}: {result}")
            return result

        elif op_type == "get_valcell":
            row = operation["row"]
            col = operation["col"]
            name = operation["file"]
            result = so.get_valcell(row, col, name)
            print(f"Value at row {row}, col {col}: {result}")
            return result

        elif op_type == "get_row":
            row = operation["row"]
            name = operation["file"]
            result = so.get_row(row, name)
            print(f"Row {row}: {result}")
            return result

        elif op_type == "get_inrange":
            row1 = operation["row1"]
            col1 = operation["col1"]
            row2 = operation["row2"]
            col2 = operation["col2"]
            name = operation["file"]
            result = so.get_inrange(row1, col1, row2, col2, name)
            print(f"Range {row1},{col1} to {row2},{col2}: {result}")
            return result
        
        elif op_type == "append_country_col":
            col = operation["range"]
            values = operation["values"]
            name = operation["file"]
            ws = so.worksheet(name)
            ws.so.upd_country_col(col, values)
            print(f"Appended values: {values} to column {col}")

        # Add more operation cases as needed

        # After executing the operations, clear the file
    clear_operations_file()

def execute_single_operation(id: int):
    result = None # initialize a result variable
    with open('/home/container/operations.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            operation = json.loads(line.strip())
            if operation["ID"] == id:
                break
    op_type = operation["type"]  # Get the operation type
    print(op_type)
    if op_type == "update":
        name = operation["file"]
        ws = so.worksheet(name)
        cell_range = operation["range"]
        values = operation["values"]
        print(f"Updating range {cell_range} with values: {values}")
        ws.update(cell_range, values)

    elif op_type == "append":
        values = operation["values"]
        name = operation["file"]
        cell_range = operation["range"]
        ws = so.worksheet(name)
        ws.append_rows(values)
        print(f"Appended values: {values} to range {cell_range}")

    elif op_type == "read":
        cell_range = operation["range"]
        print(cell_range)
        name = operation["file"]
        ws = so.worksheet(name)
        value = ws.acell(cell_range).value  # Read value from the given range
        print(f"Value at {cell_range}: {value}")

    elif op_type == "A1_get_valcell":
        cell = operation["cell"]
        name = operation["file"]
        result = so.A1_get_valcell(cell, name)
        print(f"Value at {cell}: {result}")
        id = operation["ID"]

    elif op_type == "get_valcell":
        row = operation["row"]
        col = operation["col"]
        name = operation["file"]
        result = so.get_valcell(row, col, name)
        print(f"Value at row {row}, col {col}: {result}")
        id = operation["ID"]

    elif op_type == "get_row":
        row = operation["row"]
        name = operation["file"]
        result = so.get_row(row, name)
        print(f"Row {row}: {result}")
        id = operation["ID"]

    elif op_type == "get_inrange":
        row1 = operation["row1"]
        col1 = operation["col1"]
        row2 = operation["row2"]
        col2 = operation["col2"]
        name = operation["file"]
        result = so.get_inrange(row1, col1, row2, col2, name)
        print(f"Range {row1},{col1} to {row2},{col2}: {result}")

    elif op_type == "append_country_col":
            col = operation["range"]
            values = operation["values"]
            name = operation["file"]
            print(name, values, col)
            so.upd_country_col(col, values)
            print(f"Appended values: {values} to column {col}")
    
    # Remove the operation from the file
    id = operation["ID"]
    remove_operation_from_file(id)
        
    # Update the ID of every other operation
    with open('/home/container/operations.txt', 'r') as file:
        lines = file.readlines()
    with open('/home/container/operations.txt', 'w') as file:
        for line in lines:
            operation = json.loads(line.strip())
            if operation["ID"] != id:
                operation["ID"] -= 1
            file.write(json.dumps(operation) + '\n')
    
    # Provide result if needed
    if result is not None:
        return result

    

# Function to clear the operations file after execution
def clear_operations_file():
    open('/home/container/operations.txt', 'w').close()  # This effectively clears the file
    print("Operations file cleared.")

# Function to remove an operation from the file
def remove_operation_from_file(operation_id: int):
    with open('/home/container/operations.txt', 'r') as file:
        lines = file.readlines()
    with open('/home/container/operations.txt', 'w') as file:
        for line in lines:
            operation = json.loads(line.strip())
            if operation["ID"] != operation_id:
                file.write(line)
