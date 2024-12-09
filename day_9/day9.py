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
    with open(f'{os.path.dirname(__file__)}/day9_input.txt', 'r') as file:
        file_data: str = file.read()
    
    return file_data

def generate_disk_map(data):
    id = 0

    index = 0
    disk_map = ''
    for _ in data:
        file_length = str(id) * int(data[index])
        free_disk_space = '.' * int(data[index+1])

        disk_map = disk_map + file_length + free_disk_space

        id += 1
        index += 2

    return disk_map

def generate_checksum(data):
    pass

def solve():
    data = get_data()
    disk_map = generate_disk_map(data)
    pass

if __name__ == "__main__":
    solve()