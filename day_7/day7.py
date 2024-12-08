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
    # Map operations to functions
    operations = {
        '+' : lambda x, y: int(x) + int(y),
        '*' : lambda x, y: int(x) * int(y)
    }

    # Return all possible combinations
    combinations = generate_combinations(['+', '*'], len(key_values) - 1)
    
    # Loop through combinations and perform respective operations underway
    # If result is target return true if result > target skip that set of combinations
    for combination in combinations:
        result = int(key_values[0])
        for i in range(1, len(key_values)):
            result = operations[combination[i-1]](result, int(key_values[i]))
                
            if result == target:
                return True
            
            if result > target:
                break
                
    return False

def check_if_valid_recursively(key_values, target, result, index):
    # base case if we are at the end of the key_values return True / False
    if index == len(key_values):
        return result == target
    
    # Map operations to functions
    operations = {
        '+'  : lambda x, y: int(x) + int(y),
        '*'  : lambda x, y: int(x) * int(y),
        '||' : lambda x, y: int(str(x) + str(y))
    }

    # Perform functions on key_values
    for op, func in operations.items():
        new_result = func(result, key_values[index])
        
        # If the result is true we can return
        if check_if_valid_recursively(key_values, target, new_result, index + 1):
            return True

    return False

@time_execution
def solve():
    data = get_data()
    valid_with_concat = 0
    valid = 0

    for key in data.keys():
        if check_if_valid(data[key], int(key)):
            valid += int(key)
        if check_if_valid_recursively(data[key], int(key), data[key][0], 1):
            valid_with_concat += int(key)

    print(f"Number of valid tests with * & +    : {valid}\nNumber of valid tests with *, + & ||: {valid_with_concat}")

if __name__ == '__main__':
    solve()