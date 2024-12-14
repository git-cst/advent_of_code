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

class Cell():
    def __init__(self):
        self.value : str = None

        self.has_top_perimiter    : bool      = False
        self.has_bottom_perimiter : bool      = False
        self.has_left_perimiter   : bool      = False
        self.has_right_perimiter  : bool      = False

        self.n: Cell = None
        self.s: Cell = None
        self.w: Cell = None
        self.e: Cell = None

class Map():
    def __init__(self):
        self._data: list            = get_data()
        self._num_rows: int         = len(self._data)
        self._num_cols: int         = len(self._data[0])
        self._edge_dict: dict       = {}
        self._val_count_dict: dict  = {}

    def generate_cells(self) -> None:
        self._cells = [[Cell() for _ in self._num_cols] for _ in self._num_rows]

        for i in range(0, self._num_rows):
            for j in range(0, self._num_cols):
                cell: Cell = self._cells[i][j]
                cell.value = self._data[i][j]

                # Increment count of values
                self._val_count_dict[cell.value] = self._val_count_dict.get(cell.value, 0) + 1

                # Logic for checking N
                if i - 1 >= 0:
                    cell.n = self._cells[i - 1][j]

                # Logic for checking E
                if j + 1 < self._num_cols:
                    cell.e = self._cells[i][j + 1]

                # Logic for checking S
                if i + 1 < self._num_rows:
                    cell.s = self._cells[i + 1][j]

                # Logic for checking W
                if j - 1 >= 0:
                    cell.w = self._cells[i][j - 1]

    def check_adjacencies(self):
        for i in range(0, self._num_rows):
            for j in range(0, self._num_cols):
                cell: Cell = self._cells[i][j]

                # TODO
                # CHECK DIRECTIONS TO SEE IF SAME VALUE
                # IF SAME VALUE THEN NO EDGE
                # IF NOT SAME VALUE THEN EDGE
                # ADD NUM EDGES TO EDGE DICT. KEY = CELL.VALUE AND VALUE IS NUM EDGES

    def calculate_fencing_cost(self):
        fencing_cost = 0
        for key, value in self._val_count_dict:
            fencing_cost += self._edge_dict[key] * value

@time_execution
def solve():
    pass

if __name__ == '__main__':
    solve()