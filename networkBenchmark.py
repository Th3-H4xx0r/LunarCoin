# Imports
from connections import Connections
from Transaction import Transaction
from SignaturesECDSA import SignaturesECDSA
from SocketUtil import SocketUtil
import time 
import zlib
import requests
from progress.bar import Bar
# Global Variables
from BlockchainSyncUtil import BlockchainSyncUtil
import socket
import pickle

#myPrivate, myPublic = Signatures.generate_keys()

wallets = []
walletBalances = []
walletBalanceAvgs = []
myPrivate, myPublic = SignaturesECDSA().loadKey()
addr, wif = SignaturesECDSA().make_address(myPublic.to_string())


WALLET_COUNT = 10

accuracyList = []



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



reps = 20


def getPropagatorNodes():
    try:
            r = requests.get('https://api.classvibes.net/propagator/getNodes')

            data = r.json()

            return data


    except Exception as e:
        return None

#nodesData = BlockchainSyncUtil().getNodes('testnet')

nodesData = getPropagatorNodes()



if(nodesData != None):
    if(nodesData['status'] == 'success'):
        nodes = nodesData['data']

        barW = Bar('Setting up wallets', max=WALLET_COUNT)
        for i in range(WALLET_COUNT):


            sendPrivate = SignaturesECDSA().generateKeys()
            sendPublic = sendPrivate.get_verifying_key()
            addrSend, wifSend = SignaturesECDSA().make_address(sendPublic.to_string())

            wallets.append((sendPrivate, sendPublic, addrSend))

            Tx = Transaction(myPublic, addr)
            Tx.addOutput(addrSend, 10)
            Tx.sign(myPrivate)

            for node in nodes:
                try:
                    SocketUtil.sendObj(node['ip'], {'transaction': Tx, 'network': 'testnet'}, int(node['port']))
                    #print("Transaction sent to propagator node")
                
                except Exception as e:
                    pass
                    #print("Cannot connect to propagator node: " + str(e))
            
            walletBalances.append(10)

            barW.next()

        barW.finish()


        bar = Bar('Sending transactions', max=reps*WALLET_COUNT)

        for i in range(reps):
            #try:
                #SocketUtil.sendObj('localhost', Tx, 5005)
            
            #except:
                #pass
            
            for wallet in wallets:
                Tx = Transaction(wallet[1], wallet[2])
                Tx.addOutput('testSend', 0.5)
                Tx.sign(wallet[0])

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

        rate = reps*WALLET_COUNT/(toc - tic)

        print(f"Sent " + str(reps) + f" transactions in {toc - tic:0.4f} seconds")
        print("Rate: " + str(rate))

        minerNodesList = Connections().getValidatorNodes('testnet')

        time.sleep(25)

        bar1 = Bar('Getting balances', max=WALLET_COUNT)

        for wallet in wallets:

            #print(minerNodesList)

            if(len(minerNodesList) != 0):

                balance = []

                for miner in minerNodesList:

                    try:

                        dataToSend =  b'send_user_balance_command:' + bytes(wallet[2], 'utf-8')

                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((miner['ip'], miner['port']))
                        data = pickle.dumps(dataToSend)
                        s.send(data)

                        #print("Sent data")

                        try:

                            data = s.recv(65536)

                            balance.append(float(data.decode()))

                        
                        except:
                            pass

                        s.close()


                    except Exception as e:
                        #print("Miner node is not active")
                        #print(e)
                        pass
                
            bar1.next()

            #print(balance)
            if(len(balance) != 0):
                first = balance[0]

                listMatches = True

                for b in balance:
                    if(b != first):
                        listMatches = False
                
                accuracyList.append(listMatches)

            
            walletBalanceAvgs.append(balance)

        bar1.finish()

        print(walletBalanceAvgs)
        print(accuracyList)
        trues = 0

        for acc in accuracyList:
            if(acc == True):
                trues = trues  + 1
        
        try:
            print("Accuracy of the experiment: " + str((trues/len(accuracyList)) * 100) + "%")

        except Exception as e:
            print(e)




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
