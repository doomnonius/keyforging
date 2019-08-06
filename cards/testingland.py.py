lis = [0, 1, 0, 1, 0, 1]
lis2 = [x for x in lis if x == 0]
print(lis)
lis = [lis + lis2]
print(lis)