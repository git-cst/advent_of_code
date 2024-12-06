import os

class Day5():
    def __init__(self):
        self.data = None
        self.rules = None

    def generate_data_to_check(self):
        with open(f'{os.path.dirname(__file__)}/day5_input.txt', 'r') as file:
            data: str = file.read()
        
        self.data = data

    def generate_rule_set(self):
        with open(f'{os.path.dirname(__file__)}/day5_input.txt', 'r') as file:
            data: str = file.read()

        data = data.split()
        pass
            

    def __gt__(self, other):
        pass

def solve():
    solution = Day5()
    solution.generate_rule_set()

if __name__ == '__main__':
    solve()