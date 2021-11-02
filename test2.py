list1 = [{"x": 1}, {"x": 0}, {"x": 50}, {"x": 42}]
# call int(x) on each element before comparing it
list1 = sorted(list1, key = lambda i: i['x'])


for i in range(1):
    list1.remove(list1[i])

print(list1)