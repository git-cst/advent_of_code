import re

def get_data():
    with open(r'C:\Users\cas\workspace\advent_of_code_2024\day_3\day3_input.txt', 'r') as file:
        data = file.read()
    
    return data

def find_mul_instances(data):
    indices_of_string_to_include = []
    index = 0
    include_flag = True
    for i in range(len(data)-1):
        if data[i:i+7] == "don't()" and include_flag == True:
            indices_of_string_to_include.append([index, i])
            include_flag = False

        if data[i:i+4] == "do()":
            index = i
            include_flag = True
    
    string_to_parse = ''
    for indexes in indices_of_string_to_include:
        string_to_parse += data[indexes[0]:indexes[1]]

    regex_mul_array = re.findall('(mul\(\d+,\d+\))', string_to_parse)
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