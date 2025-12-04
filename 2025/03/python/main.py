from pathlib import Path
import sys
import re

sys.path.append(str(Path(__file__).parent.parent.parent))

from helper_functions.import_data import get_data
from helper_functions.time_execution import time_execution

@time_execution
def solve_part_1(battery_banks: list[str]) -> int:
    total_joltage = 0

    for battery_bank in battery_banks:
        battery_bank_len = len(battery_bank)

        left_jolt = 0
        right_jolt = 0
        for i in range(0, battery_bank_len - 1):
            if int(battery_bank[i]) > left_jolt:
                left_jolt = int(battery_bank[i])
                l_bound_r_val = i

            if left_jolt == 9:
                break

        for i in range(battery_bank_len - 1, l_bound_r_val, -1):
            if int(battery_bank[i]) > right_jolt:
                right_jolt = int(battery_bank[i])

            if right_jolt == 9:
                break

        total_joltage += int(str(left_jolt) + str(right_jolt))

    return total_joltage

@time_execution
def solve_part_2(battery_banks: list[str]) -> int:
    total_joltage = 0
    max_length = 12 

    for battery_bank in battery_banks:       
        joltage = ""
        end_index = len(battery_bank) - (max_length - 1)
        start_index = 0
        
        while len(joltage) < max_length:
            search_interval = battery_bank[start_index:end_index]
            curr_max = 0
            for index, jolt in enumerate(search_interval):
                if jolt == '9':
                    curr_max = 9
                    new_index = index + 1
                    break
                
                if int(jolt) > curr_max:
                    curr_max = int(jolt)
                    new_index = index + 1
            
            start_index = start_index + new_index
            end_index += 1
            joltage += str(curr_max)

        total_joltage += int(joltage)       
            
    return total_joltage

if __name__ == '__main__':
    input_file_path = Path(__file__).parent.parent / 'data.csv'
    data = get_data(input_file_path).splitlines()

    print(solve_part_1(data))
    print(solve_part_2(data))