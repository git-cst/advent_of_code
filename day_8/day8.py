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
    with open(f'{os.path.dirname(__file__)}/day8_input.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')
    return file_data

def generate_node_coords(data) -> dict:
    node_pair_dictionary = {}
    # Loop through the entire grid
    # Generate a hashmap of occupied cells used for anti-node look up to see if it can be placed
    # Generate a hashmap of nodes: Where each key contains all the node coordinates
    for i in range(0, len(data)):
        for j in range(0, len(data[0])):
            if data[i][j] != '.':
                if data[i][j] in node_pair_dictionary:
                    node_pair_dictionary[data[i][j]].append((i, j))
                else:
                    node_pair_dictionary[data[i][j]] = [(i, j)]
    
    return node_pair_dictionary

def calculate_antinodes(node_coords: dict, populated_cells: set, x_max: int, y_max: int) -> set:
    antinodes = set()

    for i in range(len(node_coords)):
        for j in range(i + 1, len(node_coords)):
            x1, y1 = node_coords[i]
            x2, y2 = node_coords[j]

            # Calculate change in x and y
            delta_x, delta_y = x2 - x1, y2 - y1

            # Two potential antinodes
            antinode1 = (x1 - delta_x, y1 - delta_y)  # on one side
            antinode2 = (x2 + delta_x, y2 + delta_y)  # on the other side

            # Add antinodes if not already populated
            if (antinode1 not in populated_cells and x_max >= antinode1[0] >= 0 and y_max >= antinode1[1] >= 0):
                antinodes.add(antinode1)
                populated_cells.add(antinode1)

            if (antinode2 not in populated_cells and x_max >= antinode2[0] >= 0 and y_max >= antinode2[1] >= 0):
                antinodes.add(antinode2)
                populated_cells.add(antinode2)

    return antinodes

@time_execution
def solve():
    data = get_data()
    node_pair_dictionary = generate_node_coords(data)

    populated_cells = set()
    x_max = len(data[0])
    y_max = len(data)
    all_antinodes = []
    for key in node_pair_dictionary.keys():
        antinodes = calculate_antinodes(node_pair_dictionary[key], populated_cells, x_max, y_max)
        all_antinodes.extend(antinodes)

    print(f"Unique antinodes: {len(all_antinodes)}")

if __name__ == "__main__":
    solve()