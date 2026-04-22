from database import create_table
from load_data import load_data

create_table()

file_path = input("Enter SSA file path: ")
load_data(file_path)

print("Data loaded successfully!")