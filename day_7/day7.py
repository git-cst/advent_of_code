import os; import time; import operator

def time_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"{func.__name__} took {duration:.4f} seconds to execute.")
        return result
    return wrapper

def get_data():
    data = {}
    with open(f'{os.path.dirname(__file__)}/day7_input.txt', 'r') as file:
        file_data: str = file.read()
    
    file_data = file_data.split('\n')
    
    for row in file_data:
        values = row.split(": ")
        data[values[0]] = values[1].replace(" ", ",").split(",")

    return data

def generate_combinations(choices, n):
    if n == 0:
        return [[]]
    
    combinations = []
    for choice in choices:
        for sub_combination in generate_combinations(choices, n - 1):
            combinations.append([choice] + sub_combination)
    
    return combinations

def check_if_valid(key_values, target):
    operations = {
        '+' : operator.add,
        '*' : operator.mul
    }

    combinations = generate_combinations(['+', '*'], len(key_values) - 1)
    
    for combination in combinations:
        result = int(key_values[0])
        for i in range(1, len(key_values)):
            result = operations[combination[i-1]](result, int(key_values[i]))
                
            if result == target:
                return True
            
            if result > target:
                break
                
    return False

def check_if_valid_concat(key_values, target):
    operations = {
        '+' : operator.add,
        '*' : operator.mul,
        '||': lambda x, y: int(str(x) + str(y))
    }

    combinations = generate_combinations(['+', '*', "||"], len(key_values) - 1)
    
    for combination in combinations:
        result = int(key_values[0])
        for i in range(1, len(key_values)):
            result = operations[combination[i - 1]](result, key_values[i] if combination[i - 1] == '||' else int(key_values[i]))

            if result == target:
                return True
                
            if result > target:
                break

    return False

@time_execution
def solve():
    data = get_data()
    valid_with_concat = 0
    valid = 0

    for key in data.keys():
        if check_if_valid(data[key], int(key)):
            valid += int(key)
        if check_if_valid_concat(data[key], int(key)):
            valid_with_concat += int(key)

    print(f"Number of valid tests with * & +    : {valid}\nNumber of valid tests with *, + & ||: {valid_with_concat}")

if __name__ == '__main__':
    solve()