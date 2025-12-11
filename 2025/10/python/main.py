from pathlib import Path
import sys
from dataclasses import dataclass
from enum import Enum
import re

sys.path.append(str(Path(__file__).parent.parent.parent))

from helper_functions.import_data import get_data
from helper_functions.time_execution import time_execution

@time_execution
def solve_part_1(input_data: list[str]):
    targets = []
    buttons = []
    #joltages = []

    def convert_target_to_bitmask(target: str) -> bytes:
        result = 0
        length = len(target)
        for i, char in enumerate(target):
            if char == '#':
                bit_position = length - 1 - i
                result |= (1 << bit_position)
        return result
    
    def convert_positions_to_bitmask(position_strings: list[str], length: int) -> bytes:
        results = []
        for pos_str in position_strings:
            result = 0
            positions = pos_str.split(",")
            for pos in positions:
                bit_position = length - 1 - int(pos)
                result |= (1 << bit_position)
            results.append(result)
        return results
    
    def create_subsets(list: list[int], size: int) -> list[int]:
        from itertools import combinations
        return combinations(list, size)

    # Create bitmasks for all problems
    for manual_info in input_data:
        target = re.findall(r'\[(.+)\]', manual_info)[0]
        target_len = len(target)
        target_bitmask = convert_target_to_bitmask(target)
        targets.append(target_bitmask)

        button_list = re.findall(r'\(([^)]+)\)', manual_info)
        button_list_bitmask = convert_positions_to_bitmask(button_list, target_len)
        buttons.append(button_list_bitmask)
    
    button_presses = 0
    for i in range(len(input_data)):
        target_state = targets[i]
        button_list = buttons[i]
        
        size = 1
        found = False
        while not found:
            for subset in create_subsets(button_list, size):
                current_state = 0
                for binary_number in subset:
                    current_state = current_state ^ binary_number
                    if target_state == current_state:
                        button_presses += size
                        found = True        
                        break
                
                if found == True:
                    break

            size += 1
    
    return button_presses


if __name__ == '__main__':
    input_data_file = Path(__file__).parent.parent / 'data.csv'
    input_data = get_data(input_data_file).splitlines()

    print(solve_part_1(input_data))