import os; import time; import re

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
        parsed_value = re.findall("(\d+)", value)
        if parsed_value:
            x_value, y_value = int(parsed_value[0]), int(parsed_value[1])
        if not value:
            array.append((buttons, prize_x, prize_y))
        elif re.search("Button A", value):
            buttons = [(x_value, y_value)]
        elif re.search("Button B", value):
            buttons.append((x_value, y_value))
        elif re.search("Prize", value):
            prize_x = x_value
            prize_y = y_value

    return array

class BinaryHeap():
    def __init__(self):
        self._heap: list = []

    def push(self, moves: int, x: int, y: int, button_counts: int):
        # Add a new element to the Heap
        entry = (moves, x, y, button_counts)
        self._heap.append(entry)
        self._sift_up(len(self._heap) - 1)
    
    def pop(self):
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
    
    def _sift_up(self, index):
        # Move an element up to maintain the heap property
        parent = (index - 1) // 2
        
        # Compare moves
        while index > 0 and self._heap[parent][0] > self._heap[index][0]:
            # Swap elements
            self._heap[parent], self._heap[index] = self._heap[index], self._heap[parent]
            
            # Move up the tree
            index = parent
            parent = (index - 1) // 2
    
    def _sift_down(self, index):
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
    
    def __len__(self):
        return len(self._heap)

def min_moves_to_prize(buttons, prize_x, prize_y):
    # Track visited states to prevent redundant exploration
    visited = set()
    heap = BinaryHeap()
    
    # Initial state
    initial_button_counts = [0] * len(buttons)
    heap.push(0, 0, 0, initial_button_counts)
    
    # Store all paths that reach the prize
    prize_paths = []
    min_moves = float('inf')
    
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
        
        # Prune paths that have overshot the prize
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

@time_execution
def solve():
    data = get_data()
    tokens = 0
    for index, (buttons, prize_x, prize_y) in enumerate(data):
        print(f'{index + 1:03} / 320')
        result = min_moves_to_prize(buttons, prize_x, prize_y)
        if result:
            num_button_a = min(result, key=lambda x: x[1][0])[1][0]
            num_button_b = min(result, key=lambda x: x[1][0])[1][1]
            tokens += num_button_a * 3 + num_button_b

    print(tokens)

if __name__ == "__main__":
    solve()