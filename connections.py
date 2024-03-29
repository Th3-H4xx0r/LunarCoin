# Imports
import requests
import socket
from colorama import init 
from termcolor import colored 
import pickle

class Connections:

    # Hardcoded
    networkNodes = [
        #'http://127.0.0.1:8000'
        #'https://network-node-us1.lunarcoin.network',
        'https://lunarcoin-network-node.herokuapp.com'
        #'http://server1.protosystems.net'
    ]

    validatorPeers = []
    managerNodes = []
    propagatorNodes = []

    def __init__(self):
        init()

    def getNetworkNodes(self):
        return self.networkNodes

    def sendObj(self, ip_addr, inObj, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((ip_addr, port))
        data = pickle.dumps(inObj)
        s.sendall(data)
        s.close()
    
    def sendObjNonBlocking(self, ip_addr, inObj, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(False)
        
        s.connect((ip_addr, port))
        data = pickle.dumps(inObj)
        s.send(data)
        s.close()

    def getValidatorNodesWallet(self, net):

        minerNodesList = []

        for node in self.networkNodes:

            minerNodesList = []

            try:
                r = requests.get(node + '/validator/getNodes?network=' + str(net))

                #print(r)

                data = r.json()

                #print(data)

                if(data['status'] == "success"):
                    
                    for miner in data['data']:
                        minerNodesList.append({"ip": miner['ip'], "port": int(miner['port']), "status": miner['status']})
                    
                    break

                
                else: # Failed to get list of validators
                    #return []
                    pass
            
            except Exception as e: # Failed to get list of validators
                print("Failed to fetch list of validators: " + str(e))
                #return []
            
            #print(minerNodesList)
        
        return minerNodesList

    def getValidatorNodes(self, net):

        minerNodesList = []

        for node in self.networkNodes:

            minerNodesList = []

            try:
                r = requests.get(node + '/validator/getNodes?network=' + str(net))

                #print(r)

                data = r.json()

                #print(data)

                if(data['status'] == "success"):
                    
                    for miner in data['data']:
                        minerNodesList.append({"ip": miner['ip'], "port": int(miner['port'])})
                    
                    break

                
                else: # Failed to get list of validators
                    #return []
                    pass
            
            except Exception as e: # Failed to get list of validators
                print("Failed to fetch list of validators: " + str(e))
                #return []
            
            #print(minerNodesList)
        
        return minerNodesList
    
    def getManagerNodes(self):

        managerNodesList = []

        for node in self.networkNodes:
            managerNodesList = []
            try:
                r = requests.get(node + '/manager/getNodes')

                data = r.json()

                #print(data)

                if(data['status'] == "success"):
                    
                    for miner in data['data']:
                        managerNodesList.append({"ip": miner['ip'], "port": int(miner['port'])})

                    #return managerNodesList 

                
                else: # Failed to get list of validators
                    #return []
                    pass
            
            except Exception as e: # Failed to get list of validators
                print("Failed to fetch list of manager nodes")
                #return []
    
        return managerNodesList
    
    def connectionTest(self):

        networkNodeFound = False

        workingNetworkNode = None

        workingManagerNode = False

        managerNodes = []

        testPassCount = 0

        for node in self.networkNodes:
            try:
                r = requests.get(node)

                data = r.json()

                #print(data)

                if(data['data'] == 'server pinged'):
                    networkNodeFound = True
                    workingNetworkNode = node
            
            except Exception as e:
                pass
        

        # Gets manager nodes from network node

        if(workingNetworkNode != None):
            try:
                r = requests.get(workingNetworkNode + "/manager/getNodes")

                data = r.json()

                if(data['status'] == 'success'):
                    managerNodes = data['data']
            
            except Exception as e:
                pass
        
        # Pings manager nodes

        #print(managerNodes)
        # [{'id': 'propagator1', 'ip': '4.tcp.ngrok.io', 'port': '14002'}]
        for node in managerNodes:
            try:
                self.sendObj(node['ip'], b'ping', int(node['port']))
                print("[P2P SUCCESS] Communication successful with manager node")
                #print("Obj sent successfully manager nodes")
                workingManagerNode = True
                break
            
            except Exception as e:
                pass
        
        
        print("\n========= Connection Test Results =========")
        if(networkNodeFound):
            print(colored('[✅] Network node connection established', 'green'))
            testPassCount = testPassCount + 1
        else:
            print(colored('[❌] Network node connection failed', 'red'))
        if(workingManagerNode):
            print(colored('[✅] Manager node connection established', 'green'))
            testPassCount = testPassCount + 1
        else:
            print(colored('[❌] Manager node connection failed', 'red'))
        print("===========================================\n")

        if(testPassCount >= 2):
            return True
        else:
            return False



