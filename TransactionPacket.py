
class TransactionPacket:

    def __init__(self, transaction):
        self.__finishedNodes = []
        self.__tx = transaction

    def getNodes(self):
        return self.__finishedNodes
    
    def updateCompletedNode(self, node):
        self.__finishedNodes.append(node)

    def getTransaction(self):
        return self.__tx
    
    def __repr__(self):
        return (str(self.__finishedNodes) + " : " + str(self.__finishedNodes) + " - TX")