# Imports
from SignaturesECDSA import SignaturesECDSA
import time

class Transaction:

    outputAddress = None
    outputAmount = 0.0
    public = None
    transactionTimestamp = 1
    metaData = None

    signedData = None
    data = []
    ownWallet = None



    def __init__(self, public, wallet):
        self.public = public
        self.transactionTimestamp = None
        self.outputAddress = None
        self.outputAmount = None
        self.signedData = None
        self.ownWallet = wallet
        self.data = []

    def addOutput(self, address, coins):
        self.outputAddress = address
        self.outputAmount = coins

    def addMetadata(self, data):
        self.metaData = data

        

    def sign(self, privateKey, miningReward = False):
        
        self.transactionTimestamp = time.time()

        self.data.append(self.outputAddress)
        self.data.append(self.outputAmount)
        self.data.append(self.transactionTimestamp)
        self.data.append(self.public)

        if(miningReward):
            pass
        else:
            self.signedData = SignaturesECDSA().sign(self.data, privateKey)
        

    def miningRewardTx(self, public, amount):
        self.outputAddress = public
        self.outputAmount = amount
        self.public = "mining_reward"
        self.transactionTimestamp = time.time()



    def __repr__(self):
        return"--- Transaction ---\nInput Address: " + str(self.public) + "\nOutput Address: " + str(self.outputAddress) + "\nOutput Amount: " + str(self.outputAmount) + "\nSigned with private key\nTimestamp: " + str(self.transactionTimestamp) + "\nMetadata:  " + str(self.metaData) + "\n--- END ---"