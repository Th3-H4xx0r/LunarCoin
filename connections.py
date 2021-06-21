# Imports
import requests

class Connections:

    # Hardcoded
    networkNodes = [
        'https://network-node-us1.lunarcoin.network/',
    ]

    validatorPeers = []
    managerNodes = []
    propagatorNodes = []

    def __init__(self):
        pass

    def getNetworkNodes(self):
        return self.networkNodes

    def getValidatorNodes(self, net):

        minerNodesList = []

        for node in self.networkNodes:

            minerNodesList = []

            try:
                r = requests.get(node + '/getNodes?network=' + str(net))

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
                print("Failed to fetch list of miners")
                #return []
        
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
