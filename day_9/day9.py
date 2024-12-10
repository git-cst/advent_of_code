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

def defrag(array):
    checksum = 0
    left, right = 0, len(array)
    while left < right:
        curr_val = array[left]
        if array[left] == '\u002E':
            while right > left:
                right -= 1
                if right > left and array[right] != '\u002E':
                    array[left], array[right] = array[right], array[left]
                    right = len(array)
                    break
        left += 1

    for index, unicode in enumerate(array):
        if unicode == '\u002E':
            break
        checksum += index * generate_index(unicode)

    return checksum

@time_execution
def solve():
    data = get_data()
    disk_map = generate_disk_map(data)
    print(defrag(list(disk_map)))

if __name__ == "__main__":
    solve()