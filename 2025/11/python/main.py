from pathlib import Path
import sys
from dataclasses import dataclass
from enum import Enum
import re

sys.path.append(str(Path(__file__).parent.parent.parent))

from helper_functions.import_data import get_data
from helper_functions.time_execution import time_execution

@time_execution
def solve_part_1(input_data: list[str]) -> int:
    pass

@time_execution
def solve_part_2(input_data: list[str]) -> int:
    pass

if __name__ == '__main__':
    input_data_file = Path(__file__).parent.parent / 'test.csv'
    input_data = get_data(input_data_file).splitlines()

    print(solve_part_1(input_data))