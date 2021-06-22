# Imports
from Transaction import Transaction
from SignaturesECDSA import SignaturesECDSA
from SocketUtil import SocketUtil
import time 
import zlib
import requests
from progress.bar import Bar
# Global Variables
from BlockchainSyncUtil import BlockchainSyncUtil
from connections import Connections

#myPrivate, myPublic = Signatures.generate_keys()
myPrivate, myPublic = SignaturesECDSA().loadKey()

addr, wif = SignaturesECDSA().make_address(myPublic.to_string())


sendPrivate = SignaturesECDSA().generateKeys()

sendPublic = sendPrivate.get_verifying_key()
addrSend, wifSend = SignaturesECDSA().make_address(sendPublic.to_string())

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

Tx = Transaction(myPublic, addr)
Tx.addOutput(addrSend, 0.1)
Tx.sign(myPrivate)

reps = 3


def getPropagatorNodes():

    nodes = Connections().getNetworkNodes()

    rtnData = None

    for node in nodes:
        try:
                r = requests.get(node + '/propagator/getNodes')

                data = r.json()

                rtnData = data

                break


        except Exception as e:
            rtnData = None
    
    return rtnData

#nodesData = BlockchainSyncUtil().getNodes('testnet')

nodesData = getPropagatorNodes()



if(nodesData != None):
    if(nodesData['status'] == 'success'):
        nodes = nodesData['data']

        bar = Bar('Sending transactions', max=reps)

        for i in range(reps):
            #try:
                #SocketUtil.sendObj('localhost', Tx, 5005)
            
            #except:
                #pass


            for node in nodes:
                try:
                    SocketUtil.sendObj(node['ip'], {'transaction': Tx, 'network': 'testnet'}, int(node['port']))
                    #print("Transaction sent to propagator node")
                
                except Exception as e:
                    pass
                    #print("Cannot connect to propagator node: " + str(e))

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
