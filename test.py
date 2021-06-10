# Imports
from Transaction import Transaction
from Signatures import Signatures
from cryptography.hazmat.primitives.asymmetric import rsa
from SocketUtil import SocketUtil
import time 
import zlib
import requests
from progress.bar import Bar
# Global Variables


#myPrivate, myPublic = Signatures.generate_keys()
myPrivate, myPublic = Signatures().load_key('privateKey.pem')
sendPrivate, sendPublic = Signatures.generate_keys()

#ori = myPublic


#myPublic = myPublic.replace(b'-----BEGIN PUBLIC KEY-----\n', b'')
#myPublic = myPublic.replace(b'\n-----END PUBLIC KEY-----\n', b'')

#print(myPublic == ori)

#print(myPublic)

#myPublic = b'-----BEGIN PUBLIC KEY-----\n' + myPublic + b'\n-----END PUBLIC KEY-----\n'

#print(myPublic)

#print(myPublic == ori)



#print(myPublic)
#a = zlib.compress(myPublic)

#print(a)

tic = time.perf_counter()

Tx = Transaction(myPublic)
Tx.addOutput(sendPublic, 0.1)
Tx.sign(myPrivate)

reps = 20000

bar = Bar('Sending transactions', max=reps)

for i in range(reps):
    #try:
        #SocketUtil.sendObj('localhost', Tx, 5005)
    
    #except:
        #pass

    try:
        SocketUtil.sendObj('2.tcp.ngrok.io', Tx, 19062)
    except:
        pass

    if i % 10 == 0:
        #time.sleep(0.3) 
        pass
    
    bar.next()


bar.finish()

toc = time.perf_counter()

rate = reps/(toc - tic)

print(f"Sent " + str(reps) + f" transactions in {toc - tic:0.4f} seconds")
print("Rate: " + str(rate))




'''
#myPrivate, myPublic = Signatures.generate_keys()

myPrivate, myPublic = Signatures().load_key('privateKey.pem')

print(myPublic)

x = bytes(input(">>"), 'utf-8').decode('unicode-escape').encode("ISO-8859-1")

print(x)

print(myPublic == x)
'''
'''
r = requests.get('http://c2852cda439f.ngrok.io/blockchain')

print(eval(r.content))

'''

'''
x = "tcp://8.tcp.ngrok.io:11082"

x = x[6:]

print(x)

print(x.find(":"))

colon = x.find(":")

port = x[colon + 1:]
x = x[:colon]
'''
