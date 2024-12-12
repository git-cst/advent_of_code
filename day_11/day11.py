import os; import time

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
    with open(f'{os.path.dirname(__file__)}/day11_testinput.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split(' ')

    array = []
    for value in file_data:
        array.append(int(value))

    return array

def split_string_in_half(string, cache):
    if string in cache:
        return cache[string]
    else:
        mid = len(string) // 2
        left, right = int(string[:mid]), int(string[mid:])
        cache[string] = (left, right)
    return left, right

def multiply_by_2024(value, cache):
    if value in cache:
        return cache[value]
    else:
        mutiplication = value * 2024
        cache[value] = mutiplication
    return mutiplication

def calculate_stone_length(array: list, times_blinked: int) -> list:
    cache = {}
    blinks = 0
    while blinks < times_blinked:
        new_array = []
        for index, value in enumerate(array):
            string_value = str(value)
            if value == 0:
                new_array.append(1)
            elif len(string_value) % 2 == 0:
                left_value, right_value = split_string_in_half(string_value, cache)
                new_array.append(left_value)
                new_array.append(right_value)
            else:
                new_array.append(multiply_by_2024(value, cache))
        
        array = new_array        
        blinks += 1

    return array

memo = {}
def calculate_stone_length_recursively(value: int, max_blinks: int, times_blinked: int = 0, array: list = None) -> list:
    if array is None:
        array = []
    
    # Base case
    if times_blinked == max_blinks:
        return array
    
    # Handle both single values and tuples
    if not isinstance(value, tuple):
        # Rule processing for single value
        if value not in memo:
            string_value = str(value)
            if value == 0:
                memo[value] = 1
            elif len(string_value) % 2 == 0:
                mid = len(string_value) // 2
                memo[value] = (int(string_value[:mid]), int(string_value[mid:]))
            else:
                memo[value] = value * 2024
        
        new_value = memo[value]
    else:
        # Handle tuple (split stones)
        new_value = value

    # Append to array
    if isinstance(new_value, tuple):
        array.append(new_value[0])
        array.append(new_value[1])
        # Recursively process both parts        
        calculate_stone_length_recursively(new_value[0], max_blinks, times_blinked + 1, array)
        return calculate_stone_length_recursively(new_value[1], max_blinks, times_blinked + 1, array)
    else:
        array.append(new_value)
        return calculate_stone_length_recursively(new_value, max_blinks, times_blinked + 1, array)

@time_execution
def solve():
    array = get_data()
    num_blinks = 25
    length_of_stones = len(calculate_stone_length(array, num_blinks))

    print(f"Total length of stones after blinking {num_blinks} times: {length_of_stones}\n")
    
    print(f"Total length of stones after blinking {num_blinks} times: {length_of_stones}\n")

if __name__ == '__main__':
    solve()

