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
    with open(f'{os.path.dirname(__file__)}/day9_input.txt', 'r') as file:
        file_data: str = file.read()
    
    return file_data

def generate_unicode(number, base_char = 'a'):
    return chr(ord(base_char) + number)

def generate_index(unicode_char, base_char = 'a'):
    index = ord(unicode_char) - ord(base_char)

    return index

def generate_disk_map(data):
    id = 0
    index = 0
    parts = []
    while index <= len(data):
        file_length = generate_unicode(id) * int(data[index])
        free_disk_space = '\u002E' * int(data[index + 1]) if index + 1 < len(data) else ''
        parts.append(file_length + free_disk_space)

        id += 1
        index += 2

    return "".join(parts)

def quick_defrag(array):
    left, right = 0, len(array) - 1
    checksum = 0

    # Go from left to right.
    # If value is '.' then begin looking for a value to swap with.
    # If the value on the right is not '.' then swap, increment the checksum value and then move right on the left and left on the right.
    # If the value on the left is not '.' increment the checksum value.
    while left <= right:
        if array[left] == '\u002E':
            if array[right] != '\u002E':
                array[left], array[right] = array[right], array[left]
                checksum += left * generate_index(array[left])
                right -= 1
                left += 1
            else:
                right -= 1
        else:
            checksum += left * generate_index(array[left])
            left += 1

    return checksum

@time_execution
def solve():
    data = get_data()
    disk_map = generate_disk_map(data)
    print(quick_defrag(list(disk_map)))

if __name__ == "__main__":
    solve()