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
    targets = []
    buttons = []

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

@time_execution
def solve_part_2(input_data: list[str]) -> int:
    """
    The process for this solution was pulled from https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
    I didn't want to implement my own integer linear programming setup or use libraries such as scipy or z3
    """
    def convert_buttons_to_list(button_list: list[str], target_length) -> list[int]:
        converted_buttons = []
        for button_tuple in button_list:
            button_effects = [0 for _ in range(target_length)]
            button_tuple = list(map(int, button_tuple.split(",")))
            for button in button_tuple:
                button_effects[button] += 1

            converted_buttons.append(button_effects)

        return converted_buttons

    #########################
    #   INPUT CONVERSION    #
    #########################
    targets = []
    buttons = []

    for manual_info in input_data:
        target = list(map(int, re.findall(r'\{(.+)\}', manual_info)[0].split(",")))
        target_len = len(target)
        targets.append(target)

        button_list = re.findall(r'\(([^)]+)\)', manual_info)
        buttons.append(convert_buttons_to_list(button_list, target_len))

    # Helper functions for button calculation
    def generate_possible_button_combinations(list_of_buttons: list[int]) -> list[int]:
        from itertools import combinations
        all_combinations = []
        # Generate subsets of all lengths (0 to n)
        for r in range(len(list_of_buttons) + 1):
            for combo in combinations(list_of_buttons, r):
                all_combinations.append(list(combo))
        return all_combinations

    def convert_list_to_binary_int(list: list[int]) -> int:
        string_list = (str(val) for val in list)
        binary_string = "".join(string_list)
        return int(binary_string, 2)

    def get_valid_patterns(target: list[int], buttons: list[list[int]]) -> list[list[int]]:
        memo_key = (tuple(target), tuple(tuple(button) for button in buttons))
        if memo_key in pattern_memo:
            return pattern_memo[memo_key]

        pattern_to_reach = []
        for val in target:
            if val % 2 != 0:
                pattern_to_reach.append(1)
            else:
                pattern_to_reach.append(0)

        possible_combinations = generate_possible_button_combinations(buttons)
        target_bin_number = convert_list_to_binary_int(pattern_to_reach)
        valid_patterns = []
        for combination in possible_combinations:
            curr_bin_number = 0
            for button in combination:
                curr_bin_number ^= convert_list_to_binary_int(button)

            if curr_bin_number == target_bin_number:
                valid_patterns.append(combination)
            
        pattern_memo[memo_key] = valid_patterns
        return valid_patterns

    def min_presses_to_zero(target, buttons):
        if sum(target) == 0:
            return 0
        
        memo_key = (tuple(target), tuple(tuple(button) for button in buttons))
        if memo_key in pattern_cost_memo:
            return pattern_cost_memo[memo_key]

        valid_patterns = get_valid_patterns(target, buttons)
        min_cost = float("inf")
        for pattern in valid_patterns:
            current_pattern_cost = len(pattern)
            
            total_effects = [sum(effects) for effects in zip(*pattern)]
            new_target = [(target_val - total_effects_val) // 2 for target_val, total_effects_val in zip(target, total_effects)]
            if any(val < 0 for val in new_target):
                continue

            recursive_cost = min_presses_to_zero(new_target, buttons)
            total_cost = current_pattern_cost + recursive_cost
            min_cost = min(min_cost, total_cost)

        pattern_cost_memo[memo_key] = min_cost
        return min_cost
    
    ############################
    #   CALC BUTTON PRESSES    #
    ############################
    pattern_memo = {}
    pattern_cost_memo = {}
    button_presses = 0
    for i, target in enumerate(targets):
        button_presses += min_presses_to_zero(target, buttons[i])

    return button_presses

if __name__ == '__main__':
    input_data_file = Path(__file__).parent.parent / 'test.csv'
    input_data = get_data(input_data_file).splitlines()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))