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

                # Logic for checking NW
                if i - 1 >= 0 and j - 1 >= 0:
                    cell.nw = self.cells[i - 1][j - 1]

                # Logic for checking N
                if i - 1 >= 0:
                    cell.n = self.cells[i - 1][j]

                # Logic for checking NE
                if i - 1 >= 0 and j + 1 < self.num_cols:
                    cell.ne = self.cells[i - 1][j + 1]

                # Logic for checking E
                if j + 1 < self.num_cols:
                    cell.e = self.cells[i][j + 1]

                # Logic for checking SE
                if i + 1 < self.num_rows and j + 1 < self.num_cols:
                    cell.se = self.cells[i + 1][j + 1]

                # Logic for checking S
                if i + 1 < self.num_rows:
                    cell.s = self.cells[i + 1][j]

                # Logic for checking SW
                if i + 1 < self.num_rows and j - 1 >= 0:
                    cell.sw = self.cells[i + 1][j - 1]

                # Logic for checking W
                if j - 1 >= 0:
                    cell.w = self.cells[i][j - 1]

    def look_for_xmas(self, i, j):
        count = 0
        start_cell = self.cells[i][j]
        directions_to_search = ['nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w']

        # Loop through directions from a center point that is X
        for direction in directions_to_search:
            value = None
            index = 0
            chars_to_find = ['M', 'A', 'S']
            cell = getattr(start_cell, direction, None)

            # If there is a cell in that direction get the value of that cell
            if cell:
                value = getattr(cell, "value", None)

            # Loop through the index and check if each letter is the next expected value
            while value == chars_to_find[index]:
                # If the value found is S exit and increment count and then check next direction from start cell
                if value == 'S':
                    count += 1
                    break

                # If value is correct go to next cell and get it's value
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

        # If any cell is missing then MAS in X form cannot be found
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
    
    def check_adjacencies(self):
        count_of_xmas = 0
        count_of_mas_in_x_form = 0

        # Check each cell in graph if a value is X then it is possible to find XMAS if valus is A then it is possible to find MAS in X form
        for i in range(0, self.num_rows):
            for j in range(0, self.num_cols):
                if self.cells[i][j].value == 'X':
                    count_of_xmas += self.look_for_xmas(i, j)

                if self.cells[i][j].value == 'A':
                    count_of_mas_in_x_form += self.look_for_mas_in_x_form(i, j)

        return count_of_xmas, count_of_mas_in_x_form
    
@time_execution
def solve():
    data = get_data()
    graph = Graph(len(data), len(data[0]))
    graph.generate_graph(data)
    count_xmas, count_mas = graph.check_adjacencies()
    print(f'Number of xmas: {count_xmas}\nNumber of mas in x-form: {count_mas}')

if __name__ == "__main__":
    solve()