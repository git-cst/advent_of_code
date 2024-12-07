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
    with open(f'{os.path.dirname(__file__)}/day4_input.txt', 'r') as file:
        data: str = file.read()
    
    data = data.split()

    return data

class Cell():
    def __init__(self, value = None):
        self.value: str = value
        
        self.n: Cell = None
        self.s: Cell = None
        self.w: Cell = None
        self.e: Cell = None
        
        self.nw: Cell = None
        self.ne: Cell = None
        self.sw: Cell = None
        self.se: Cell = None

class Graph():
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols

    def generate_graph(self, data):
        self.cells = [[Cell() for _ in range(self.num_cols)] for _ in range(self.num_rows)]

        for i in range(0, self.num_rows):
            for j in range(0, self.num_cols):
                cell: Cell = self.cells[i][j]
                cell.value = data[i][j]

                # LOGIC FOR CHECKING NW
                if i - 1 >= 0 and j - 1 >= 0:
                    cell.nw = self.cells[i - 1][j - 1]

                # LOGIC FOR CHECKING N
                if i - 1 >= 0:
                    cell.n = self.cells[i - 1][j]

                # LOGIC FOR CHECKING NE
                if i - 1 >= 0 and j + 1 < self.num_cols:
                    cell.ne = self.cells[i - 1][j + 1]

                # LOGIC FOR CHECKING E
                if j + 1 < self.num_cols:
                    cell.e = self.cells[i][j + 1]

                # LOGIC FOR CHECKING SE
                if i + 1 < self.num_rows and j + 1 < self.num_cols:
                    cell.se = self.cells[i + 1][j + 1]

                # LOGIC FOR CHECKING S
                if i + 1 < self.num_rows:
                    cell.s = self.cells[i + 1][j]

                # LOGIC FOR CHECKING SW
                if i + 1 < self.num_rows and j - 1 >= 0:
                    cell.sw = self.cells[i + 1][j - 1]

                # LOGIC FOR CHECKING W
                if j - 1 >= 0:
                    cell.w = self.cells[i][j - 1]

    def check_adjacencies(self):
        count_of_xmas = 0
        count_of_mas_in_x_form = 0

        for i in range(0, self.num_rows):
            for j in range(0, self.num_cols):
                if self.cells[i][j].value == 'X':
                    count_of_xmas += self.look_for_xmas(i, j)

                if self.cells[i][j].value == 'A':
                    count_of_mas_in_x_form += self.look_for_mas_in_x_form(i, j)

        return count_of_xmas, count_of_mas_in_x_form

    def look_for_xmas(self, i, j):
        count = 0
        start_cell = self.cells[i][j]
        directions_to_search = ['nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w']

        for direction in directions_to_search:
            value = None
            index = 0
            chars_to_find = ['M', 'A', 'S']
            cell = getattr(start_cell, direction, None)

            if cell:
                value = getattr(cell, "value", None)

            while value == chars_to_find[index]:
                if value == 'S':
                    count += 1
                    break

                cell = getattr(cell, direction, None)
                value = getattr(cell, "value", None)
                index += 1
                
        return count
    
    def look_for_mas_in_x_form(self, i, j):
        count = 0
        nw_se, ne_sw = False, False
        start_cell = self.cells[i][j]

        nw_cell: Cell = getattr(start_cell, 'nw', None)
        se_cell: Cell = getattr(start_cell, 'se', None)
        ne_cell: Cell = getattr(start_cell, 'ne', None)
        sw_cell: Cell = getattr(start_cell, 'sw', None)

        if not nw_cell or not se_cell or not ne_cell or not sw_cell:
            return count

        # Check NW-SE diagonal
        nw_se = (
            nw_cell.value == 'M' and self.cells[i][j].value == 'A' and se_cell.value == 'S'
        ) or (
            nw_cell.value == 'S' and self.cells[i][j].value == 'A' and se_cell.value == 'M'
        )

        # Check NE-SW diagonal
        ne_sw = (
            ne_cell.value == 'M' and self.cells[i][j].value == 'A' and sw_cell.value == 'S'
        ) or (
            ne_cell.value == 'S' and self.cells[i][j].value == 'A' and sw_cell.value == 'M'
        )

        # Increment count if both diagonals form MAS or SAM
        if nw_se and ne_sw:
            count += 1

        return count 

@time_execution
def solve():
    data = get_data()
    graph = Graph(len(data), len(data[0]))
    graph.generate_graph(data)
    count_xmas, count_mas = graph.check_adjacencies()
    print(f'Number of xmas: {count_xmas}\nNumber of mas in x-form: {count_mas}')

if __name__ == "__main__":
    solve()