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

def generate_data_to_check() -> str:
    with open(f'{os.path.dirname(__file__)}/day5_input.txt', 'r') as file:
        data: str = file.read()
    
    return data.split()

def generate_rule_set() -> {list[str]}:
    with open(f'{os.path.dirname(__file__)}/day5_rules.txt', 'r') as file:
        data: str = file.read()

    data = data.split()

    complete_rule_set = {}
    # Create a dictionary of the rules. Each key is the left most value and the key values are what it should be before.
    for row in data:
        greater_than, less_than = row.split("|")

        # If the left most value already exists append the less than value if it doesn't exist to the key values.
        if greater_than in complete_rule_set:
            temp: list = complete_rule_set[greater_than]
            if less_than not in temp:
                temp.append(less_than)
            complete_rule_set[greater_than] = sorted(temp)
        # Else create a new key value pair.
        else: 
            complete_rule_set[greater_than] = [less_than]
    
    return complete_rule_set

def valid(rule_set: dict, input: list[str]) -> bool:
    for i in range(0, len(input)-1):
        key = input[i]
        val_to_check = input[i + 1]
        if val_to_check not in rule_set[key]:
            return False
    return True

def reorder(rule_set: dict, input: list[str]) -> list[str]:
    # If the list is already valid, exit early
    if valid(rule_set, input):
        return input

    array = input[:]
    i = 0

    while i < len(array) - 1:
        key = array[i]
        value_to_check = array[i + 1]

        if value_to_check not in rule_set.get(key, []):
            # Propagate upwards to fix the violation
            j = i
            while j >= 0 and value_to_check not in rule_set.get(array[j], []):
                array[j], array[j + 1] = array[j + 1], array[j]
                j -= 1

            # After propagation, revalidate the current segment
            i = max(j, 0)  # Restart from the resolved position
        else:
            i += 1
    return array if valid(rule_set, array) else [0]

def median_val(valid_input: list[str]) -> int:
    return int(valid_input[len(valid_input) // 2])

@time_execution
def solve():
    data = generate_data_to_check()
    rule_set = generate_rule_set()

    valid_results = 0
    reordered_results = 0
    for row in data:
        row_as_list = row.split(',')
        if valid(rule_set, row_as_list):
            valid_results += median_val(row_as_list)
        else:
            reordered_row = reorder(rule_set, row_as_list)
            reordered_results += median_val(reordered_row)

    print(f'Valid sets: {valid_results}\nReordered sets: {reordered_results}')

if __name__ == '__main__':
    solve()