import os; import time; import re
from math import ceil

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
    with open(f'{os.path.dirname(__file__)}/day14_{type}input.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')
    
    return file_data

class Robot:
    def __init__(self, position: tuple[int, int], vector: tuple[int, int], ubound_x: int, ubound_y: int):
        self._start_x, self._start_y = position

        self.x_pos, self.y_pos = position
        self.x_movement, self.y_movement = vector
        
        self.ubound_x = ubound_x
        self.ubound_y = ubound_y

        self.quadrant = "" 

    def move(self, num_movements: int):
        delta_x = abs(self.x_movement * num_movements)
        delta_y = abs(self.y_movement * num_movements)

        self.x_pos = self.x_pos + delta_x if self.x_movement > 0 else self.x_pos - delta_x
        self.y_pos = self.y_pos + delta_y if self.y_movement > 0 else self.y_pos - delta_y

        self.x_pos %= self.ubound_x
        self.y_pos %= self.ubound_y

        self.quadrant = self.check_quadrant()
        
    def reset(self):
        self.x_pos = self._start_x
        self.y_pos = self._start_y

    def check_quadrant(self) -> str:
        mid_x = self.ubound_x // 2
        mid_y = self.ubound_y // 2

        if self.x_pos == mid_x or self.y_pos == mid_y:
            return "NA"

        if self.x_pos < mid_x and self.y_pos > mid_y:
            return "upper_left"
        elif self.x_pos > mid_x and self.y_pos > mid_y:
            return "upper_right"
        elif self.x_pos < mid_x and self.y_pos < mid_y:
            return "lower_left"
        elif self.x_pos > mid_x and self.y_pos < mid_y:
            return "lower_right"
        
        return "NA"

    def __repr__(self):
        return f'Position: x:{self.x_pos}, y:{self.y_pos}\nQuadrant:{self.quadrant}'

def count_connected_robots(robot_list: list[Robot]) -> int:
    positions = {(robot.x_pos, robot.y_pos) for robot in robot_list}
    connected_count = 0
    
    for robot in robot_list:
        x, y = robot.x_pos, robot.y_pos
        neighbours = [
            (x-1, y-1), (x, y-1), (x+1, y-1),
            (x-1, y), (x+1, y),
            (x-1, y+1), (x, y+1), (x+1, y+1)
        ]
        
        for neighbour in neighbours:
            if neighbour in positions:
                connected_count += 1
                break
    
    return connected_count

def candidate_grid(robot_list: list[Robot]) -> bool:
    positions = {(robot.x_pos, robot.y_pos) for robot in robot_list}

    for robot in robot_list:
        x, y = robot.x_pos, robot.y_pos
            
        neighbours = {
            'north' : (x, y+1), 
            'east'  : (x+1, y),
            'south' : (x, y-1),
            'west'  : (x-1, y)
        }
        
        for direction, coordinate in neighbours.items():
            if coordinate in positions:
                if check_robot(positions, coordinate, direction):
                    return True

        return False    

def check_robot(positions: set[tuple[int, int]], neighbour_position: tuple[int, int], direction: str) -> bool:
    direction_modifier = {
        'north' : (0, 1), 
        'east'  : (1, 0),
        'south' : (0, -1),
        'west'  : (-1, 0)
    }

    curr_x, curr_y = neighbour_position
    delta_x, delta_y = direction_modifier[direction]

    robots_in_a_row = 1
    for _ in range(0, 10):
        position_to_check = (curr_x + delta_x, curr_y + delta_y)
        if position_to_check in positions:
            curr_x, curr_y = position_to_check
            robots_in_a_row += 1
            continue
        else:
            break
    return robots_in_a_row >= 8

def print_grid(robot_list: list[Robot], ubound_x: int, ubound_y: int):
    grid = [['.' for _ in range(ubound_x)] for _ in range(ubound_y)]
    
    for robot in robot_list:
        grid[robot.y_pos][robot.x_pos] = '#'
    
    # Print from top to bottom (reverse y-axis for display)
    for row in reversed(grid):
        print(''.join(row))

@time_execution
def main():
    input_data = get_data()

    upper_bound_x = 101
    upper_bound_y = 103

    robot_positions = [(int(x), int(y)) for x, y in [position.split(" ")[0].replace("p=", "").split(",") for position in input_data]]
    robot_vectors = [(int(x), int(y)) for x, y in [position.split(" ")[1].replace("v=", "").split(",") for position in input_data]]
    robot_list = [Robot(position, vector, upper_bound_x, upper_bound_y) for position, vector in zip(robot_positions, robot_vectors)]

    for robot in robot_list:
        robot.move(100)
    
    print(" ========= Part 1 =========\n")
    print(f""" Safety factor: {sum([1 for robot in robot_list if robot.quadrant == "upper_left"])*
          sum([1 for robot in robot_list if robot.quadrant == "upper_right"])*
          sum([1 for robot in robot_list if robot.quadrant == "lower_left"])*
          sum([1 for robot in robot_list if robot.quadrant == "lower_right"])}\n""")
    print(" ========= Part 2 =========\n")

    for robot in robot_list:
        robot.reset()

    tick = 1
    while tick <= 9000:
        for robot in robot_list:
            robot.move(1)

        if candidate_grid(robot_list):
            print(f" Potential candidate at tick {tick}")
            print_grid(robot_list, upper_bound_x, upper_bound_y)

        tick += 1

    print_grid(robot_list, upper_bound_x, upper_bound_y)

    print("\n =========================")

if __name__ == '__main__':
    main()