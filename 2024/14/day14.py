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

def get_data(grid, type=''):
    with open(f'{os.path.dirname(__file__)}/day14_{type}input.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')
    
    robots = []
    for row in file_data:
        row = row.replace("p=","").replace(" v=", ",")
        row = row.split(',')
        robots.append(Robot(int(row[0]), int(row[1]), int(row[2]), int(row[3]), grid))

    return robots

class Bathroom():
    def __init__(self):
        self.num_cols = 11#101
        self.num_rows = 7#103

class Bathroom():
    def __init__(self):
        self.num_cols = 11
        self.num_rows = 7 

        self.x_safety = self.num_cols // 2 + 1
        self.y_safety = self.num_rows // 2 + 1
    
        # Now our quadrants would be:
        self.upper_left_quadrant = [(1, self.y_safety + 1), (self.x_safety - 1, self.num_rows)]
        self.upper_right_quadrant = [(self.x_safety + 1, self.y_safety + 1), (self.num_cols, self.num_rows)]
        self.lower_left_quadrant = [(1, 1), (self.x_safety - 1, self.y_safety - 1)]
        self.lower_right_quadrant = [(self.x_safety + 1, 1), (self.num_cols, self.y_safety - 1)]

    def safety_factor(self, robots: list):
        num_upper_left, num_upper_right = 0, 0
        num_lower_left, num_lower_right = 0, 0
        for robot in robots:
            x, y = robot.position_x, robot.position_y
        
            # Calculate upper left
            if (self.upper_left_quadrant[0][0] <= x <= self.upper_left_quadrant[1][0] and
                self.upper_left_quadrant[0][1] <= y <= self.upper_left_quadrant[1][1]):
                num_upper_left += 1
                
            # Calculate upper right
            if (self.upper_right_quadrant[0][0] <= x <= self.upper_right_quadrant[1][0] and
                self.upper_right_quadrant[0][1] <= y <= self.upper_right_quadrant[1][1]):
                num_upper_right += 1
                
            # Calculate lower left
            if (self.lower_left_quadrant[0][0] <= x <= self.lower_left_quadrant[1][0] and
                self.lower_left_quadrant[0][1] <= y <= self.lower_left_quadrant[1][1]):
                num_lower_left += 1
                
            # Calculate lower right
            if (self.lower_right_quadrant[0][0] <= x <= self.lower_right_quadrant[1][0] and
                self.lower_right_quadrant[0][1] <= y <= self.lower_right_quadrant[1][1]):
                num_lower_right += 1

        return max(num_lower_left, 1) * max(num_lower_right, 1) * max(num_upper_left, 1) * max(num_upper_right, 1)

class Robot():
    def __init__(self, start_pos_x, start_pos_y, velocity_x, velocity_y, grid: Bathroom):
        self.position_x = start_pos_x
        self.position_y = start_pos_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

        self.x_upper_bound = grid.num_cols
        self.y_upper_bound = grid.num_rows
        self.x_lower_bound = 1
        self.y_lower_bound = 1

    def move(self):
        # Handle x movement
        new_x = self.position_x + self.velocity_x
        if new_x > self.x_upper_bound:
            # If we exceed the upper bound, wrap to beginning
            # e.g., if we're at position 11 and move +2, we should end up at position 2
            self.position_x = new_x - self.x_upper_bound
        elif new_x < self.x_lower_bound:
            # If we go below lower bound, wrap to end
            # e.g., if we're at position 1 and move -2, we should end up at position 10
            self.position_x = self.x_upper_bound - (self.x_lower_bound - new_x)
        else:
            self.position_x = new_x

        # Handle y movement
        new_y = self.position_y + self.velocity_y
        if new_y > self.y_upper_bound:
            self.position_y = new_y - self.y_upper_bound
        elif new_y < self.y_lower_bound:
            self.position_y = self.y_upper_bound - (self.y_lower_bound - new_y)
        else:
            self.position_y = new_y

def print_grid(robots: list, grid: Bathroom):
    # Initialize the grid with zeros to count robots
    grid_visual = [[0 for _ in range(grid.num_cols)] for _ in range(grid.num_rows)]

    # Count the robots at each position
    for robot in robots:
        x, y = robot.position_x, robot.position_y
        if 0 <= x < grid.num_cols and 0 <= y < grid.num_rows:
            grid_visual[y][x] += 1  # Increment robot count at the position

    # Print the grid
    for row in grid_visual:  # Reversed to print from top to bottom
        print(' '.join(str(cell) if cell > 0 else '.' for cell in row))

@time_execution
def main():
    grid = Bathroom()
    robots: list[Robot] = get_data(grid, 'test')
    
    print('Start grid is as follows:')
    print_grid(robots, grid)

    tick = 0
    while tick < 100:
        for robot in robots:
            robot.move()
        tick += 1
        print(f'Grid for tick {tick}:')
        print_grid(robots, grid)

    print('----------------------------------------------------------')
    print(f'The grid safety factor is {grid.safety_factor(robots)}')

if __name__ == '__main__':
    main()