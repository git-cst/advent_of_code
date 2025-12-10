from pathlib import Path
import sys
from dataclasses import dataclass
from enum import Enum

sys.path.append(str(Path(__file__).parent.parent.parent))

from helper_functions.import_data import get_data
from helper_functions.time_execution import time_execution

@dataclass
class Coord:
    x: int
    y: int    

@dataclass
class VerticalEdge:
    x: int = None
    y_min: int = float("inf")
    y_max: int = float("-inf")

    def create_edge(self, y1, y2):
        self.y_min = min(y1, y2)
        self.y_max = max(y1, y2)

@dataclass
class HorizontalEdge:
    y: int = None
    x_min: int = float("inf")
    x_max: int = float("-inf")   

    def create_edge(self, x1, x2):
        self.x_min = min(x1, x2)
        self.x_max = max(x1, x2)

@time_execution
def solve_part_1(input_data: list[str]) -> int:
    # Generate coordinates
    coords = [Coord(*map(int, coord.split(","))) for coord in input_data]
    
    # Brute force iterate through all possible rectangles
    max_area = float("-inf")
    for index, coord in enumerate(coords):
        for i in range(index + 1, len(coords)):
            max_area = max(max_area, abs(coord.x - coords[i].x + 1) * abs(coord.y - coords[i].y + 1))

    return max_area


@time_execution
def solve_part_2(input_data: list[str]) -> int:
    """
    Implements a scanline based algorithm with bruteforce checking of each possible square.
    
    Steps:
    1) Calculate all vertical and horizontal edges between the coordinates.
    2) Store the valid x intervals for each valid y coordinate by iterating through the horizontal edge keys
    3) Iterate through all coordinates and check if the rectangle is valid by checking if it is a) within the 
    bounds of the y interval we specified as being valid, and b) if it is within the x bounds for that y coordinate
    
    Return the maximum value of the rectangles' area
    """
    # Helper function to merge x intervals
    def merge_intervals(intervals):
        if not intervals:
            return []
        
        # Sort by start point
        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        
        merged = [sorted_intervals[0]]
        
        for current in sorted_intervals[1:]:
            last = merged[-1]
            
            # If current overlaps or touches last, merge them
            if current[0] <= last[1]:
                merged[-1] = (last[0], max(last[1], current[1]))
            else:
                merged.append(current)
        
        return merged

    # Generate coordinates
    coords = [Coord(*map(int, coord.split(","))) for coord in input_data]

    # Store all edges
    vertical_edges: dict[int, list[VerticalEdge]] = {}
    horizontal_edges: dict[int, list[HorizontalEdge]] = {}
    for i in range(len(coords)):
        current_coord = coords[i]
        next_coord = coords[(i + 1) % len(coords)] # Mod to make it so that it wraps back to the first coordinate at the end :)

        # Vertical edge (e.g. both x coords are the same so we are moving vertically)
        if current_coord.x == next_coord.x:
            v_edge = VerticalEdge(x = current_coord.x)
            v_edge.create_edge(current_coord.y, next_coord.y)

            if vertical_edges.get(current_coord.x, None) is None:
                vertical_edges[current_coord.x] = [v_edge]
            else:
                vertical_edges[current_coord.x].append(v_edge)
        
        # Horizontal edge (e.g. both y coords are the same so we are moving horizontally)
        if current_coord.y == next_coord.y:
            h_edge = HorizontalEdge(y = current_coord.y)
            h_edge.create_edge(current_coord.x, next_coord.x)

            if horizontal_edges.get(current_coord.y, None) is None:
                horizontal_edges[current_coord.y] = [h_edge]
            else:
                horizontal_edges[current_coord.y].append(h_edge)

    # Create scanline hashmap
    scanline = {y: [] for y in horizontal_edges.keys()}
    # Only search through the horizontal keys as we know that a vertical line is always proceeded by a horizontal line
    # No need to search all levels of y and implement a nearest value binary search
    for y in horizontal_edges.keys():
        # Get vertical crossing intervals
        # Meaning for each y coordinate where a horizontal edge is we check each vertical edges minimum y and maximum y
        # If the horizontal edge is within the minimum y and the maximum y then we have an x coordinate we can use (which is the x coordinate of the vertical edge crossing)
        crossing_x_coords = []
        for edges in vertical_edges.values():
            for edge in edges:
                if edge.y_min <= y < edge.y_max: # This edge crosses this y coordinate meaning we have an x coordinate that is inclusive in for this y
                # Half-open interval [y_min, y_max) prevents double-counting edges
                # that meet at horizontal boundaries
                    crossing_x_coords.append(edge.x)
        
        # Sort them into order to so we can pair them into intervals
        crossing_x_coords.sort()
        
        # Pair them into intervals (e.g. lbound x to ubound x)
        vertical_intervals = []
        for i in range(0, len(crossing_x_coords), 2):
            if i + 1 < len(crossing_x_coords):
                vertical_intervals.append((crossing_x_coords[i], crossing_x_coords[i+1]))
        
        # Get horizontal edge intervals at this y
        # Horizontal edges form the boundary of the shape and must be included in valid regions.
        # The half-open interval check (y_min <= y < y_max) for vertical edges
        # excludes vertical edges that terminate at this y, so we explicitly add
        # the horizontal edges that exist at this exact y-coordinate.
        horizontal_intervals = []
        for h_edge in horizontal_edges[y]:
            horizontal_intervals.append((h_edge.x_min, h_edge.x_max))
        
        # Combine/merge all intervals e.g. removing ranges such as 2 → 4 and having 3 → 5 in your intervals
        # Should just show 2 → 5
        all_intervals = vertical_intervals + horizontal_intervals
        merged_intervals = merge_intervals(all_intervals)
        
        scanline[y] = merged_intervals

    max_area = float("-inf")
    # Iterate over all coordinates and check if they give a valid rectangles
    for idx, coord in enumerate(coords):
        for i in range(idx + 1, len(coords)):
            x_min = min(coord.x, coords[i].x)
            x_max = max(coord.x, coords[i].x)
            y_min = min(coord.y, coords[i].y)
            y_max = max(coord.y, coords[i].y)

            valid_rectangle = True
            # We don't need to actually check every y coordinate, we actually only need to check
            # where there is a change from vertical to horizontal and vice versa. 
            # As this is where a rectangle can become invalid.
            relevant_ys = [y for y in scanline.keys() if y_min <= y <= y_max]

            # If no relevant y-coords exist, rectangle is outside polygon bounds
            if not relevant_ys:
                continue

            # Scan from top to bottom for that y coordinates range
            for y in relevant_ys:
                intervals = scanline[y]
                
                # Check if x is outside the bounds for the relevant y
                is_covered = False
                for start, end in intervals:
                    if start <= x_min and x_max <= end:
                        is_covered = True
                        break
                
                if not is_covered:
                    valid_rectangle = False
                    break

            # We have a valid rectangle calculate the size
            if valid_rectangle:
                max_area = max(max_area, (x_max - x_min + 1) * (y_max - y_min + 1))

    return max_area

if __name__ == '__main__':
    input_data_file = Path(__file__).parent.parent / 'data.csv'
    input_data = get_data(input_data_file).splitlines()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))