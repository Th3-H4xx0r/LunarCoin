# Imports
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

    
    def getManagerNodes():

        managerNodesList = []

        try:
            r = requests.get('https://api.classvibes.net/manager/getNodes')

            data = r.json()

            #print(data)

            if(data['status'] == "success"):
                
                for miner in data['data']:
                    managerNodesList.append({"ip": miner['ip'], "port": int(miner['port'])})

                return managerNodesList 

            
            else: # Failed to get list of validators
                return []
        
        except Exception as e: # Failed to get list of validators
            print("Failed to fetch list of manager nodes")
            return []

    def getMinerNodes(net):

        minerNodesList = []

        '''

        if not firebase_admin._apps:
            cred = credentials.Certificate("./cryptocoin-de716-firebase-adminsdk-r78ms-08b475d8f8.json")
            firebase_admin.initialize_app(cred)

        
        db = firestore.client()

        ref = db.collection(u"Miner Nodes")

        docs = ref.stream()

        configRef = db.collection(u"Config").document("Config")

        configDocs = configRef.get()

        apiServer = configDocs.to_dict()['apiServerURL']


        for doc in docs:
            #print(doc.to_dict())
            minerNodesList.append(doc.to_dict())
        
        '''

        try:
            r = requests.get('https://api.classvibes.net/validator/getNodes?network=' + str(net))

            data = r.json()

            #print(data)

            if(data['status'] == "success"):
                
                for miner in data['data']:
                    minerNodesList.append({"ip": miner['ip'], "port": int(miner['port'])})

                return minerNodesList 

            
            else: # Failed to get list of validators
                return []
        
        except Exception as e: # Failed to get list of validators
            print("Failed to fetch list of miners")
            return []



    def verifyTransaction(self, transaction, public):

        try:

            #print(transaction.data)

            #print(transaction.signedData)

            verifed = Signatures.verify(transaction.data, transaction.signedData, public)

            if verifed == True: #  Checks if transaction is valid
                if transaction.outputAmount > 0: # Checks if transaction amount is greater than zero
                    return True
                else: # If transaction value is less than zero
                    print(colored("[Share Rejected] Transaction value is less than zero", 'yellow'))
                    return False
            
            else: # If transaction is not valid
                return False
        
        except Exception as e: # On error
            print(" Error occured verifyTransaction - MinerUtil.py: " + str(e))
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

        try:
            r = requests.get('https://api.classvibes.net/validator/update?ip=' + str(ip) + "&port=" + str(port) + "&id=" + str(minerID) + "&network=" + str(net))
            #print("Updated miner ip: " + str(r.json()))

        except Exception as e:
            print("[FATAL ERROR] Network node is offline: " + str(e))

            return None, None

        #doc = db.collection(u'Miner Nodes').document(minerID)

        #doc.set({
            #"ip": ip,
            #"port": int(port)
        #})

        return ip, int(port)

