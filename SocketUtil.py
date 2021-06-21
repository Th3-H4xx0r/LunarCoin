# Imports
from connections import Connections
from SignaturesECDSA import SignaturesECDSA
from Signatures import Signatures
import socket
import pickle
from colorama import init 
from termcolor import colored 
import requests


init()
# Global Variables
TCP_PORT = 5005
# Functions

class SocketUtil:

    def __init__(self):
        pass


    def verifyTransaction(self, transaction, public):

        try:

            #print(transaction.data)

            #print(transaction.signedData)

            #message, sig, verifyingKey

            verifed = SignaturesECDSA().verify(bytes(str(transaction.data), 'utf-8'), transaction.signedData, public)

            if verifed == True: #  Checks if transaction is valid
                if transaction.outputAmount > 0: # Checks if transaction amount is greater than zero
                    return True
                else: # If transaction value is less than zero
                    print(colored("[Share Rejected] Transaction value is less than zero", 'yellow'))
                    return False
            
            else: # If transaction is not valid
                return False
        
        except Exception as e: # On error
            print(" Error occured verifyTransaction - SocketUtil.py: " + str(e))
            return False

    def newServerConnection(ip_addr, port=TCP_PORT):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip_addr, port))
        s.listen()
        return s


    def sendObj(ip_addr, inObj, port=TCP_PORT):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_addr, port))
        data = pickle.dumps(inObj)
        s.send(data)
        s.close()

        return False

    
    def updateMinerIp(ip, minerID, net):

        ip = ip[6:]

        colon = ip.find(":")

        port = ip[colon + 1:]
        ip = ip[:colon]

        networkNodes = Connections().getNetworkNodes()

        rtnStatement = None

        for node in networkNodes:
            try:
                r = requests.get(node + '/validator/update?ip=' + str(ip) + "&port=" + str(port) + "&id=" + str(minerID) + "&network=" + str(net))
                #print("Updated miner ip: " + str(r.json()))
                rtnStatement =  ip, int(port)
                break

            except Exception as e:
                print("[FATAL ERROR] Network node is offline: " + str(e))
                rtnStatement = None, None

            #doc = db.collection(u'Miner Nodes').document(minerID)

            #doc.set({
                #"ip": ip,
                #"port": int(port)
            #})
        
        return rtnStatement

