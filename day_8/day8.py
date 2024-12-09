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
    with open(f'{os.path.dirname(__file__)}/day8_input.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')
    return file_data

def generate_node_coords(data):
    node_pair_dictionary = {}
    populated_cells = {}

    # Loop through the entire grid
    # Generate a hashmap of occupied cells used for anti-node look up to see if it can be placed
    # Generate a hashmap of nodes: Where each key contains all the node coordinates
    for i in range(0, len(data)):
        for j in range(0, len(data[0])):
            if data[i][j] != '.':
                populated_cells[(i, j)] = 1
                if data[i][j] in node_pair_dictionary:
                    temp: list[tuple] = node_pair_dictionary[data[i][j]]
                    temp.append((i,j))
                    node_pair_dictionary[data[i][j]] = temp
                else:
                    node_pair_dictionary[data[i][j]] = [(i, j)]
    
    return node_pair_dictionary, populated_cells

def calculate_antinodes_recursive(node_coords, populated_cells, current_index=0, antinodes=None) -> list:
    if antinodes is None:
        antinodes = []

    # Base case: If we reach the last node, stop recursion
    if current_index >= len(node_coords) - 1:
        return antinodes

    # Get the current base node
    base_node = node_coords[current_index]

    # Recurse through remaining nodes
    for i in range(current_index + 1, len(node_coords)):
        # Pair the base node with another node
        other_node = node_coords[i]
        x1, y1 = base_node
        x2, y2 = other_node

        # Compute the displacement vector
        delta_x = x2 - x1
        delta_y = y2 - y1

        # Calculate the antinode coordinates
        antinode1 = (x1 - delta_x // 3, y1 - delta_y // 3)
        # Check if the coordinates are out of bounds and the antinode does not already exist
        if (antinode1[0] >= 0 and antinode1[1] >= 0) and antinode1 not in populated_cells:
            antinodes.append(antinode1)
            populated_cells[antinode1] = 1

        # Repeat for antinode 2
        antinode2 = (x2 - delta_x // 3, y2 - delta_y // 3)
        if (antinode2[0] >= 0 or antinode2[1] >= 0) and antinode2 not in populated_cells:
            antinodes.append(antinode2)
            populated_cells[antinode2] = 1

    # Recurse with the next base node
    return calculate_antinodes_recursive(node_coords, populated_cells, current_index + 1, antinodes)

def solve():
    data = get_data()
    node_pair_dictionary, populated_cells = generate_node_coords(data)

    antinodes = []
    for key in node_pair_dictionary.keys():
        antinodes.append(calculate_antinodes_recursive(node_pair_dictionary[key], populated_cells))

    count_unique_antinodes = 0
    for set_of_antinodes in antinodes:
        count_unique_antinodes += len(set_of_antinodes)

    print(count_unique_antinodes)

if __name__ == "__main__":
    solve()