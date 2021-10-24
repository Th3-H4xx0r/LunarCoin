
import time 

x = 1

def service():
    global x
    x = x + 1
    while True:
        x = x * x
        time.sleep(0.1)
        print(x)
