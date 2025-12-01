import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from helper_functions.import_data import get_data
from helper_functions.time_execution import time_execution

data = get_data(Path(__file__).parent / 'data.csv').splitlines()

@time_execution
def solve_part_1(data: list[str]) -> int:
    def turn_left(current_state: int, running_total: int, magnitude: int) -> tuple[int, int]:
        new_state = current_state - magnitude

        if new_state < 0:
            new_state %= 100

        return (new_state, running_total) if new_state != 0 else (new_state, running_total + 1)

    def turn_right(current_state: int, running_total: int, magnitude: int) -> tuple[int, int]:
        new_state = current_state + magnitude
        
        if new_state > 99:
            new_state %= 100

        return (new_state, running_total) if new_state != 0 else (new_state, running_total + 1)

    turn = {
        "L": turn_left,
        "R": turn_right
    }

    running_total = 0
    current_state = 50
    for instruction in data:
        direction = instruction[0]
        magnitude = int(instruction[1:])

        current_state, running_total = turn[direction](current_state, running_total, magnitude)
            
    return running_total

@time_execution
def solve_part_2(data: list[str]) -> int:
    def turn_left(current_state: int, running_total: int, magnitude: int) -> tuple[int, int]:
        new_state = current_state - magnitude

        if new_state <= 0:
            change = abs(new_state) // 100 + 1 if current_state != 0 else abs(new_state) // 100
            running_total += change
            new_state %= 100

        return new_state, running_total

    def turn_right(current_state: int, running_total: int, magnitude: int) -> tuple[int, int]:
        new_state = current_state + magnitude
        
        if new_state > 99:
            change = new_state // 100
            running_total += change
            new_state %= 100

        return new_state, running_total

    turn = {
        "L": turn_left,
        "R": turn_right
    }

    running_total = 0
    current_state = 50
    for instruction in data:
        direction = instruction[0]
        magnitude = int(instruction[1:])

        current_state, running_total = turn[direction](current_state, running_total, magnitude)
            
    return running_total    

if __name__ == '__main__':
    print(solve_part_1(data))
    print(solve_part_2(data))