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
    with open(f'{os.path.dirname(__file__)}/day6_input.txt', 'r') as file:
        data: str = file.read()
    
    data = data.split()

    return data

class Cell():
    def __init__(self, value = None):
        self.value: str = value
        # ADD A VALUE FOR NUMBER OF TIMES VISITED AND DIRECTION FROM WHICH IT WAS VISITED

        self.n: Cell = None
        self.s: Cell = None
        self.w: Cell = None
        self.e: Cell = None

class Graph():
    def __init__(self, num_rows, num_cols):
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._start_position = None
        self._path_length = 0

    def get_path_length(self):
        return self._path_length

    def generate_graph(self, data) -> None:
        self._cells  = [[Cell() for _ in range(self._num_cols)] for _ in range(self._num_rows)]

        for i in range(0, self._num_cols):
            for j in range(0, self._num_rows):
                cell: Cell = self._cells [i][j]
                cell.value = data[i][j]

                if cell.value == "^":
                    self._start_position = (i, j)

                # LOGIC FOR CHECKING N
                if i - 1 >= 0:
                    cell.n = self._cells [i - 1][j]

                # LOGIC FOR CHECKING E
                if j + 1 < self._num_cols:
                    cell.e = self._cells [i][j + 1]

                # LOGIC FOR CHECKING S
                if i + 1 < self._num_rows:
                    cell.s = self._cells [i + 1][j]

                # LOGIC FOR CHECKING W
                if j - 1 >= 0:
                    cell.w = self._cells [i][j - 1]

    def create_path(self):
        index = 0
        cell: Cell = self._cells [self._start_position[0]][self._start_position[1]]
        direction_order = ['n', 'e', 's', 'w']
        direction = direction_order[0]
        while True:
            if cell.value != "X":
                cell.value = "X"
                self._path_length += 1
            check_cell: Cell = getattr(cell, direction, None)
            if not check_cell:
                return

            if check_cell.value == "#":
                if index < 3:
                    index += 1
                else:
                    index = 0
                direction = direction_order[index]
            else:
                cell = check_cell

@time_execution
def solve():
    data = get_data()
    graph = Graph(len(data), len(data[0]))
    graph.generate_graph(data)
    graph.create_path()
    print(graph.get_path_length())

if __name__ == '__main__':
    solve()