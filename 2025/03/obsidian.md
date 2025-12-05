Tags:: [[Advent of Code]], [[Python]]
Link:: https://adventofcode.com/2025/day/3
## Problem 1
You descend a short staircase, enter the surprisingly vast lobby, and are quickly cleared by the security checkpoint. When you get to the main elevators, however, you discover that each one has a red light above it: they're all _offline_.

"Sorry about that," an Elf apologizes as she tinkers with a nearby control panel. "Some kind of electrical surge seems to have fried them. I'll try to get them online soon."

You explain your need to get further underground. "Well, you could at least take the escalator down to the printing department, not that you'd get much further than that without the elevators working. That is, you could if the escalator weren't also offline."

"But, don't worry! It's not fried; it just needs power. Maybe you can get it running while I keep working on the elevators."

There are batteries nearby that can supply emergency power to the escalator for just such an occasion. The batteries are each labeled with their [joltage](https://adventofcode.com/2020/day/10) rating, a value from `1` to `9`. You make a note of their joltage ratings (your puzzle input). For example:

```
987654321111111
811111111111119
234234234234278
818181911112111
```

The batteries are arranged into _banks_; each line of digits in your input corresponds to a single bank of batteries. Within each bank, you need to turn on _exactly two_ batteries; the joltage that the bank produces is equal to the number formed by the digits on the batteries you've turned on. For example, if you have a bank like `12345` and you turn on batteries `2` and `4`, the bank would produce `24` jolts. (You cannot rearrange batteries.)

You'll need to find the largest possible joltage each bank can produce. In the above example:

- In `_98_7654321111111`, you can make the largest joltage possible, _`98`_, by turning on the first two batteries.
- In `_8_1111111111111_9_`, you can make the largest joltage possible by turning on the batteries labeled `8` and `9`, producing _`89`_ jolts.
- In `2342342342342_78_`, you can make _`78`_ by turning on the last two batteries (marked `7` and `8`).
- In `818181_9_1111_2_111`, the largest joltage you can produce is _`92`_.

The total output joltage is the sum of the maximum joltage from each bank, so in this example, the total output joltage is `98` + `89` + `78` + `92` = `_357_`.

There are many batteries in front of you. Find the maximum joltage possible from each bank; _what is the total output joltage?_
### Solution
```python
def solve_part_1(battery_banks: list[str]) -> int:
    total_joltage = 0

    for battery_bank in battery_banks:
        battery_bank_len = len(battery_bank)

        left_jolt = 0
        right_jolt = 0
        for i in range(0, battery_bank_len - 1):
            if int(battery_bank[i]) > left_jolt:
                left_jolt = int(battery_bank[i])
                l_bound_r_val = i

            if left_jolt == 9:
                break

        for i in range(battery_bank_len - 1, l_bound_r_val, -1):
            if int(battery_bank[i]) > right_jolt:
                right_jolt = int(battery_bank[i])

            if right_jolt == 9:
                break

        total_joltage += int(str(left_jolt) + str(right_jolt))

    return total_joltage
```
### Explanation
The key insight is that we want the two largest digits positioned to form the largest two-digit number. This means finding the maximum digit in valid left positions (all but the last), then finding the maximum digit in valid right positions (everything after the chosen left digit).

**Algorithm:**
1. Scan left-to-right through positions 0 to n-2, tracking the maximum digit and its index
2. Early exit if we find a 9 (can't do better)
3. Scan right-to-left from the last position down to just after the left digit's position
4. Early exit if we find a 9
5. Combine digits as `left * 10 + right`

**Optimizations:**
- Early termination when finding 9s saves unnecessary iterations
- Restricting the right search to positions after the left digit ensures we select two different batteries
- Direct arithmetic (`left * 10 + right`) is cleaner than string concatenation

**Constraints:** Input guaranteed to contain only digits 1-9 (no zeros) and non-empty strings.
## Problem 2
The escalator doesn't move. The Elf explains that it probably needs more joltage to overcome the [static friction](https://en.wikipedia.org/wiki/Static_friction) of the system and hits the big red "joltage limit safety override" button. You lose count of the number of times she needs to confirm "yes, I'm sure" and decorate the lobby a bit while you wait.

Now, you need to make the largest joltage by turning on _exactly twelve_ batteries within each bank.

The joltage output for the bank is still the number formed by the digits of the batteries you've turned on; the only difference is that now there will be `_12_` digits in each bank's joltage output instead of two.

Consider again the example from before:

```
987654321111111
811111111111119
234234234234278
818181911112111
```

Now, the joltages are much larger:

- In `_987654321111_111`, the largest joltage can be found by turning on everything except some `1`s at the end to produce `_987654321111_`.
- In the digit sequence `_81111111111_111_9_`, the largest joltage can be found by turning on everything except some `1`s, producing `_811111111119_`.
- In `23_4_2_34234234278_`, the largest joltage can be found by turning on everything except a `2` battery, a `3` battery, and another `2` battery near the start to produce `_434234234278_`.
- In `_8_1_8_1_8_1_911112111_`, the joltage `_888911112111_` is produced by turning on everything except some `1`s near the front.

The total output joltage is now much larger: `987654321111` + `811111111119` + `434234234278` + `888911112111` = `_3121910778619_`.
### Solution
```python
def solve_part_2(battery_banks: list[str]) -> int:
    total_joltage = 0
    max_length = 12 

    for battery_bank in battery_banks:       
        joltage = ""
        end_index = len(battery_bank) - (max_length - 1)
        start_index = 0
        
        while len(joltage) < max_length:
            search_interval = battery_bank[start_index:end_index]
            curr_max = 0
            for index, jolt in enumerate(search_interval):
                if jolt == '9':
                    curr_max = 9
                    new_index = index + 1
                    break
                
                if int(jolt) > curr_max:
                    curr_max = int(jolt)
                    new_index = index + 1
            
            start_index = start_index + new_index
            end_index += 1
            joltage += str(curr_max)

        total_joltage += int(joltage)       
            
    return total_joltage
```
### Explanation
Part 2 extends the problem to selecting 12 batteries instead of 2. The greedy sliding window approach still works because we want to maximize the leftmost digits first.

**Algorithm:**
1. For each of the 12 positions in our result, determine a valid search window
2. The window starts at our current position and ends where we still have enough remaining digits to complete the 12-digit number
3. Select the maximum digit in that window
4. Move our starting position to just after the selected digit
5. Repeat for the next position

**Why Greedy Works:**
- Digits on the left contribute more to the final value (10^11 vs 10^0)
- By maximizing each position from left to right, we ensure the largest possible number
- The sliding window ensures we always have enough digits remaining

**Example Walkthrough** for `987654321111111`:
- Position 1: Search window `987654321111` (need 11 more after) → pick 9
- Position 2: Search window `87654321111` (need 10 more after) → pick 8
- Continue until we've selected 12 digits: `987654321111`

**Constraints:** Input guaranteed to contain only digits 1-9 (no zeros) and non-empty strings with sufficient length.
### Complexity Analysis
For both parts it is at worst O(n)
## Related Concepts
- [[String Manipulation]] - Character-by-character processing and slicing
- [[Greedy Algorithms]] - Making locally optimal choices (maximum digit at each position)
- [[Sliding Window]] - Dynamically adjusting search ranges based on constraints
- [[Early Termination]] - Optimization technique using problem constraints (9 is maximum)