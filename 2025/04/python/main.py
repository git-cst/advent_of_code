from pathlib import Path
import sys
import re
from typing import Optional

sys.path.append(str(Path(__file__).parent.parent.parent))

from helper_functions.import_data import get_data
from helper_functions.time_execution import time_execution

class PaperRoll:
    def __init__(self):
        # Value
        self.value: Optional[str] = None

        # Adjacencies
        self.n: Optional[PaperRoll] = None
        self.ne: Optional[PaperRoll] = None
        self.e: Optional[PaperRoll] = None
        self.se: Optional[PaperRoll] = None
        self.s: Optional[PaperRoll] = None
        self.sw: Optional[PaperRoll] = None
        self.w: Optional[PaperRoll] = None
        self.nw: Optional[PaperRoll] = None

    def __iter__(self):
        yield from [self.n, self.ne, self.e, self.se, self.s, self.sw, self.w, self.nw]

    def count_adjacencies(self):
        if self.value == ".":
            return 0

        count = 0
        for adjacency in self:
            if adjacency and adjacency.value in ["@", "x"]:
                count += 1

        return count
    
    def should_remove(self):
        return self.value != "." and self.count_adjacencies() < 4

class Warehouse:
    def __init__(self):
        self._num_cols: int = None
        self._num_rows: int = None
        self.warehouse_layout: list[list[PaperRoll]] = None

        self._active_cells: dict[tuple[int, int], PaperRoll] = {}
        self._valid_paper_rolls: dict[tuple[int, int], PaperRoll] = {}

    def generate_grid(self, warehouse_layout: list[str]):
        self._num_cols = len(data[0])
        self._num_rows = len(data)

        if not self.warehouse_layout:
            self.warehouse_layout: list[list[PaperRoll]] = [[PaperRoll() for _ in range(self._num_cols)] for _ in range(self._num_rows)]

        for row in range(self._num_rows):
            for col in range(self._num_cols):
                paper_roll = self.warehouse_layout[row][col]
                paper_roll.value = warehouse_layout[row][col]

                if paper_roll.value != ".":
                    self._active_cells[(row, col)] = paper_roll

                # north west adjacency
                if row - 1 >= 0 and col - 1 >= 0:
                    paper_roll.nw = self.warehouse_layout[row - 1][col - 1]

                # north adjacency
                if row - 1 >= 0:
                    paper_roll.n = self.warehouse_layout[row - 1][col]

                # north east adjacency
                if row - 1 >= 0 and col + 1 < self._num_cols:
                    paper_roll.ne = self.warehouse_layout[row - 1][col + 1]

                # east adjacency
                if col + 1 < self._num_cols:
                    paper_roll.e = self.warehouse_layout[row][col + 1]

                # south east adjacency
                if row + 1 < self._num_rows and col + 1 < self._num_cols:
                    paper_roll.se = self.warehouse_layout[row + 1][col + 1]

                # south adjacency
                if row + 1 < self._num_rows:
                    paper_roll.s = self.warehouse_layout[row + 1][col]

                # south west adjacency
                if row + 1 < self._num_rows and col - 1 >= 0:
                    paper_roll.sw = self.warehouse_layout[row + 1][col - 1]

                # west adjacency
                if col - 1 >= 0:
                    paper_roll.w = self.warehouse_layout[row][col - 1]

    def count_valid_adjacencies(self):
        if self.warehouse_layout is None:
            raise RuntimeError("Calling count before a warehouse layout is created")
        
        self._valid_paper_rolls.clear()

        for (row, col), paper_roll in self._active_cells.items():
            paper_roll_adjacencies = paper_roll.count_adjacencies()
            if paper_roll_adjacencies < 4:
                self._valid_paper_rolls[(row, col)] = paper_roll

    def remove_valid_paper_rolls(self):
        if not hasattr(self, '_removed_rolls'):
            self._removed_rolls = 0

        for (row, col), paper_roll in self._valid_paper_rolls.items():
            paper_roll.value = "."
            self._removed_rolls += 1
            self._active_cells.pop((row, col))
        
    def print_warehouse_layout(self):
        """Debug method"""       
        def mark_removable_rolls():
            for _, paper_roll in self._active_cells.items():
                if paper_roll.should_remove():
                    paper_roll.value = 'x'

        if self.warehouse_layout is None:
            raise RuntimeError("Calling debug before a warehouse layout is created")
        
        mark_removable_rolls()

        for row in range(self._num_rows):
            print_value = []
            for col in range(self._num_cols):
                print_value.append(self.warehouse_layout[row][col].value)

            print(print_value)    

    @property
    def num_valid_paper_rolls(self):
        return len(self._valid_paper_rolls.keys())
    
    @property
    def num_removed_paper_rolls(self):
        return self._removed_rolls

@time_execution
def solve_part_1(warehouse_layout: list[str]) -> int:
    warehouse = Warehouse()
    warehouse.generate_grid(warehouse_layout)
    warehouse.count_valid_adjacencies()
    return warehouse.num_valid_paper_rolls

@time_execution
def solve_part_2(warehouse_layout: list[str]) -> int:
    warehouse = Warehouse()
    warehouse.generate_grid(warehouse_layout)
    warehouse.count_valid_adjacencies()

    while warehouse.num_valid_paper_rolls > 0:
        warehouse.remove_valid_paper_rolls()
        warehouse.count_valid_adjacencies()

    return warehouse.num_removed_paper_rolls

if __name__ == '__main__':
    input_file_path = Path(__file__).parent.parent / 'data.csv'
    data = get_data(input_file_path).splitlines()

    print('='*20)
    print(' ' * 7 + 'Part 1' + ' ' * 7)
    print('='*20)
    print(f'Number of removable paper rolls: {solve_part_1(data)}')

    print('='*20)
    print(' ' * 7 + 'Part 2' + ' ' * 7)
    print('='*20)
    print(f'Number of removed paper rolls: {solve_part_2(data)}')