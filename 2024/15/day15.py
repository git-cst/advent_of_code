import os; import time; import re
from math import ceil

def time_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"{func.__name__} took {duration:.4f} seconds to execute.")
        return result
    return wrapper

def get_warehouse_data(type=''):
    with open(f'{os.path.dirname(__file__)}/day14_{type}_warehouse_input.txt' if type == '' else f'{os.path.dirname(__file__)}/day14_warehouse_input.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')
    
    return file_data

def get_moves_data(type=''):
    with open(f'{os.path.dirname(__file__)}/day14_{type}_moves_input.txt' if type == '' else f'{os.path.dirname(__file__)}/day14_moves_input.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')
    
    return file_data