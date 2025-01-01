import re; import os; import time

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
    with open(f'{os.path.dirname(__file__)}/day3_input.txt', 'r') as file:
        data: str = file.read()
    
    return data

def find_mul_instances(data: str):
    regex_mul_array: list[str] = re.findall(r'(mul\(\d+,\d+\))', data)
    return regex_mul_array

def find_mul_instances_do_criteria(data: str):
    indices_of_string_to_include: list[str] = []
    index: int = 0
    include_flag: bool = True
    for i in range(len(data)-1):
        if data[i:i+7] == "don't()" and include_flag:
            indices_of_string_to_include.append([index, i])
            include_flag = False

        if data[i:i+4] == "do()" and not include_flag:
            index = i
            include_flag = True
    
    string_to_parse: str = ''
    for start, end in indices_of_string_to_include:
        string_to_parse += data[start:end]

    regex_mul_array: list[str] = re.findall(r'(mul\(\d+,\d+\))', string_to_parse)
    return regex_mul_array

def calculate_result(array: list[str]):
    result: int = 0
    for mul in array:
        values: tuple[str, str] = mul.replace("mul(", "").replace(")","").split(',')
        result += int(values[0]) * int(values[1])
    
    return result

@time_execution
def solve():
    data = get_data()
    mul_val = find_mul_instances(data)
    print(f'Mul value: {calculate_result(mul_val)}')
    mul_val_with_do = find_mul_instances_do_criteria(data)
    print(f'Mul value including do criteria: {calculate_result(mul_val_with_do)}')

if __name__ == "__main__":
    solve()