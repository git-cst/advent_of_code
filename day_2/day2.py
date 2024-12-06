import os
import time

def time_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"{func.__name__} took {duration:.4f} seconds to execute.")
        return result
    return wrapper

def generate_arrays():
    array1 = []
    with open(f'{os.path.dirname(__file__)}/day2_input.csv', "r") as file:
        data = file.read()
        data = data.split('\n')

        for row in data:
            values = row.split(' ')
            array1.append(values)
    
    return array1

def safe(array: list, err: bool = None) -> bool:
    if len(array) < 2:
        return True

    offending_indices = set()

    for i in range(len(array) - 1):
        curr_element = int(array[i])
        next_element = int(array[i + 1])

        difference = abs(curr_element - next_element)
        if difference > 3 or difference == 0:
            offending_indices.add(i)
            offending_indices.add(i + 1)

        if i > 0:
            prev_element = int(array[i - 1])
            prev_diff = curr_element - prev_element
            curr_diff = next_element - curr_element
            if (prev_diff < 0 and curr_diff > 0) or (prev_diff > 0 and curr_diff < 0):
                offending_indices.add(i - 1)
                offending_indices.add(i)
                offending_indices.add(i + 1)

    if not offending_indices:
        return True
    if err:
        return False
    
    for index in offending_indices:
        new_array = array[:index] + array[index + 1:]
        if safe(new_array, True):
            return True

    return False

@time_execution
def solve():
    arrays = generate_arrays()

    count_safe = 0
    for arr in arrays:
        if safe(arr):
            count_safe += 1

    print(count_safe)

if __name__ == '__main__':
    solve()