import ntplib
from time import ctime
import time
import threading

c = ntplib.NTPClient()
response = c.request('us.pool.ntp.org', version=3)

start = response.tx_time

start += 1



def update():
    global start
    while True:
        start += 1
        time.sleep(1)

updateService = threading.Thread(target=update)
updateService.start()


already5 = False
while True:
    #print(ctime(start) + str(" : ") + ctime(time.time()))
    diff = start % 5
    #print(diff)

    if(str(diff)[0] == '0' and already5 == False):
        print("----------------")
        print("its been 5 sec")
        already5 = True
    
    if(str(diff)[0] != '0' and already5 == True):
        already5 = False
    time.sleep(0.1)

