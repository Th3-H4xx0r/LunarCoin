# Imports
from SignaturesECDSA import SignaturesECDSA
import time
import pickle

class Transaction:

    __outputAddress = None
    __outputAmount = 0.0
    __public = None
    __transactionTimestamp = 1
    __metaData = None

    __signedData = None
    __data = []
    __ownWallet = None
    __hashData = None



    def __init__(self, public, wallet):
        self.__public = public
        self.__transactionTimestamp = None
        self.__outputAddress = None
        self.__outputAmount = None
        self.__signedData = None
        self.__ownWallet = wallet
        self.__data = []

    def addOutput(self, address, coins):
        self.__outputAddress = address
        self.__outputAmount = coins

    def addMetadata(self, data):
        self.__metaData = data

        
    def sign(self, privateKey, miningReward = False):
        
        self.__transactionTimestamp = time.time()

        self.__data.append(self.__outputAddress)
        self.__data.append(self.__outputAmount)
        self.__data.append(self.__transactionTimestamp)
        self.__data.append(self.__public)

        if(miningReward):
            pass
        else:
            self.__signedData = SignaturesECDSA().sign(self.__data, privateKey)
        
        self.__hashData = pickle.dumps(self.__data)
    
    def getPublic(self):
        return self.__public
    
    def getOutputAddress(self):
        return self.__outputAddress
    
    def getOutputAmount(self):
        return self.__outputAmount

    def getOwnWallet(self):
        return self.__ownWallet
    
    def getMetaData(self):
        return self.__metaData
    
    def getSignedData(self):
        return self.__signedData
    
    def getHash(self):
        return self.__hashData
    

    def __repr__(self):
        return"--- Transaction ---\nInput Address: " + str(self.__public) + "\nOutput Address: " + str(self.__outputAddress) + "\nOutput Amount: " + str(self.__outputAmount) + "\nSigned with private key\nTimestamp: " + str(self.__transactionTimestamp) + "\nMetadata:  " + str(self.__metaData) + "\n--- END ---"