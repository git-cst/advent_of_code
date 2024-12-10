import os; import time

def time_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"{func.__name__} took {duration:.10f} seconds to execute.")
        return result
    return wrapper

def get_data():
    with open(f'{os.path.dirname(__file__)}/day8_input.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')
    return file_data

class Node_Grid():
    def __init__(self):
        self.data = get_data()
        self.x_max = len(self.data[0]) - 1 
        self.y_max = len(self.data) - 1

    def generate_node_coords(self) -> dict:
        data = self.data
        node_pair_dictionary = {}
        # Loop through the entire grid
        # Generate a hashmap of nodes: Where each key contains all the node coordinates
        for i in range(0, len(data)):
            for j in range(0, len(data[0])):
                if data[i][j] != '.':
                    if data[i][j] in node_pair_dictionary:
                        node_pair_dictionary[data[i][j]].append((i, j))
                    else:
                        node_pair_dictionary[data[i][j]] = [(i, j)]
        
        self.node_pair_dictionary = node_pair_dictionary

    def calculate_antinodes(self, node_coords: dict) -> set:
        antinodes = set()
        x_max = self.x_max
        y_max = self.y_max

        for i in range(len(node_coords)):
            for j in range(i + 1, len(node_coords)):
                x1, y1 = node_coords[i]
                x2, y2 = node_coords[j]

                # Calculate change in x and y
                delta_x, delta_y = x2 - x1, y2 - y1

                # Two potential antinodes
                antinode1 = (x1 - delta_x, y1 - delta_y)  # on one side
                antinode2 = (x2 + delta_x, y2 + delta_y)  # on the other side

                # Add antinodes if not already populated and add that this position is now occupied
                if (x_max >= antinode1[0] >= 0 and y_max >= antinode1[1] >= 0):
                    antinodes.add(antinode1)

                if (x_max >= antinode2[0] >= 0 and y_max >= antinode2[1] >= 0):
                    antinodes.add(antinode2)

        return antinodes

    def calculate_antinodes_part2(self, node_coords: dict) -> set:
        antinodes = set()
        x_max = self.x_max
        y_max = self.y_max

        for i in range(len(node_coords)):
            for j in range(i + 1, len(node_coords)):
                x1, y1 = node_coords[i]
                x2, y2 = node_coords[j]

                # Calculate change in x and y
                delta_x, delta_y = x2 - x1, y2 - y1
                increment_x, increment_y = delta_x, delta_y

                # Loop creation of antinodes
                antinodes_in_bounds = True
                count_added_antinode1, count_added_antinode2 = 0, 0
                while antinodes_in_bounds:
                    # Two potential antinodes
                    antinode1 = (x1 - delta_x, y1 - delta_y)  # on one side
                    antinode2 = (x2 + delta_x, y2 + delta_y)  # on the other side

                    # Add antinodes if not already populated and add that this position is now occupied
                    if (x_max >= antinode1[0] >= 0 and y_max >= antinode1[1] >= 0):
                        antinodes.add(antinode1)
                        count_added_antinode1 += 1

                    if (x_max >= antinode2[0] >= 0 and y_max >= antinode2[1] >= 0):
                        antinodes.add(antinode2)
                        count_added_antinode2 += 1

                    # Check if there is more than 1 added antinode if so then add the original nodes as antinodes
                    if count_added_antinode2 >= 2 or count_added_antinode1 >= 2:
                        antinodes.add((x1, y1))
                        antinodes.add((x2, y2))

                    # Increment distance
                    delta_x += increment_x
                    delta_y += increment_y

                    # If the both nodes are outside the bounds of the grid then break while loop
                    if (not (0 <= antinode1[0] <= x_max and 0 <= antinode1[1] <= y_max) and 
                    not (0 <= antinode2[0] <= x_max and 0 <= antinode2[1] <= y_max)):
                        antinodes_in_bounds = False

        return antinodes

def print_antinode_diagram(data, antinodes):
    # Create a copy of the original grid
    diagram = [list(row) for row in data]
    
    # Mark antinodes with '#'
    for x, y in antinodes:
        # Ensure the antinode is within the grid bounds
        if 0 <= x < len(diagram) and 0 <= y < len(diagram[0]):
            diagram[x][y] = '#'
    
    # Convert back to strings and print
    for row in diagram:
        print(''.join(row))

@time_execution
def solve():
    node_grid = Node_Grid()
    node_grid.generate_node_coords()

    all_antinodes_part1 = set()
    all_antinodes_part2 = set()
    for key in node_grid.node_pair_dictionary.keys():
        antinodes_part1 = node_grid.calculate_antinodes(node_grid.node_pair_dictionary[key])
        all_antinodes_part1.update(antinodes_part1)
        antinodes_part2 = node_grid.calculate_antinodes_part2(node_grid.node_pair_dictionary[key])
        all_antinodes_part2.update(antinodes_part2)

    print(f"Unique antinodes in part 1: {len(all_antinodes_part1)}")
    print(f"Unique antinodes in part 2: {len(all_antinodes_part2)}")

if __name__ == "__main__":
    solve()