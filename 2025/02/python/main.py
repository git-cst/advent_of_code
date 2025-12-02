from pathlib import Path
import sys
import re

sys.path.append(str(Path(__file__).parent.parent.parent))

from helper_functions.import_data import get_data
from helper_functions.time_execution import time_execution

@time_execution
def solve_part_1(input_data: list[str]) -> int:
    invalid_sum = 0
    for product_id in input_data:
        l_bound, u_bound = product_id.split("-")

        for num in range(int(l_bound), int(u_bound)+1):
            str_num = str(num)
            len_num = len(str_num)
            if len_num % 2 != 0: # odd numbers cannot be invalid
                continue

            midpoint = len_num//2
            left_part = str_num[:midpoint]
            right_part = str_num[midpoint:]
            
            if left_part == right_part:
                invalid_sum += num

    return invalid_sum

@time_execution
def solve_part_1_regex(input_data: list[str]) -> int:
    invalid_sum = 0
    regex_pattern = r'^(\d+)\1$'
    for product_id in input_data:
        l_bound, u_bound = product_id.split("-")

        for num in range(int(l_bound), int(u_bound)+1):
            str_num = str(num)
            if bool(re.match(regex_pattern, str_num)):
                invalid_sum += num

    return invalid_sum

@time_execution
def solve_part_2(input_data: list[str]) -> int:
    def factors(n: int) -> list[int]:
        result = []
        for i in range(1, int(n ** 0.5)+1):
            if n % i == 0:
                result.append(i)
                if i != n // i:
                    result.append(n // i)
        return sorted(result)
    
    def split_after_n(number: str, n):
        return [number[i:i+n] for i in range(0, len(number), n)]

    invalid_sum = 0
    for product_id in input_data:
        l_bound, u_bound = product_id.split("-")

        for num in range(int(l_bound), int(u_bound)+1):
            str_num = str(num)
            list_of_factors = factors(len(str_num))

            for factor in list_of_factors:
                comparators = split_after_n(str_num, factor)
                if len(comparators) == 1:
                    continue
                if len(set(comparators)) == 1:
                    invalid_sum += num
                    break                         

    return invalid_sum

@time_execution
def solve_part_2_regex(input_data: list[str]) -> int:
    invalid_sum = 0
    regex_pattern = r'^(\d+)\1+$'
    for product_id in input_data:
        l_bound, u_bound = product_id.split("-")

        for num in range(int(l_bound), int(u_bound)+1):
            str_num = str(num)
            if bool(re.match(regex_pattern, str_num)):
                invalid_sum += num

    return invalid_sum

if __name__ == '__main__':
    input_file_path = Path(__file__).parent.parent / 'data.csv'
    data = get_data(input_file_path.absolute()).split(",")
    
    print(solve_part_1(data))
    print(solve_part_1_regex(data))
    print(solve_part_2(data))
    print(solve_part_2_regex(data))