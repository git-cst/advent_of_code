import os

def generate_arrays():
    array1 = []
    with open(f'{os.path.dirname(__file__)}\\day2_input.csv', "r") as file:
        data = file.read()
        data = data.split('\n')

        for row in data:
            values = row.split(' ')
            array1.append(values)
    
    return array1

def safe(array):
    trajectory = None
    for i in range(len(array)):
        if (i + 1) > len(array) - 1:
            return True
        
        curr_element = int(array[i])
        next_element = int(array[i+1])

        difference = abs(curr_element - next_element)
        if difference > 3 or difference == 0:
            return False
        
        curr_trajectory = "DESC" if curr_element - next_element < 0 else "ASC"

        if trajectory is None:
            trajectory = curr_trajectory
        elif curr_trajectory != trajectory:
            return False
    
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