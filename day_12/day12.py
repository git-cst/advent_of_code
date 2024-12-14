import os; import time

def time_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"{func.__name__} took {duration:.4f} seconds to execute.")
        return result
    return wrapper

def get_data():
    data = {}
    with open(f'{os.path.dirname(__file__)}/day11_input.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')

    array = []
    for value in file_data:
        array.append(value)

    return array

@time_execution
def solve():
    pass

if __name__ == '__main__':
    solve()