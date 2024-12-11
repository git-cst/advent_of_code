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
    with open(f'{os.path.dirname(__file__)}/day10_input.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')

    return file_data

class Cell():
    def __init__(self, value = None):
        self.value: str = value
        self.visited = False

        self.n: Cell = None
        self.s: Cell = None
        self.w: Cell = None
        self.e: Cell = None

class Graph():
    def __init__(self):
        self._data = get_data()
        self._num_rows = len(self._data)
        self._num_cols = len(self._data[0])
        self._generate_graph(self._data)

    def _generate_graph(self, data) -> None:
        self._cells  = [[Cell() for _ in range(self._num_cols)] for _ in range(self._num_rows)]

        for i in range(0, self._num_cols):
            for j in range(0, self._num_cols):
                cell: Cell = self._cells [i][j]
                cell.value = data[i][j]

                if cell.value == "^":
                    self._start_position = (i, j)

                # LOGIC FOR CHECKING N
                if i - 1 >= 0:
                    cell.n = self._cells [i - 1][j]

                # LOGIC FOR CHECKING E
                if j + 1 < self._num_cols:
                    cell.e = self._cells [i][j + 1]

                # LOGIC FOR CHECKING S
                if i + 1 < self._num_cols:
                    cell.s = self._cells [i + 1][j]

                # LOGIC FOR CHECKING W
                if j - 1 >= 0:
                    cell.w = self._cells [i][j - 1]

    def calculate_trails(self) -> int:
        def get_trail_score(start_position: Cell) -> int:
            visited = []
            to_visit = []
            to_visit.append(start_position)
            full_trail = 0

            unexplored = True
            while unexplored:
                neighbouring_positions = []

                if to_visit == []:
                    unexplored = False
                    continue

                new_position: Cell                  = to_visit.pop(0)
                visited.append(new_position)
                current_position: Cell              = new_position
                current_position.visited = True

                current_value                       = int(new_position.value)
                if current_value == 1:
                    pass

                if current_value == 9:
                    full_trail += 1

                if current_position.n:
                    if int(current_position.n.value) - current_value == 1: # NORTH
                        neighbouring_positions.append(current_position.n)

                if current_position.s:
                    if int(current_position.s.value) - current_value == 1: # SOUTH
                        neighbouring_positions.append(current_position.s)

                if current_position.w:
                    if int(current_position.w.value) - current_value == 1: # WEST
                        neighbouring_positions.append(current_position.w)

                if current_position.e:
                    if int(current_position.e.value) - current_value == 1: # EAST
                        neighbouring_positions.append(current_position.e)

                for position in neighbouring_positions:
                    if position not in visited and position not in to_visit:
                        to_visit.append(position)       
            
            return full_trail

        def get_trail_rating(start_position: Cell) -> int:
            pass


        total_trail_score = 0
        total_trail_rating = 0
        for i in range(0, self._num_rows):
            for j in range(0, self._num_cols):
                if self._cells[i][j].value == '0':
                    total_trail_score += get_trail_score(self._cells[i][j])
                    total_trail_rating += get_trail_rating(self._cells[i][j])

        return total_trail_score

@time_execution
def solve():
    data = get_data()
    topographic_map = Graph()
    print(topographic_map.calculate_trails())


if __name__ == '__main__':
    solve()