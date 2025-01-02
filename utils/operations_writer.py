import json
import os

# Define the maximum number of operations allowed
MAX_OPERATIONS = 100
OPERATIONS_FILE_PATH = "/home/container/operations.txt"

# Function to check how many operations are in the file
def count_operations_in_file():
    if os.path.exists(OPERATIONS_FILE_PATH):
        with open(OPERATIONS_FILE_PATH, 'r') as file:
            operations = file.readlines()
            return len(operations)
    return 0

# Function to append a command to the operations file
def write_operation_to_file(command):
    # Count how many operations are in the file
    operations_count = count_operations_in_file()

    # If there are more than 100 operations, print a message and do nothing
    if operations_count >= MAX_OPERATIONS:
        print("Wait until operations are done.")
        return 100

    # Append the new command to the file
    with open(OPERATIONS_FILE_PATH, 'a') as file:
        json.dump(command, file)
        file.write("\n")  # Add a newline after each operation
    print(f"Command added: {command}")

# Example of how to add different commands
def update_cell(cell: str, values, ws):
    command = {"type": "update", "range": cell, "values": [[values]], "file": ws,  "ID": count_operations_in_file()}
    write_operation_to_file(command)
    return count_operations_in_file
def append_cell(cell: str, values, ws):
    command = {"type": "append", "range": cell, "values": [[values]], "file": ws, "ID": count_operations_in_file()}
    write_operation_to_file(command)
    return count_operations_in_file
def read_cell(cell: str, ws):
    command = {"type": "read", "range": cell, "file": ws,  "ID": count_operations_in_file()}
    write_operation_to_file(command)
    return count_operations_in_file()
def append_country_col(col: int, values, ws):
    # Wrap the input values in the correct 2D format
    l = [[value] for value in values]  # Transform `values` into column
    command = {"type": "append_country_col", "range": col, "values": l, "file": "Countries",  "ID": count_operations_in_file()}
    write_operation_to_file(command)
    return count_operations_in_file()
def read_row(row: int, ws):
    command = {"type": "read_row", "range": row, "file": ws,  "ID": count_operations_in_file()}
    write_operation_to_file(command)
    return count_operations_in_file()