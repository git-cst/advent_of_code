import os

def generate_arrays():
    array1 = []
    array2 = []
    with open(f'{os.path.dirname(__file__)}/day1_input.csv', "r") as file:
        data = file.read()
        data = data.split('\n')

        for row in data:
            values = row.split(',')
            array1.append(values[0]), array2.append(values[1])

    return array1, array2

def quick_sort(array, low, high):
    if low < high:
        parted_array = partition(array, low, high)
        quick_sort(array, low, parted_array - 1)
        quick_sort(array, parted_array + 1, high)

def partition(array, low, high):
    pivot = array[high]
    i = low
    for j in range(low, high):
        if array[j] < pivot:
            array[i], array[j] = array[j], array[i]
            i += 1
    array[i], array[high] = array[high], array[i]
    return i

def generate_hash_map(array):
    hash_map = {}
    for item in array:
        if item in hash_map:
            hash_map[item] += 1
        else:
            hash_map[item] = 1

    return hash_map

def solve():
    array1, array2 = generate_arrays()
    quick_sort(array1, 0, len(array1)-1)
    quick_sort(array2, 0, len(array2)-1)

    hash_map = generate_hash_map(array2)
    distance, similarity_score = 0, 0
    for i in range(len(array1)):
        distance += abs(int(array1[i]) - int(array2[i]))
        similarity_score += int(array1[i]) * hash_map.get(array1[i], 0)


    print(f'Distance = {distance}, Similarity score = {similarity_score}')



if __name__ == '__main__':
    solve()