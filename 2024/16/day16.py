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

def get_data(type=''):
    with open(f'{os.path.dirname(__file__)}/day14_{type}input.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')

    ret_data = []
    for row in file_data:
        ret_data.append(row.split())
    
    return ret_data

class Cell():
    def __init__(self, value: str = ""):
        self.value = value

        self.n_neighbour = None
        self.e_neighbour = None
        self.s_neighbour = None
        self.w_neighbour = None

        self.blocking = False

    def set_blocking(self):
        self.blocking = True

    def is_blocking(self):
        return self.blocking

class Grid():
    def __init__(self, num_cols: int, num_rows: int, data: list[list[str]]):
        self.start_point = None
        self.end_point = None

        self.generate_grid(num_cols, num_rows, data)

    def generate_grid(self, num_cols: int, num_rows: int, data: list[list[str]]):
        self.cells = [[Cell() for _ in range(num_cols)] for _ in range(num_rows)]

        for i in range(0, num_cols):
            for j in range(0, num_rows):
                cell: Cell = self.cells[i][j]
                cell.value = data[i][j]

                if cell.value == "S":
                    self.start_point = cell
                elif cell.value == "E":
                    self.end_point = cell
                elif cell.value == "#":
                    cell.set_blocking()

                # Logic for checking N
                if i - 1 >= 0:
                    cell.n_neighbour = self.cells[i - 1][j]

                # Logic for checking E
                if j + 1 < num_cols:
                    cell.e_neighbour = self.cells[i][j + 1]

                # Logic for checking S
                if i + 1 < num_rows:
                    cell.s_neighbour = self.cells[i + 1][j]

                # Logic for checking W
                if j - 1 >= 0:
                    cell.w_neighbour = self.cells[i][j - 1]

    def evaluate_paths(self):
        self.valid_paths = []

    def best_path_score(self) -> int:
        return 

def main():
    data = get_data('test')
    num_cols = len(data[0])
    num_rows = len(data)

    grid = Grid()
    grid.generate_grid(num_cols, num_rows, data)
    grid.evaluate_paths()
    print(grid.best_path_score())

if __name__ == '__main__':
    main()