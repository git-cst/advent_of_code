import re

def get_data():
    with open(r'C:\Users\cas\workspace\advent_of_code_2024\day_3\day3_input.txt', 'r') as file:
        data = file.read()
    
    return data

def find_mul_instances(data):
    regex_mul_array = re.findall('(mul\(\d+,\d+\))', data)
    return regex_mul_array

def calculate_result(array):
    result = 0
    for mul in array:
        values = mul.replace("mul(", "").replace(")","").split(',')
        result += int(values[0]) * int(values[1])
    
    return result

def solve():
    data = get_data()
    mul_instances = find_mul_instances(data)
    print(calculate_result(mul_instances))

if __name__ == "__main__":
    solve()