import os

def generate_arrays():
    array1 = []
    with open(f'{os.path.dirname(__file__)}/day2_input.csv', "r") as file:
        data = file.read()
        data = data.split('\n')

        for row in data:
            values = row.split(' ')
            array1.append(values)
    
    return array1

def safe(array: list, err: bool = None):
    if len(array) < 2:
        return True

    trajectory = None
    i = 0
    while i < len(array) - 1:        
        curr_element = int(array[i])
        next_element = int(array[i+1])

        difference = abs(curr_element - next_element)
        if difference > 3 or difference == 0:
            if not err:
                recheck_array = array[:i + 1]+array[i + 2:]
                return safe(recheck_array, True)
            else:
                return False
        
        if i > 0:
            prev_element = int(array[i-1])
            prev_diff = curr_element - prev_element
            curr_diff = next_element - curr_element
            if (prev_diff < 0 and curr_diff > 0) or (prev_diff > 0 and curr_diff < 0):
                if not err:
                    recheck_array = array[:i + 1]+array[i + 2:]
                    return safe(recheck_array, True)
                else:
                    return False
        
        i += 1
    
    return True

def solve():
    arrays = generate_arrays()

    count_safe = 0
    for arr in arrays:
        if safe(arr):
            count_safe += 1

    print(count_safe)

if __name__ == '__main__':
    solve()