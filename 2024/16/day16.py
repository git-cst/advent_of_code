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
    file_path = os.path.join(os.path.dirname(__file__), f'day16_{type}input.txt')
    with open(file_path, 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')
    
    return file_data

class Cell():
    def __init__(self):
        self.value = ""

        self.n_neighbour = None
        self.e_neighbour = None
        self.s_neighbour = None
        self.w_neighbour = None

        self.blocking = False

    def set_value(self, value):
        self.value = value

    def set_position(self, position: tuple[int, int]):
        self.x_pos, self.y_pos = position

    def set_blocking(self):
        self.blocking = True

    def get_value(self):
        return self.value

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
                cell.set_value(data[i][j])
                cell.set_position((i, j))

                cell_value = cell.get_value()

                if cell_value == "S":
                    self.start_point = cell
                elif cell_value == "E":
                    self.end_point = cell
                elif cell_value == "#":
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
        stack = []
        valid_paths = []

        start_position = self.start_point
        stack.append(start_position, valid_paths)

        while stack:
            current, path = stack.pop()

    def best_path_score(self) -> int:
        return 

def main():
    data = get_data('test')
    num_cols = len(data[0])
    num_rows = len(data)

    grid = Grid(num_cols, num_rows, data)
    grid.evaluate_paths()
    print(grid.best_path_score())

if __name__ == '__main__':
    main()