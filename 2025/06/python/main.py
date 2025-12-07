from pathlib import Path
import sys
import re

sys.path.append(str(Path(__file__).parent.parent.parent))

from helper_functions.import_data import get_data
from helper_functions.time_execution import time_execution

@time_execution
def solve_part_1(input_data: list[str]) -> int:
    memo = {}
    operations = {
        '+': lambda x, y: int(x) + int(y),
        '*': lambda x, y: int(x) * int(y)
    }

    def calculate_sum(val1: str, val2: str, operator: str) -> int:
        if (val1, val2, operator) in memo:
            return memo[(val1, val2, operator)]
        
        memo[(val1, val2, operator)] = operations[operator](val1, val2)

        return memo[(val1, val2, operator)]

    # Normalize dataset
    val1_list, val2_list, val3_list, val4_list, operator_list = input_data
    operator_list: list[str]  =  re.findall("([*+])", operator_list)
    val1_list: list[str]  = re.findall("(\\d+)", val1_list)
    val2_list: list[str]  = re.findall("(\\d+)", val2_list)
    val3_list: list[str]  = re.findall("(\\d+)", val3_list)
    val4_list: list[str]  = re.findall("(\\d+)", val4_list)
    
    num_operations = len(operator_list)
    problem_sum = 0
    for i in range(0, num_operations):
        intermediate_calc1 = calculate_sum(val1_list[i], val2_list[i], operator_list[i])
        intermediate_calc2 = calculate_sum(intermediate_calc1, val3_list[i], operator_list[i])
        final_calc = calculate_sum(intermediate_calc2, val4_list[i], operator_list[i])

        problem_sum += final_calc

    return problem_sum

@time_execution
def solve_part_2(input_data):
    memo = {}
    operations = {
        '+': lambda x, y: int(x) + int(y),
        '*': lambda x, y: int(x) * int(y)
    }

    def extract_data(input_data: list[list[str]]) -> list[list[str]]:
        num_lists = len(input_data) - 1
        num_chars = len(input_data[0])

        problem_values: dict[int, list] = {}
        problem_counter = 0
        for i in range(num_chars):
            if problem_values.get(problem_counter, 0) == 0:
                problem_values[problem_counter] = []
            curr_val = ""
            all_spaces = True
            for j in range(num_lists):
                if input_data[j][i] != " ":
                    curr_val += input_data[j][i]
                    all_spaces = False

            if all_spaces:
                problem_counter += 1
            else:
                problem_values[problem_counter].append(int(curr_val))

        return problem_values

    def calculate_sum(val1: str, val2: str, operator: str) -> int:
        if (val1, val2, operator) in memo:
            return memo[(val1, val2, operator)]
        
        memo[(val1, val2, operator)] = operations[operator](val1, val2)

        return memo[(val1, val2, operator)]
    
    # Normalize dataset
    problem_values = extract_data(input_data)
    operator_list = input_data[-1]
    operator_list: list[str] =  re.findall("([*+])", operator_list)

    problem_sum = 0
    for idx, operation in enumerate(operator_list):
        curr_sum = 0
        for i in range(len(problem_values[idx])-1):
            if curr_sum == 0:
                curr_sum = calculate_sum(problem_values[idx][i], problem_values[idx][i+1], operation)
            else:
                curr_sum = calculate_sum(curr_sum, problem_values[idx][i+1], operation)

        problem_sum += curr_sum

    return problem_sum

if __name__ == '__main__':
    input_data_path = Path(__file__).parent.parent / 'data.csv'
    input_data = get_data(input_data_path).splitlines()

    #print(solve_part_1(input_data))
    print(solve_part_2(input_data))