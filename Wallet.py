# Imports
from TransactionPacket import TransactionPacket
from Blockchain import Blockchain
from Transaction import Transaction
from SignaturesECDSA import SignaturesECDSA
from SocketUtil import SocketUtil
import pickle
from colorama import init 
from termcolor import colored 

import statistics
import socket
from progress.bar import Bar
import sys
import requests
from connections import Connections
import time

minerNodesList = []
BUFFER_SIZE = 1024

init()



# Global Variables
#myPrivate, myPublic = Signatures.generate_keys()
#sendPrivate, sendPublic = Signatures.generate_keys()

#save_key(myPrivate)

myPrivateSigning, myVerifyingKey = SignaturesECDSA().loadKey()
walletAddress, wif = SignaturesECDSA().make_address(myVerifyingKey.to_string())
#walletAddress = "LC" + walletAddress

#print(myPublicSigning)
#print(type(myPublicSigning))

#print(sendPublic)

def getPropagatorNodes():

    networkNodes = Connections().getNetworkNodes()

    data = None

    print(networkNodes)

    for node in networkNodes:
        #print(node)
        try:
            r = requests.get(node + '/propagator/getNodes')

            data = r.json()

            print(data)

            break


        except Exception as e:
            #print(e)
            pass
    
    return data

        



if __name__ == "__main__":

    networkInp = input("Mainnet(m) or testnet(t) (testnet default if left blank) mode>>")

    if(networkInp == "t" or networkInp == "m" or networkInp == ""):

        network = None

        if(networkInp == ""):
            network = "testnet"

        elif networkInp == "m":
            network = "mainnet"

        elif networkInp == "t":
            network = "testnet"




        #server = SocketUtil.newServerConnection('localhost', my_port)

        #print(minerNodesList)
        while True:

            #print(myPublic)

            inp = input("Send (s) - view blanance(b) - view wallet address(v) - (q) to quit >>")

            #try:

            #  Makes a transaction
            if(inp == "s"):

                #minerNodesList = SocketUtil.getMinerNodes(network)

                #if(len(minerNodesList) == 0):
                    #print(colored("No online nodes detected.", "yellow"))
                
                #else:
                addr = input("Wallet address>>")

                if(addr == b"" or addr == None or addr == ""):
                    print("Address cannot be left blank")

                
                                
                #print("Sending to: " + str(addr))
                
                elif(walletAddress == addr):
                    print(colored("You cannot send coins to your own wallet", 'red'))


                
                else:

                    validInput = False

                    try:
                
                        amount = float(input("Enter amount to send>> "))
                        validInput = True

                    except:
                        print("Input is not valid. Please enter a decimal or whole number") 
                        pass


                    #print(type(sendPublic))
                    #print(type(addr))

                    if(validInput == True):

                        if(addr and amount):    
                            Tx = Transaction(myVerifyingKey, walletAddress)
                            Tx.addOutput(addr, amount)
                            Tx.sign(myPrivateSigning)

                            #print(Tx)

                        
                            print(colored("====== Transaction confirmation ======\nSend to: " + addr + "\nAmount: " + str(amount) + "\n====================", 'green'))
                            
                            confirm = input("Execute transaction (Y/N)?>> ")

                            if(confirm == "Y" or confirm == "y"):

                                '''

                                bar = Bar('Sending transaction', max=len(minerNodesList))

                                for i in range(len(minerNodesList)):

                                    #print(colored("Sending transaction for processing to miner node: " + str(minerNodesList[i]['ip']) + ":" + str(minerNodesList[i]['port']), 'yellow'))

                                    txPacket = TransactionPacket()
                                    try:
                                        SocketUtil.sendObj(minerNodesList[i]['ip'], Tx, minerNodesList[i]['port'])
                                        #print(colored("Sent to miner node " + str(minerNodesList[i]['ip']) + ":" + str(minerNodesList[i]['port']), 'green'))

                                    except:
                                        #print(colored("Miner node " + str(minerNodesList[i]['ip']) + ":" + str(minerNodesList[i]['port']) +" is offline", 'red'))
                                        pass
                                        
                                    i = i + 1

                                    bar.next()

                                
                                bar.finish()
                                '''

                                nodesData = getPropagatorNodes()

                                oneNodeRecv = False

                                print(nodesData)

                                if(nodesData != None):
                                    if(nodesData['status'] == 'success'):
                                        nodes = nodesData['data']

                                        #print(nodes)

                                        for node in nodes:
                                            try:
                                                SocketUtil.sendObj(node['ip'], {'transaction': Tx, 'network': network}, int(node['port']))
                                                oneNodeRecv = True
                                                #print("Transaction sent to propagator node")
                                            
                                            except Exception as e:
                                                pass
                                                #print("Cannot connect to propagator node: " + str(e))
                                        
                                        if(oneNodeRecv == False):
                                            print("Error sending transaction. Cannot connect to the network,")
                                        
                                        else:
                                            print("Transaction sent successfully.")


                            elif(confirm == "N" or confirm == "n"):
                                pass
                                
                            else:
                                print("Selection does not match Y or N")


            #  Gets balance of wallet

            elif(inp == "b"):

                minerNodesList = Connections().getValidatorNodes(network)

                #print(minerNodesList)

                if(len(minerNodesList) == 0):
                    print(colored("No online nodes detected. Failed to fetch balance", "yellow"))

                else:
                    bar = Bar('Fetching balance', max=len(minerNodesList))

                    balance = []

    

                    for miner in minerNodesList:

                        try:

                            dataToSend =  b'send_user_balance_command:' + bytes(walletAddress, 'utf-8')

                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            s.connect((miner['ip'], miner['port']))
                            #s.setblocking(0)
                            data = pickle.dumps(dataToSend)
                            s.send(data)

                            print("Sent data")

                            #time.sleep(1)


                            
                            try:

            
                                data = s.recv(BUFFER_SIZE)

                                print(data)

                                balance.append(float(data.decode()))

                                #balance = 10

                            
                            except:
                                pass
                            
                            #time.sleep(1)
                            #s.close()


                        except Exception as e:
                            #print("Miner node is not active")
                            #print(e)
                            pass


                        bar.next()

                    bar.finish()

                    sys.stdout.write("\033[F")
                    sys.stdout.write("\033[K")


                        #print()   


                    
                    print(balance)

                    
                    try:
                        print("Current balance: " + colored(str(statistics.mode(balance)) + " coins", 'yellow'))
                    
                    except Exception as e:
                        print(colored("Error loading balance: " + str(e) , 'yellow'))



                    '''
                    try:
                        
                        balance = Blockchain.getUserBalance(myPublic, apiServer, False)  

                        print("Current balance: " + colored(str(balance) + " coins", 'yellow'))

                    except Exception as e:
                        if(str(e) == "[Errno 2] No such file or directory: 'blockchain.dat'"):
                            print("Blockchain file does not exist")
                        else:
                            print("An error has occured: " + str(e))

                #   Quits wallet interface

                '''

            elif(inp == "q"):
                break

            elif(inp == "v"):

                printPublic = walletAddress

                #printPublic = printPublic.replace(b'-----BEGIN PUBLIC KEY-----\n', b'')
                #printPublic = printPublic.replace(b'\n-----END PUBLIC KEY-----\n', b'')

                #myPublic = b'-----BEGIN PUBLIC KEY-----\n' + myPublic + b'\n-----END PUBLIC KEY-----\n'
                print("Wallet address " + colored("(Inside quotes): ", "green") + colored(printPublic, "yellow"))
                

                
        
        #except Exception as e:
            #print(colored("An error has occured: " + str(e), 'red'))

    else:
        print("Input not recognized")
    

