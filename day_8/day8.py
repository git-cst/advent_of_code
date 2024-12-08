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
    with open(f'{os.path.dirname(__file__)}/day7_input.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')
    return data

def generate_node_pairs(data):
    node_pair_dictionary = {}
    hashmap_of_populated_cells = {}
    # create a set of all nodes e.g. there is a 3 node, a a node, a X node, etc.
    # create all the pairings of these nodes as a dictionary containing tuples which are coordinate sets?
    
    return node_pair_dictionary, hashmap_of_populated_cells

def generate_anti_nodes(node_pair_dictionary: dict, hashmap_of_populated_cells: dict):
    unique_anti_nodes = 0
    
    for key in node_pair_dictionary.keys():
        for coordinate_set in node_pair_dictionary[key]:
            pass
            # generate anti nodes
                # anti node positions can be described as the distance between each node and just - the first node and + on the second node.
                # check if the created coordinates would result in a negative value (as such it would be invalid and go to next anti node creation)
            # check if anti node would already be in already populated cells
                # if yes then don't increment unique anti nodes
                # if no then increment unique anti nodes and add the coordinates to the hashmap of populated cells

    # DO STUFF

    return unique_anti_nodes

def solve():
    pass

if __name__ == "__main__":
    solve()