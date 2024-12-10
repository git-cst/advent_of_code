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
    files = []
    id = 0
    index = 0
    parts = []
    while index <= len(data):
        file_length = generate_unicode(id) * int(data[index])
        free_disk_space = '\u002E' * int(data[index + 1]) if index + 1 < len(data) else ''
        parts.append(file_length + free_disk_space)
        files.append((id, int(data[index])))

        id += 1
        index += 2

    return "".join(parts), files

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


# def move_files(disk_map: list, files: list[int, int], open_positions: list) -> str:
#     if not files:
#         return "".join(disk_map)

#     file_id, file_length = files.pop(0)
#     unicode_file_id = generate_unicode(file_id)

#     file_positions = [i for i, value in enumerate(disk_map) if value == unicode_file_id]

#     for index, (start_open, block_length) in enumerate(open_positions):
#         if block_length >= file_length:
#             for pos in file_positions:
#                 disk_map[pos] = '\u002E'
#             for i in range(file_length):
#                 disk_map[start_open + i] = unicode_file_id

            
#             old_positions = open_positions[:]
#             #open_positions.pop(index)
#             if start_open + file_length == start_open + block_length:
#                 open_positions.pop(index)
#             if start_open + file_length < start_open + block_length:
#                 new_position = (start_open + file_length, block_length - file_length)
#                 open_positions[index] = new_position

#             #open_positions = open_positions[:index] + new_positions + open_positions[index + 1:]
#             break
            
#     return move_files(disk_map, files, open_positions)

def move_files(disk_map: list, files: list[int, int], open_positions: list) -> str:
    for file_id, file_length in files:
        unicode_file_id = generate_unicode(file_id)
        file_positions = [i for i, value in enumerate(disk_map) if value == unicode_file_id]

        for index, (start_open, block_length) in enumerate(open_positions):
            if block_length >= file_length:
                for pos in file_positions:
                    disk_map[pos] = '\u002E'
                for i in range(file_length):
                    disk_map[start_open + i] = unicode_file_id

                if start_open + file_length == start_open + block_length:
                    open_positions.pop(index)
                if start_open + file_length < start_open + block_length:
                    new_position = (start_open + file_length, block_length - file_length)
                    open_positions[index] = new_position
                break
    
    return disk_map

def change_into_file_ids(disk_map):
    disk_map = list(disk_map)
    for i, value in enumerate(disk_map):
        if value != '\u002E':
            disk_map[i] = generate_index(value)

    return "".join(map(str, disk_map))

def generate_checksum(disk_map):
    checksum = 0
    for i, value in enumerate(disk_map):
        if value != '\u002E':
            checksum += i * generate_index(value)

    return checksum


@time_execution
def solve():
    data = get_data()
    disk_map, files = generate_disk_map(data)
    part1 = quick_defrag(list(disk_map))
    files.sort(reverse=True)

    open_positions = []
    start_open, block_length = None, 0
    for i, value in enumerate(disk_map):
        if value == '\u002E':
            if start_open == None:
                start_open = i
            block_length += 1
        else:
            if block_length > 0:
                open_positions.append((start_open, block_length))
                start_open = None
                block_length = 0

    part2 = generate_checksum(move_files(list(disk_map), files, open_positions))

    print(f"Checksum while fragmenting files: {part1}\nChecksum while keeping files intact: {part2}")

if __name__ == "__main__":
    solve()