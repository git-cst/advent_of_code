import os; import time

"""J ikke rigtig
E ikke rigtig
F ikke rigtig
C region_0 ikke rigtig
I region 1 ikke rigtig
"""

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
    with open(f'{os.path.dirname(__file__)}/day12_testinput5.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')

    array = []
    for value in file_data:
        array.append(value)

    return array

def num_boundary(outside_region):
    corner_count = 0
    match outside_region:
        # Top-left corner (both inner and outer possible)
        case [False, False, False, False, True, False, False, False]:  # Inner corner (variation 1)
            print('Top left inner corner variation 1')
            corner_count += 1
        case [False, False, False, True, True, False, False, False]:  # Inner corner (variation 2)
            print('Top left inner corner variation 2')
            corner_count += 1
        case [False, False, False, False, True, True, False, False]:  # Inner corner (variation 3)
            print('Top left inner corner variation 3')
            corner_count += 1
        case [True, True, True, False, False, False, True, True]:  # Outer corner
            print('Top left outer corner')
            corner_count += 1
        case [True, True, True, False, True, False, True, True]:  # Inner + Outer (variation 1)
            print('Top left inner outer corner variation 1')
            corner_count += 2
        case [True, True, False, False, True, False, True, True]:  # Inner + Outer (variation 2)
            print('Top left inner outer corner variation 2')
            corner_count += 2

        # Top-right corner (both inner and outer possible)
        case [False, False, False, False, False, False, True, False]:  # Inner corner (variation 1)
            print('Top right inner corner variation 1')
            corner_count += 1
        case [False, False, False, False, False, False, True, True]:  # Inner corner (variation 2)
            print('Top right inner corner variation 2')
            corner_count += 1
        case [False, False, False, False, False, True, True, False]:  # Inner corner (variation 3)
            print('Top right inner corner variation 3')
            corner_count += 1
        case [True, True, True, True, True, False, False, False]:  # Outer corner
            print('Top right outer corner')
            corner_count += 1
        case [True, True, True, True, True, False, True, False]:  # Inner + Outer (variation 1)
            print('Top right inner outer corner variation 1')
            corner_count += 2
        case [False, True, True, True, True, False, True, False]:  # Inner + Outer (variation 2)
            print('Top right inner outer corner variation 2')
            corner_count += 2

        # Bottom-right corner (both inner and outer possible)
        case [True, False, False, False, False, False, False, False]:  # Inner corner (variation 1)
            print('Bottom right inner corner variation 1')
            corner_count += 1
        case [True, False, False, False, False, False, False, True]:  # Inner corner (variation 2)
            print('Bottom right inner corner variation 2')
            corner_count += 1
        case [True, True, False, False, False, False, False, False]:  # Inner corner (variation 3)
            print('Bottom right inner corner variation 3')
            corner_count += 1
        case [False, False, True, True, True, True, True, False]:  # Outer corner
            print('Bottom right outer corner')
            corner_count += 1
        case [True, False, True, True, True, True, True, False]:  # Inner + Outer (variation 1)
            print('Bottom right inner outer corner variation 1')
            corner_count += 2
        case [True, False, True, True, True, True, True, False]:  # Inner + Outer (variation 2)
            print('Bottom right inner outer corner variation 2')
            corner_count += 2

        # Bottom-left corner (both inner and outer possible)
        case [False, False, True, False, False, False, False, False]:  # Inner corner (variation 1)
            print('Bottom left inner corner variation 1')
            corner_count += 1
        case [False, False, True, True, False, False, False, False]:  # Inner corner (variation 2)
            print('Bottom left inner corner variation 2')
            corner_count += 1
        case [False, True, True, False, False, False, False, False]:  # Inner corner (variation 3)
            print('Bottom left inner corner variation 2')
            corner_count += 1
        case [True, False, False, False, True, True, True, True]:  # Outer corner
            print('Bottom left outer corner')
            corner_count += 1
        case [True, False, True, False, True, True, True, True]:  # Inner + Outer (variation 1)
            print('Bottom left inner outer corner variation 1')
            corner_count += 2
        case [True, False, True, False, False, True, True, True]:  # Inner + Outer (variation 2)
            print('Bottom left inner outer corner variation 2')
            corner_count += 2

        # Peninsulas
        # I-shape Peninsula (Vertical)
        case [True, True, True, True, True, False, True, True]:  # Vertical I-shape (north)
            print('I Shape North')
            corner_count += 2
        case [True, False, True, True, True, True, True, True]:  # Vertical I-shape (south)
            print('I Shape South')
            corner_count += 2

        # I-shape Peninsula (Horizontal)
        case [True, True, True, True, True, True, True, False]:  # Horizontal I-shape (east)
            print('I Shape East')
            corner_count += 2
        case [True, True, True, False, True, True, True, True]:  # Horizontal I-shape (west)
            print('I Shape West')
            corner_count += 2

        # T-shape Peninsula (Vertical)
        case [True, True, True, False, True, False, True, False]:  # Vertical T-shape (north)
            print('T Shape North')
            corner_count += 2
        case [True, False, True, False, True, True, True, False]:  # Vertical T-shape (south)
            print('T Shape South')
            corner_count += 2

        # T-shape Peninsula (Horizontal)
        case [True, False, True, False, True, False, True, True]:  # Horizontal T-shape (east)
            print('T Shape East')
            corner_count += 2
        case [True, False, True, True, True, False, True, False]:  # Horizontal T-shape (west)
            print('T Shape West')
            corner_count += 2

        # L-shape Peninsula (Vertical)
        case [True, True, True, True, False, False, True, True]:  # Vertical L-shape (north variation 1)
            print('L Shape North variation 1')
            corner_count += 2
        case [True, True, True, True, True, False, False, True]:  # Vertical L-shape (north variation 2)
            print('L Shape North variation 2')
            corner_count += 2
        case [False, False, True, True, True, True, True, True]:  # Vertical L-shape (south variation 1)
            print('L Shape South variation 1')
            corner_count += 2
        case [True, False, False, True, True, True, True, True]:  # Vertical L-shape (south variation 2)
            print('L Shape South variation 2')
            corner_count += 2

        # L-shape Peninsula (Horizontal)
        case [False, True, True, True, True, True, True, False]:  # Horizontal L-shape (east variation 1)
            print('L Shape East variation 1')
            corner_count += 2
        case [True, True, True, True, True, True, False, False]:  # Horizontal L-shape (east variation 2)
            print('L Shape East variation 2')
            corner_count += 2
        case [True, True, False, False, True, True, True, True]:  # Horizontal L-shape (west variation 1)
            print('L Shape West variation 1')
            corner_count += 2
        case [True, True, True, False, False, True, True, True]:  # Horizontal L-shape (west variation 2)
            print('L Shape West variation 2')
            corner_count += 2

        # Edge case
        case [False, True, True, False, False, False, True, True]:
            print("Edge case")
            corner_count += 2

        # Cross region
        case [True, False, True, False, True, False, True, False]: # Cross region on cardinals
            print('Cross region variation 1')
            corner_count += 4
        case [False, True, False, True, False, True, False, True]: # Cross region on intercardinals
            print('Cross region variation 2')
            corner_count += 4

        # Alone region
        case [True, True, True, True, True, True, True, True]:
            print('Alone region')
            corner_count += 4

    return corner_count
