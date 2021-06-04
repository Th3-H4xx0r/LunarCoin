import pickle
import sys


x = "hello"

y = pickle.dumps(x)

print(len(y))

print(sys.getsizeof(y))
print(sys.getsizeof(x))