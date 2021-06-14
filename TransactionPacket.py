# Imports


class TransactionPacket:

    def __init__(self, nodes, completed, transaction):
        self.__allNodes = nodes
        self.__completedNodes = completed
        self.__tx = transaction
    
    def updateCompletedNode(self, node):
        try:
            self.__allNodes.remove(node)
        
        except Exception as e:
            print("Error removing node: " + str(e))