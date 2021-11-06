import ntplib
from time import ctime
import time
c = ntplib.NTPClient()
import threading
response = c.request('us.pool.ntp.org', version=3)

startTime = response.tx_time

print(startTime)

print(response.offset)

print(ctime(response.tx_time))

print(response.root_delay)
'''
while True:
    current = time.time()
    if(current >= startTime + 5):
        print("its been 5 sec")
        pass
    
        startTime+=5
'''

def incrementTime():
    global startTime
    while True:
        startTime += 0.1
        time.sleep(0.1)

incrementLiveCounter = threading.Thread(target=incrementTime)
incrementLiveCounter.start()



def printit():
  threading.Timer(0.2, printit).start()
  print(ctime(startTime))
  #startTime = 

printit()
    

