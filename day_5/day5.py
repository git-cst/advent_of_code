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

def valid(rule_set: dict, input: str) -> bool:
    i = 0
    while i < len(input) - 1:
        key = input[i]
        for j in range(i + 1, len(input) - 1):
            val_to_check = input[j]
            if val_to_check not in rule_set[key]:
                return False
        i += 1
    
    return True

def median_val(valid_input: list[str]) -> int:
    median = len(valid_input) // 2
    median_val = valid_input[median]
    return int(valid_input[median])
 
def solve():
    data = generate_data_to_check()
    rule_set = generate_rule_set()

    result = 0
    for row in data:
        row_as_list = row.split(',')
        if valid(rule_set, row_as_list):
            result += median_val(row_as_list)

    print(result)

if __name__ == '__main__':
    solve()