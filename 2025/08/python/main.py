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

class DisjointSetUnion:
    """
    This code is pulled from Claude.
    Did not know about the DisjoinSetUnion / Union-Find data structure.
    Shown here for reference purposes.
    """

    def __init__(self, elements):
        self.parent = {elem: elem for elem in elements} # Initially each element is its own parent
        self.rank = {elem: 0 for elem in elements} # Rank for union by rank optimization
        self.size = {elem: 1 for elem in elements} # Track size of each set for easier querying

    def find(self, x):
        """
        Find the root / representative of the set containing x.
        
        Uses path compression by making all nodes on the path point directly to root.
        Thus flattening the tree structure for faster future operations.
        
        Args:
            x: Element to find root of

        Returns:
            The root element of the set containing x.
        """
        if self.parent[x] != x:
            # Path compression: recursively find root and update parent
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """
        Merge the sets containing x and y
        
        Uses union by rank: attaches smaller tree under larger tree
        to keep trees shallow and operations fast.
        
        Args:
            x, y: Elements whose sets should be merged
            
        Returns:
            True if sets were merged, False if already in same set
        """

        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in same set
        
        # Union by rank: attach smaller tree under larger
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        else:
            # Equal rank: choose one as parent and increment its rank
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
            self.rank[root_x] += 1
        
        return True

    def get_set_sizes(self):
        """Get sizes of all disjoint sets.
        
        Returns:
            List of set sizes
        """
        # Group by root to find unique sets
        roots = set(self.find(elem) for elem in self.parent)
        return [self.size[root] for root in roots]
    
def distance_to_point(point_1: Point, point_2: Point) -> float:
    """Calculate Euclidean distance between two 3D points."""
    return math.dist(point_1, point_2)

@time_execution
def solve_part_1_using_DSU(data: list[str], num_connections: int = 1000) -> int:
    """Solve using Kruskal's algorithm with DSU.
    
    This is essentially building a Minimum Spanning Forest by:
    1. Sorting all edges by weight (distance)
    2. Greedily adding edges that connect different components
    
    Args:
        data: List of comma-separated x,y,z coordinates
        num_connections: Number of shortest connections to make
        
    Returns:
        Product of three largest component sizes
    """
    points = [Point(*map(int, row.split(","))) for row in data]
    dsu = DisjointSetUnion(points)
    
    # Build all edges
    edges = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = distance_to_point(points[i], points[j])
            edges.append((distance, points[i], points[j]))
    
    edges.sort()
    
    # Try to make the num_connections shortest connections
    # Some might be redundant (already in same component)
    for i in range(min(num_connections, len(edges))):
        _, point_1, point_2 = edges[i]
        dsu.union(point_1, point_2)  # Don't care if it returns True or False
    
    sizes = sorted(dsu.get_set_sizes(), reverse=True)
    return math.prod(sizes[:3])

@time_execution
def solve_part_2_using_DSU(data: list[str]) -> int:
    """Continue connecting until all points form one circuit.
    
    Returns:
        Product of X coordinates of the last two points connected
    """
    points = [Point(*map(int, row.split(","))) for row in data]
    dsu = DisjointSetUnion(points)
    
    # Build and sort all edges (same as part 1)
    edges = []
    for i, point_1 in enumerate(points):
        for point_2 in points[i + 1:]:
            distance = distance_to_point(point_1, point_2)
            edges.append((distance, point_1, point_2))
    
    edges.sort()
    
    # Keep connecting until we have one component
    num_components = len(points)  # Start with each point as its own component
    last_connection = None
    
    for distance, point_1, point_2 in edges:
        if num_components == 1:
            break
        
        # If union succeeds, we merged two components
        if dsu.union(point_1, point_2):
            num_components -= 1
            last_connection = (point_1, point_2)
    
    return last_connection[0].x * last_connection[1].x

if __name__ == '__main__':
    input_data_file = Path(__file__).parent.parent / 'data.csv'
    input_data = get_data(input_data_file).splitlines()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))

    print(solve_part_1_using_DSU(input_data, 1000))
    print(solve_part_2_using_DSU(input_data))