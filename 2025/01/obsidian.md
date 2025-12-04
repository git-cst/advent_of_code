Tags:: [[Advent of Code]], [[Math]], [[Python]], [[Modulo Arithmetic]]
Link:: https://adventofcode.com/2025/day/1
## Problem 1
The Elves have good news and bad news.

The good news is that they've discovered [project management](https://en.wikipedia.org/wiki/Project_management)! This has given them the tools they need to prevent their usual Christmas emergency. For example, they now know that the North Pole decorations need to be finished soon so that other critical tasks can start on time.

The bad news is that they've realized they have a _different_ emergency: according to their resource planning, none of them have any time left to decorate the North Pole!

To save Christmas, the Elves need _you_ to _finish decorating the North Pole by December 12th_.

Collect stars by solving puzzles. Two puzzles will be made available on each day; the second puzzle is unlocked when you complete the first. Each puzzle grants _one star_. Good luck!

You arrive at the secret entrance to the North Pole base ready to start decorating. Unfortunately, the _password_ seems to have been changed, so you can't get in. A document taped to the wall helpfully explains:

"Due to new security protocols, the password is locked in the safe below. Please see the attached document for the new combination."

The safe has a dial with only an arrow on it; around the dial are the numbers `0` through `99` in order. As you turn the dial, it makes a small _click_ noise as it reaches each number.

The attached document (your puzzle input) contains a sequence of _rotations_, one per line, which tell you how to open the safe. A rotation starts with an `L` or `R` which indicates whether the rotation should be to the _left_ (toward lower numbers) or to the _right_ (toward higher numbers). Then, the rotation has a _distance_ value which indicates how many clicks the dial should be rotated in that direction.

So, if the dial were pointing at `11`, a rotation of `R8` would cause the dial to point at `19`. After that, a rotation of `L19` would cause it to point at `0`.

Because the dial is a circle, turning the dial _left from `0`_ one click makes it point at `99`. Similarly, turning the dial _right from `99`_ one click makes it point at `0`.

So, if the dial were pointing at `5`, a rotation of `L10` would cause it to point at `95`. After that, a rotation of `R5` could cause it to point at `0`.

The dial starts by pointing at `50`.

You could follow the instructions, but your recent required official North Pole secret entrance security training seminar taught you that the safe is actually a decoy. The actual password is _the number of times the dial is left pointing at `0` after any rotation in the sequence_.

For example, suppose the attached document contained the following rotations:

```
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
```

Following these rotations would cause the dial to move as follows:

- The dial starts by pointing at `50`.
- The dial is rotated `L68` to point at `82`.
- The dial is rotated `L30` to point at `52`.
- The dial is rotated `R48` to point at `_0_`.
- The dial is rotated `L5` to point at `95`.
- The dial is rotated `R60` to point at `55`.
- The dial is rotated `L55` to point at `_0_`.
- The dial is rotated `L1` to point at `99`.
- The dial is rotated `L99` to point at `_0_`.
- The dial is rotated `R14` to point at `14`.
- The dial is rotated `L82` to point at `32`.

Because the dial points at `0` a total of three times during this process, the password in this example is `_3_`.

Analyze the rotations in your attached document. _What's the actual password to open the door?_
### Solution
```python
def solve_part_1(data: list[str]) -> int:
    def turn_left(current_state: int, running_total: int, magnitude: int) -> tuple[int, int]:
        new_state = current_state - magnitude
        new_state %= 100

        return (new_state, running_total) if new_state != 0 else (new_state, running_total + 1)

    def turn_right(current_state: int, running_total: int, magnitude: int) -> tuple[int, int]:
        new_state = current_state + magnitude
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
```
### Explanation
My first intuition here is that the problem can be simplified into viewing it as a a series of numbers from 0 to 99 (100 numbers). This means that any move should be represented as `modulo 100` e.g. if we start at `50` and move `R10` then `modulo 100` of `60` is `60` but if we move `L75` then we are at `-15` but `modulo 100` of `-15` gives `85` which is exactly what turning the dial in real life would do. Perfect.

Now we just need to check if the number is 0 and if so increment the total number of times we ended on 0 and return that.

