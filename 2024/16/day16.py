import os; import time; import re
from math import ceil

from dataclasses import dataclass
import heapq

def time_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"{func.__name__} took {duration:.4f} seconds to execute.")
        return result
    return wrapper

def get_data(type=''):
    file_path = os.path.join(os.path.dirname(__file__), f'day16_{type}input.txt')
    with open(file_path, 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')
    
    return file_data

@dataclass
class State:
    position: 'Cell'
    direction: str
    g_cost: int  # Actual cost (path length + turn penalties)
    f_cost: int  # g_cost + heuristic
    path: list['Cell']
    turn_count: int

    def __lt__(self, other):
        return self.f_cost < other.f_cost

class Cell():
    def __init__(self):
        self.value = ""

        self.n = None
        self.e = None
        self.s = None
        self.w = None

        self.blocking = False

    def set_value(self, value):
        self.value = value

    def set_position(self, position: tuple[int, int]):
        self.x_pos, self.y_pos = position

    def __hash__(self):
        return hash((self.x_pos, self.y_pos))

    def __eq__(self, other):
        return (self.x_pos, self.y_pos) == (other.x_pos, other.y_pos)

    def set_blocking(self):
        self.blocking = True

    def get_value(self):
        return self.value

    def is_blocking(self):
        return self.blocking

class Grid():
    def __init__(self, num_cols: int, num_rows: int, data: list[list[str]]):
        self.start_point = None
        self.end_point = None

        self.generate_grid(num_cols, num_rows, data)

    def generate_grid(self, num_cols: int, num_rows: int, data: list[list[str]]):
        self.cells = [[Cell() for _ in range(num_cols)] for _ in range(num_rows)]

        for i in range(0, num_cols):
            for j in range(0, num_rows):
                cell: Cell = self.cells[i][j]
                cell.set_value(data[i][j])
                cell.set_position((i, j))

                cell_value = cell.get_value()

                if cell_value == "S":
                    self.start_point = cell
                elif cell_value == "E":
                    self.end_point = cell
                elif cell_value == "#":
                    cell.set_blocking()

                # Logic for checking N
                if i - 1 >= 0:
                    cell.n = self.cells[i - 1][j]

                # Logic for checking E
                if j + 1 < num_cols:
                    cell.e = self.cells[i][j + 1]

                # Logic for checking S
                if i + 1 < num_rows:
                    cell.s = self.cells[i + 1][j]

                # Logic for checking W
                if j - 1 >= 0:
                    cell.w = self.cells[i][j - 1]

    def manhatten_distance_heuristic(self, current_pos: Cell, goal_pos: Cell):
        return abs(current_pos.x_pos - goal_pos.x_pos) + abs(current_pos.y_pos - goal_pos.y_pos)

    def evaluate_paths_dfs(self):
        stack = []
        valid_paths = []

        start_position = self.start_point
        moves = 0
        path_information = ([start_position], moves)
        curr_direction = "e"
        stack.append([start_position, path_information, curr_direction])

        directions = {}

        directions["n"] = [("n", 0), ("e", 1), ("w", 1)]
        directions["e"] = [("e", 0), ("s", 1), ("n", 1)]
        directions["s"] = [("s", 0), ("w", 1), ("e", 1)]
        directions["w"] = [("w", 0), ("s", 1), ("n", 1)]

        while stack:
            current_position, (path, current_cost), curr_direction = stack.pop()

            if current_position == self.end_point:
                valid_paths.append((path, current_cost))
                continue

            for direction, turn_cost in directions[curr_direction]:
                neighbour: Cell = getattr(current_position, direction, None)
                if neighbour and not neighbour.is_blocking() and neighbour not in path:
                    new_path = path.copy()
                    new_path.append(neighbour)
                    stack.append([neighbour, (new_path, current_cost+turn_cost+1), direction])

        return valid_paths

    def best_path_score(self, valid_paths: list[tuple[list[Cell], int]]) -> int:
        current_best_score = float("inf")
        for path, number_of_turns in valid_paths:
            score = len(path)-1 + (number_of_turns * 1000)
            current_best_score = score if score < current_best_score else current_best_score

        return current_best_score

    def evaluate_paths_astar(self):
        open_set = []
        best_costs = {}

        initial_state = State(
            position=self.start_point,
            direction="e",
            g_cost=0,
            f_cost=self.manhatten_distance_heuristic(self.start_point, self.end_point),
            path=[self.start_point],
            turn_count=0
        )

        heapq.heappush(open_set, initial_state)
        directions = {
            "n": [("n", 0), ("e", 1), ("w", 1)],
            "e": [("e", 0), ("s", 1), ("n", 1)],
            "s": [("s", 0), ("w", 1), ("e", 1)],
            "w": [("w", 0), ("s", 1), ("n", 1)]
        }

        while open_set:
            current_state: State = heapq.heappop(open_set)

            if current_state.position == self.end_point: # uses __eq__ dunder in Cell
                return current_state.path, current_state.turn_count

            state_key = (current_state.position, current_state.direction)
            if state_key in best_costs and best_costs[state_key] <= current_state.g_cost:
                continue
            best_costs[state_key] = current_state.g_cost

            possible_moves = directions[current_state.direction]
            for direction, turn_cost in possible_moves:
                neighbour: Cell = getattr(current_state.position, direction, None)
                
                if (neighbour and 
                    not neighbour.is_blocking() and 
                    neighbour not in current_state.path):

                    new_g_cost = current_state.g_cost + 1 + (turn_cost * 1000)  # 1 for move, turn penalty
                    new_f_cost = new_g_cost + self.manhatten_distance_heuristic(neighbour, self.end_point)
                    new_turn_count = current_state.turn_count + turn_cost
                    
                    new_state = State(
                        position=neighbour,
                        direction=direction,
                        g_cost=new_g_cost,
                        f_cost=new_f_cost,
                        path=current_state.path + [neighbour],
                        turn_count=new_turn_count
                    )
                    
                    heapq.heappush(open_set, new_state) # reorders heap
        
        return None, None  # No path found

def main():
    data = get_data()
    num_cols = len(data[0])
    num_rows = len(data)

    grid = Grid(num_cols, num_rows, data)
    best_path, turn_count = grid.evaluate_paths_astar()
    print(len(best_path)-1 + turn_count * 1000)

if __name__ == '__main__':
    main()