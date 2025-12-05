Tags:: [[Advent of Code]], [[Math]], [[Python]], [[Regex]], [[String Manipulation]]
Link:: https://adventofcode.com/2025/day/2
## Problem 1
You get inside and take the elevator to its only other stop: the gift shop. "Thank you for visiting the North Pole!" gleefully exclaims a nearby sign. You aren't sure who is even allowed to visit the North Pole, but you know you can access the lobby through here, and from there you can access the rest of the North Pole base.

As you make your way through the surprisingly extensive selection, one of the clerks recognizes you and asks for your help.

As it turns out, one of the younger Elves was playing on a gift shop computer and managed to add a whole bunch of invalid product IDs to their gift shop database! Surely, it would be no trouble for you to identify the invalid product IDs for them, right?

They've even checked most of the product ID ranges already; they only have a few product ID ranges (your puzzle input) that you'll need to check. For example:

```
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
```

(The ID ranges are wrapped here for legibility; in your input, they appear on a single long line.)

The ranges are separated by commas (`,`); each range gives its _first ID_ and _last ID_ separated by a dash (`-`).

Since the young Elf was just doing silly patterns, you can find the _invalid IDs_ by looking for any ID which is made only of some sequence of digits repeated twice. So, `55` (`5` twice), `6464` (`64` twice), and `123123` (`123` twice) would all be invalid IDs.

None of the numbers have leading zeroes; `0101` isn't an ID at all. (`101` is a _valid_ ID that you would ignore.)

Your job is to find all of the invalid IDs that appear in the given ranges. In the above example:

- `11-22` has two invalid IDs, `_11_` and `_22_`.
- `95-115` has one invalid ID, `_99_`.
- `998-1012` has one invalid ID, `_1010_`.
- `1188511880-1188511890` has one invalid ID, `_1188511885_`.
- `222220-222224` has one invalid ID, `_222222_`.
- `1698522-1698528` contains no invalid IDs.
- `446443-446449` has one invalid ID, `_446446_`.
- `38593856-38593862` has one invalid ID, `_38593859_`.
- The rest of the ranges contain no invalid IDs.

Adding up all the invalid IDs in this example produces `_1227775554_`.

_What do you get if you add up all of the invalid IDs?_
### Solution
```python
def solve_part_1(input_data: list[str]) -> int:
    invalid_sum = 0
    for product_id in input_data:
        l_bound, u_bound = product_id.split("-")

        for num in range(int(l_bound), int(u_bound)+1):
            str_num = str(num)
            len_num = len(str_num)
            if len_num % 2 != 0: # odd numbers cannot be invalid
                continue

            midpoint = len_num//2
            left_part = str_num[:midpoint]
            right_part = str_num[midpoint:]
            
            if left_part == right_part:
                invalid_sum += num

    return invalid_sum
```
### Explanation
My immediate thought is that this is potentially going to be annoying. I first thought that we would have to check all the numbers using pointers but the reality is that we can ignore this by just comparing the left side to the right side of the generated number (yay string manipulation).
Additionally, I realised that we could ignore all odd numbers since the left part and the right part would never equal each other.
## Problem 2
The clerk quickly discovers that there are still invalid IDs in the ranges in your list. Maybe the young Elf was doing other silly patterns as well?

Now, an ID is invalid if it is made only of some sequence of digits repeated _at least_ twice. So, `12341234` (`1234` two times), `123123123` (`123` three times), `1212121212` (`12` five times), and `1111111` (`1` seven times) are all invalid IDs.

From the same example as before:

- `11-22` still has two invalid IDs, `_11_` and `_22_`.
- `95-115` now has two invalid IDs, `_99_` and `_111_`.
- `998-1012` now has two invalid IDs, `_999_` and `_1010_`.
- `1188511880-1188511890` still has one invalid ID, `_1188511885_`.
- `222220-222224` still has one invalid ID, `_222222_`.
- `1698522-1698528` still contains no invalid IDs.
- `446443-446449` still has one invalid ID, `_446446_`.
- `38593856-38593862` still has one invalid ID, `_38593859_`.
- `565653-565659` now has one invalid ID, `_565656_`.
- `824824821-824824827` now has one invalid ID, `_824824824_`.
- `2121212118-2121212124` now has one invalid ID, `_2121212121_`.

