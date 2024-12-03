def generate_arrays():
    array1 = []
    with open('advent_of_code_2024/day_2/day2_input.csv', "r") as file:
        data = file.read()
        data = data.split('\n')

        for row in data:
            values = row.split(' ')
            array1.append(values)
    
    return array1

def safe(array):
    curr_trajectory = None
    for i in range(len(array)):
        if (i + 1) > len(array) - 1:
            return True
        
        curr_element = int(array[i])
        next_element = int(array[i+1])

        difference = abs(curr_element - next_element)
        if difference > 3 or difference == 0:
            return False
        
        trajectory = "DESC" if curr_element - next_element < 0 else "ASC"

        if curr_trajectory != None:
            if curr_trajectory != trajectory:
                return False
        else:
            curr_trajectory = trajectory
    
    return True


if __name__ == '__main__':
    arrays = generate_arrays()

    count_unsafe = 0
    for arr in arrays:
        if not(safe(arr)):
            count_unsafe += 1

    print(count_unsafe)