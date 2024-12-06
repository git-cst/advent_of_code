import os

def get_data():
    with open(f'{os.path.dirname(__file__)}/day4_input.txt', 'r') as file:
        data: str = file.read()
    
    data = data.split()

    return data

class Cell():
    def __init__(self, value = None):
        self.value: str = value
        
        self.n = None
        self.s = None
        self.w = None
        self.e = None
        
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None

class Graph():
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols

    def generate_graph(self, data):
        self.cells: Cell = [[Cell() for _ in range(self.num_rows)] for _ in range(self.num_cols)]

        for i in range(0, self.num_cols):
            for j in range(0, self.num_rows):
                self.cells[i][j].value = data[i][j]

                # GENERATE THE ADJACENCIES
                # LOGIC FOR CHECKING NE

                # LOGIC FOR CHECKING N

                # LOGIC FOR CHECKING NW

                # LOGIC FOR CHECKING W

                # LOGIC FOR CHECKING E

                # LOGIC FOR CHECKING SW

                # LOGIC FOR CHECKING S

                # LOGIC FOR CHECKING SE

def check_adjacencies(graph: Graph):
    count_of_xmas = 0

    for i in range(0, graph.num_cols):
        for j in range(0, graph.num_rows):
            pass

    return count_of_xmas

def solve():
    data = get_data()
    graph = Graph(len(data), len(data[0]))
    graph.generate_graph(data)
    print(check_adjacencies(graph))

if __name__ == "__main__":
    solve()