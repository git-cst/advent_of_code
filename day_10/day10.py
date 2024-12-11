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

                # Base case all paths are explored
                if to_visit == []:
                    unexplored = False
                    continue

                # Get new position from to_visit to check
                new_position: Cell = to_visit.pop(0)
                visited.append(new_position)
                position: Cell = new_position
                position.visited = True

                # If the value of a cell is 9 then trail summit reached and increment the full_trail variable
                current_value = int(new_position.value)
                if current_value == 9:
                    full_trail += 1

                # Loop through positions checking if there is a cell. If there is a cell at the position and it increments the value by 1 append to neighbouring positions
                for position in [position.n, position.s, position.w, position.e]:
                    if position:
                        if int(position.value) - current_value == 1:
                            neighbouring_positions.append(position)

                # Check if the position is already visited or already added to to_visit. If not append to to_visit
                for position in neighbouring_positions:
                    if position not in visited and position not in to_visit:
                        to_visit.append(position)       
            
            return full_trail

        def get_trail_rating(position: Cell) -> int:
            def depth_first_search_of_trail(position: Cell, current_path=None) -> list:
                if current_path is None:
                    current_path = []
                
                # Prevent revisiting cells
                if position in current_path:
                    return []
                
                # Add current cell to path
                current_path = current_path + [position]
                current_value = int(position.value)
                
                # If the value of a cell is 9 then trail summit reached return this path
                if current_value == 9:
                    return [current_path]
                
                # Collect paths
                goal_paths = []
                
                # Explore each direction checking if cell exists and the path is incremented by 1 if yes then we go to the next level of the search
                for next_pos in [position.n, position.s, position.w, position.e]:
                    if next_pos and int(next_pos.value) - current_value == 1:
                        # Extend the goal paths with the sub path (if summit reached then the sub path is the unique path)
                        sub_paths = depth_first_search_of_trail(next_pos, current_path)
                        goal_paths.extend(sub_paths)
                
                return goal_paths
            
            # Clean up paths (checking if there are duplicates)
            unique_goal_paths = []
            paths = depth_first_search_of_trail(position)
            for path in paths:
                if path not in unique_goal_paths:
                    unique_goal_paths.append(path)
            
            return len(unique_goal_paths)

        total_trail_score = 0
        total_trail_rating = 0
        for i in range(0, self._num_rows):
            for j in range(0, self._num_cols):
                if self._cells[i][j].value == '0':
                    total_trail_score += get_trail_score(self._cells[i][j])
                    total_trail_rating += get_trail_rating(self._cells[i][j])

        return total_trail_score, total_trail_rating

@time_execution
def solve():
    data = get_data()
    topographic_map = Graph()
    trail_information = topographic_map.calculate_trails()

    print(f"Total trail score: {trail_information[0]}\nTotal trail rating: {trail_information[1]}")


if __name__ == '__main__':
    solve()