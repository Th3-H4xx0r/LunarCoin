# Imports
from SignaturesECDSA import SignaturesECDSA
import pickle
import logging

class TransactionPacket:

    def __init__(self, nodes, public, transaction):
        self.__remainingNodes = nodes
        self.__myVerifyingKey = public
        self.__tx = transaction

    
    def getNodes(self):
        return self.__remainingNodes

    def getPublic(self):
        return self.__myVerifyingKey
    
    def updateCompletedNode(self, node):
        try:
            self.__allNodes.remove(node)
        
        except Exception as e:
            print("Error removing node: " + str(e))

    def getTransaction(self):
        return self.__tx

    def sign(self, privateKey):
        self.__signedData = SignaturesECDSA().signRaw(pickle.dumps(self.__tx), privateKey)

    def verifySig(self, tx):
        try:
            return SignaturesECDSA().verify(pickle.dumps(tx) , self.__signedData, self.__myVerifyingKey)
        except Exception as e:
            print("Failed to verify signature for transaction packet: " + str(e))
            return False
        
    
    def getSig(self):
        return self.__signedData
    
    def __repr__(self):
        return (str(self.__allNodes) + " : " + str(self.__completedNodes) + " - TX")