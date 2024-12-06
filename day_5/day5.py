import os


def generate_data_to_check() -> str:
    with open(f'{os.path.dirname(__file__)}/day5_input.txt', 'r') as file:
        data: str = file.read()
    
    return data.split()

def generate_rule_set() -> {list[str]}:
    with open(f'{os.path.dirname(__file__)}/day5_rules.txt', 'r') as file:
        data: str = file.read()

    data = data.split()

    complete_rule_set = {}
    for row in data:
        greater_than, less_than = row.split("|")

        if greater_than in complete_rule_set:
            temp: list = complete_rule_set[greater_than]
            if less_than not in temp:
                temp.append(less_than)
            complete_rule_set[greater_than] = sorted(temp)
        else:
            complete_rule_set[greater_than] = [less_than]
    
    return complete_rule_set

def valid(rule_set: dict, input: list[str]) -> bool:
    i = 0
    while i < len(input) - 1:
        key = input[i]
        for j in range(i + 1, len(input)):
            val_to_check = input[j]
            if val_to_check not in rule_set[key]:
                return False
        i += 1
    return True

def reorder(rule_set: dict, input: list[str]) -> list[str]:
    if valid(rule_set, input):
        return input

    array = input[:]
    
    i = 0
    while i < len(array) - 1:
        key = array[i]
        next_val = array[i + 1]
        
        if next_val not in rule_set.get(key, []):
            array[i], array[i + 1] = array[i + 1], array[i]
            i = 0
            continue
        
        i += 1
    return array if valid(rule_set, array) else [0]

def median_val(valid_input: list[str]) -> int:
    return int(valid_input[len(valid_input) // 2])
 
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

    print(reordered_results)

if __name__ == '__main__':
    solve()