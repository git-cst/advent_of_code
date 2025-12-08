from pathlib import Path
import sys
from enum import Enum

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


class Direction(Enum):
    DOWN = "s"
    DOWN_LEFT = "w"
    DOWN_RIGHT = "e"
    
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
        self.active_beams: dict[int, set[Cell]] = {}
        
    def generate_grid(self, input_data):
        self._num_rows = len(input_data)
        self._num_cols = len(input_data[0])

        self._cells: list[list[Cell]] = [[Cell() for _ in range(self._num_cols)] for _ in range(self._num_rows)]

        for row in range(self._num_rows):
            for col in range(self._num_cols):
                node = self._cells[row][col]
                input_data_value = input_data[row][col]
                node.value = input_data_value
                node.pos = (row, col)
                
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
        self.count_splits: int = 0

        start_row, start_col = self.start_point.pos
        start_beam: Cell = self._cells[start_row + 1][start_col]
        start_beam.value = "|"

        self.active_beams[1] = set()
        self.active_beams[1].add(start_beam)
        
        for row in range(2, self._num_rows):
            self.active_beams[row] = set()
            for beam in self.active_beams[row - 1]:
                _, beam_col = beam.pos

                current_cell: Cell = self._cells[row][beam_col]

                if (row, beam_col) in self.splitters:
                    self.count_splits += 1
                    left_adjacent_cell = current_cell.w
                    right_adjacent_cell = current_cell.e

                    if left_adjacent_cell:
                        left_adjacent_cell.value = "|" 
                        self.active_beams[row].add(left_adjacent_cell)

                    if right_adjacent_cell:
                        right_adjacent_cell.value = "|"
                        self.active_beams[row].add(right_adjacent_cell)

                else:
                    current_cell.value = "|"
                    self.active_beams[row].add(current_cell)

    def calculate_unique_paths(self):
        memo = {}
        def count_paths(cell: Cell, direction: Direction):
            state = (cell.pos, direction)

            if state in memo:
                return memo[state]
            
            if not cell.s:
                return 1
            
            count = 0
            if cell.s.pos in self.splitters:
                count += count_paths(cell.s.w, Direction.DOWN_LEFT)
                count += count_paths(cell.s.e, Direction.DOWN_RIGHT)
            else:
                count += count_paths(cell.s, Direction.DOWN)

            memo[state] = count
            return count
    
        self.path_count = count_paths(self.start_point, Direction.DOWN)

    def print_grid(self):
        """Debug method"""               

        for row in range(self._num_rows):
            print_value = []
            for col in range(self._num_cols):
                cell_value = self._cells[row][col].value
                print_value.append(COLORS[cell_value] + cell_value + COLORS['reset'])

            print("".join(print_value))
        print("\n")


@time_execution
def solve_part_1(input_data: list[str]) -> int:
    grid = Grid()
    grid.generate_grid(input_data)
    grid.calculate_tachyons()
    return grid.count_splits

@time_execution
def solve_part_2(input_data: list[str]) -> int:
    grid = Grid()
    grid.generate_grid(input_data)
    grid.calculate_unique_paths()
    return grid.path_count

if __name__ == '__main__':
    input_data_path = Path(__file__).parent.parent / 'data.csv'
    input_data = get_data(input_data_path).splitlines()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))