Adding up all the invalid IDs in this example produces `_4174379265_`.

_What do you get if you add up all of the invalid IDs using these new rules?_
### Solution
```python
def solve_part_2(input_data: list[str]) -> int:
    def factors(n: int) -> list[int]:
        result = []
        for i in range(1, int(n ** 0.5)+1):
            if n % i == 0:
                result.append(i)
                if i != n // i:
                    result.append(n // i)
        return sorted(result)
    
    def split_after_n(number: str, n):
        return [number[i:i+n] for i in range(0, len(number), n)]

    invalid_sum = 0
    for product_id in input_data:
        l_bound, u_bound = product_id.split("-")

        for num in range(int(l_bound), int(u_bound)+1):
            str_num = str(num)
            list_of_factors = factors(len(str_num))

            for factor in list_of_factors:
                comparators = split_after_n(str_num, factor)
                if len(comparators) == 1:
                    continue
                if len(set(comparators)) == 1:
                    invalid_sum += num
                    break                         

    return invalid_sum
```
### Explanation
OK we can break down this problem into parts. A number can only have a repeating pattern of at maximum length of it's factors where the factors are the length of the number. E.g. a number of length 36 as the following factors: `[1, 2, 4, 6, 9, 18, 36]`. This means that there could be a pattern of the same number repeated 36 times, 18 times, 9 times, 6 times, 4 times, 2 times, once. As such we can split the number (again string manipulation) into parts equal to it's lengths factors and then convert that list into a [[Set|set]]. If the set is of length `1` then we have a repeating pattern and we can exit checking the factors and go to the next number.

The factorization method was first proposed by Andreas :). What a G.
#### Why Factors?
A repeating pattern means the string length must be divisible by the pattern length.
For `"565656"` (length 6):
- Factors of 6: \[1, 2, 3, 6]
- Pattern length 1: "5" repeated? Check: \["5","6","5","6","5","6"] - No
- Pattern length 2: "56" repeated? Check: \["56","56","56"] - Yes! ✓

We only need to check factors because:
- If a pattern of length 5 repeated, the total length would be 10, 15, 20...
- A pattern can only repeat if its length divides evenly into the total length
- Factors are exactly the numbers that divide evenly

This is why we can skip checking pattern lengths like 4, 5, 7, 8, etc. for a 6-digit number.
### Optimization
The reality is that this problem could be solved better recursively using regex.
The following pattern `^(\d+?)\1+$` perfectly checks the integer if it fulfills the pattern perfectly.
Let's break this pattern down:
- `^` states that from the start of the string.
- `(\d+)` states find a continuous series of digits
- `?` makes the regex *non-greedy* e.g. capture as little as possible first and then work upwards.
- `\1+` states that the first capture group should be repeated continuously
- `$` states until the end of the string.
Putting that together makes the following from the start of the string find a continuous series of digits that are repeated continuously until the end of the string.

Let's take `121212` as an example:
The regex engine would find 1 as it's first move and then check if `1` is repeating.
This is not the case so it would go on to the next set of continuous digits `12`.
It then checks if this is repeating.
Yes for the first case.
Yes for the second case.

The first problem could be solved similarly  `^(\d+)\1$` the difference is the removal of the `+` means that the capture group is repeated exactly once. However, this is less optimal than my solution as in my solution you only check one thing in the regex solution for part 1 you check `O(n)` times in the worst case.

### Complexity Analysis
**Current approach**:
- Time: O(m * f * n) where:
  - m = numbers in range
  - f = number of factors (typically O(√n))
  - n = digits in number
- Space: O(n) for string operations and factor list

**Regex approach**:
- Time: O(m * n) with potential O(n²) worst case per number due to backtracking
- Space: O(1) beyond the string itself
## Related Concepts
- [[Factoring|Factors]] - core to the Part 2 solution
- [[String Manipulation]] - slicing and chunking techniques  
- [[Regex]] - pattern matching with backreferences
- [[Sets]] - using `set()` to check for uniqueness
- [[Backtracking]] - how regex engines work
- [[Greedy vs Non-Greedy]] - regex quantifier behavior