class Cell():
    def __init__(self):
        self.value : str = None
        self.perimiter_length: int = 0

        self.n_perimiter : bool = True
        self.s_perimiter : bool = True
        self.w_perimiter : bool = True
        self.e_perimiter : bool = True

        self.n: Cell = None
        self.s: Cell = None
        self.w: Cell = None
        self.e: Cell = None

        self.nw: Cell = None
        self.ne: Cell = None
        self.sw: Cell = None
        self.se: Cell = None
        
        self.visited: bool = False
        
class Region():
    _instances = {}

    def __init__(self, identifier):
        self.cells: list[Cell]      = []
        self.identifier: str        = identifier
        self.perimiter_length: int  = 0
        self.num_sides: int         = 0

        Region._instances[identifier] = self

    def add_cell(self, cell):
        self.cells.append(cell)

    def calculate_boundaries(self):
        boundary_sides = 0        
        region_value = self.cells[0].value
        directions = ['nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w']

        for cell in self.cells:
            outside_region = []
            for direction in directions:
                new_cell: Cell = getattr(cell, direction, None)

                if not new_cell or new_cell.value != region_value:
                    outside_region.append(True)
                else:
                    outside_region.append(False)
            boundary_sides += num_boundary(outside_region)
            
        self.num_sides = boundary_sides
        return self.num_sides

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

                # Logic for checking NW
                if i - 1 >= 0 and j - 1 >= 0:
                    cell.nw = self._cells[i - 1][j - 1]

                # Logic for checking N
                if i - 1 >= 0:
                    cell.n = self._cells[i - 1][j]

                # Logic for checking NE
                if i - 1 >= 0 and j + 1 < self._num_cols:
                    cell.ne = self._cells[i - 1][j + 1]

                # Logic for checking E
                if j + 1 < self._num_cols:
                    cell.e = self._cells[i][j + 1]

                # Logic for checking SE
                if i + 1 < self._num_rows and j + 1 < self._num_cols:
                    cell.se = self._cells[i + 1][j + 1]

                # Logic for checking S
                if i + 1 < self._num_rows:
                    cell.s = self._cells[i + 1][j]

                # Logic for checking SW
                if i + 1 < self._num_rows and j - 1 >= 0:
                    cell.sw = self._cells[i + 1][j - 1]

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
    regions: dict[Region] = garden_map.create_regions()
    
    cost_inner_outer    = 0
    cost_outer          = 0
    for key, region_list in regions.items():
        if key == 'C':
            pass
        for region in region_list:
            print('------------------------------------------------')
            print(f'Starting Region: {region.identifier}')
            cost_inner_outer    += len(region.cells) * region.perimiter_length
            cost_outer          += len(region.cells) * region.calculate_boundaries()
            print(f'Region: {region.identifier}. It has {region.num_sides} sides with {len(region.cells)} cells')
            print(f'End Region: {region.identifier}. It has cost {region.num_sides*len(region.cells)}')

    print('------------------------------------------------')
    print(f'Cost of fencing with inner & outer perimiter: {cost_inner_outer}\nCost of fencing with outer perimiter: {cost_outer}')

if __name__ == '__main__':
    solve()