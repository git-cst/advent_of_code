Tags:: [[Advent of Code]], [[Python]], [[Object-Oriented Programming]], [[Graph Theory]]
Link:: https://adventofcode.com/2025/day/4
## Problem 1
You ride the escalator down to the printing department. They're clearly getting ready for Christmas; they have lots of large rolls of paper everywhere, and there's even a massive printer in the corner (to handle the really big print jobs).

Decorating here will be easy: they can make their own decorations. What you really need is a way to get further into the North Pole base while the elevators are offline.

"Actually, maybe we can help with that," one of the Elves replies when you ask for help. "We're pretty sure there's a cafeteria on the other side of the back wall. If we could break through the wall, you'd be able to keep moving. It's too bad all of our forklifts are so busy moving those big rolls of paper around."

If you can optimize the work the forklifts are doing, maybe they would have time to spare to break through the wall.

The rolls of paper (`@`) are arranged on a large grid; the Elves even have a helpful diagram (your puzzle input) indicating where everything is located.

For example:

```
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
```

The forklifts can only access a roll of paper if there are _fewer than four rolls of paper_ in the eight adjacent positions. If you can figure out which rolls of paper the forklifts can access, they'll spend less time looking and more time breaking down the wall to the cafeteria.

In this example, there are `_13_` rolls of paper that can be accessed by a forklift (marked with `x`):

```
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.
```

Consider your complete diagram of the paper roll locations. _How many rolls of paper can be accessed by a forklift?_
### Solution
#### OOP Setup
```python
class PaperRoll:
    def __init__(self):
        # Value
        self.value: Optional[str] = None

        # Adjacencies
        self.n: Optional[PaperRoll] = None
        self.ne: Optional[PaperRoll] = None
        self.e: Optional[PaperRoll] = None
        self.se: Optional[PaperRoll] = None
        self.s: Optional[PaperRoll] = None
        self.sw: Optional[PaperRoll] = None
        self.w: Optional[PaperRoll] = None
        self.nw: Optional[PaperRoll] = None

    def __iter__(self):
        yield from [self.n, self.ne, self.e, self.se, self.s, self.sw, self.w, self.nw]

    def count_adjacencies(self):
        if self.value == ".":
            return 0

        count = 0
        for adjacency in self:
            if adjacency and adjacency.value in ["@", "x"]:
                count += 1

        return count
    
    def should_remove(self):
        return self.value != "." and self.count_adjacencies() < 4

class Warehouse:
    def __init__(self):
        self._num_cols: int = None
        self._num_rows: int = None
        self.warehouse_layout: list[list[PaperRoll]] = None

        self._active_cells: dict[tuple[int, int], PaperRoll] = {}
        self._valid_paper_rolls: dict[tuple[int, int], PaperRoll] = {}

    def generate_grid(self, warehouse_layout: list[str]):
        self._num_cols = len(warehouse_layout[0])
        self._num_rows = len(warehouse_layout)

        if not self.warehouse_layout:
            self.warehouse_layout: list[list[PaperRoll]] = [[PaperRoll() for _ in range(self._num_cols)] for _ in range(self._num_rows)]

        for row in range(self._num_rows):
            for col in range(self._num_cols):
                paper_roll = self.warehouse_layout[row][col]
                paper_roll.value = warehouse_layout[row][col]

                if paper_roll.value != ".":
                    self._active_cells[(row, col)] = paper_roll

                # north west adjacency
                if row - 1 >= 0 and col - 1 >= 0:
                    paper_roll.nw = self.warehouse_layout[row - 1][col - 1]

                # north adjacency
                if row - 1 >= 0:
                    paper_roll.n = self.warehouse_layout[row - 1][col]

                # north east adjacency
                if row - 1 >= 0 and col + 1 < self._num_cols:
                    paper_roll.ne = self.warehouse_layout[row - 1][col + 1]

                # east adjacency
                if col + 1 < self._num_cols:
                    paper_roll.e = self.warehouse_layout[row][col + 1]

                # south east adjacency
                if row + 1 < self._num_rows and col + 1 < self._num_cols:
                    paper_roll.se = self.warehouse_layout[row + 1][col + 1]

                # south adjacency
                if row + 1 < self._num_rows:
                    paper_roll.s = self.warehouse_layout[row + 1][col]

                # south west adjacency
                if row + 1 < self._num_rows and col - 1 >= 0:
                    paper_roll.sw = self.warehouse_layout[row + 1][col - 1]

                # west adjacency
                if col - 1 >= 0:
                    paper_roll.w = self.warehouse_layout[row][col - 1]

    def count_valid_adjacencies(self):
        if self.warehouse_layout is None:
            raise RuntimeError("Calling count before a warehouse layout is created")
        
        self._valid_paper_rolls.clear()

        for (row, col), paper_roll in self._active_cells.items():
            paper_roll_adjacencies = paper_roll.count_adjacencies()
            if paper_roll_adjacencies < 4:
                self._valid_paper_rolls[(row, col)] = paper_roll

    def remove_valid_paper_rolls(self):
        if not hasattr(self, '_removed_rolls'):
            self._removed_rolls = 0

        for (row, col), paper_roll in self._valid_paper_rolls.items():
            paper_roll.value = "."
            self._removed_rolls += 1
            self._active_cells.pop((row, col))

    def print_warehouse_layout(self):
        """Debug method"""       
        def mark_removable_rolls():
            for _, paper_roll in self._active_cells.items():
                if paper_roll.should_remove():
                    paper_roll.value = 'x'

        if self.warehouse_layout is None:
            raise RuntimeError("Calling debug before a warehouse layout is created")
        
        mark_removable_rolls()

        for row in range(self._num_rows):
            print_value = []
            for col in range(self._num_cols):
                paper_roll_value = self.warehouse_layout[row][col].value
                print_value.append(COLORS[paper_roll_value] + paper_roll_value + COLORS['reset'])

            print("".join(print_value))

    @property
    def num_valid_paper_rolls(self):
        return len(self._valid_paper_rolls.keys())
    
    @property
    def num_removed_paper_rolls(self):
        return self._removed_rolls
```
#### Solving code
```python
def solve_part_1(warehouse_layout: list[str]) -> int:
    warehouse = Warehouse()
    warehouse.generate_grid(warehouse_layout)
    warehouse.count_valid_adjacencies()
    return warehouse.num_valid_paper_rolls
```
### Explanation
Alright. My first intuition with this problem was is that we can model the problem into a graph and node problem. You could do this as a set of 2d arrays and then handle the adjacencies on the fly. 