Another solution would be to make a mock up of the dial represented as a [[Linked Lists|doubly linked list]] (e.g. creating a circular list from `0 → 99 → 0` and vice versa). Then we would increment through the linked list the number of times the instruction indicates. If the node.value is 0 then we landed on 0.
## Problem 2
You're sure that's the right password, but the door won't open. You knock, but nobody answers. You build a snowman while you think.

As you're rolling the snowballs for your snowman, you find another security document that must have fallen into the snow:

"Due to newer security protocols, please use _password method 0x434C49434B_ until further notice."

You remember from the training seminar that "method 0x434C49434B" means you're actually supposed to count the number of times _any click_ causes the dial to point at `0`, regardless of whether it happens during a rotation or at the end of one.

Following the same rotations as in the above example, the dial points at zero a few extra times during its rotations:

- The dial starts by pointing at `50`.
- The dial is rotated `L68` to point at `82`; during this rotation, it points at `0` _once_.
- The dial is rotated `L30` to point at `52`.
- The dial is rotated `R48` to point at `_0_`.
- The dial is rotated `L5` to point at `95`.
- The dial is rotated `R60` to point at `55`; during this rotation, it points at `0` _once_.
- The dial is rotated `L55` to point at `_0_`.
- The dial is rotated `L1` to point at `99`.
- The dial is rotated `L99` to point at `_0_`.
- The dial is rotated `R14` to point at `14`.
- The dial is rotated `L82` to point at `32`; during this rotation, it points at `0` _once_.

In this example, the dial points at `0` three times at the end of a rotation, plus three more times during a rotation. So, in this example, the new password would be `_6_`.

Be careful: if the dial were pointing at `50`, a single rotation like `R1000` would cause the dial to point at `0` ten times before returning back to `50`!

Using password method 0x434C49434B, _what is the password to open the door?_

### Solution
```python
def solve_part_2(data: list[str]) -> int:
    def turn_left(current_state: int, running_total: int, magnitude: int) -> tuple[int, int]:
        new_state = current_state - magnitude

        if new_state <= 0:
            change = abs(new_state) // 100 + 1 if current_state != 0 else abs(new_state) // 100
            running_total += change

        return new_state % 100, running_total

    def turn_right(current_state: int, running_total: int, magnitude: int) -> tuple[int, int]:
        new_state = current_state + magnitude
        
        if new_state > 99:
            change = new_state // 100
            running_total += change

        return new_state % 100, running_total

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
```
### Explanation
Here I see that it might have been easier to implement it as a doubly linked list since we could just check on each tick of the rotation that we are pointing at `0`. Alas, I did not do that.

But.. that's not to say that we couldn't just calculate how many times we passed 0 anyways. Well before we `modulo 100` now we want to check how many times we can [[Floor Division|integer divide]] the new state (e.g. how far we turned) by `100`. This would return the number of times. 

Moving left we always have to add 1 additional crossing because when we go negative, 
we're already past 0. For example:
- Starting at 50, moving L68 gives -18
- Integer division: abs(-18) // 100 = 0 (no complete wraps)
- But we DID cross 0 to get to -18, so +1
- Result: 0 + 1 = 1 crossing

**Exception**: If we START at 0 and move left, we haven't crossed 0 yet, 
so we don't add the extra 1.

To show this I've sketched it out in Excalidraw:
![[2025 Day 1 Secret Entrance Figure 1.png]]
456 is the amount we are moving left.
As you can see we pass `0` 4 times.

Moving right is simpler:
- Starting at 50, moving R60 gives 110
- Integer division: 110 // 100 = 1
- We crossed 0 once (at position 100)
- No special case needed
### Complexity Analysis
**Time**: `O(n)` where n is the number of instructions
**Space**: `O(1)` - only tracking current state and running total

The modulo arithmetic approach is `O(1)` per instruction, much better than 
simulating each click which would be `O(m)` where `m` is the magnitude.
## Related Concepts
- [[Modulo Arithmetic]] - core technique for circular/wrapping problems
- [[Integer Division]] - counting complete cycles
- [[State Machines]] - the dial position is state that transitions
- [[Linked Lists]] - alternative implementation approach