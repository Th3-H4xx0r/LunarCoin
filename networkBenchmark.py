# Imports
from TransactionPacket import TransactionPacket
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


WALLET_COUNT = 1
TRANSACTION_COUNT_PER_WALLET = 10

reps = TRANSACTION_COUNT_PER_WALLET

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

nodesDataTemp = Connections().getValidatorNodesWallet('testnet')

nodesData = [{'ip': '192.168.1.100', 'port': '6003'}]

# Filters out inactive nodes

'''
for node in nodesDataTemp:
    if(node['status'] == 'online'):
        nodesData.append(node)

'''

print("Filtered out inactive nodes")


if(nodesData != None):
    nodesToSendTo = nodesData

    barW = Bar('Setting up wallets', max=WALLET_COUNT)
    for i in range(WALLET_COUNT):

        sendPrivate = SignaturesECDSA().generateKeys()
        sendPublic = sendPrivate.get_verifying_key()
        addrSend, wifSend = SignaturesECDSA().make_address(sendPublic.to_string())

        wallets.append((sendPrivate, sendPublic, addrSend))

        Tx = Transaction(myPublic, addr)
        Tx.addOutput(addrSend, 10)
        Tx.sign(myPrivate)

        TxPacket = TransactionPacket(Tx)

        for node in nodesToSendTo:
            try:
                SocketUtil.sendObj(node['ip'], TxPacket, int(node['port']))
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
            Tx.addOutput('testSend', 0.05)
            Tx.sign(wallet[0])
            TxPacket = TransactionPacket(Tx)

            for node in nodesToSendTo:
                try:
                    SocketUtil.sendObj(node['ip'], TxPacket, int(node['port']))
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

    nodesDataTemp = Connections().getValidatorNodesWallet('testnet')

    nodesData = []

    # Filters out inactive nodes


    for node in nodesDataTemp:
        if(node['status'] == 'online'):
            nodesData.append(node)
    
    minerNodesList = nodesData

    time.sleep(5)

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


