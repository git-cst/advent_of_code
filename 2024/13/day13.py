import os; import time; import re
from itertools import product
from sympy import Eq, solve, symbols

CONSTANT = 10_000_000_000_000

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
    with open(f'{os.path.dirname(__file__)}/day13_input.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')
    array = []
    for value in file_data:
        # Extract numbers from string
        parsed_value = re.findall(r"(\d+)", value)
        # If there is a value then assign them to variables
        if parsed_value:
            x_value, y_value = int(parsed_value[0]), int(parsed_value[1])
        # If there is no value to be parsed
        if not value:
            array.append((buttons, prize_x, prize_y))
        # If button A line then overwrite buttons variable
        elif re.search("Button A", value):
            buttons = [(x_value, y_value)]
        # If button B line then append to buttons variable
        elif re.search("Button B", value):
            buttons.append((x_value, y_value))
        # If prize line then assign prize_x, prize_y 
        elif re.search("Prize", value):
            prize_x = x_value
            prize_y = y_value
    return array

class BinaryHeap():
    def __init__(self):
        self._heap: list = []

    def push(self, moves: int, x: int, y: int, button_counts: dict[int]) -> None:
        # Add a new element to the Heap
        entry = (moves, x, y, button_counts)
        self._heap.append(entry)
        self._sift_up(len(self._heap) - 1)
    
    def pop(self) -> tuple[int, int, int, dict]:
        # Remove and return the smallest element in the heap (prioritized by moves)
        if not self._heap:
            raise IndexError("Heap is empty")
        
        # Swap first and last elements
        if len(self._heap) > 1:
            self._heap[0] = self._heap[-1]
            self._heap.pop()
            self._sift_down(0)
        else:
            return self._heap.pop()
        
        return self._heap[0]
    
    def _sift_up(self, index: int) -> None:
        # Move an element up to maintain the heap property
        parent = (index - 1) // 2
        
        # Compare moves
        while index > 0 and self._heap[parent][0] > self._heap[index][0]:
            # Swap elements
            self._heap[parent], self._heap[index] = self._heap[index], self._heap[parent]
            
            # Move up the tree
            index = parent
            parent = (index - 1) // 2
    
    def _sift_down(self, index: int) -> None:
        # Move an element down to maintain heap property
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2
            
            # Check left child
            if (left < len(self._heap) and 
                self._heap[left][0] < self._heap[smallest][0]):
                smallest = left
            
            # Check right child
            if (right < len(self._heap) and 
                self._heap[right][0] < self._heap[smallest][0]):
                smallest = right
            
            # If no change needed, we're done
            if smallest == index:
                break
            
            # Swap elements
            self._heap[index], self._heap[smallest] = self._heap[smallest], self._heap[index]
            index = smallest
    
    def __len__(self) -> int:
        return len(self._heap)

def heap_min_moves_to_prize(buttons, prize_x, prize_y) -> list[tuple[int, dict[int]]]:
    # Track visited states to prevent redundant exploration
    visited = set()
    heap = BinaryHeap()
    
    # Initial state
    initial_button_counts = [0] * len(buttons)
    min_moves = float('inf')
    heap.push(0, 0, 0, initial_button_counts)
    
    # Store all paths that reach the prize
    prize_paths = []
    
    while len(heap) > 0:
        moves, current_x, current_y, button_counts = heap.pop()
        
        # Skip if we've already found shorter paths
        if moves > min_moves:
            break
        
        # Check if we've reached the prize
        if current_x == prize_x and current_y == prize_y:
            if moves <= min_moves:
                # Update minimum moves
                min_moves = moves
                prize_paths.append((moves, button_counts))
            continue
        
        # If overshot go next
        if current_x > prize_x and current_y > prize_y:
            continue
        
        # State to prevent revisiting
        state = (current_x, current_y)
        if state in visited:
            continue
        visited.add(state)
        
        # Try each button
        for button_index, (button_x, button_y) in enumerate(buttons):
            new_x = current_x + button_x
            new_y = current_y + button_y
            
            # Create a new button counts list
            new_button_counts = button_counts.copy()
            new_button_counts[button_index] += 1
            
            # Add to heap
            heap.push(moves + 1, new_x, new_y, new_button_counts)
    
    return prize_paths

def min_moves_to_prize_part1(buttons, prize_x, prize_y):
    tokens = []
    button_a_x, button_a_y = buttons[0][0], buttons[0][1]
    button_b_x, button_b_y = buttons[1][0], buttons[1][1]
    button_presses = list(product(range(101), range(101)))
    for (push_a, push_b) in button_presses:
        state_x = button_a_x * push_a + button_b_x * push_b
        state_y = button_a_y * push_a + button_b_y * push_b

        if state_x == prize_x and state_y == prize_y:
            state_cost = 3 * push_a + push_b
            tokens.append(state_cost)
    
    return min(tokens) if tokens else 0

def min_moves_to_prize_part2(buttons, prize_x, prize_y):
    button_a_x, button_a_y = buttons[0][0], buttons[0][1]
    button_b_x, button_b_y = buttons[1][0], buttons[1][1]
    a, b = symbols('a b', integer = True)
    equation_1 = Eq(button_a_x * a + button_b_x * b, prize_x)
    equation_2 = Eq(button_a_y * a + button_b_y * b, prize_y)
    solution = solve((equation_1, equation_2), (a, b))
    return (solution[a] * 3 + solution[b]) if solution else 0
    
@time_execution
def main():
    data = get_data()
    part1_tokens = 0
    part2_tokens = 0
    # for index, (buttons, prize_x, prize_y) in enumerate(data):
    #     print(f'{index + 1:03} / 320')
    #     result = heap_min_moves_to_prize(buttons, prize_x, prize_y)
    #     if result:
    #         num_button_a = min(result, key=lambda x: x[1][0])[1][0]
    #         num_button_b = min(result, key=lambda x: x[1][0])[1][1]
    #         tokens += num_button_a * 3 + num_button_b

    for index, (buttons, prize_x, prize_y) in enumerate(data):
        print(f'Part1: {index + 1:03} / 320. Current cost: {part1_tokens}')
        part1_tokens += min_moves_to_prize_part1(buttons, prize_x, prize_y)

    print('Part1 Complete')
    print('------------------------------------------------------')

    for index, (buttons, prize_x, prize_y) in enumerate(data):
        print(f'Part2: {index + 1:03} / 320. Current cost: {part2_tokens}')
        part2_tokens += min_moves_to_prize_part2(buttons, prize_x + CONSTANT, prize_y + CONSTANT)

    print('Part2 Complete')
    print('------------------------------------------------------')
    print(f'It costs {part1_tokens} in part 1.\nIt costs {part2_tokens} in part 2.')

if __name__ == "__main__":
    main()