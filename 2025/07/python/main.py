from pathlib import Path
import sys
import re

sys.path.append(str(Path(__file__).parent.parent.parent))

from helper_functions.import_data import get_data
from helper_functions.time_execution import time_execution

COLORS = {
    'S': '\033[93m',  # Yellow
    '^': '\033[92m',  # Red  
    '.': '\033[90m',  # Gray
    '|': '\033[91m',  # Gray
    'reset': '\033[0m'
}


class Cell:
    def __init__(self):
        self.value = None
        self.pos = None

        # Adjacencies
        self.w: Cell = None
        self.e: Cell = None
        self.s: Cell = None

    def set_pos(self, row, col):
        self.pos = (row, col)

class Grid:
    def __init__(self):
        self._num_cols: None | int = None
        self._num_rows: None | int = None

        self.start_point: Cell = None
        self.splitters: dict[tuple[int, int], Cell] = {}
        self.active_beams: list[Cell] = []

    def generate_grid(self, input_data):
        self._num_rows = len(input_data)
        self._num_cols = len(input_data[0])

        self._cells: list[list[Cell]] = [[Cell() for _ in range(self._num_cols)] for _ in range(self._num_rows)]

        for row in range(self._num_rows):
            for col in range(self._num_cols):
                node = self._cells[row][col]
                input_data_value = input_data[row][col]
                node.value = input_data_value
                
                if input_data_value != ".":
                    node.set_pos(row, col)

                    if input_data_value == "^":
                        self.splitters[(row, col)] = node
                    elif input_data_value == "S":
                        self.start_point = node

                # east adjacency
                if col + 1 < self._num_cols:
                    node.e = self._cells[row][col + 1]

                # south adjacency
                if row + 1 < self._num_rows:
                    node.s = self._cells[row + 1][col]

                # west adjacency
                if col - 1 >= 0:
                    node.w = self._cells[row][col - 1]
                        
    def calculate_tachyons(self):
        """Calculates the answer based on the x coordinates"""
        pass

    def generate_tachyons(self):
        """Iteratively calculates if there should be a tachyon beam or not. Useful for animation"""
        pass

    def print_grid(self):
        """Debug method"""               

        for row in range(self._num_rows):
            print_value = []
            for col in range(self._num_cols):
                cell_value = self._cells[row][col].value
                print_value.append(COLORS[cell_value] + cell_value + COLORS['reset'])

            print("".join(print_value))


@time_execution
def solve_part_1(input_data: list[str]) -> int:
    grid = Grid()
    grid.generate_grid(input_data)
    grid.print_grid()
    pass

if __name__ == '__main__':
    input_data_path = Path(__file__).parent.parent / 'test.csv'
    input_data = get_data(input_data_path).splitlines()

    print(solve_part_1(input_data))