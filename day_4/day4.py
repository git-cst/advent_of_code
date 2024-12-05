import os

def get_data():
    with open(f'{os.path.dirname(__file__)}/day3_input.txt', 'r') as file:
        data: str = file.read()
    
    return data

class Cell():
    def __init__(self, value = None):
        self.value = value
        
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
                self.cells.value = data[i][j]