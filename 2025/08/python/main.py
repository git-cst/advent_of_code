from pathlib import Path
import sys
import math
from dataclasses import dataclass

sys.path.append(str(Path(__file__).parent.parent.parent))

from helper_functions.import_data import get_data
from helper_functions.time_execution import time_execution

# Euclidean distance calculated as math.sqrt((x_point_1 - x_point_2) ** 2 + (y_point_1 - y_point_2) ** 2 + (y_point_1 - y_point_2) ** 2)
# But math apparently has an even better formula (math.dist)

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __iter__(self):
        yield from (self.x, self.y, self.z)

def distance_to_point(point_1: Point, point_2: Point) -> int:
    return math.dist(point_1, point_2)

@time_execution
def solve_part_1(data: list[str]) -> int:
    points = [Point(*map(int, row.split(","))) for row in data]
    circuits: list[set[Point]] = [{point} for point in points]

    distance_list = []
    num_points = len(points)
    for index, point in enumerate(points):
        for i in range(index + 1, num_points):
            distance_list.append((point, points[i], distance_to_point(point, points[i])))

    distance_list = sorted(distance_list, key=lambda x: x[2]) 
    
    for i in range(min(1000, len(distance_list))):
        point_1, point_2, _ = distance_list[i]
        
        circuit_1 = next((circuit for circuit in circuits if point_1 in circuit), None)
        circuit_2 = next((circuit for circuit in circuits if point_2 in circuit), None)

        if circuit_1 is not circuit_2:
            merged = circuit_1 | circuit_2
            circuits.remove(circuit_1)
            circuits.remove(circuit_2)
            circuits.append(merged)

    circuits.sort(key=len, reverse=True)
    top_3_sizes = [len(circuits[i]) for i in range(3)]
    return math.prod(top_3_sizes)

@time_execution
def solve_part_2(data: list[str]) -> int:
    points = [Point(*map(int, row.split(","))) for row in data]
    circuits: list[set[Point]] = [{point} for point in points]

    distance_list: list[tuple[Point, Point, float]] = []
    num_points = len(points)
    for index, point in enumerate(points):
        for i in range(index + 1, num_points):
            distance_list.append((point, points[i], distance_to_point(point, points[i])))

    distance_list = sorted(distance_list, key=lambda x: x[2]) 
    
    i = 0
    while len(circuits) != 1:
        point_1, point_2, _ = distance_list[i]
        
        circuit_1 = next((circuit for circuit in circuits if point_1 in circuit), None)
        circuit_2 = next((circuit for circuit in circuits if point_2 in circuit), None)

        if circuit_1 is not circuit_2:
            merged = circuit_1 | circuit_2
            circuits.remove(circuit_1)
            circuits.remove(circuit_2)
            circuits.append(merged)

        i += 1

    return point_1.x * point_2.x

if __name__ == '__main__':
    input_data_file = Path(__file__).parent.parent / 'data.csv'
    input_data = get_data(input_data_file).splitlines()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))