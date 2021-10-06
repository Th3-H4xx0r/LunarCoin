# Imports
from SignaturesECDSA import SignaturesECDSA
import time
import pickle
import os,binascii
import hashlib

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
    __transactionID = None
    



    def __init__(self, public, wallet):
        self.__public = public
        self.__transactionTimestamp = None
        self.__outputAddress = None
        self.__outputAmount = None
        self.__signedData = None
        self.__ownWallet = wallet
        self.__data = []
        self.__transactionID = (b'0x' + binascii.b2a_hex(os.urandom(48))).decode()

    def addOutput(self, address, coins):
        if(self.__outputAddress == None and self.__outputAmount == None):
            self.__outputAddress = address
            self.__outputAmount = coins

    def addMetadata(self, data):
        if(self.__metaData == None):
            self.__metaData = data

        
    def sign(self, privateKey, miningReward = False):

        if(self.__transactionTimestamp == None and self.__data == []):
        
            self.__transactionTimestamp = time.time()

            self.__data.append(self.__outputAddress)
            self.__data.append(self.__outputAmount)
            self.__data.append(self.__transactionTimestamp)
            self.__data.append(self.__public)

            if(miningReward):
                pass
            else:
                self.__signedData = SignaturesECDSA().sign(self.__data, privateKey)
            
            hashRaw = hashlib.sha256(pickle.dumps(self.__data))
            self.__hashData = hashRaw.hexdigest()
    
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
    
    def getData(self):
        return self.__data
    
    def getTransactionID(self):
        return self.__transactionID
    
    def getTimestamp(self):
        return self.__transactionTimestamp
    

    def __repr__(self):
        return"--- Transaction ---\nInput Address: " + str(self.__public) + "\nOutput Address: " + str(self.__outputAddress) + "\nOutput Amount: " + str(self.__outputAmount) + "\nSigned with private key\nTimestamp: " + str(self.__transactionTimestamp) + "\nMetadata:  " + str(self.__metaData) + "\n--- END ---"