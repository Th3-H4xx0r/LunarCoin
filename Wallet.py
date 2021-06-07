# Imports
from Blockchain import Blockchain
from Transaction import Transaction
from Signatures import Signatures
from cryptography.hazmat.primitives.asymmetric import rsa
from SocketUtil import SocketUtil
import pickle
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from colorama import init 
from termcolor import colored 

import statistics
import socket
from progress.bar import Bar
import sys

minerNodesList = []
BUFFER_SIZE = 1024

init()



# Global Variables
#myPrivate, myPublic = Signatures.generate_keys()
sendPrivate, sendPublic = Signatures.generate_keys()

#save_key(myPrivate)

myPrivate, myPublic = Signatures().load_key('privateKey.pem')

#print(myPublic)

#print(sendPublic)



if __name__ == "__main__":

    networkInp = input("Mainnet(m) or testnet(t) mode>>")

    if(networkInp == "t" or networkInp == "m"):

        network = None

        if networkInp == "m":
            network = "mainnet"

        elif networkInp == "t":
            network = "testnet"


        minerNodesList = SocketUtil.getMinerNodes(network)

        #server = SocketUtil.newServerConnection('localhost', my_port)

        #print(minerNodesList)
        while True:

            #print(myPublic)

            inp = input("Send (s) - view blanance(b) - view wallet address(v) - (q) to quit >>")

            #try:

            #  Makes a transaction
            if(inp == "s"):

                if(len(minerNodesList) == 0):
                    print(colored("No online nodes detected.", "yellow"))
                
                else:
                    addr = bytes(input("Wallet address>>"), 'utf-8').decode('unicode-escape').encode("ISO-8859-1")

                    addr = b'-----BEGIN PUBLIC KEY-----\n' + addr + b'\n-----END PUBLIC KEY-----\n'


                    if(addr == b"" or addr == None or addr == ""):
                        addr = sendPublic

                    
                                    
                    #print("Sending to: " + str(addr))
                    
                    if(myPublic == addr):
                        print(colored("You cannot send coins to your own wallet", 'red'))


                    
                    else:
                    
                        amount = float(input("Enter amount to send>> "))


                        #print(type(sendPublic))
                        #print(type(addr))


                        if(addr and amount):    
                            Tx = Transaction(myPublic)
                            Tx.addOutput(addr, amount)
                            Tx.sign(myPrivate)

                        
                            print(colored("====== Transaction confirmation ======\nSend to: " + str(addr) + "\nAmount: " + str(amount) + "\n====================", 'green'))
                            
                            confirm = input("Execute transaction (Y/N)?>> ")

                            if(confirm == "Y" or confirm == "y"):

                                bar = Bar('Sending transaction', max=len(minerNodesList))

                                for i in range(len(minerNodesList)):

                                    #print(colored("Sending transaction for processing to miner node: " + str(minerNodesList[i]['ip']) + ":" + str(minerNodesList[i]['port']), 'yellow'))

                                    try:
                                        SocketUtil.sendObj(minerNodesList[i]['ip'], Tx, minerNodesList[i]['port'])
                                        #print(colored("Sent to miner node " + str(minerNodesList[i]['ip']) + ":" + str(minerNodesList[i]['port']), 'green'))

                                    except:
                                        #print(colored("Miner node " + str(minerNodesList[i]['ip']) + ":" + str(minerNodesList[i]['port']) +" is offline", 'red'))
                                        pass
                                        
                                    i = i + 1

                                    bar.next()

                                
                                bar.finish()


                            elif(confirm == "N" or confirm == "n"):
                                pass
                                
                            else:
                                print("Selection does not match Y or N")


            #  Gets balance of wallet

            elif(inp == "b"):

                if(len(minerNodesList) == 0):
                    print(colored("No online nodes detected. Failed to fetch balance", "yellow"))

                else:
                    bar = Bar('Fetching balance', max=len(minerNodesList))

                    balance = []

                    for miner in minerNodesList:

                        try:

                            dataToSend =  b'send_user_balance_command:' + myPublic

                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            s.connect((miner['ip'], miner['port']))
                            data = pickle.dumps(dataToSend)
                            s.send(data)

                            try:

                                data = s.recv(BUFFER_SIZE)

                                balance.append(float(data.decode()))

                            
                            except:
                                pass

                            s.close()


                        except:
                            #print("Miner node is not active")
                            pass


                        bar.next()

                    bar.finish()

                    sys.stdout.write("\033[F")
                    sys.stdout.write("\033[K")


                        #print()   


                    
                    print(balance)

                    

                    print("Current balance: " + colored(str(statistics.mode(balance)) + " coins", 'yellow'))



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

                printPublic = myPublic

                printPublic = printPublic.replace(b'-----BEGIN PUBLIC KEY-----\n', b'')
                printPublic = printPublic.replace(b'\n-----END PUBLIC KEY-----\n', b'')

                #myPublic = b'-----BEGIN PUBLIC KEY-----\n' + myPublic + b'\n-----END PUBLIC KEY-----\n'
                print("Wallet address " + colored("(Inside quotes): ", "green") + colored(printPublic, "yellow"))
                

                
        
        #except Exception as e:
            #print(colored("An error has occured: " + str(e), 'red'))

    else:
        print("Input not recognized")
    

