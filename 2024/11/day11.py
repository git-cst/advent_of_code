import os; import time
from collections import defaultdict

def time_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"{func.__name__} took {duration:.4f} seconds to execute.")
        return result
    return wrapper

def get_data():
    data = {}
    with open(f'{os.path.dirname(__file__)}/day11_input.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split(' ')

    array = []
    for value in file_data:
        array.append(value)

    return array

def split_string_in_half(string, cache):
    if string in cache:
        return cache[string]
    else:
        mid = len(string) // 2
        left, right = string[:mid], str(int(string[mid:]))
        cache[string] = (left, right)
    return left, right

def multiply_by_2024(value, cache):
    if value in cache:
        return cache[value]
    else:
        mutiplication = value * 2024
        cache[value] = str(mutiplication)
    return str(mutiplication)

cache = {}
def calculate_stone_length(array: list, times_blinked: int) -> list:
    blinks = 0
    while blinks < times_blinked:
        new_array = []
        for index, value in enumerate(array):
            if value == 0:
                new_array.append('1')
            elif len(value) % 2 == 0:
                left_value, right_value = split_string_in_half(value, cache)
                new_array.append(left_value)
                new_array.append(right_value)
            else:
                new_array.append(multiply_by_2024(int(value), cache))
        
        array = new_array        
        blinks += 1

    return array

def calculate_stone_length_dictionary(array: list, max_blinks: int) -> list:
    stones = defaultdict(int)
    for stone in array:
        stones[stone] = 1

    blinks = 0
    while blinks < max_blinks:
        new_stones = defaultdict(int)
        for key, value in stones.items():
            if key == '0':
                new_stones['1'] += value
            elif len(key) % 2 == 0:
                left, right = split_string_in_half(key, cache)
                new_stones[left] += value
                new_stones[right] += value
            else:
                new_stones[str(int(key)*2024)] += value

        stones = new_stones        
        blinks += 1

    return sum([value for value in stones.values()])

def calculate_stone_length_dictionary2(array: list, max_blinks: int) -> list:
    stones = {}
    for stone in array:
        stones[stone] = 1

    blinks = 0
    while blinks < max_blinks:
        new_stones = {}
        for key, value in stones.items():
            if key == '0':
                new_stones['1'] = new_stones.get('1', 0) + value
            elif len(key) % 2 == 0:
                left, right = split_string_in_half(key, cache)
                new_stones[left] = new_stones.get(left, 0) + value
                new_stones[right] = new_stones.get(right, 0) + value
            else:
                new_stones[str(int(key)*2024)] = new_stones.get(str(int(key)*2024), 0) + value

        stones = new_stones
        blinks += 1

    return sum([value for value in stones.values()])

@time_execution
def solve():
    array = get_data()
    num_blinks = 25
    length_of_stones = calculate_stone_length_dictionary(array, num_blinks)

    print(f"Total length of stones after blinking {num_blinks} times: {length_of_stones}\n")

    num_blinks = 75
    length_of_stones = calculate_stone_length_dictionary2(array, num_blinks)
    
    print(f"Total length of stones after blinking {num_blinks} times: {length_of_stones}\n")

if __name__ == '__main__':
    solve()