Buuuut. OOP seems soi clean here.
So firstly we can create an object that tracks it's adjacencies and can handle resolving the criteria for the object.

Then we can create an object that simulates the actual warehouse.
At this point it's literally just a case of iterating through it and counting how many.

Simple.
## Problem 2
Now, the Elves just need help accessing as much of the paper as they can.

Once a roll of paper can be accessed by a forklift, it can be _removed_. Once a roll of paper is removed, the forklifts might be able to access _more_ rolls of paper, which they might also be able to remove. How many total rolls of paper could the Elves remove if they keep repeating this process?

Starting with the same example as above, here is one way you could remove as many rolls of paper as possible, using highlighted `_@_` to indicate that a roll of paper is about to be removed, and using `x` to indicate that a roll of paper was just removed:

```
Initial state:
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.

Remove 13 rolls of paper:
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.

Remove 12 rolls of paper:
.......x..
.@@.x.x.@x
x@@@@...@@
x.@@@@..x.
.@.@@@@.x.
.x@@@@@@.x
.x.@.@.@@@
..@@@.@@@@
.x@@@@@@@.
....@@@...

Remove 7 rolls of paper:
..........
.x@.....x.
.@@@@...xx
..@@@@....
.x.@@@@...
..@@@@@@..
...@.@.@@x
..@@@.@@@@
..x@@@@@@.
....@@@...

Remove 5 rolls of paper:
..........
..x.......
.x@@@.....
..@@@@....
...@@@@...
..x@@@@@..
...@.@.@@.
..x@@.@@@x
...@@@@@@.
....@@@...

Remove 2 rolls of paper:
..........
..........
..x@@.....
..@@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@x.
....@@@...

Remove 1 roll of paper:
..........
..........
...@@.....
..x@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
...x@.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
....x.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
..........
...x@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...
```

Stop once no more rolls of paper are accessible by a forklift. In this example, a total of `_43_` rolls of paper can be removed.

Start with your original diagram. _How many rolls of paper in total can be removed by the Elves and their forklifts?_
### Solution
```python
def solve_part_2(warehouse_layout: list[str]) -> int:
    warehouse = Warehouse()
    warehouse.generate_grid(warehouse_layout)
    warehouse.count_valid_adjacencies()

    while warehouse.num_valid_paper_rolls > 0:
        warehouse.remove_valid_paper_rolls()
        warehouse.count_valid_adjacencies()

    return warehouse.num_removed_paper_rolls
```
### Explanation
Now it's even easier since I modelled it using OOP so I can literally just make a method to remove the _paper rolls_ and then loop it.

Added a cheeky little optimization with tracking which cells are actually active (e.g. have a paper roll) reducing the search space once again (instead of iterating through it all again and again).
### Complexity Analysis
**Part 1:** 
- Grid generation: O(n × m) where n and m are grid dimensions
- Finding accessible rolls: O(k) where k is the number of active cells (paper rolls)
- Space: O(n × m) for the grid

**Part 2:**
- Worst case: O(k × i) where k is active cells and i is the number of iterations
- Best case: O(k) if no cascade occurs (all rolls removed in one pass)
- In practice: The active cells shrink with each iteration, making subsequent passes faster
- The number of iterations is bounded by the grid size but typically much smaller (example: 43 removals in 9 iterations)

**Space Complexity:** O(n × m) for both parts due to the grid structure
## Related Concepts
- [[Graph Theory]] - Modeling the grid as a graph with 8-directional adjacency
- [[Object-Oriented Programming]] - Encapsulation of node logic and grid management
- [[Moore Neighborhood]] - Eight-directional adjacency pattern
- [[Cascading Effects]] - Iterative state changes triggering further changes
- [[State Tracking Optimization]] - Using `_active_cells` to reduce search space
- [[Simulation]] - Modeling a dynamic system that evolves over discrete steps