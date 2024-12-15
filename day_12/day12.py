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
    with open(f'{os.path.dirname(__file__)}/day12_input.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')

    array = []
    for value in file_data:
        array.append(value)

    return array
      
class Cell():
    def __init__(self):
        self.value : str = None

        self.n_perimiter : bool = True
        self.s_perimiter : bool = True
        self.w_perimiter : bool = True
        self.e_perimiter : bool = True
        self.perimiter_length: int = 0

        self.n: Cell = None
        self.s: Cell = None
        self.w: Cell = None
        self.e: Cell = None
        
        self.visited: bool = False

class Region():
    _instances = {}

    def __init__(self, identifier):
        self.cells: list[Cell]      = []
        self.identifier: str        = identifier
        self.perimiter_length: int  = 0

        Region._instances[identifier] = self

    def add_cell(self, cell):
        self.cells.append(cell)

    @classmethod
    def exists(cls, identifier) -> bool:
        return identifier in cls._instances

class Map():
    def __init__(self):
        self._data: list            = get_data()
        self._num_rows: int         = len(self._data)
        self._num_cols: int         = len(self._data[0])
        self.regions: dict          = {}

    def generate_cells(self) -> None:
        self._cells = [[Cell() for _ in range(self._num_cols)] for _ in range(self._num_rows)]

        for i in range(0, self._num_rows):
            for j in range(0, self._num_cols):
                cell: Cell = self._cells[i][j]
                cell.value = self._data[i][j]

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

    def create_perimiters(self):
        for i in range(0, self._num_rows):
            for j in range(0, self._num_cols):
                cell: Cell = self._cells[i][j]
                current_value = cell.value
                num_edges = 4

                directions = ['n', 'e', 's', 'w']

                for direction in directions:
                    check_cell = getattr(cell, direction, None)

                    if check_cell:
                        check_value = getattr(check_cell, 'value', None)

                        if check_value == current_value:
                            setattr(cell, f'{direction}_perimiter', False)
                            num_edges -= 1
                
                cell.perimiter_length = num_edges

    def create_regions(self):
        for i in range(0, self._num_rows):
            for j in range(0, self._num_cols):
                self._cells[i][j].visited = False

        self.regions.clear()

        for i in range(0, self._num_rows):
            for j in range(0, self._num_cols):
                cell = self._cells[i][j]
                if not cell.visited:
                    self._explore_region(cell)

        return self.regions

    def _explore_region(self, start_cell: Cell):
        if start_cell.visited == True:
            return

        if start_cell.value not in self.regions:
            self.regions[start_cell.value] = []

        current_region = Region(f"{start_cell.value}_region_{len(self.regions[start_cell.value])}")
        self.regions[start_cell.value].append(current_region)

        stack = [start_cell]
        while stack:
            cell = stack.pop()

            if cell.visited == True or cell.value != start_cell.value:
                continue

            cell.visited = True
            current_region.perimiter_length += cell.perimiter_length
            current_region.add_cell(cell)

            directions = ['n', 'e', 's', 'w']

            for direction in directions:
                check_cell = getattr(cell, direction, None)
                if check_cell:
                    if cell.value == getattr(check_cell, "value", None):
                        stack.append(check_cell)

@time_execution
def solve():
    garden_map = Map()
    garden_map.generate_cells()
    garden_map.create_perimiters()
    regions = garden_map.create_regions()
    
    cost = 0
    for key, region_list in regions.items():
        for region in region_list:
            cost += len(region.cells) * region.perimiter_length

    print(f'Cost of fencing is {cost}')

if __name__ == '__main__':
    solve()