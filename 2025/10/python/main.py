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
    The pseudocode for this solution was pulled from https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
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

    def get_valid_pattern_costs(buttons: list[list[int]]) -> dict[tuple[int, ...], int]:
        from itertools import combinations
        
        pattern_costs = {}
        num_buttons = len(buttons)
        
        for pattern_len in range(num_buttons + 1):
            for button_indices in combinations(range(num_buttons), pattern_len):
                if button_indices:
                    total_effect = tuple(sum(buttons[i][j] for i in button_indices) 
                                    for j in range(len(buttons[0])))
                else:
                    total_effect = tuple(0 for _ in range(len(buttons[0])))
                
                if total_effect not in pattern_costs:
                    pattern_costs[total_effect] = pattern_len
        
        return pattern_costs

    def min_presses_to_zero(target, buttons, all_pattern_costs):
        if all(val == 0 for val in target):
            return 0
        
        memo_key = tuple(target)
        if memo_key in pattern_cost_memo:
            return pattern_cost_memo[memo_key]
        
        min_cost = float("inf")
        for effect_pattern, pattern_cost in all_pattern_costs.items():
            if all(effect <= target_val and effect % 2 == target_val % 2 
                for effect, target_val in zip(effect_pattern, target)):
                
                new_target = tuple((target_val - effect) // 2 
                                for target_val, effect in zip(target, effect_pattern))
                
                recursive_cost = min_presses_to_zero(new_target, buttons, all_pattern_costs)
                total_cost = pattern_cost + (2 * recursive_cost)
                min_cost = min(min_cost, total_cost)

        pattern_cost_memo[memo_key] = min_cost
        return min_cost
    
    ############################
    #   CALC BUTTON PRESSES    #
    ############################
    pattern_cost_memo = {}
    button_presses = 0
    for i, target in enumerate(targets):
        pattern_cost_memo.clear()
        all_pattern_costs = get_valid_pattern_costs(buttons[i])
        button_presses += min_presses_to_zero(target, buttons[i], all_pattern_costs)

    return button_presses

if __name__ == '__main__':
    input_data_file = Path(__file__).parent.parent / 'data.csv'
    input_data = get_data(input_data_file).splitlines()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))