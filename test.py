a = [(0, 1)]
b = [(1, 2)]
c = list(zip(a, b))


d = list(map(lambda pair: (pair[0][0] + pair[1][0], 
                                      pair[0][1] + pair[1][1]), 
                        zip(a, b)))
print(d)