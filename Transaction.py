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

    __txType = 'regular'
    __mobileTxData = None
    __publicHex = None
    



    def __init__(self, public, wallet, timestamp=None, outputAddr=None, amount=None, signature=None, txID=None, publicHex=None, metaData=None):

        if(timestamp == None and outputAddr == None and amount == None and signature == None and txID == None and publicHex == None):
            self.__public = public
            self.__transactionTimestamp = None
            self.__outputAddress = None
            self.__outputAmount = None
            self.__signedData = None
            self.__ownWallet = wallet
            self.__data = []
            self.__transactionID = (b'0x' + binascii.b2a_hex(os.urandom(48))).decode()
        
        else:
            print("Mobile tx init")
            self.__txType = 'mobile'
            self.__metaData = metaData
            self.__public = public
            self.__transactionTimestamp = timestamp
            self.__outputAddress = outputAddr
            self.__outputAmount = amount
            self.__signedData = signature
            self.__ownWallet = wallet
            self.__data = [self.__outputAddress, self.__outputAmount, self.__transactionTimestamp, self.__public]
            self.__transactionID = txID

            print(type(publicHex))
            print(type(self.__transactionID))
            print(type(self.__outputAddress))

            self.__mobileTxData =  (str(self.__outputAddress) + str(self.__outputAmount) + str(self.__transactionTimestamp) + str(publicHex) + str(self.__transactionID)).encode('utf-8')
            
            
            print(self.__mobileTxData)

            #LC123410.01634018761.481045feff91e0171e2fa0c96863e0b4054747e10e295854b91a5af274c0d2bde908f4f3f9f5a74f6b232b42c1ac3f9d4cb628420fb518bddbe0a7cb8b8a869cd86440xAfAcdvjiuOorb_sfeB6Pb-CqPT5OzGeLC-ErKRrk7XyTygK_QZGY2Q1gh4-UnmAG
            #LC123410.01634018761481045feff91e0171e2fa0c96863e0b4054747e10e295854b91a5af274c0d2bde908f4f3f9f5a74f6b232b42c1ac3f9d4cb628420fb518bddbe0a7cb8b8a869cd86440xAfAcdvjiuOorb_sfeB6Pb-CqPT5OzGeLC
            
                                #"LC1234" + 10.0.toString() + timestamp.toString() + pub.toHex().toString() + txID.toString()
            
            print
            hashRaw = hashlib.sha256(pickle.dumps(self.__data))
            self.__hashData = hashRaw.hexdigest()


    def addOutput(self, address, coins):
        if(self.__outputAddress == None and self.__outputAmount == None and self.__txType == 'regular'):
            self.__outputAddress = address
            self.__outputAmount = coins

    def addMetadata(self, data):
        if(self.__metaData == None and self.__txType == 'regular'):
            self.__metaData = data

        
    def sign(self, privateKey, miningReward = False):

        if(self.__transactionTimestamp == None and self.__data == [] and self.__txType == 'regular'):
        
            self.__transactionTimestamp = time.time()

            self.__data.append(self.__outputAddress)
            self.__data.append(self.__outputAmount)
            self.__data.append(self.__transactionTimestamp)
            self.__data.append(self.__public.to_string().hex())
            self.__data.append(self.__transactionID)

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
    
    def getMobileSignedData(self):
        return self.__mobileTxData

    def getTxType(self):
        return self.__txType
    

    def __repr__(self):
        return"--- Transaction ---\nInput Address: " + str(self.__public) + "\nOutput Address: " + str(self.__outputAddress) + "\nOutput Amount: " + str(self.__outputAmount) + "\nSigned with private key\nTimestamp: " + str(self.__transactionTimestamp) + "\nMetadata:  " + str(self.__metaData) + "\n--- END ---"